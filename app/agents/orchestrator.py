from __future__ import annotations

from typing import TypedDict, Any
from langgraph.graph import StateGraph, START, END

from app.agents.prompts import PRICING_AGENT_SYSTEM, LEAD_SCOUT_SYSTEM
from app.agents.schemas import ComplianceDecision
from app.services.audit_repo import AuditRepository
from app.services.llm_loader import build_llm
from app.services.pricing_etl import PricingETL
from app.services.leads_pipeline import LeadsPipeline
from app.services.sqlserver_repo import SQLServerRepo
from app.services.vector_store import VectorStore


class EngineState(TypedDict, total=False):
    request_type: str
    payload: dict[str, Any]
    pricing_scenarios: list[dict]
    lead_results: list[dict]
    compliance: dict
    audit_context: dict


class IndustrialEngine:
    def __init__(self):
        self.llm = build_llm()
        self.sql_repo = SQLServerRepo()
        self.audit = AuditRepository(self.sql_repo)
        self.etl = PricingETL(self.sql_repo)
        self.vector_store = VectorStore()
        self.leads = LeadsPipeline(self.vector_store)
        self.graph = self._build_graph()

    def _call_llm_json(self, system: str, user: str) -> dict:
        prompt = f"{system}\n\nReturn ONLY JSON.\n\nINPUT:\n{user}"
        raw = self.llm.generate(prompt)
        import json, re
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            return {"raw": raw}
        try:
            return json.loads(match.group(0))
        except Exception:
            return {"raw": raw}

    def pricing_node(self, state: EngineState) -> EngineState:
        payload = state.get("payload", {})
        df = self.etl.extract(since_days=int(payload.get("since_days", 90)))
        features = self.etl.transform(df)
        scenarios = self.etl.simulate_price_scenarios(
            features,
            min_margin_pct=float(payload.get("min_margin_pct", 0.20)),
            discount_cap_pct=float(payload.get("discount_cap_pct", 0.15)),
        )

        llm_result = self._call_llm_json(
            PRICING_AGENT_SYSTEM,
            str({
                "features_rows": features.head(20).to_dict(orient="records"),
                "scenarios": scenarios[:10],
                "business_goal": payload.get("goal", "maximize margin without losing volume"),
            }),
        )

        state["pricing_scenarios"] = scenarios
        state["audit_context"] = {"pricing_llm": llm_result}
        return state

    def leads_node(self, state: EngineState) -> EngineState:
        payload = state.get("payload", {})
        leads_input = payload.get("leads", [])
        urls = payload.get("urls", [])
        enriched = self.leads.enrich_from_inputs(leads_input)
        scraped = self.leads.scrape_and_store(urls)

        llm_result = self._call_llm_json(
            LEAD_SCOUT_SYSTEM,
            str({"enriched": enriched[:20], "scraped": scraped[:20]}),
        )

        state["lead_results"] = [{"enriched": enriched, "scraped": scraped, "llm": llm_result}]
        return state

    def compliance_node(self, state: EngineState) -> EngineState:
        request_type = state.get("request_type")
        approval = ComplianceDecision(
            approved=True,
            reason_code="OK",
            reasons=["Complies with base business rules"],
            audit_payload={
                "request_type": request_type,
                "pricing_count": len(state.get("pricing_scenarios", [])),
                "lead_count": len(state.get("lead_results", [])),
            },
        )

        if request_type == "pricing":
            scenarios = state.get("pricing_scenarios", [])
            if any(float(x["suggested_price"]) < float(x["min_allowed_price"]) for x in scenarios):
                approval.approved = False
                approval.reason_code = "PRICE_FLOOR_BREACH"
                approval.reasons = ["At least one recommendation falls below the minimum allowed price"]

        if request_type == "leads":
            if not state.get("lead_results"):
                approval.approved = False
                approval.reason_code = "NO_LEADS_FOUND"
                approval.reasons = ["No lead results to audit"]

        state["compliance"] = approval.model_dump()
        self.audit.log(
            actor="Compliance & Audit Agent",
            action=f"validate_{request_type}",
            entity_type=request_type or "unknown",
            entity_id="batch",
            status="approved" if approval.approved else "rejected",
            reason_code=approval.reason_code,
            request_obj=state.get("payload", {}),
            response_obj=state,
        )
        return state

    def _build_graph(self):
        graph = StateGraph(EngineState)
        graph.add_node("pricing", self.pricing_node)
        graph.add_node("leads", self.leads_node)
        graph.add_node("compliance", self.compliance_node)
        graph.add_edge(START, "compliance")
        graph.add_edge("pricing", "compliance")
        graph.add_edge("leads", "compliance")
        graph.add_edge("compliance", END)
        return graph.compile()

    def run(self, request_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        state: EngineState = {"request_type": request_type, "payload": payload}
        if request_type == "pricing":
            state = self.pricing_node(state)
        elif request_type == "leads":
            state = self.leads_node(state)
        else:
            raise ValueError("request_type must be 'pricing' or 'leads'")
        state = self.compliance_node(state)
        return state

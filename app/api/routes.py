from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.api.deps import get_current_user
from app.agents.orchestrator import IndustrialEngine

router = APIRouter()
engine = IndustrialEngine()


class RunPricingRequest(BaseModel):
    since_days: int = 90
    min_margin_pct: float = 0.2
    discount_cap_pct: float = 0.15
    goal: str = "maximize margin without losing volume"


class RunLeadsRequest(BaseModel):
    leads: list[dict] = Field(default_factory=list)
    urls: list[str] = Field(default_factory=list)


@router.post("/pricing/run")
def run_pricing(body: RunPricingRequest, user=Depends(get_current_user)):
    result = engine.run("pricing", body.model_dump())
    return {"user": user, "result": result}


@router.post("/leads/run")
def run_leads(body: RunLeadsRequest, user=Depends(get_current_user)):
    result = engine.run("leads", body.model_dump())
    return {"user": user, "result": result}


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/metrics")
def metrics():
    from app.core.observability import metrics_response
    return metrics_response()

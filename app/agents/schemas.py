from pydantic import BaseModel, Field
from typing import Any


class PricingScenario(BaseModel):
    product_id: str
    current_price: float
    suggested_price: float
    min_allowed_price: float
    max_allowed_price: float
    expected_margin_delta: float
    expected_volume_delta_pct: float
    confidence: float = Field(ge=0, le=1)
    rationale: str
    needs_more_data: bool = False


class LeadItem(BaseModel):
    company_name: str
    contact_name: str | None = None
    role: str | None = None
    email: str | None = None
    phone: str | None = None
    website: str | None = None
    source_url: str
    source_type: str = "api_or_scrape"
    industry_fit_score: float = Field(ge=0, le=1)
    next_action: str
    notes: str | None = None


class ComplianceDecision(BaseModel):
    approved: bool
    reason_code: str
    reasons: list[str]
    required_changes: list[str] = []
    audit_payload: dict[str, Any] = {}

from pydantic import BaseModel, EmailStr, StrictInt, Field
from typing import Literal

class CustomerCreate(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=120)
    tax_id: str = Field(..., min_length=1, max_length=20)
    email: EmailStr
    country: Literal["ES", "FR", "DE", "IT", "PT"]
    plan: Literal["starter", "pro", "enterprise"]

class CustomerResponse(CustomerCreate):
    id: str
    tax_id_kind: str
    created_at: str

class SimulationCreate(BaseModel):
    customer_id: str
    active_users: StrictInt = Field(..., ge=0)
    storage_gb: StrictInt = Field(..., ge=0)
    api_calls: StrictInt = Field(..., ge=0)

class BreakdownDTO(BaseModel):
    base_cost: str
    storage_cost: str
    api_cost: str
    subtotal: str
    tax_rate: str
    tax: str
    total: str
    currency: str

class SimulationResponse(BaseModel):
    id: str
    customer_id: str
    active_users: int
    storage_gb: int
    api_calls: int
    breakdown: BreakdownDTO
    rules_version: str
    created_at: str

class SimulationPreviewResponse(BaseModel):
    breakdown: BreakdownDTO
    rules_version: str
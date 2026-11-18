from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from saas_o_matic.infrastructure.db import get_db
from saas_o_matic.application import use_cases
from . import schemas

router = APIRouter()

@router.post("/customers", status_code=201, response_model=schemas.CustomerResponse)
def create_customer(payload: schemas.CustomerCreate, db: Session = Depends(get_db)):
    customer = use_cases.create_customer(
        db, payload.company_name, payload.tax_id, payload.email, payload.country, payload.plan
    )
    return customer

@router.post("/simulations", status_code=201, response_model=schemas.SimulationResponse)
def create_simulation(payload: schemas.SimulationCreate, db: Session = Depends(get_db)):
    sim = use_cases.save_simulation(
        db, payload.customer_id, payload.active_users, payload.storage_gb, payload.api_calls
    )
    # Construimos el DTO de respuesta con el breakdown
    return {
        "id": sim.id,
        "customer_id": sim.customer_id,
        "active_users": sim.active_users,
        "storage_gb": sim.storage_gb,
        "api_calls": sim.api_calls,
        "breakdown": {
            "base_cost": sim.base_cost,
            "storage_cost": sim.storage_cost,
            "api_cost": sim.api_cost,
            "subtotal": sim.subtotal,
            "tax_rate": sim.tax_rate,
            "tax": sim.tax,
            "total": sim.total,
            "currency": sim.currency,
        },
        "rules_version": sim.rules_version,
        "created_at": sim.created_at
    }

@router.post("/simulations/preview", response_model=schemas.SimulationPreviewResponse)
def preview_simulation(payload: schemas.SimulationCreate, db: Session = Depends(get_db)):
    breakdown = use_cases.calculate_simulation(
        db, payload.customer_id, payload.active_users, payload.storage_gb, payload.api_calls
    )
    return {
        "breakdown": {
            "base_cost": str(breakdown.base_cost),
            "storage_cost": str(breakdown.storage_cost),
            "api_cost": str(breakdown.api_cost),
            "subtotal": str(breakdown.subtotal),
            "tax_rate": str(breakdown.tax_rate),
            "tax": str(breakdown.tax),
            "total": str(breakdown.total),
            "currency": breakdown.currency,
        },
        "rules_version": breakdown.rules_version
    }
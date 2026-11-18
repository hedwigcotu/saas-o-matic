import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from saas_o_matic.domain.tax_id.validator import validate_tax_id
from saas_o_matic.domain.billing.calculator import build_breakdown
from saas_o_matic.domain.errors import CustomerNotFoundError, DuplicateTaxIdError
from saas_o_matic.infrastructure.db.models import CustomerModel, SimulationModel
from saas_o_matic.infrastructure.db import SessionLocal

def create_customer(db: Session, company_name: str, tax_id: str, email: str, country: str, plan: str) -> CustomerModel:
    # 1. Validar dominio
    kind = validate_tax_id(tax_id, country)
    
    # 2. Comprobar duplicados
    existing = db.query(CustomerModel).filter(CustomerModel.tax_id == tax_id).first()
    if existing:
        raise DuplicateTaxIdError(tax_id)

    # 3. Guardar en BD
    customer = CustomerModel(
        id=str(uuid.uuid4()),
        company_name=company_name,
        tax_id=tax_id,
        tax_id_kind=kind.value,
        email=email,
        country=country,
        plan=plan,
        created_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def calculate_simulation(db: Session, customer_id: str, active_users: int, storage_gb: int, api_calls: int) -> dict:
    # 1. Buscar cliente
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    if not customer:
        raise CustomerNotFoundError(customer_id)

    # 2. Calcular breakdown (Dominio)
    breakdown = build_breakdown(
        active_users=active_users,
        storage_gb=storage_gb,
        api_calls=api_calls,
        country=customer.country
    )

    # 3. Devolver dict para el DTO (sin guardar todavía)
    return breakdown

def save_simulation(db: Session, customer_id: str, active_users: int, storage_gb: int, api_calls: int) -> SimulationModel:
    # 1. Calcular
    breakdown = calculate_simulation(db, customer_id, active_users, storage_gb, api_calls)

    # 2. Persistir
    sim = SimulationModel(
        id=str(uuid.uuid4()),
        customer_id=customer_id,
        active_users=active_users,
        storage_gb=storage_gb,
        api_calls=api_calls,
        base_cost=str(breakdown.base_cost),
        storage_cost=str(breakdown.storage_cost),
        api_cost=str(breakdown.api_cost),
        subtotal=str(breakdown.subtotal),
        tax_rate=str(breakdown.tax_rate),
        tax=str(breakdown.tax),
        total=str(breakdown.total),
        currency=breakdown.currency,
        rules_version=breakdown.rules_version,
        created_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    )
    db.add(sim)
    db.commit()
    db.refresh(sim)
    return sim
from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from .base import Base

class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, index=True)
    company_name = Column(String, nullable=False, index=True)
    tax_id = Column(String, nullable=False, unique=True, index=True)
    tax_id_kind = Column(String, nullable=False)
    email = Column(String, nullable=False)
    country = Column(String, nullable=False)
    plan = Column(String, nullable=False)
    created_at = Column(String, nullable=False)

    simulations = relationship("SimulationModel", back_populates="customer", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("tax_id_kind IN ('DNI', 'NIE', 'CIF', 'FOREIGN')", name="check_tax_id_kind"),
        CheckConstraint("country IN ('ES', 'FR', 'DE', 'IT', 'PT')", name="check_country"),
        CheckConstraint("plan IN ('starter', 'pro', 'enterprise')", name="check_plan"),
    )

class SimulationModel(Base):
    __tablename__ = "simulations"

    id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    active_users = Column(Integer, nullable=False)
    storage_gb = Column(Integer, nullable=False)
    api_calls = Column(Integer, nullable=False)
    
    # Guardamos los importes como String (TEXT) por precisión Decimal
    base_cost = Column(String, nullable=False)
    storage_cost = Column(String, nullable=False)
    api_cost = Column(String, nullable=False)
    subtotal = Column(String, nullable=False)
    tax_rate = Column(String, nullable=False)
    tax = Column(String, nullable=False)
    total = Column(String, nullable=False)
    
    currency = Column(String, nullable=False, default="EUR")
    rules_version = Column(String, nullable=False)
    created_at = Column(String, nullable=False)

    customer = relationship("CustomerModel", back_populates="simulations")

    __table_args__ = (
        CheckConstraint("active_users >= 0", name="check_active_users"),
        CheckConstraint("storage_gb >= 0", name="check_storage_gb"),
        CheckConstraint("api_calls >= 0", name="check_api_calls"),
        CheckConstraint("currency = 'EUR'", name="check_currency"),
        Index("idx_simulations_customer_created", "customer_id", "created_at"),
    )
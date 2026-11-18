import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from saas_o_matic.infrastructure.db.base import Base
from saas_o_matic.infrastructure.db.models import CustomerModel
from saas_o_matic.infrastructure.db.session import engine
import uuid
from datetime import datetime, timezone

@pytest.fixture
def db_session():
    # Usamos una BD en memoria para los tests (no ensucia el archivo real)
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_customer_in_db(db_session):
    customer = CustomerModel(
        id=str(uuid.uuid4()),
        company_name="URKO BALU S.L.",
        tax_id="B12345674",
        tax_id_kind="CIF",
        email="test@urkobalu.es",
        country="ES",
        plan="pro",
        created_at=datetime.now(timezone.utc).isoformat()
    )
    db_session.add(customer)
    db_session.commit()
    
    saved = db_session.query(CustomerModel).filter_by(tax_id="B12345674").first()
    assert saved is not None
    assert saved.company_name == "URKO BALU S.L."
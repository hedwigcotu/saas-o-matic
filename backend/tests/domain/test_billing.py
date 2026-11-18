import pytest
from decimal import Decimal
from saas_o_matic.domain.billing.tiers import base_cost
from saas_o_matic.domain.billing.storage_api import storage_cost, api_cost
from saas_o_matic.domain.billing.calculator import build_breakdown
from saas_o_matic.domain.errors import NegativeUsersError, NegativeInputError, UnsupportedCountryError
from saas_o_matic.domain.tax_id.dni import is_valid_dni

@pytest.mark.parametrize("users, expected", [
    (0, Decimal("0")),
    (1, Decimal("10")),
    (10, Decimal("100")),
    (11, Decimal("108")),
    (50, Decimal("420")),
    (51, Decimal("425")),
    (100, Decimal("670")),
    (1000, Decimal("5170")),
])
def test_tiered_pricing(users, expected):
    assert base_cost(users) == expected

def test_negative_users():
    with pytest.raises(NegativeUsersError):
        base_cost(-1)

def test_full_breakdown():
    # Caso de la spec: 15 usuarios, 10 GB, 1000 llamadas, ES
    b = build_breakdown(15, 10, 1000, "ES")
    assert b.base_cost == Decimal("140.00")
    assert b.storage_cost == Decimal("5.00")
    assert b.api_cost == Decimal("1.00")
    assert b.subtotal == Decimal("146.00")
    assert b.tax == Decimal("30.66")
    assert b.total == Decimal("176.66")

def test_rounding_edge_case():
    # Caso de la spec: 1 usuario, 1 GB, 1 llamada, ES -> subtotal 10.501
    b = build_breakdown(1, 1, 1, "ES")
    assert b.subtotal == Decimal("10.50")
    assert b.tax == Decimal("2.21") # 10.501 * 0.21 = 2.20521 -> 2.21
    assert b.total == Decimal("12.71")
    
def test_negative_storage():
    with pytest.raises(NegativeInputError):
        storage_cost(-10)

def test_negative_api():
    with pytest.raises(NegativeInputError):
        api_cost(-5)

def test_unsupported_country():
    with pytest.raises(UnsupportedCountryError):
        build_breakdown(10, 10, 10, "US")

def test_invalid_dni_format():
    assert is_valid_dni("1234567") is False
    assert is_valid_dni("12345678") is False    
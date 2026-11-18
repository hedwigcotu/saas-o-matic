from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from .tiers import base_cost
from .storage_api import storage_cost, api_cost
from .taxes import get_tax_rate

RULES_VERSION = "1.0"
TWOPLACES = Decimal("0.01")

@dataclass(frozen=True)
class Breakdown:
    base_cost: Decimal
    storage_cost: Decimal
    api_cost: Decimal
    subtotal: Decimal
    tax_rate: Decimal
    tax: Decimal
    total: Decimal
    currency: str
    rules_version: str = RULES_VERSION

def build_breakdown(active_users: int, storage_gb: int, api_calls: int, country: str) -> Breakdown:
    base = base_cost(active_users)
    storage = storage_cost(storage_gb)
    api = api_cost(api_calls)
    
    subtotal = base + storage + api
    tax_rate = get_tax_rate(country)
    
    tax = (subtotal * tax_rate).quantize(TWOPLACES, rounding=ROUND_HALF_UP)
    total = (subtotal + tax).quantize(TWOPLACES, rounding=ROUND_HALF_UP)
    
    return Breakdown(
        base_cost=base,
        storage_cost=storage,
        api_cost=api,
        subtotal=subtotal.quantize(TWOPLACES, rounding=ROUND_HALF_UP),
        tax_rate=tax_rate,
        tax=tax,
        total=total,
        currency="EUR"
    )
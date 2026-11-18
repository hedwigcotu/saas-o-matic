from decimal import Decimal
from ..errors import NegativeInputError

def storage_cost(storage_gb: int) -> Decimal:
    if storage_gb < 0:
        raise NegativeInputError("storage_gb")
    return Decimal(storage_gb) * Decimal("0.50")

def api_cost(api_calls: int) -> Decimal:
    if api_calls < 0:
        raise NegativeInputError("api_calls")
    return Decimal(api_calls) * Decimal("0.001")
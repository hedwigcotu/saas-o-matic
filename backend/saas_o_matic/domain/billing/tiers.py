from decimal import Decimal
from ..errors import NegativeUsersError

def base_cost(active_users: int) -> Decimal:
    if active_users < 0:
        raise NegativeUsersError()
    
    total = Decimal("0")
    remaining = active_users
    prev_limit = 0
    
    # Tramo 1: 0-10 -> 10€
    band = min(remaining, 10)
    total += band * Decimal("10")
    remaining -= band
    prev_limit = 10

    # Tramo 2: 11-50 -> 8€
    if remaining > 0:
        band = min(remaining, 40)
        total += band * Decimal("8")
        remaining -= band
        prev_limit = 50

    # Tramo 3: >50 -> 5€
    if remaining > 0:
        total += remaining * Decimal("5")

    return total
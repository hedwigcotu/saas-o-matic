from decimal import Decimal
from ..errors import UnsupportedCountryError

TAX_RATES: dict[str, Decimal] = {
    "ES": Decimal("0.21"),
    "FR": Decimal("0.20"),
    "DE": Decimal("0.19"),
    "IT": Decimal("0.22"),
    "PT": Decimal("0.23"),
}

def get_tax_rate(country: str) -> Decimal:
    if country not in TAX_RATES:
        raise UnsupportedCountryError(country)
    return TAX_RATES[country]
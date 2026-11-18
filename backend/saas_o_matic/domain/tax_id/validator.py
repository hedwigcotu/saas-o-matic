import re
from .dni import is_valid_dni
from .nie import is_valid_nie
from .cif import is_valid_cif
from ..errors import InvalidTaxIdError
from enum import Enum

class TaxIdKind(str, Enum):
    DNI = "DNI"
    NIE = "NIE"
    CIF = "CIF"
    FOREIGN = "FOREIGN"

def validate_tax_id(raw: str, country: str) -> TaxIdKind:
    value = raw.strip().upper().replace("-", "").replace(" ", "")
    
    if country == "ES":
        if re.match(r"^\d{8}[A-Z]$", value):
            if is_valid_dni(value): return TaxIdKind.DNI
            raise InvalidTaxIdError("DNI letter mismatch")
        elif re.match(r"^[XYZ]\d{7}[A-Z]$", value):
            if is_valid_nie(value): return TaxIdKind.NIE
            raise InvalidTaxIdError("NIE letter mismatch")
        elif re.match(r"^[ABCDEFGHJKLMNPQRSUVW]\d{7}[0-9A-J]$", value):
            if is_valid_cif(value): return TaxIdKind.CIF
            raise InvalidTaxIdError("CIF control mismatch")
        else:
            raise InvalidTaxIdError("Invalid Spanish tax ID format")
    
    # Validación básica para países no ESPAÑA (FR, DE, IT, PT)
    if len(value) < 5:
        raise InvalidTaxIdError("Foreign tax ID too short")
    
    return TaxIdKind.FOREIGN
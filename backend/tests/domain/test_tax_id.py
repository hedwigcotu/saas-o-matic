import pytest
from saas_o_matic.domain.tax_id.validator import validate_tax_id, TaxIdKind
from saas_o_matic.domain.errors import InvalidTaxIdError

@pytest.mark.parametrize("tax_id, expected_kind", [
    ("12345678Z", TaxIdKind.DNI),
    ("00000000T", TaxIdKind.DNI),
    ("X1234567L", TaxIdKind.NIE),
    ("Y1234567X", TaxIdKind.NIE),
    ("A12345674", TaxIdKind.CIF), # Verificado en la spec
    ("B12345674", TaxIdKind.CIF),
    ("K1234567D", TaxIdKind.CIF), # Letra
])
def test_valid_spanish_tax_ids(tax_id, expected_kind):
    assert validate_tax_id(tax_id, "ES") == expected_kind

@pytest.mark.parametrize("tax_id", [
    "12345678A", # Letra DNI mala
    "1234567Z",  # Longitud mala
    "B12345678", # CIF control malo (debería ser 4)
    "Q1234567A", # CIF letra en lugar de dígito
    "I1234567B", # Letra no permitida
])
def test_invalid_spanish_tax_ids(tax_id):
    with pytest.raises(InvalidTaxIdError):
        validate_tax_id(tax_id, "ES")

def test_foreign_tax_id():
    assert validate_tax_id("FR12345678901", "FR") == TaxIdKind.FOREIGN
    
def test_empty_tax_id():
    with pytest.raises(InvalidTaxIdError):
        validate_tax_id("", "ES")

def test_unsupported_format_es():
    with pytest.raises(InvalidTaxIdError):
        validate_tax_id("123", "ES")

def test_foreign_tax_id_too_short():
    with pytest.raises(InvalidTaxIdError):
        validate_tax_id("123", "FR")    
# Spec: Excepciones de dominio

## Jerarquía
DomainError (base)
├── InvalidTaxIdError(reason: str)      → INVALID_TAX_ID (400)
├── NegativeUsersError                  → NEGATIVE_USERS (400)
├── NegativeInputError(field: str)      → NEGATIVE_INPUT (400)
├── UnsupportedCountryError(country)    → UNSUPPORTED_COUNTRY (400)
├── CustomerNotFoundError(id)           → CUSTOMER_NOT_FOUND (404)
├── DuplicateTaxIdError(tax_id)         → DUPLICATE_TAX_ID (409)
└── FxUnavailableError                  → FX_UNAVAILABLE (503)

## Regla
Toda excepción de dominio hereda de DomainError.
El handler HTTP mapea 1:1 a la tabla de api-contracts.md.
Ninguna excepción de dominio conoce HTTP.
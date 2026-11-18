from typing import Any

class DomainError(Exception):
    """Base class for all domain exceptions."""
    pass

class InvalidTaxIdError(DomainError):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)

class NegativeUsersError(DomainError):
    def __init__(self):
        super().__init__("Active users cannot be negative")

class NegativeInputError(DomainError):
    def __init__(self, field: str):
        self.field = field
        super().__init__(f"Input '{field}' cannot be negative")

class UnsupportedCountryError(DomainError):
    def __init__(self, country: str):
        self.country = country
        super().__init__(f"Country '{country}' is not supported")

class CustomerNotFoundError(DomainError):
    def __init__(self, customer_id: str):
        self.customer_id = customer_id
        super().__init__(f"Customer '{customer_id}' not found")

class DuplicateTaxIdError(DomainError):
    def __init__(self, tax_id: str):
        self.tax_id = tax_id
        super().__init__(f"Tax ID '{tax_id}' already exists")
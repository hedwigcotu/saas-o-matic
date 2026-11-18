from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from saas_o_matic.domain.errors import *

async def domain_exception_handler(request: Request, exc: Exception):
    error_code = "INTERNAL_ERROR"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    details = {}

    if isinstance(exc, InvalidTaxIdError):
        error_code, status_code = "INVALID_TAX_ID", 400
        details = {"reason": exc.reason}
    elif isinstance(exc, NegativeUsersError):
        error_code, status_code = "NEGATIVE_USERS", 400
    elif isinstance(exc, NegativeInputError):
        error_code, status_code = "NEGATIVE_INPUT", 400
        details = {"field": exc.field}
    elif isinstance(exc, UnsupportedCountryError):
        error_code, status_code = "UNSUPPORTED_COUNTRY", 400
        details = {"country": exc.country}
    elif isinstance(exc, CustomerNotFoundError):
        error_code, status_code = "CUSTOMER_NOT_FOUND", 404
        details = {"customer_id": exc.customer_id}
    elif isinstance(exc, DuplicateTaxIdError):
        error_code, status_code = "DUPLICATE_TAX_ID", 409
        details = {"tax_id": exc.tax_id}

    return JSONResponse(
        status_code=status_code,
        content={"error": error_code, "details": details}
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "VALIDATION_ERROR", "details": {"errors": exc.errors()}}
    )
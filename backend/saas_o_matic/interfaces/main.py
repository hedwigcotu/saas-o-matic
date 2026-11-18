from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from saas_o_matic.interfaces.http import routes, errors
from saas_o_matic.domain.errors import DomainError
from fastapi.exceptions import RequestValidationError
from saas_o_matic.infrastructure.db import create_tables

app = FastAPI(title="SaaS-O-Matic API", version="1.0.0")

# Configurar CORS para que Vue pueda llamar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción, poner la URL de Vue
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar manejadores de errores
app.add_exception_handler(DomainError, errors.domain_exception_handler)
app.add_exception_handler(RequestValidationError, errors.validation_exception_handler)

# Registrar rutas
app.include_router(routes.router, prefix="/api")

@app.on_event("startup")
def startup():
    create_tables() # Crea las tablas si no existen

@app.get("/")
def read_root():
    return {"message": "SaaS-O-Matic API funcionando"}
from .base import Base
from .session import engine, SessionLocal, get_db

def create_tables():
    from . import models # Importación local para evitar circularidad
    Base.metadata.create_all(bind=engine)

__all__ = ["Base", "engine", "SessionLocal", "get_db", "create_tables"]
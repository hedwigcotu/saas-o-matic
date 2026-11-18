from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# El archivo de la BD se creará en la raíz de backend/
SQLALCHEMY_DATABASE_URL = "sqlite:///./saas_o_matic.db"

# check_same_thread=False es necesario solo para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./students.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Importar modelos DESPUÉS de definir Base
from models.db_model import Students

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)
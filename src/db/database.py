from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Criar diretório se não existir
os.makedirs("./db", exist_ok=True)

DATABASE_URL = "sqlite:///./db/suport_agent.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Criar tabelas no banco de dados"""
    Base.metadata.create_all(bind=engine)

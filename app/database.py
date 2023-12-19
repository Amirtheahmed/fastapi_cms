import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

load_dotenv()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def _get_conn_str() -> str:
    return f"postgresql+psycopg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_db}"


SQLALCHEMY_DATABASE_URL = _get_conn_str()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

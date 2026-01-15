from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL_POSTGRES = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:admin@localhost:5432/postgres"
)
enginePostgres = create_engine(DATABASE_URL_POSTGRES)
SessionPostgres = sessionmaker(autocommit=False, autoflush=False, bind=enginePostgres)

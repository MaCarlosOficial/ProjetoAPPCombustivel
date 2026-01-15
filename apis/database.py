from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL_POSTGRES = "postgresql://postgres:admin@localhost:5432/postgres"
enginePostgres = create_engine(DATABASE_URL_POSTGRES)
SessionPostgres = sessionmaker(autocommit=False, autoflush=False, bind=enginePostgres)

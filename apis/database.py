from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL_POSTGRES = "postgresql://admin:KcPUzimXt9Ryvw6dhYsBCviKHoxMFbcm@dpg-d5kihdemcj7s73d7q7m0-a/dbcombustivel"
enginePostgres = create_engine(DATABASE_URL_POSTGRES)
SessionPostgres = sessionmaker(autocommit=False, autoflush=False, bind=enginePostgres)

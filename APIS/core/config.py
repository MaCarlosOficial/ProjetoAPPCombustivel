import os

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DATABASE_URL do ambiente: {DATABASE_URL}")

if not DATABASE_URL:
    print("⚠️  AVISO: DATABASE_URL não encontrada! Usando fallback localhost")
    DATABASE_URL = "postgresql://admin:KcPUzimXt9Ryvw6dhYsBCviKHoxMFbcm@dpg-d5kihdemcj7s73d7q7m0-a/dbcombustivel"
    #DATABASE_URL = "postgresql://postgres:admin@localhost:5432/postgres"

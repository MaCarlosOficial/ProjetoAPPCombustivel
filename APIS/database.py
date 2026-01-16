from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Debug: Verificar se variável está sendo lida
print("=== DEBUG Banco de Dados ===")

print("\n📋 TODAS AS VARIÁVEIS DE AMBIENTE:")
for key, value in sorted(os.environ.items()):
    if any(word in key.upper() for word in ['DATABASE', 'POSTGRES', 'URL', 'HOST', 'PORT', 'USER', 'PASS','PG']):
        print(f"   {key}: {value}")

DATABASE_URL_POSTGRES = os.getenv("DATABASE_URL")
print(f"DATABASE_URL do ambiente: {DATABASE_URL_POSTGRES}")

if not DATABASE_URL_POSTGRES:
    print("⚠️  AVISO: DATABASE_URL não encontrada! Usando fallback localhost")
    DATABASE_URL_POSTGRES = "postgresql://admin:KcPUzimXt9Ryvw6dhYsBCviKHoxMFbcm@dpg-d5kihdemcj7s73d7q7m0-a/dbcombustivel"

enginePostgres = create_engine(DATABASE_URL_POSTGRES)
SessionPostgres = sessionmaker(autocommit=False, autoflush=False, bind=enginePostgres)
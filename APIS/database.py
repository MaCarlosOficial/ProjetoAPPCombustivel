from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Debug: Verificar se variável está sendo lida
print("=== DATABASE DEBUG ===")
print(f"Todas as variáveis: {dict(os.environ)}")

DATABASE_URL_POSTGRES = os.getenv("DATABASE_URL")
print(f"DATABASE_URL do ambiente: {DATABASE_URL_POSTGRES}")

if not DATABASE_URL_POSTGRES:
    print("⚠️  AVISO: DATABASE_URL não encontrada! Usando fallback localhost")
    DATABASE_URL_POSTGRES = "postgresql://postgres:admin@localhost:5432/postgres"
else:
    # Verificar se é uma URL válida do Render
    if "render.com" in DATABASE_URL_POSTGRES or "onrender.com" in DATABASE_URL_POSTGRES:
        print("✅ URL do Render detectada")
    else:
        print(f"ℹ️  URL do banco: {DATABASE_URL_POSTGRES[:50]}...")

print(f"URL final usada: {DATABASE_URL_POSTGRES[:50]}...")
print("=====================")

enginePostgres = create_engine(DATABASE_URL_POSTGRES)
SessionPostgres = sessionmaker(autocommit=False, autoflush=False, bind=enginePostgres)
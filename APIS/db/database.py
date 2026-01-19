import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from APIS.core.config import DATABASE_URL

# Debug: Verificar se variável está sendo lida
print("=== DEBUG Banco de Dados ===")

print("\n📋 TODAS AS VARIÁVEIS DE AMBIENTE:")
for key, value in sorted(os.environ.items()):
    if any(word in key.upper() for word in ['DATABASE', 'POSTGRES', 'URL', 'HOST', 'PORT', 'USER', 'PASS','PG']):
        print(f"   {key}: {value}")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

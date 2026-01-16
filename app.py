from dotenv import load_dotenv
load_dotenv()  # Carrega variáveis do arquivo .env se existir

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Criar app principal
app = FastAPI(title="API Find Fuel")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DEBUG: Verificar estrutura
print("=== DEBUG: Estrutura de diretórios ===")
print(f"Diretório atual: {os.getcwd()}")
print(f"Conteúdo: {os.listdir('.')}")

# Importar e montar a API de login
try:
    from APIS.login import app as login_app
    from APIS.main import app as main_app
    
    # Montar ambas as APIs com prefixos diferentes
    app.mount("/login", login_app)    # Rotas em /login/
    app.mount("/findFuel", main_app)  # Rotas em /findFuel/
    
    print("✅ APIs importadas com sucesso!")
    
except ImportError as e:
    print(f"❌ Erro ao importar APIs: {e}")
    import traceback
    traceback.print_exc()

# Rota raiz
@app.get("/")
def root():
    return {
        "message": "API Find Fuel",
        "endpoints": {
            "login": "/login/docs",
            "api": "/findFuel/docs",
            "fuel_prices": "/findFuel/fuelPrices"
        }
    }

# Health check
@app.get("/health")
def health():
    return {"status": "ok", "service": "main-gateway"}
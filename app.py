from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys

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

# Importar e montar a API de login
sys.path.insert(0, 'apis')
from apis.login import app as login_app
from apis.main import app as main_app

# Montar ambas as APIs com prefixos diferentes
app.mount("/login", login_app)    # Rotas em /login/
app.mount("/findFuel", main_app)       # Rotas em /api/

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
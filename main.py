from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from APIS.routes import auth, usuarios, fuel

app = FastAPI(title="API Find Fuel")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔗 REGISTRAR ROTAS
app.include_router(auth.router, prefix="/login")
app.include_router(usuarios.router, prefix="/login")
app.include_router(fuel.router, prefix="/findFuel")

# Rota raiz
@app.get("/", tags=["Root"])
def root():
    return {
        "service": "API Find Fuel",
        "docs": "/docs"
    }

# Health check
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}

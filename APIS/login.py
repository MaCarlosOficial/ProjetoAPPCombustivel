from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from APIS.routes import auth, usuarios

app = FastAPI(title="API Login e Usuários")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)

@app.get("/health")
def health():
    return {"status": "ok"}

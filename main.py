from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Modelo de entrada usando Pydantic
class TextInput(BaseModel):
    text: str

# -------------------- FastAPI App --------------------
app = FastAPI(
    title="API de Processamento de Texto",
    description="Serviço simples de demonstração para arquitetura distribuída",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "null"],  # Ou ["*"] para desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint POST para processar texto
@app.post("/process")
async def process_text(data: TextInput):
    result = {
        "original": data.text,
        "uppercased": data.text.upper()
    }
    return JSONResponse(content=result)


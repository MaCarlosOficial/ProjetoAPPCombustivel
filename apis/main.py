from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionPostgres
from security import get_current_user

app = FastAPI(title="API de Combustível")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "null"],  # Ou ["*"] para desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DEPENDÊNCIA DO DB ---
def get_db():
    db = SessionPostgres()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def configure_swagger():
    app.openapi() # Gera o esquema

# --- ROTA PROTEGIDA ---
@app.get("/fuelPrices", tags=["Combustível"], summary="Consulta de preços de combustíveis por localização")
def consultar_combustiveis(
    latitude: float = -23.55052,
    longitude: float = -46.633308,
    raio_km: float = 5.0,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    try:
        query = text("""
            SELECT id_revenda, nome_revenda as nome, produto, valor_venda, distancia, unidade_medida
            ,latitute as latitude, longitude, bandeira, data_atualizacao as atualizado_em
            FROM (
                SELECT *,
                    (6371 * acos(
                            cos(radians(:lat)) *
                            cos(radians(latitute)) *
                            cos(radians(longitude) - radians(:lon)) +
                            sin(radians(:lat)) *
                            sin(radians(latitute))
                        )
                    ) AS distancia
                FROM combustivel_preco_consulta
                WHERE latitute IS NOT NULL
                AND longitude IS NOT NULL
            ) sub
            WHERE distancia <= :raio
            ORDER BY distancia
        """)

        result = db.execute(
            query,
            {"lat": latitude, "lon": longitude, "raio": raio_km}
        ).fetchall()

        return [
            {
                "id_revenda": r.id_revenda,
                "nome": r.nome,
                "produto": r.produto,
                "valor_venda": float(r.valor_venda),
                "distancia": round(r.distancia, 3),
                "unidade_medida": r.unidade_medida,
                "latitude": r.latitude,
                "longitude": r.longitude,
                "bandeira": r.bandeira,
                "atualizado_em": r.atualizado_em.isoformat()
            }
            for r in result
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao processar requisição: {str(e)}"
        )
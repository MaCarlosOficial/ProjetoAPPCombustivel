from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from APIS.db.database import get_db
from APIS.core.security import get_current_user

router = APIRouter(
    prefix="/fuel",
    tags=["⛽ FindFuel / Combustível"]
)

@router.get(
    "/prices",
    summary="Consulta de preços de combustíveis por localização"
)
def consultar_combustiveis(
    latitude: float = -23.55052,
    longitude: float = -46.633308,
    raio_km: float = 5.0,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # qualquer usuário autenticado
):
    try:
        query = text("""
            SELECT id_revenda,
                   nome_revenda AS nome,
                   produto,
                   valor_venda,
                   unidade_medida,
                   latitude,
                   longitude,
                   bandeira,
                   data_atualizacao AS atualizado_em,
                   distancia
            FROM (
                SELECT *,
                    (6371 * acos(
                        cos(radians(:lat)) *
                        cos(radians(latitude)) *
                        cos(radians(longitude) - radians(:lon)) +
                        sin(radians(:lat)) *
                        sin(radians(latitude))
                    )) AS distancia
                FROM combustivel_preco_consulta
                WHERE latitude IS NOT NULL
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
            detail="Erro ao consultar preços de combustível"
        )

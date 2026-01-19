from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from APIS.db.database import get_db
from APIS.db.models import Usuario
from APIS.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token
)
from APIS.schemas.token import Token

router = APIRouter(
    prefix="/auth",
    tags=["🔐 Login / Auth"]
)

@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter(
        (Usuario.usuario == form.username) |
        (Usuario.email == form.username)
    ).first()

    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")

    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "usuario": user.usuario,
            "nome": user.nome,
            "email": user.email,
            "role": user.role
        }
    }

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    from jose import jwt, JWTError
    from APIS.core.config import SECRET_KEY, ALGORITHM

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise ValueError()
        username = payload.get("sub")
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Refresh token inválido")

    user = db.query(Usuario).filter(Usuario.usuario == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user)
    }

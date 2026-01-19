from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from APIS.db.database import get_db
from APIS.db.models import Usuario
from APIS.schemas.usuario import UsuarioCreate, UsuarioOut
from APIS.core.security import (
    hash_password,
    get_current_user,
    require_role
)

router = APIRouter(
    prefix="/usuarios",
    tags=["👤 Login / Usuários"]
)

# 🔓 CADASTRO PÚBLICO (NÃO REMOVER)
@router.post(
    "/",
    response_model=UsuarioOut,
    status_code=status.HTTP_201_CREATED,
    summary="Criar usuário"
)
def criar_usuario(payload: UsuarioCreate, db: Session = Depends(get_db)):
    exists = db.query(Usuario).filter(
        (Usuario.usuario == payload.usuario) |
        (Usuario.email == payload.email)
    ).first()

    if exists:
        raise HTTPException(
            status_code=409,
            detail="Usuário ou e-mail já cadastrado"
        )

    user = Usuario(
        usuario=payload.usuario,
        nome=payload.nome,
        email=payload.email,
        hashed_password=hash_password(payload.senha),
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# 🔒 LISTAGEM (SÓ ADMIN)
@router.get(
    "/",
    response_model=list[UsuarioOut],
    summary="Listar usuários só adminitrador"
)
def listar_usuarios(
    _: Usuario = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    return db.query(Usuario).all()


# 🔐 USUÁRIO LOGADO
@router.get(
    "/me",
    response_model=UsuarioOut,
    summary="Perfil do usuário logado"
)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user

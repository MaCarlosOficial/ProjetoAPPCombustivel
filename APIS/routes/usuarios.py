from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from APIS.db.database import get_db
from APIS.db.models import Usuario
from APIS.schemas.usuario import UsuarioCreate, UsuarioOut, UsuarioUpdate
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

# 🔐 ATUALIZAR DADOS DO USUÁRIO (PRÓPRIO OU ADMIN)
@router.put(
    "/{user_id}",
    response_model=UsuarioOut,  # Correção: deve retornar UsuarioOut
    summary="Atualizar usuário por ID"
)
def atualizar_usuario(
    user_id: int,
    payload: UsuarioUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Usuário só pode atualizar seu próprio perfil, exceto admin
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode atualizar seu próprio perfil"
        )
    
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Validações de duplicidade
    if payload.usuario is not None and payload.usuario != user.usuario:
        exists = db.query(Usuario).filter(
            Usuario.usuario == payload.usuario,
            Usuario.id != user_id
        ).first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome de usuário já está em uso"
            )
        user.usuario = payload.usuario
    
    if payload.nome is not None:
        user.nome = payload.nome
    
    if payload.email is not None and payload.email != user.email:
        exists = db.query(Usuario).filter(
            Usuario.email == payload.email,
            Usuario.id != user_id
        ).first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-mail já cadastrado por outro usuário"
            )
        user.email = payload.email
    
    if payload.senha is not None:
        user.hashed_password = hash_password(payload.senha)
    
    try:
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        print(f"Erro ao atualizar usuário: {str(e)}")  # Log para debug
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar usuário"
        )
    
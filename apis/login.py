from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

from security import create_access_token, get_current_user, get_user_by_username

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------- DB Setup -----------------------
DATABASE_URL = "sqlite:///./usuarios.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- Modelos ORM --------------------
class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String, unique=True, index=True, nullable=False)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")

Base.metadata.create_all(bind=engine)

# -------------------- Schemas Pydantic --------------------
class UsuarioCreate(BaseModel):
    usuario: str
    nome: str
    email: EmailStr
    senha: str

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None

class UsuarioOut(BaseModel):
    id: int
    usuario: str
    nome: str
    email: EmailStr
    class Config:
        from_attributes = True  # pydantic v2

class Token(BaseModel):
    access_token: str
    token_type: str

# -------------------- Segurança (hash/verify + JWT) --------------------
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password.encode('utf-8'))

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(UsuarioDB).filter(
        or_(
            UsuarioDB.usuario == username,
            UsuarioDB.email == username
        )
    ).first()

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user

# -------------------- FastAPI App --------------------
app = FastAPI(title="API de Usuários")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "null"],  # Ou ["*"] para desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- Cadastro (público) ----------
@app.post("/usuarios/", response_model=UsuarioOut, status_code=201, summary="Criar novo usuário")
def criar_usuario(payload: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(UsuarioDB).filter(UsuarioDB.usuario == payload.usuario).first():
        raise HTTPException(status_code=400, detail="Usuário já existe")
    if db.query(UsuarioDB).filter(UsuarioDB.email == payload.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    user = UsuarioDB(
        usuario=payload.usuario,
        nome=payload.nome,
        email=payload.email,
        hashed_password=get_password_hash(payload.senha),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# --------- Rotas protegidas ----------
# --------- Auth: obter token (login) ----------
@app.post("/token", response_model=Token, summary="Login e obtenção de Token Acesso")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm usa campos: username, password
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")
    access_token = create_access_token(data={"sub": user.usuario})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/usuarios/", response_model=List[UsuarioOut], summary="Listar todos usuários")
def listar_usuarios(current_user: UsuarioDB = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(UsuarioDB).all()

@app.get("/usuarios/me", response_model=UsuarioOut, summary="Perfil do usuário logado")
def meu_perfil(current_user: UsuarioDB = Depends(get_current_user)):
    return current_user

@app.get("/usuarios/{user_id}", response_model=UsuarioOut, summary="Buscar usuário por ID")
def buscar_usuario(user_id: int, current_user: UsuarioDB = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(UsuarioDB).filter(UsuarioDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@app.put("/usuarios/{user_id}", response_model=UsuarioOut, summary="Atualizar usuário por ID")
def atualizar_usuario(user_id: int, payload: UsuarioUpdate, current_user: UsuarioDB = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(UsuarioDB).filter(UsuarioDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if payload.nome is not None:
        user.nome = payload.nome
    if payload.email is not None:
        # checar duplicidade de email
        exists = db.query(UsuarioDB).filter(UsuarioDB.email == payload.email, UsuarioDB.id != user_id).first()
        if exists:
            raise HTTPException(status_code=400, detail="E-mail já cadastrado por outro usuário")
        user.email = payload.email
    if payload.senha is not None:
        user.hashed_password = get_password_hash(payload.senha)

    db.commit()
    db.refresh(user)
    return user

@app.delete("/usuarios/{user_id}", summary="Deletar usuário por ID")
def deletar_usuario(user_id: int, current_user: UsuarioDB = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(UsuarioDB).filter(UsuarioDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(user)
    db.commit()
    return {"message": "Usuário deletado com sucesso"}

# Endpoint para validar token
@app.get("/valida-token")
async def validate_token(current_user: UsuarioDB = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"valid": True, "username": current_user}

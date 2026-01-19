from pydantic import BaseModel, EmailStr, Field

class UsuarioCreate(BaseModel):
    usuario: str = Field(..., min_length=3)
    nome: str
    email: EmailStr
    senha: str = Field(..., min_length=6)

class UsuarioOut(BaseModel):
    id: int
    usuario: str
    nome: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

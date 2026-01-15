from sqlalchemy import Column, String, Date, Numeric, Boolean, DateTime, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CombustivelPrecoConsulta(Base):
    __tablename__ = "combustivel_preco_consulta"

    id_revenda = Column(Integer, primary_key=True)
    produto = Column(String, primary_key=True)
    valor_venda = Column(Numeric(10, 2))
    unidade_medida = Column(String(20))
    bandeira = Column(String(100))
    data_atualizacao = Column(Date)
    latitute = Column(Numeric(18, 16))
    longitude = Column(Numeric(18, 16))

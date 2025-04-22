from sqlalchemy import Column, Integer, String, DateTime, Enum
from database.session import Base
from enum import Enum as PyEnum

class EstadoVuelo(str, PyEnum):
    PROGRAMADO = "programado"
    EMERGENCIA = "emergencia"
    RETRASADO = "retrasado"

class DBVuelo(Base):
    __tablename__ = "vuelos"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True, nullable=False)
    estado = Column(Enum(EstadoVuelo), nullable=False)
    hora = Column(DateTime, nullable=False)
    origen = Column(String(100), nullable=False)
    destino = Column(String(100), nullable=False)
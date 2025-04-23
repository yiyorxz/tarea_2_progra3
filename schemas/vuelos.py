from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class EstadoVuelo(str, Enum):
    programado = "programado"
    emergencia = "emergencia"
    retrasado = "retrasado"

class VueloBase(BaseModel):
    codigo: str
    estado: EstadoVuelo
    hora: datetime
    origen: str
    destino: str

class VueloCreate(VueloBase):
    pass

class Vuelo(VueloBase):
    id: int
    posicion: float
    
    class Config:
        orm_mode = True
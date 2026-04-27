from pydantic import BaseModel
from datetime import date
from typing import Optional

class ExpedienteCreate(BaseModel):
    numero_expediente: str
    caratula: Optional[str]
    fecha_ingreso: date
    persona_id: int

class ExpedienteResponse(BaseModel):
    id: int
    numero: str
    caratula: Optional[str]
    fecha_ingreso: date
    color: str

    class Config:
        orm_mode = True
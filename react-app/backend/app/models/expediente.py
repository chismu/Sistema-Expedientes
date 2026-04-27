from sqlalchemy import Column, Integer, String, Text, Date, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Expediente(Base):
    __tablename__ = "expedientes"

    id = Column(Integer, primary_key=True, index=True)
    numero_expediente = Column(String(50), unique=True, nullable=False)
    caratula = Column(Text)
    fecha_ingreso = Column(Date, nullable=False)

    estado = Column(String(50))
    prioridad = Column(String(50))
    tipo = Column(String(50))
    responsable = Column(String(100))

    fecha_limite = Column(Date)

    accion = Column(Text)
    observaciones = Column(Text)

    activo = Column(Boolean, default=True)
    fecha_finalizacion = Column(Date)

    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relación con asignaciones
    personas = relationship("ExpedientePersona", back_populates="expediente")
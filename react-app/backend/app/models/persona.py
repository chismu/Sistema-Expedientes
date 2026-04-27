from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

    # Relación con asignaciones
    expedientes = relationship("ExpedientePersona", back_populates="persona")
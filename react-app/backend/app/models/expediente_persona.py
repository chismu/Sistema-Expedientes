from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class ExpedientePersona(Base):
    __tablename__ = "expediente_persona"

    id = Column(Integer, primary_key=True, index=True)

    expediente_id = Column(Integer, ForeignKey("expedientes.id", ondelete="CASCADE"), nullable=False)
    persona_id = Column(Integer, ForeignKey("personas.id"), nullable=False)

    fecha_asignacion = Column(TIMESTAMP, server_default=func.now())
    fecha_fin = Column(TIMESTAMP, nullable=True)

    # Relaciones
    expediente = relationship("Expediente", back_populates="personas")
    persona = relationship("Persona", back_populates="expedientes")
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Persona, ExpedientePersona
from app.database import get_db
from app.models import Persona

router = APIRouter(prefix="/personas", tags=["Personas"])


@router.get("/")
def listar_personas(db: Session = Depends(get_db)):
    personas = db.query(Persona).all()

    return [
        {
            "id": p.id,
            "nombre": p.nombre
        }
        for p in personas
    ]

@router.get("/estadisticas")
def estadisticas_personas(db: Session = Depends(get_db)):

    personas = db.query(Persona).all()
    resultado = []

    for p in personas:
        asignaciones = db.query(ExpedientePersona).filter(
            ExpedientePersona.persona_id == p.id,
            ExpedientePersona.fecha_fin == None
        ).all()

        expedientes = [
            a.expediente.numero_expediente
            for a in asignaciones
            if a.expediente
        ]

        resultado.append({
            "persona": p.nombre,
            "expedientes": expedientes,
            "total": len(expedientes)
        })

    return resultado
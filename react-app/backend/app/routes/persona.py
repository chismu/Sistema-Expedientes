from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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
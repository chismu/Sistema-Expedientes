from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.models import Persona
from app.database import get_db
from app.models import Expediente, ExpedientePersona
from app.utils.fechas import dias_habiles, calcular_color
from app.schemas.expediente import ExpedienteCreate

router = APIRouter(prefix="/expedientes", tags=["Expedientes"])

@router.post("/")
def crear_expediente(data: dict, db: Session = Depends(get_db)):
    nuevo = Expediente(
        numero_expediente=data["numero_expediente"],
        caratula=data.get("caratula"),
        fecha_ingreso=data["fecha_ingreso"],
        estado="pendiente",
        activo=True
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    # asignación inicial
    asignacion = ExpedientePersona(
        expediente_id=nuevo.id,
        persona_id=data["persona_id"]
    )

    db.add(asignacion)
    db.commit()

    return {"msg": "Expediente creado", "id": nuevo.id}

def calcular_color(fecha_ingreso):
    dias = (date.today() - fecha_ingreso).days

    if dias >= 55:
        return "rojo"
    elif dias >= 45:
        return "Naranja"
    else:
        return "verde"
    
@router.get("/")
def listar_expedientes(db: Session = Depends(get_db)):
    expedientes = db.query(Expediente).filter(Expediente.activo == True).all()

    resultado = []

    for e in expedientes:
        color = calcular_color(e.fecha_ingreso)

        resultado.append({
            "id": e.id,
            "numero": e.numero_expediente,
            "caratula": e.caratula,
            "fecha_ingreso": e.fecha_ingreso,
            "color": color
        })

    # ordenar: rojo, amarillo, verde
    orden = {"rojo": 1, "amarillo": 2, "verde": 3}
    resultado.sort(key=lambda x: orden[x["color"]])

    return resultado

@router.put("/{expediente_id}/asignar")
def asignar_persona(expediente_id: int, persona_id: int, db: Session = Depends(get_db)):

    # cerrar asignación actual
    actual = db.query(ExpedientePersona)\
        .filter(
            ExpedientePersona.expediente_id == expediente_id,
            ExpedientePersona.fecha_fin == None
        ).first()

    if actual:
        actual.fecha_fin = date.today()

    # nueva asignación
    nueva = ExpedientePersona(
        expediente_id=expediente_id,
        persona_id=persona_id
    )

    db.add(nueva)
    db.commit()

    return {"msg": "Asignación actualizada"}

@router.put("/{expediente_id}/finalizar")
def finalizar_expediente(expediente_id: int, db: Session = Depends(get_db)):

    expediente = db.query(Expediente).get(expediente_id)

    if not expediente:
        return {"error": "No existe"}

    # cerrar asignación activa
    actual = db.query(ExpedientePersona)\
        .filter(
            ExpedientePersona.expediente_id == expediente_id,
            ExpedientePersona.fecha_fin == None
        ).first()

    if actual:
        actual.fecha_fin = date.today()

    # marcar como finalizado
    expediente.activo = False
    expediente.estado = "finalizado"
    expediente.fecha_finalizacion = date.today()

    db.commit()

    return {"msg": "Expediente finalizado"}

@router.get("/estadisticas")
def estadisticas(db: Session = Depends(get_db)):

    personas = db.query(Persona).all()
    resultado = []

    for p in personas:
        total = db.query(ExpedientePersona)\
            .join(Expediente)\
            .filter(
                ExpedientePersona.persona_id == p.id,
                Expediente.activo == True,
                ExpedientePersona.fecha_fin == None
            ).count()

        resultado.append({
            "persona": p.nombre,
            "total_expedientes": total
        })

    return resultado

@router.get("/{id}")
def obtener_expediente(id: int, db: Session = Depends(get_db)):
    expediente = db.query(Expediente).get(id)

    if not expediente:
        return {"error": "No existe"}

    return expediente

@router.get("/{id}/historial")
def historial_expediente(id: int, db: Session = Depends(get_db)):

    historial = db.query(ExpedientePersona)\
        .filter(ExpedientePersona.expediente_id == id)\
        .all()

    resultado = []

    for h in historial:
        resultado.append({
            "persona_id": h.persona_id,
            "fecha_asignacion": h.fecha_asignacion,
            "fecha_fin": h.fecha_fin
        })

    return resultado

@router.post("/")
def crear_expediente(data: ExpedienteCreate, db: Session = Depends(get_db)):

    nuevo = Expediente(
        numero_expediente=data.numero_expediente,
        caratula=data.caratula,
        fecha_ingreso=data.fecha_ingreso,
        estado="pendiente",
        activo=True
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    asignacion = ExpedientePersona(
        expediente_id=nuevo.id,
        persona_id=data.persona_id
    )

    db.add(asignacion)
    db.commit()

    return {"msg": "creado", "id": nuevo.id}

@router.get("/")
def listar_expedientes(db: Session = Depends(get_db)):

    expedientes = db.query(Expediente).filter(Expediente.activo == True).all()

    resultado = []

    for e in expedientes:
        dias = dias_habiles(e.fecha_ingreso)
        color = calcular_color(e.fecha_ingreso)

        resultado.append({
            "id": e.id,
            "numero": e.numero_expediente,
            "caratula": e.caratula,
            "fecha_ingreso": e.fecha_ingreso,
            "dias": dias,
            "color": color
        })

    orden = {"rojo": 1, "amarillo": 2, "verde": 3}
    resultado.sort(key=lambda x: orden[x["color"]])

    return resultado
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models import Expediente, ExpedientePersona, Persona
from app.schemas.expediente import ExpedienteCreate
from app.utils.fechas import dias_habiles, calcular_estado

router = APIRouter(prefix="/expedientes", tags=["Expedientes"])


# ✅ CREAR EXPEDIENTE
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

    return {"msg": "Expediente creado", "id": nuevo.id}


# ✅ LISTAR EXPEDIENTES (CON TODA LA LÓGICA)
@router.get("/")
def listar_expedientes(db: Session = Depends(get_db)):

    expedientes = db.query(Expediente)\
        .filter(Expediente.activo == True)\
        .all()

    resultado = []

    for e in expedientes:
        dias = dias_habiles(e.fecha_ingreso)
        color, prioridad, dias = calcular_estado(e.fecha_ingreso)

        # 🔥 obtener responsable actual
        asignacion = db.query(ExpedientePersona)\
            .filter(
                ExpedientePersona.expediente_id == e.id,
                ExpedientePersona.fecha_fin == None
            ).first()

        responsable = None
        if asignacion:
            persona = db.query(Persona).get(asignacion.persona_id)
            responsable = persona.nombre if persona else None

        resultado.append({
            "id": e.id,
            "numero": e.numero_expediente,
            "caratula": e.caratula,
            "fecha_ingreso": e.fecha_ingreso,
            "estado": e.estado,
            "prioridad": prioridad,
            "tipo": e.tipo,
            "responsable": responsable,
            "fecha_limite": e.fecha_limite,
            "dias_sin_mover": dias,
            "accion": e.accion,
            "observaciones": e.observaciones,
            "color": color
        })

    # 🔥 ORDEN POR PRIORIDAD VISUAL
    orden = {
        "rojo_oscuro": 1,
        "rojo": 2,
        "naranja": 3,
        "amarillo": 4,
        "verde": 5
    }

    resultado.sort(key=lambda x: orden.get(x["color"], 99))

    return resultado


# ✅ EDITAR EXPEDIENTE
@router.put("/{id}")
def editar_expediente(id: int, data: dict, db: Session = Depends(get_db)):

    expediente = db.query(Expediente).get(id)

    if not expediente:
        raise HTTPException(status_code=404, detail="No existe")

    for key, value in data.items():
        setattr(expediente, key, value)

    db.commit()

    return {"msg": "Expediente actualizado"}


# ✅ ASIGNAR
@router.put("/{expediente_id}/asignar")
def asignar_expediente(expediente_id: int, persona_id: int, db: Session = Depends(get_db)):

    expediente = db.query(Expediente).get(expediente_id)
    if not expediente:
        raise HTTPException(status_code=404, detail="Expediente no existe")

    persona = db.query(Persona).get(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no existe")

    asignacion_actual = db.query(ExpedientePersona)\
        .filter(
            ExpedientePersona.expediente_id == expediente_id,
            ExpedientePersona.fecha_fin == None
        ).first()

    if asignacion_actual:
        asignacion_actual.fecha_fin = date.today()

    nueva = ExpedientePersona(
        expediente_id=expediente_id,
        persona_id=persona_id,
        fecha_asignacion=date.today()
    )

    db.add(nueva)
    db.commit()

    return {"msg": "Asignado correctamente"}


# ✅ FINALIZAR
@router.put("/{expediente_id}/finalizar")
def finalizar_expediente(expediente_id: int, db: Session = Depends(get_db)):

    expediente = db.query(Expediente).get(expediente_id)

    if not expediente:
        raise HTTPException(status_code=404, detail="No existe")

    expediente.activo = False
    expediente.fecha_finalizacion = date.today()

    asignacion = db.query(ExpedientePersona)\
        .filter(
            ExpedientePersona.expediente_id == expediente_id,
            ExpedientePersona.fecha_fin == None
        ).first()

    if asignacion:
        asignacion.fecha_fin = date.today()

    db.commit()

    return {"msg": "Finalizado correctamente"}


# ✅ ESTADISTICAS
@router.get("/estadisticas")
def estadisticas(db: Session = Depends(get_db)):

    personas = db.query(Persona).all()
    resultado = []

    for p in personas:
        asignaciones = db.query(ExpedientePersona)\
            .filter(
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
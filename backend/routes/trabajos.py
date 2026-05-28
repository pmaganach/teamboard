import json
from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Trabajo, TrabajoCreate, TrabajoUpdate, EstadoUpdate, Estado

router = APIRouter(prefix="/trabajos", tags=["trabajos"])


@router.get("/")
def listar_trabajos(
    analista_id : Optional[int]    = None,
    estado      : Optional[Estado] = None,
    area        : Optional[str]    = None,
    desde       : Optional[date]   = None,
    hasta       : Optional[date]   = None,
    session     : Session          = Depends(get_session)
):
    query = select(Trabajo)
    if analista_id : query = query.where(Trabajo.responsable_id == analista_id)
    if estado      : query = query.where(Trabajo.estado == estado)
    if area        : query = query.where(Trabajo.area_cliente == area)
    if hasta       : query = query.where((Trabajo.fecha_inicio <= hasta) | (Trabajo.fecha_inicio == None))
    if desde       : query = query.where((Trabajo.fecha_sla >= desde)   | (Trabajo.fecha_sla == None))
    return session.exec(query).all()


@router.post("/", status_code=201)
def crear_trabajo(trabajo: TrabajoCreate, session: Session = Depends(get_session)):
    data = trabajo.model_dump(exclude={'responsables_ids'})
    db_trabajo = Trabajo(**data)
    db_trabajo.area_equipo = "Customer Intelligence"
    if trabajo.responsables_ids:
        db_trabajo.responsables_ids = json.dumps(trabajo.responsables_ids)
        db_trabajo.responsable_id = trabajo.responsables_ids[0]
    session.add(db_trabajo)
    session.commit()
    session.refresh(db_trabajo)
    return db_trabajo


@router.put("/{id}")
def editar_trabajo(id: int, datos: TrabajoUpdate, session: Session = Depends(get_session)):
    trabajo = session.get(Trabajo, id)
    if not trabajo:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado")
    update_data = datos.model_dump(exclude_unset=True, exclude={'responsables_ids'})
    for campo, valor in update_data.items():
        setattr(trabajo, campo, valor)
    if datos.responsables_ids is not None:
        trabajo.responsables_ids = json.dumps(datos.responsables_ids)
        trabajo.responsable_id = datos.responsables_ids[0] if datos.responsables_ids else None
    session.commit()
    session.refresh(trabajo)
    return trabajo


@router.patch("/{id}/estado")
def cambiar_estado(id: int, datos: EstadoUpdate, session: Session = Depends(get_session)):
    trabajo = session.get(Trabajo, id)
    if not trabajo:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado")
    trabajo.estado = datos.estado
    session.commit()
    session.refresh(trabajo)
    return trabajo


@router.delete("/{id}", status_code=204)
def eliminar_trabajo(id: int, session: Session = Depends(get_session)):
    trabajo = session.get(Trabajo, id)
    if not trabajo:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado")
    session.delete(trabajo)
    session.commit()

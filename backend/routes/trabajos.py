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
    if desde       : query = query.where(Trabajo.fecha_sla >= desde)
    if hasta       : query = query.where(Trabajo.fecha_sla <= hasta)
    return session.exec(query).all()


@router.post("/", status_code=201)
def crear_trabajo(trabajo: TrabajoCreate, session: Session = Depends(get_session)):
    db_trabajo = Trabajo.model_validate(trabajo)
    session.add(db_trabajo)
    session.commit()
    session.refresh(db_trabajo)
    return db_trabajo


@router.put("/{id}")
def editar_trabajo(id: int, datos: TrabajoUpdate, session: Session = Depends(get_session)):
    trabajo = session.get(Trabajo, id)
    if not trabajo:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(trabajo, campo, valor)
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

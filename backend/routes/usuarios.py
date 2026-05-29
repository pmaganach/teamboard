from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Usuario, Nota
from pydantic import BaseModel

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/")
def listar_usuarios(session: Session = Depends(get_session)):
    return session.exec(select(Usuario).where(Usuario.activo == True).order_by(Usuario.nombre)).all()


# ── Notas ────────────────────────────────────────────────

class NotaCreate(BaseModel):
    texto             : str
    usuario_origen_id : int


@router.get("/{uid}/notas")
def listar_notas(uid: int, session: Session = Depends(get_session)):
    notas = session.exec(
        select(Nota).where(Nota.usuario_destino_id == uid).order_by(Nota.creado_en.desc())
    ).all()
    # Enriquecer con nombre del origen
    result = []
    for n in notas:
        origen = session.get(Usuario, n.usuario_origen_id)
        result.append({
            "id":                 n.id,
            "texto":              n.texto,
            "leida":              n.leida,
            "creado_en":          n.creado_en.isoformat(),
            "usuario_origen_id":  n.usuario_origen_id,
            "origen_nombre":      origen.nombre    if origen else "?",
            "origen_iniciales":   origen.iniciales if origen else "?",
            "origen_color":       origen.color     if origen else "#636466",
        })
    return result


@router.post("/{uid}/notas")
def agregar_nota(uid: int, body: NotaCreate, session: Session = Depends(get_session)):
    nota = Nota(
        usuario_destino_id=uid,
        usuario_origen_id=body.usuario_origen_id,
        texto=body.texto.strip(),
    )
    session.add(nota)
    session.commit()
    session.refresh(nota)
    return nota


@router.patch("/{uid}/notas/leer")
def marcar_leidas(uid: int, session: Session = Depends(get_session)):
    notas = session.exec(
        select(Nota).where(Nota.usuario_destino_id == uid, Nota.leida == False)
    ).all()
    for n in notas:
        n.leida = True
        session.add(n)
    session.commit()
    return {"ok": True}


@router.delete("/{uid}/notas/{nota_id}")
def eliminar_nota(uid: int, nota_id: int, session: Session = Depends(get_session)):
    nota = session.get(Nota, nota_id)
    if not nota or nota.usuario_destino_id != uid:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    session.delete(nota)
    session.commit()
    return {"ok": True}

from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from models import Usuario

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/")
def listar_usuarios(session: Session = Depends(get_session)):
    return session.exec(select(Usuario).where(Usuario.activo == True)).all()

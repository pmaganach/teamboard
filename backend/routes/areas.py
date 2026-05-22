from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from models import Area

router = APIRouter(prefix="/areas", tags=["areas"])


@router.get("/")
def listar_areas(session: Session = Depends(get_session)):
    return session.exec(select(Area)).all()


@router.post("/", status_code=201)
def crear_area(area: Area, session: Session = Depends(get_session)):
    session.add(area)
    session.commit()
    session.refresh(area)
    return area

from typing import Optional
from datetime import date, datetime
from sqlmodel import SQLModel, Field
from enum import Enum


class Estado(str, Enum):
    por_comenzar = "por_comenzar"
    en_gestion   = "en_gestion"
    en_revision  = "en_revision"
    pendiente    = "pendiente"
    completado   = "completado"


class Prioridad(str, Enum):
    alta  = "alta"
    media = "media"
    baja  = "baja"


class Rol(str, Enum):
    analista = "analista"
    gerente  = "gerente"


# ─── USUARIO ───────────────────────────────────────────
class Usuario(SQLModel, table=True):
    id        : Optional[int] = Field(default=None, primary_key=True)
    nombre    : str
    iniciales : str
    rol       : Rol  = Rol.analista
    color     : str  = "#636466"
    activo    : bool = True


# ─── ÁREA ──────────────────────────────────────────────
class Area(SQLModel, table=True):
    id        : Optional[int] = Field(default=None, primary_key=True)
    nombre    : str
    icono     : str = "📋"
    color     : str = "#636466"
    encargado : Optional[str] = None   # Nombre del encargado del área cliente


# ─── TRABAJO ───────────────────────────────────────────
class Trabajo(SQLModel, table=True):
    id             : Optional[int]  = Field(default=None, primary_key=True)
    nombre         : str
    area_cliente   : str
    responsable_id : Optional[int]  = Field(default=None, foreign_key="usuario.id")
    area_equipo    : Optional[str]  = None
    estado         : Estado         = Estado.por_comenzar
    progreso       : int            = 0
    prioridad      : Prioridad      = Prioridad.media
    fecha_inicio   : date           = Field(default_factory=date.today)
    fecha_sla      : Optional[date] = None
    comentarios    : Optional[str]  = None
    creado_en      : datetime       = Field(default_factory=datetime.now)


# Esquemas para crear/editar (sin id ni fechas automáticas)
class TrabajoCreate(SQLModel):
    nombre         : str
    area_cliente   : str
    responsable_id : Optional[int]  = None
    area_equipo    : Optional[str]  = None
    estado         : Estado         = Estado.por_comenzar
    progreso       : int            = 0
    prioridad      : Prioridad      = Prioridad.media
    fecha_sla      : Optional[date] = None
    comentarios    : Optional[str]  = None


class TrabajoUpdate(SQLModel):
    nombre         : Optional[str]       = None
    area_cliente   : Optional[str]       = None
    responsable_id : Optional[int]       = None
    area_equipo    : Optional[str]       = None
    estado         : Optional[Estado]    = None
    progreso       : Optional[int]       = None
    prioridad      : Optional[Prioridad] = None
    fecha_sla      : Optional[date]      = None
    comentarios    : Optional[str]       = None


class EstadoUpdate(SQLModel):
    estado: Estado


# ─── AUTH ───────────────────────────────────────────────
class UserAuth(SQLModel, table=True):
    id         : Optional[int] = Field(default=None, primary_key=True)
    email      : str           = Field(unique=True)
    nombre     : str
    rol        : Rol           = Rol.analista
    usuario_id : Optional[int] = Field(default=None, foreign_key="usuario.id")


class OTP(SQLModel, table=True):
    id         : Optional[int] = Field(default=None, primary_key=True)
    email      : str
    code       : str
    expires_at : datetime

from sqlmodel import Session, select
from database import engine
from models import Usuario, Area, Rol

USUARIOS = [
    {"nombre": "Aníbal Preez",        "iniciales": "AP", "rol": Rol.gerente,  "color": "#ED002F"},
    {"nombre": "Pablo Magaña",         "iniciales": "PM", "rol": Rol.analista, "color": "#10b981"},
    {"nombre": "Álvaro Román",         "iniciales": "AR", "rol": Rol.analista, "color": "#3b82f6"},
    {"nombre": "Miguel Bravo",         "iniciales": "MB", "rol": Rol.analista, "color": "#f59e0b"},
    {"nombre": "Karla Hidalgo",        "iniciales": "KH", "rol": Rol.analista, "color": "#a78bfa"},
    {"nombre": "Víctor Benítez",       "iniciales": "VB", "rol": Rol.analista, "color": "#06b6d4"},
    {"nombre": "Dominique Navarrete",  "iniciales": "DN", "rol": Rol.analista, "color": "#ec4899"},
    {"nombre": "Manuel Maldonado",     "iniciales": "MM", "rol": Rol.analista, "color": "#f97316"},
    {"nombre": "Wilmari Ruiz",         "iniciales": "WR", "rol": Rol.analista, "color": "#84cc16"},
]

AREAS = [
    {"nombre": "Comercial",    "icono": "📣", "color": "#ED002F"},
    {"nombre": "Postventa",    "icono": "🔧", "color": "#f59e0b"},
    {"nombre": "Operaciones",  "icono": "⚙️",  "color": "#3b82f6"},
    {"nombre": "Finanzas",     "icono": "💰", "color": "#10b981"},
    {"nombre": "RR.HH.",       "icono": "👥", "color": "#a78bfa"},
    {"nombre": "TI",           "icono": "💻", "color": "#06b6d4"},
    {"nombre": "Marketing",    "icono": "📊", "color": "#ec4899"},
    {"nombre": "Gerencia",     "icono": "🏢", "color": "#636466"},
]


def seed():
    with Session(engine) as session:
        # Usuarios
        existing = session.exec(select(Usuario)).first()
        if not existing:
            for u in USUARIOS:
                session.add(Usuario(**u))
            print("Usuarios cargados.")

        # Áreas
        existing_area = session.exec(select(Area)).first()
        if not existing_area:
            for a in AREAS:
                session.add(Area(**a))
            print("Áreas cargadas.")

        session.commit()


if __name__ == "__main__":
    from database import create_db
    create_db()
    seed()
    print("Seed completado.")

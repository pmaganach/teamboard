from sqlmodel import Session, select
from database import engine
from models import Usuario, Area, UserAuth, Rol

USUARIOS = [
    {"nombre": "Álvaro Román",         "iniciales": "AR", "rol": Rol.analista, "color": "#3b82f6"},
    {"nombre": "Aníbal Preez",         "iniciales": "AP", "rol": Rol.gerente,  "color": "#ED002F"},
    {"nombre": "Dominique Navarrete",  "iniciales": "DN", "rol": Rol.analista, "color": "#ec4899"},
    {"nombre": "Karla Hidalgo",        "iniciales": "KH", "rol": Rol.analista, "color": "#a78bfa"},
    {"nombre": "Manuel Maldonado",     "iniciales": "MM", "rol": Rol.analista, "color": "#f97316"},
    {"nombre": "Miguel Bravo",         "iniciales": "MB", "rol": Rol.analista, "color": "#f59e0b"},
    {"nombre": "Pablo Magaña",         "iniciales": "PM", "rol": Rol.analista, "color": "#84cc16"},
    {"nombre": "Víctor Benítez",       "iniciales": "VB", "rol": Rol.analista, "color": "#06b6d4"},
    {"nombre": "Wilmari Ruiz",         "iniciales": "WR", "rol": Rol.analista, "color": "#10b981"},
]

AREAS = [
    {"nombre": "Customer Intelligence",       "icono": "📈", "color": "#3b82f6", "encargado": "Aníbal Preez"},
    {"nombre": "Estrategia Comercial",        "icono": "🔍", "color": "#ED002F", "encargado": "Hyun Park"},
    {"nombre": "Operaciones Comerciales",     "icono": "🏪", "color": "#f59e0b", "encargado": "Natalia Sandoval"},
    {"nombre": "Performance & Reporting",     "icono": "📋", "color": "#10b981", "encargado": "Javier Fernández"},
    {"nombre": "Excelencia Operacional & CEX","icono": "⭐", "color": "#a78bfa", "encargado": "Rubén Tapia"},
    {"nombre": "Monitoring",                  "icono": "📡", "color": "#06b6d4", "encargado": "Raul Spano"},
    {"nombre": "Customer Care",               "icono": "📞", "color": "#ec4899", "encargado": "Marion Zembo"},
    {"nombre": "Field Service",               "icono": "🔧", "color": "#f97316", "encargado": "Felipe Vega"},
    {"nombre": "Otras Áreas",                 "icono": "🎯", "color": "#8A8C8E", "encargado": None},
]


USER_EMAILS = [
    {"nombre": "Aníbal Preez",        "email": "anibal.preez@verisure.cl",      "rol": Rol.gerente  },
    {"nombre": "Álvaro Román",        "email": "alvaro.roman@verisure.cl",      "rol": Rol.analista },
    {"nombre": "Dominique Navarrete", "email": "d.navarrete@verisure.cl",       "rol": Rol.analista },
    {"nombre": "Karla Hidalgo",       "email": "karla.hidalgo@verisure.cl",     "rol": Rol.analista },
    {"nombre": "Manuel Maldonado",    "email": "manuel.maldonado@verisure.cl",  "rol": Rol.analista },
    {"nombre": "Miguel Bravo",        "email": "miguel.bcaceres@verisure.cl",   "rol": Rol.analista },
    {"nombre": "Pablo Magaña",        "email": "pablo.magana@verisure.cl",      "rol": Rol.analista },
    {"nombre": "Víctor Benítez",      "email": "victor.benitez@verisure.cl",    "rol": Rol.analista },
    {"nombre": "Wilmari Ruiz",        "email": "wilmari.ruiz@verisure.cl",      "rol": Rol.analista },
    {"nombre": "Ignacio Algarra",     "email": "ignacio.algarra@verisure.cl",   "rol": Rol.gerente  },
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

        # UserAuth — vincula email con usuario_id
        existing_auth = session.exec(select(UserAuth)).first()
        if not existing_auth:
            for ue in USER_EMAILS:
                usuario = session.exec(
                    select(Usuario).where(Usuario.nombre == ue["nombre"])
                ).first()
                session.add(UserAuth(
                    email      = ue["email"],
                    nombre     = ue["nombre"],
                    rol        = ue["rol"],
                    usuario_id = usuario.id if usuario else None,
                ))
            session.commit()
            print("UserAuth cargados.")


if __name__ == "__main__":
    from database import create_db
    create_db()
    seed()
    print("Seed completado.")

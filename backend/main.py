from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db
from seed import seed
from routes import trabajos, usuarios, areas

app = FastAPI(title="TeamBoard API", version="1.0.0")

# CORS — acepta cualquier origen local (desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Al iniciar: crear tablas y cargar datos iniciales
@app.on_event("startup")
def on_startup():
    create_db()
    seed()


# Registrar rutas
app.include_router(trabajos.router)
app.include_router(usuarios.router)
app.include_router(areas.router)


@app.get("/")
def root():
    return {"status": "ok", "app": "TeamBoard API"}

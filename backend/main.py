# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from apscheduler.schedulers.background import BackgroundScheduler
# pyrefly: ignore [missing-import]
from apscheduler.triggers.cron import CronTrigger
import os
from dotenv import load_dotenv

load_dotenv()

from database import create_db
from seed import seed
from routes import trabajos, usuarios, areas, auth
from reminders import job_lunes, job_miercoles, job_viernes

app = FastAPI(title="TeamBoard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler(timezone=os.getenv("TZ", "America/Santiago"))


@app.on_event("startup")
def on_startup():
    create_db()
    seed()
    # Lunes 09:00 — Resumen semanal
    scheduler.add_job(job_lunes,     CronTrigger(day_of_week="mon", hour=9,  minute=0))
    # Miércoles 09:00 — Seguimiento mid-week
    scheduler.add_job(job_miercoles, CronTrigger(day_of_week="wed", hour=9,  minute=0))
    # Viernes 12:00 — Cierre de semana
    scheduler.add_job(job_viernes,   CronTrigger(day_of_week="fri", hour=12, minute=0))
    scheduler.start()
    print("[scheduler] Recordatorios programados: Lun 9am · Mié 9am · Vie 12pm")


@app.on_event("shutdown")
def on_shutdown():
    scheduler.shutdown()


app.include_router(auth.router)
app.include_router(trabajos.router)
app.include_router(usuarios.router)
app.include_router(areas.router)


# ── Endpoints de prueba (disparo manual) ──────────────────────────
@app.post("/reminders/test/lunes", tags=["reminders"])
def test_lunes():
    job_lunes()
    return {"ok": True, "mensaje": "Correo de lunes enviado (modo prueba)"}

@app.post("/reminders/test/miercoles", tags=["reminders"])
def test_miercoles():
    job_miercoles()
    return {"ok": True, "mensaje": "Correo de miércoles enviado (modo prueba)"}

@app.post("/reminders/test/viernes", tags=["reminders"])
def test_viernes():
    job_viernes()
    return {"ok": True, "mensaje": "Correo de viernes enviado (modo prueba)"}


@app.post("/test-otp-email")
def test_otp_email():
    import requests as req
    r = req.post("https://mandrillapp.com/api/1.0/messages/send", json={
        "key": os.getenv("MANDRILL_API_KEY"),
        "message": {
            "from_email": "noreply@verisure.cl",
            "from_name": "Bitacora",
            "to": [{"email": "pablo.magana@verisure.cl", "name": "Pablo"}],
            "subject": "Test desde uvicorn",
            "html": "<p>Este correo lo mando el backend uvicorn directamente.</p>"
        }
    }, timeout=10)
    return {"status": r.status_code, "body": r.json()}


@app.get("/")
def root():
    return {"status": "ok", "app": "TeamBoard API"}

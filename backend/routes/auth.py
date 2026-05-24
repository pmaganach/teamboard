import random
import string
import requests
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import UserAuth, OTP

router = APIRouter(prefix="/auth", tags=["auth"])

MANDRILL_API_KEY = "md-c5Cl5K6R5KA67QO5PML3mQ"
OTP_EXPIRY_MIN   = 10


def _send_otp_email(email: str, code: str, nombre: str):
    payload = {
        "key": MANDRILL_API_KEY,
        "message": {
            "from_email": "noreply@verisure.cl",
            "from_name":  "Bitácora · Customer Intelligence",
            "to": [{"email": email, "name": nombre}],
            "subject": f"{code} es tu código de acceso",
            "text": f"Hola {nombre},\n\nTu código de acceso a Bitácora es: {code}\n\nVence en {OTP_EXPIRY_MIN} minutos.\n\nSi no solicitaste este código, ignora este mensaje.",
            "html": f"""
            <div style="font-family:sans-serif;max-width:480px;margin:0 auto;padding:32px">
              <h2 style="color:#ED002F;margin-bottom:8px">Bitácora</h2>
              <p style="color:#64748b;font-size:13px;margin-bottom:24px">Customer Intelligence · Verisure</p>
              <p style="color:#1e293b">Hola <strong>{nombre}</strong>,</p>
              <p style="color:#1e293b">Tu código de acceso es:</p>
              <div style="background:#f1f5f9;border-radius:12px;padding:24px;text-align:center;margin:20px 0">
                <span style="font-size:36px;font-weight:900;letter-spacing:8px;color:#ED002F">{code}</span>
              </div>
              <p style="color:#64748b;font-size:12px">Vence en {OTP_EXPIRY_MIN} minutos.</p>
            </div>"""
        }
    }
    requests.post("https://mandrillapp.com/api/1.0/messages/send", json=payload, timeout=10)


@router.post("/request-otp")
def request_otp(body: dict, session: Session = Depends(get_session)):
    email = body.get("email", "").strip().lower()
    if not email.endswith("@verisure.cl"):
        raise HTTPException(400, "Solo correos @verisure.cl")

    user = session.exec(select(UserAuth).where(UserAuth.email == email)).first()
    if not user:
        raise HTTPException(404, "Correo no registrado en el equipo")

    # Eliminar OTPs anteriores del mismo email
    old = session.exec(select(OTP).where(OTP.email == email)).all()
    for o in old:
        session.delete(o)

    code = "".join(random.choices(string.digits, k=6))
    otp  = OTP(email=email, code=code, expires_at=datetime.now() + timedelta(minutes=OTP_EXPIRY_MIN))
    session.add(otp)
    session.commit()

    _send_otp_email(email, code, user.nombre)
    return {"ok": True}


@router.post("/verify-otp")
def verify_otp(body: dict, session: Session = Depends(get_session)):
    email = body.get("email", "").strip().lower()
    code  = body.get("code", "").strip()

    otp = session.exec(
        select(OTP).where(OTP.email == email, OTP.code == code)
    ).first()

    if not otp:
        raise HTTPException(401, "Código incorrecto")
    if otp.expires_at < datetime.now():
        session.delete(otp)
        session.commit()
        raise HTTPException(401, "Código expirado")

    user = session.exec(select(UserAuth).where(UserAuth.email == email)).first()
    session.delete(otp)
    session.commit()

    return {
        "id":         user.id,
        "email":      user.email,
        "nombre":     user.nombre,
        "rol":        user.rol,
        "usuario_id": user.usuario_id,
    }

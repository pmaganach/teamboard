"""
Recordatorios automáticos — Bitácora · Customer Intelligence
Lunes 9am     → Resumen semanal
Miércoles 9am → Seguimiento mid-week
Viernes 12pm  → Cierre de semana
"""

import os
import requests
from datetime import date, timedelta
from sqlmodel import Session, select
from dotenv import load_dotenv
from database import engine
from models import Trabajo, UserAuth, Usuario, Estado, Rol

load_dotenv()

MANDRILL_API_KEY = os.getenv("MANDRILL_API_KEY")
FROM_EMAIL       = os.getenv("FROM_EMAIL", "noreply@verisure.cl")
FROM_NAME        = os.getenv("FROM_NAME", "Bitácora · Customer Intelligence")
APP_URL          = os.getenv("APP_URL", "https://verisure.vicbc.cl/bitacora-equipo-ci/")

TEST_MODE  = os.getenv("TEST_MODE", "True").lower() == "true"
TEST_EMAIL = os.getenv("TEST_EMAIL", "pablo.magana@verisure.cl")

ESTADOS_ACTIVOS = [Estado.por_comenzar, Estado.en_gestion, Estado.en_revision, Estado.pendiente]

ESTADO_LABEL = {
    "por_comenzar": "Por comenzar",
    "en_gestion":   "En gestión",
    "en_revision":  "En revisión",
    "pendiente":    "Pendiente",
    "completado":   "Completado",
}
PRIO_COLOR = {"alta": "#ED002F", "media": "#f59e0b", "baja": "#10b981"}
PRIO_BG    = {"alta": "#fde8e8", "media": "#fef9ec", "baja": "#f0fdf4"}
PRIO_LABEL = {"alta": "Alta", "media": "Media", "baja": "Baja"}


# ── ENVÍO MANDRILL ────────────────────────────────────────────────
def _send(to_email: str, to_nombre: str, subject: str, html: str):
    dest = TEST_EMAIL if TEST_MODE else to_email
    payload = {
        "key": MANDRILL_API_KEY,
        "message": {
            "from_email": FROM_EMAIL,
            "from_name":  FROM_NAME,
            "to": [{"email": dest, "name": to_nombre}],
            "subject": subject,
            "html": html,
        }
    }
    try:
        r = requests.post("https://mandrillapp.com/api/1.0/messages/send", json=payload, timeout=10)
        print(f"[reminders] OK Enviado a {dest} | {r.json()[0]['status']}")
    except Exception as e:
        print(f"[reminders] ERROR: {e}")


# ── COMPONENTES HTML ──────────────────────────────────────────────
def _header(titulo: str, subtitulo: str, acento: str, emoji: str) -> str:
    return f"""
    <tr>
      <td style="background:#AB0020;padding:28px 36px 24px">
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td>
              <div style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#ffffff;margin-bottom:8px">Customer Intelligence &middot; Verisure</div>
              <div style="font-size:22px;font-weight:800;color:#ffffff;line-height:1.2">{titulo}</div>
              <div style="font-size:13px;color:#ffffff;opacity:0.85;margin-top:5px">{subtitulo}</div>
            </td>
            <td align="right" valign="top">
              <div style="width:42px;height:42px;background:{acento};border-radius:10px;text-align:center;line-height:42px;font-size:20px">{emoji}</div>
            </td>
          </tr>
        </table>
      </td>
    </tr>"""


def _footer() -> str:
    return """
    <tr>
      <td style="background:#f8f8f8;padding:18px 36px;border-top:1px solid #f0f0f0">
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td><span style="font-size:11px;color:#bbb">Bit&aacute;cora &middot; Customer Intelligence &middot; Verisure Chile</span></td>
            <td align="right"><span style="font-size:11px;color:#ddd">Recordatorio autom&aacute;tico</span></td>
          </tr>
        </table>
      </td>
    </tr>"""


def _cta(texto: str, color: str) -> str:
    return f"""
    <div style="height:1px;background:#f0f0f0;margin-bottom:24px"></div>
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr><td align="center">
        <a href="{APP_URL}" style="display:inline-block;background:{color};color:#ffffff;text-decoration:none;font-size:13px;font-weight:700;padding:13px 32px;border-radius:8px;letter-spacing:.3px">
          {texto} &rarr;
        </a>
      </td></tr>
    </table>"""


def _section_title(texto: str, color: str) -> str:
    return f"""
    <div style="margin-bottom:14px">
      <div style="width:3px;height:16px;background:{color};border-radius:2px;display:inline-block;vertical-align:middle;margin-right:8px"></div>
      <span style="font-size:10px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:{color};vertical-align:middle">{texto}</span>
    </div>"""


def _trabajo_card(t, urgente: bool = False, warn: bool = False) -> str:
    prio    = str(t.prioridad) if hasattr(t, 'prioridad') else "media"
    estado  = ESTADO_LABEL.get(str(t.estado), str(t.estado)) if hasattr(t, 'estado') else "—"
    progreso = t.progreso if hasattr(t, 'progreso') else 0
    area    = t.area_cliente if hasattr(t, 'area_cliente') else ""
    nombre  = t.nombre if hasattr(t, 'nombre') else str(t)
    sla_str = ""
    border_color = "#fde8e8" if urgente else "#fef3cd" if warn else "#f0f0f0"
    bg_color     = "#fff8f8" if urgente else "#fffdf5" if warn else "#ffffff"
    bar_color    = "#ED002F" if urgente else "#f59e0b" if warn else "#3b82f6"

    if hasattr(t, 'fecha_sla') and t.fecha_sla:
        dias = (t.fecha_sla - date.today()).days
        chip_color = "#ED002F" if dias <= 0 else "#f59e0b" if dias <= 3 else "#888"
        chip_bg    = "#fde8e8" if dias <= 0 else "#fef3cd" if dias <= 3 else "#f0f0f0"
        label      = "Vencido" if dias < 0 else "Vence hoy" if dias == 0 else f"Vence en {dias}d"
        sla_str    = f'<span style="background:{chip_bg};color:{chip_color};font-size:10px;font-weight:800;padding:4px 10px;border-radius:20px;white-space:nowrap">{label}</span>'

    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:7px;border:1px solid {border_color};border-radius:10px;overflow:hidden">
      <tr>
        <td style="background:{bg_color};padding:14px 16px">
          <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
              <td>
                <div style="font-size:13px;font-weight:700;color:#1a1a1a;margin-bottom:3px">{nombre}</div>
                <div style="font-size:11px;color:#888">{area} &middot; {estado} &middot; Progreso {progreso}%</div>
              </td>
              <td align="right" valign="top" style="padding-left:12px">
                {sla_str if sla_str else f'<span style="background:{PRIO_BG.get(prio,"#f0f0f0")};color:{PRIO_COLOR.get(prio,"#888")};font-size:10px;font-weight:700;padding:3px 8px;border-radius:6px">{PRIO_LABEL.get(prio,"—")}</span>'}
              </td>
            </tr>
            <tr>
              <td colspan="2" style="padding-top:10px">
                <div style="background:#efefef;border-radius:4px;height:5px;overflow:hidden">
                  <div style="background:{bar_color};height:100%;width:{progreso}%;border-radius:4px"></div>
                </div>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>"""


def _trabajo_card_dict(t: dict) -> str:
    """Versión que acepta diccionario para datos de prueba."""
    class Obj:
        pass
    o = Obj()
    for k, v in t.items():
        setattr(o, k, v)
    urgente = t.get('_urgente', False)
    warn    = t.get('_warn', False)
    return _trabajo_card(o, urgente=urgente, warn=warn)


# ── QUERIES ───────────────────────────────────────────────────────
def _get_trabajos_de(usuario_id: int, session: Session):
    return session.exec(
        select(Trabajo).where(
            Trabajo.responsable_id == usuario_id,
            Trabajo.estado.in_(ESTADOS_ACTIVOS)
        )
    ).all()


def _get_usuarios(session: Session):
    return session.exec(select(UserAuth)).all()


def _es_gerente(user: UserAuth, session: Session) -> bool:
    if not user.usuario_id:
        return False
    u = session.get(Usuario, user.usuario_id)
    return u is not None and u.rol == Rol.gerente


# ── REPORTE GERENTE ────────────────────────────────────────────────
def _analista_seccion(nombre: str, trabajos, hoy: date, highlight_fn) -> str:
    iniciales = "".join(p[0].upper() for p in nombre.split()[:2])
    rows = "".join(highlight_fn(t, hoy) for t in trabajos)
    total = len(trabajos)
    prog_avg = int(sum(t.progreso for t in trabajos) / total) if total else 0
    return f"""
    <div style="margin-bottom:20px;border:1px solid #f0f0f0;border-radius:12px;overflow:hidden">
      <div style="background:#f8f8f8;padding:12px 16px;display:flex;align-items:center">
        <div style="width:30px;height:30px;border-radius:50%;background:#AB002018;color:#AB0020;font-size:11px;font-weight:800;display:inline-flex;align-items:center;justify-content:center;margin-right:10px;flex-shrink:0">{iniciales}</div>
        <span style="font-size:13px;font-weight:700;color:#1a1a1a">{nombre}</span>
        <span style="margin-left:auto;font-size:11px;color:#888">{total} activo{'s' if total!=1 else ''} &middot; Prom. {prog_avg}%</span>
      </div>
      <div style="padding:12px 14px">
        {rows}
      </div>
    </div>"""


def _html_reporte_gerente(titulo: str, subtitulo: str, acento: str, emoji: str,
                           intro: str, analistas_data: list) -> str:
    hoy = date.today()
    total_global   = sum(d['total'] for d in analistas_data)
    riesgo_global  = sum(d['riesgo'] for d in analistas_data)
    secciones = "".join(d['html'] for d in analistas_data)

    resumen = f"""
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:24px">
      <tr>
        <td align="center" style="padding:0 6px">
          <div style="background:#f8f8f8;border-radius:10px;padding:14px 10px;text-align:center">
            <div style="font-size:22px;font-weight:800;color:#1a1a1a">{total_global}</div>
            <div style="font-size:10px;color:#888;margin-top:2px">Trabajos activos</div>
          </div>
        </td>
        <td align="center" style="padding:0 6px">
          <div style="background:#fde8e8;border-radius:10px;padding:14px 10px;text-align:center">
            <div style="font-size:22px;font-weight:800;color:#ED002F">{riesgo_global}</div>
            <div style="font-size:10px;color:#ED002F;margin-top:2px">SLA en riesgo</div>
          </div>
        </td>
        <td align="center" style="padding:0 6px">
          <div style="background:#f8f8f8;border-radius:10px;padding:14px 10px;text-align:center">
            <div style="font-size:22px;font-weight:800;color:#1a1a1a">{len(analistas_data)}</div>
            <div style="font-size:10px;color:#888;margin-top:2px">Analistas activos</div>
          </div>
        </td>
      </tr>
    </table>"""

    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width:620px;margin:0 auto;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.10);font-family:-apple-system,'Segoe UI',Arial,sans-serif">
      {_header(titulo, subtitulo, acento, emoji)}
      <tr>
        <td style="background:#ffffff;padding:32px 36px">
          <p style="margin:0 0 6px;font-size:15px;font-weight:700;color:#1a1a1a">Hola An&iacute;bal,</p>
          <p style="margin:0 0 24px;font-size:13px;color:#666;line-height:1.6">{intro}</p>
          <div style="height:1px;background:#f0f0f0;margin-bottom:24px"></div>
          {resumen}
          <div style="margin-bottom:8px">
            {_section_title("Estado del equipo", acento)}
          </div>
          {secciones}
          {_cta("Ver Bit&aacute;cora completa", acento)}
        </td>
      </tr>
      {_footer()}
    </table>"""


# ══════════════════════════════════════════════════════════════════
# LUNES — Resumen semanal
# ══════════════════════════════════════════════════════════════════
def _html_lunes(nombre: str, trabajos, en_riesgo) -> str:
    hoy = date.today()
    total = len(trabajos)
    rows_riesgo = "".join(_trabajo_card(t, urgente=(t.fecha_sla and (t.fecha_sla - hoy).days <= 2), warn=(t.fecha_sla and 2 < (t.fecha_sla - hoy).days <= 5)) for t in en_riesgo)
    rows_todos  = "".join(_trabajo_card(t) for t in trabajos if not (t.fecha_sla and (t.fecha_sla - hoy).days <= 7))

    seccion_riesgo = ""
    if en_riesgo:
        seccion_riesgo = f"""
        <div style="margin-bottom:24px">
          {_section_title("SLA en riesgo esta semana", "#ED002F")}
          {rows_riesgo}
        </div>"""

    seccion_todos = ""
    if rows_todos:
        seccion_todos = f"""
        <div style="margin-bottom:28px">
          {_section_title("Tus trabajos activos", "#3b82f6")}
          {rows_todos}
        </div>"""

    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width:580px;margin:0 auto;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.10);font-family:-apple-system,'Segoe UI',Arial,sans-serif">
      {_header("Resumen semanal", f"Semana del {hoy.strftime('%d de %B, %Y')}", "#ED002F", "📋")}
      <tr>
        <td style="background:#ffffff;padding:32px 36px">
          <p style="margin:0 0 6px;font-size:15px;font-weight:700;color:#1a1a1a">Hola {nombre},</p>
          <p style="margin:0 0 28px;font-size:13px;color:#666;line-height:1.6">
            Aqu&iacute; tienes tu resumen para comenzar la semana. Tienes <strong style="color:#1a1a1a">{total} trabajo{'s' if total!=1 else ''} activo{'s' if total!=1 else ''}</strong> — te compartimos el estado actual y lo que requiere atenci&oacute;n.
          </p>
          <div style="height:1px;background:#f0f0f0;margin-bottom:24px"></div>
          {seccion_riesgo}
          {seccion_todos}
          {_cta("Ver mis trabajos en Bit&aacute;cora", "#ED002F")}
        </td>
      </tr>
      {_footer()}
    </table>"""


def job_lunes():
    hoy = date.today()
    fin_semana = hoy + timedelta(days=7)
    with Session(engine) as session:
        usuarios = _get_usuarios(session)
        # Reporte gerente
        analistas_data = []
        for user in usuarios:
            if not user.usuario_id or _es_gerente(user, session):
                continue
            trabajos = _get_trabajos_de(user.usuario_id, session)
            if not trabajos:
                continue
            riesgo = [t for t in trabajos if t.fecha_sla and t.fecha_sla <= fin_semana]
            def hl(t, hoy=hoy, fin=fin_semana):
                u = t.fecha_sla and (t.fecha_sla - hoy).days <= 7
                w = t.fecha_sla and 7 < (t.fecha_sla - hoy).days <= 14
                return _trabajo_card(t, urgente=u, warn=w)
            analistas_data.append({
                'total': len(trabajos), 'riesgo': len(riesgo),
                'html': _analista_seccion(user.nombre, trabajos, hoy, hl)
            })
        # Envío
        for user in usuarios:
            if not user.usuario_id:
                continue
            if _es_gerente(user, session):
                if not analistas_data:
                    continue
                intro = f"Aqu&iacute; tienes el estado del equipo para arrancar la semana. {sum(d['total'] for d in analistas_data)} trabajos activos en total, {sum(d['riesgo'] for d in analistas_data)} con SLA en riesgo esta semana."
                html = _html_reporte_gerente("Reporte semanal del equipo", f"Semana del {hoy.strftime('%d de %B, %Y')}", "#ED002F", "📊", intro, analistas_data)
                _send(user.email, user.nombre, f"📊 Reporte semanal del equipo · {hoy.strftime('%d/%m')} — Bit\u00e1cora", html)
            else:
                trabajos = _get_trabajos_de(user.usuario_id, session)
                if not trabajos:
                    continue
                en_riesgo = [t for t in trabajos if t.fecha_sla and t.fecha_sla <= fin_semana]
                html = _html_lunes(user.nombre, trabajos, en_riesgo)
                _send(user.email, user.nombre, f"📋 Resumen semanal · {hoy.strftime('%d/%m')} — Bit\u00e1cora", html)


# ══════════════════════════════════════════════════════════════════
# MIÉRCOLES — Seguimiento mid-week
# ══════════════════════════════════════════════════════════════════
def _html_miercoles(nombre: str, trabajos, sin_avance, en_riesgo) -> str:
    hoy = date.today()
    rows_sin    = "".join(_trabajo_card(t, warn=True) for t in sin_avance)
    rows_riesgo = "".join(_trabajo_card(t, urgente=True) for t in en_riesgo)

    if not sin_avance and not en_riesgo:
        contenido = """
        <div style="background:#f0fdf4;border:1px solid #d1fae5;border-radius:10px;padding:18px 20px;margin-bottom:28px">
          <p style="margin:0;font-size:13px;color:#065f46;line-height:1.6">
            &#x2714; Todo parece estar al d&iacute;a. Sigue as&iacute; &mdash; tu equipo lo nota.
          </p>
        </div>"""
    else:
        seccion_sin = f"""
        <div style="margin-bottom:24px">
          {_section_title("Requieren atenci&oacute;n &middot; Progreso bajo", "#f59e0b")}
          {rows_sin}
        </div>""" if sin_avance else ""

        seccion_riesgo = f"""
        <div style="margin-bottom:24px">
          {_section_title("SLA en riesgo esta semana", "#ED002F")}
          {rows_riesgo}
        </div>""" if en_riesgo else ""

        contenido = f"""
        {seccion_sin}
        {seccion_riesgo}
        <div style="background:#f8f8f8;border-radius:10px;padding:16px 20px;margin-bottom:28px">
          <p style="margin:0;font-size:12px;color:#888;line-height:1.6">
            &#x1F4A1; <strong style="color:#555">Recuerda:</strong> Mantener el progreso actualizado permite que el equipo tenga visibilidad real del trabajo. Solo toma un minuto.
          </p>
        </div>"""

    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width:580px;margin:0 auto;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.10);font-family:-apple-system,'Segoe UI',Arial,sans-serif">
      {_header("Seguimiento mid-week", f"Mi&eacute;rcoles {hoy.strftime('%d de %B, %Y')}", "#f59e0b", "⚡")}
      <tr>
        <td style="background:#ffffff;padding:32px 36px">
          <p style="margin:0 0 6px;font-size:15px;font-weight:700;color:#1a1a1a">Hola {nombre},</p>
          <p style="margin:0 0 28px;font-size:13px;color:#666;line-height:1.6">
            A mitad de semana, te compartimos un vistazo r&aacute;pido a los trabajos que necesitan atenci&oacute;n antes del cierre.
          </p>
          <div style="height:1px;background:#f0f0f0;margin-bottom:24px"></div>
          {contenido}
          {_cta("Actualizar mis trabajos", "#f59e0b")}
        </td>
      </tr>
      {_footer()}
    </table>"""


def job_miercoles():
    hoy = date.today()
    limite_sla = hoy + timedelta(days=7)
    with Session(engine) as session:
        usuarios = _get_usuarios(session)
        analistas_data = []
        for user in usuarios:
            if not user.usuario_id or _es_gerente(user, session):
                continue
            trabajos = _get_trabajos_de(user.usuario_id, session)
            if not trabajos:
                continue
            riesgo = [t for t in trabajos if t.fecha_sla and t.fecha_sla <= limite_sla]
            sin_avance = [t for t in trabajos if t.progreso <= 25]
            def hl(t, hoy=hoy, lim=limite_sla):
                u = t.fecha_sla and t.fecha_sla <= lim
                w = t.progreso <= 25
                return _trabajo_card(t, urgente=u, warn=w and not u)
            analistas_data.append({
                'total': len(trabajos), 'riesgo': len(riesgo),
                'html': _analista_seccion(user.nombre, trabajos, hoy, hl)
            })
        for user in usuarios:
            if not user.usuario_id:
                continue
            if _es_gerente(user, session):
                if not analistas_data:
                    continue
                intro = f"A mitad de semana, aqu&iacute; tienes el seguimiento del equipo. {sum(d['riesgo'] for d in analistas_data)} trabajo(s) con SLA en riesgo esta semana."
                html = _html_reporte_gerente("Seguimiento mid-week", f"Mi&eacute;rcoles {hoy.strftime('%d de %B, %Y')}", "#f59e0b", "⚡", intro, analistas_data)
                _send(user.email, user.nombre, "⚡ Seguimiento mid-week del equipo — Bit\u00e1cora", html)
            else:
                trabajos = _get_trabajos_de(user.usuario_id, session)
                if not trabajos:
                    continue
                sin_avance = [t for t in trabajos if t.progreso <= 25]
                en_riesgo  = [t for t in trabajos if t.fecha_sla and t.fecha_sla <= limite_sla]
                html = _html_miercoles(user.nombre, trabajos, sin_avance, en_riesgo)
                _send(user.email, user.nombre, "⚡ Seguimiento mid-week — Bit\u00e1cora", html)


# ══════════════════════════════════════════════════════════════════
# VIERNES — Cierre de semana
# ══════════════════════════════════════════════════════════════════
def _html_viernes(nombre: str, trabajos, sin_actualizar) -> str:
    hoy = date.today()
    total = len(trabajos)
    rows = "".join(_trabajo_card(t) for t in sin_actualizar)

    seccion_pendientes = f"""
    <div style="margin-bottom:24px">
      {_section_title("Pendientes de actualizar", "#ED002F")}
      {rows}
    </div>""" if sin_actualizar else ""

    cierre = """
    <div style="background:#f0fdf4;border:1px solid #d1fae5;border-radius:10px;padding:16px 20px;margin-bottom:28px">
      <p style="margin:0;font-size:12px;color:#065f46;line-height:1.6">
        &#x2714; Un equipo informado toma mejores decisiones. Gracias por mantener Bit&aacute;cora al d&iacute;a &mdash; que tengas un excelente fin de semana.
      </p>
    </div>"""

    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width:580px;margin:0 auto;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.10);font-family:-apple-system,'Segoe UI',Arial,sans-serif">
      {_header("Cierre de semana", f"Viernes {hoy.strftime('%d de %B, %Y')}", "#10b981", "✅")}
      <tr>
        <td style="background:#ffffff;padding:32px 36px">
          <p style="margin:0 0 6px;font-size:15px;font-weight:700;color:#1a1a1a">Hola {nombre},</p>
          <p style="margin:0 0 28px;font-size:13px;color:#666;line-height:1.6">
            Ya es viernes &mdash; antes de cerrar la semana, t&oacute;mate un momento para dejar tus trabajos al d&iacute;a. Es lo que nos permite arrancar el lunes con claridad. Tienes <strong style="color:#1a1a1a">{total} trabajo{'s' if total!=1 else ''} activo{'s' if total!=1 else ''}</strong>.
          </p>
          <div style="height:1px;background:#f0f0f0;margin-bottom:24px"></div>
          {seccion_pendientes}
          {cierre}
          {_cta("Cerrar la semana en Bit&aacute;cora", "#10b981")}
        </td>
      </tr>
      {_footer()}
    </table>"""


def job_viernes():
    hoy = date.today()
    with Session(engine) as session:
        usuarios = _get_usuarios(session)
        analistas_data = []
        for user in usuarios:
            if not user.usuario_id or _es_gerente(user, session):
                continue
            trabajos = _get_trabajos_de(user.usuario_id, session)
            if not trabajos:
                continue
            sin_act = [t for t in trabajos if t.progreso == 0 or t.estado == Estado.por_comenzar]
            def hl(t, sa=sin_act):
                return _trabajo_card(t, warn=(t in sa))
            analistas_data.append({
                'total': len(trabajos), 'riesgo': len(sin_act),
                'html': _analista_seccion(user.nombre, trabajos, hoy, hl)
            })
        for user in usuarios:
            if not user.usuario_id:
                continue
            if _es_gerente(user, session):
                if not analistas_data:
                    continue
                sin_act_total = sum(d['riesgo'] for d in analistas_data)
                intro = f"Aqu&iacute; tienes el cierre de semana del equipo. {sin_act_total} trabajo(s) sin actualizaci&oacute;n &mdash; buen momento para hacer seguimiento antes del fin de semana."
                html = _html_reporte_gerente("Cierre de semana", f"Viernes {hoy.strftime('%d de %B, %Y')}", "#10b981", "📋", intro, analistas_data)
                _send(user.email, user.nombre, "📋 Cierre de semana del equipo — Bit\u00e1cora", html)
            else:
                trabajos = _get_trabajos_de(user.usuario_id, session)
                if not trabajos:
                    continue
                sin_actualizar = [t for t in trabajos if t.progreso == 0 or t.estado == Estado.por_comenzar]
                html = _html_viernes(user.nombre, trabajos, sin_actualizar)
                _send(user.email, user.nombre, "✅ \u00bfTodo al d\u00eda antes del fin de semana? — Bit\u00e1cora", html)


# ══════════════════════════════════════════════════════════════════
# FUNCIONES DE PRUEBA CON DATOS MOCK
# ══════════════════════════════════════════════════════════════════
class _MockTrabajo:
    def __init__(self, nombre, area, estado, progreso, prioridad, fecha_sla=None):
        self.nombre      = nombre
        self.area_cliente = area
        self.estado      = type('E', (), {'__str__': lambda s: estado})()
        self.progreso    = progreso
        self.prioridad   = type('P', (), {'__str__': lambda s: prioridad})()
        self.fecha_sla   = fecha_sla


def test_lunes():
    hoy = date.today()
    trabajos = [
        _MockTrabajo("Análisis de churn Q2",       "Customer Care",          "en_gestion",   40, "alta",  hoy + timedelta(days=2)),
        _MockTrabajo("Reporte NPS Mayo",            "Performance & Reporting","en_revision",  65, "media", hoy + timedelta(days=5)),
        _MockTrabajo("Modelo de propensión",        "Customer Intelligence",  "por_comenzar",  0, "alta"),
        _MockTrabajo("Dashboard Cobranza Activa",   "Field Service",          "en_gestion",   50, "media"),
        _MockTrabajo("Análisis de rotación RRHH",   "Excelencia Operacional", "en_revision",  75, "baja"),
    ]
    en_riesgo = [t for t in trabajos if t.fecha_sla and (t.fecha_sla - hoy).days <= 7]
    html = _html_lunes("Pablo", trabajos, en_riesgo)
    _send(TEST_EMAIL, "Pablo", f"📋 Resumen semanal · {hoy.strftime('%d/%m')} — Bitácora", html)


def test_miercoles():
    hoy = date.today()
    trabajos = [
        _MockTrabajo("Modelo de propensión",      "Customer Intelligence",  "por_comenzar",  0, "alta"),
        _MockTrabajo("Análisis de churn Q2",      "Customer Care",          "en_gestion",   40, "alta",  hoy + timedelta(days=2)),
        _MockTrabajo("Dashboard Cobranza Activa", "Field Service",          "en_gestion",   50, "media"),
    ]
    sin_avance = [t for t in trabajos if t.progreso <= 25]
    en_riesgo  = [t for t in trabajos if t.fecha_sla and (t.fecha_sla - hoy).days <= 7]
    html = _html_miercoles("Pablo", trabajos, sin_avance, en_riesgo)
    _send(TEST_EMAIL, "Pablo", "⚡ Seguimiento mid-week — Bitácora", html)


def test_viernes():
    trabajos = [
        _MockTrabajo("Modelo de propensión",        "Customer Intelligence",  "por_comenzar",  0, "alta"),
        _MockTrabajo("Análisis de churn Q2",        "Customer Care",          "en_gestion",   40, "alta"),
        _MockTrabajo("Dashboard Cobranza Activa",   "Field Service",          "en_gestion",   50, "media"),
        _MockTrabajo("Análisis de rotación RRHH",   "Excelencia Operacional", "en_revision",  75, "baja"),
    ]
    sin_actualizar = [t for t in trabajos if t.progreso == 0]
    html = _html_viernes("Pablo", trabajos, sin_actualizar)
    _send(TEST_EMAIL, "Pablo", "✅ ¿Todo al día antes del fin de semana? — Bitácora", html)

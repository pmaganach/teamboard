# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
sys.stdout.reconfigure(encoding='utf-8')
from datetime import date, timedelta
from reminders import _html_reporte_gerente, _analista_seccion, _trabajo_card, _send, TEST_EMAIL

hoy = date.today()

class M:
    def __init__(self, nombre, area, estado, progreso, prioridad, fecha_sla=None):
        self.nombre = nombre; self.area_cliente = area
        self.estado = type('E', (), {'__str__': lambda s: estado})()
        self.progreso = progreso
        self.prioridad = type('P', (), {'__str__': lambda s: prioridad})()
        self.fecha_sla = fecha_sla

def hl_lunes(t, hoy=hoy):
    u = t.fecha_sla and (t.fecha_sla - hoy).days <= 7
    w = t.fecha_sla and 7 < (t.fecha_sla - hoy).days <= 14
    return _trabajo_card(t, urgente=u, warn=w)

analistas = [
    ("Pablo Magaña", [
        M("Análisis churn Q2",      "Customer Care",         "en_gestion",   40, "alta",  hoy+timedelta(days=2)),
        M("Modelo propensión",      "Customer Intelligence", "por_comenzar",  0, "alta"),
        M("Reporte NPS Mayo",       "Performance",           "en_revision",  65, "media", hoy+timedelta(days=10)),
    ]),
    ("Álvaro Román", [
        M("Dashboard Cobranza",     "Field Service",         "en_gestion",   50, "media"),
        M("Análisis rotación RRHH", "Excelencia Operacional","en_revision",  75, "baja"),
    ]),
    ("Karla Hidalgo", [
        M("Segmentación clientes",  "Estrategia Comercial",  "en_gestion",   30, "alta",  hoy+timedelta(days=4)),
        M("Control KPI junio",      "Performance",           "por_comenzar",  0, "media"),
    ]),
    ("Miguel Bravo", [
        M("Informe Chuquicamata",   "Monitoring",            "en_gestion",   60, "media"),
    ]),
]

analistas_data = []
for nombre, trabajos in analistas:
    riesgo = [t for t in trabajos if t.fecha_sla and (t.fecha_sla - hoy).days <= 7]
    analistas_data.append({
        'total': len(trabajos),
        'riesgo': len(riesgo),
        'html': _analista_seccion(nombre, trabajos, hoy, hl_lunes)
    })

total = sum(d['total'] for d in analistas_data)
riesgo = sum(d['riesgo'] for d in analistas_data)
intro = f"Aqu&iacute; tienes el estado del equipo para arrancar la semana. {total} trabajos activos en total, {riesgo} con SLA en riesgo esta semana."

html = _html_reporte_gerente(
    "Reporte semanal del equipo",
    f"Semana del {hoy.strftime('%d de %B, %Y')}",
    "#ED002F", "📊", intro, analistas_data
)
_send(TEST_EMAIL, "Aníbal", f"📊 Reporte semanal del equipo · {hoy.strftime('%d/%m')} — Bitácora", html)
print("Enviado a", TEST_EMAIL)

# TeamBoard — Design Spec
**Fecha:** 2026-05-22
**Proyecto:** TeamBoard · Verisure Análisis
**Estado:** Aprobado

---

## Contexto

El equipo de Análisis de Verisure (7 analistas + 1 gerente) necesita visibilidad en tiempo real sobre los trabajos que está gestionando cada integrante. Actualmente no existe un sistema centralizado para esto.

---

## Objetivo

Una app web interna que muestre en qué está trabajando cada analista, en qué estado va cada trabajo, y que permita también registrar trabajos a nivel de área (sin asignar a persona específica).

---

## Usuarios

| Rol | Acceso |
|---|---|
| Analista (7) | Ver y editar sus propios trabajos |
| Gerente (1) | Vista de solo lectura de todo el equipo |

---

## Stack tecnológico

- **Frontend:** Vue.js
- **Backend:** FastAPI (Python)
- **Base de datos:** SQLite (local) → escalable a PostgreSQL
- **Infraestructura:** Servidor local Verisure (mismo esquema que app Llamadas Técnicas)

---

## Vistas

### 1. Dashboard
- **Fila de KPIs:** Trabajos activos · Por comenzar · En gestión · En revisión · Pendientes · Completadas
  - Definición de "Trabajos activos": pendiente de confirmar (¿total sin completadas? ¿solo gestión+revisión?)
- **Sección Analistas:** Grid de cards, una por persona
  - Cada card muestra: avatar, nombre, estado de conexión, chips de trabajos activos con color de estado
- **Sección Trabajos por Área:** Cards de área sin asignar a persona
  - Cada área puede tener sus propios trabajos activos
- **Desglose completo:** Tabla con todos los trabajos, progreso, SLA y estado

### 2. Agenda
- Vista semanal (lun–dom)
- Una fila por analista + filas de áreas
- Bloques de color por trabajo, con indicadores de alerta

### 3. Kanban
- Columnas: Por comenzar / En gestión / En revisión / Pendientes / Completadas
- Agrupación configurable: por estado, por analista, por área
- Cards con título, área, responsable, prioridad, progreso y SLA

---

## Modelo de datos

### Trabajo
| Campo | Tipo | Descripción |
|---|---|---|
| id | int | Identificador |
| nombre | string | Nombre del trabajo |
| area_cliente | string | Área Verisure que lo solicita |
| responsable_id | int? | Analista asignado (null = tarea de área) |
| area_equipo | string? | Área del equipo si no hay responsable |
| estado | enum | por_comenzar / en_gestion / en_revision / pendiente / completado |
| progreso | int | 0–100 |
| fecha_inicio | date | |
| fecha_sla | date | Estimado por el analista |
| prioridad | enum | alta / media / baja |

### Usuario
| Campo | Tipo |
|---|---|
| id | int |
| nombre | string |
| iniciales | string |
| rol | analista / gerente |
| color | string (hex) |

---

## Estados de un trabajo

```
Por comenzar → En gestión → En revisión → Completado
                              ↓
                          Pendiente (bloqueado)
```

---

## Temas visuales

7 temas seleccionables por el usuario (se guarda en localStorage):
- Oscuro (default)
- Claro
- Bosque (verde)
- Océano (azul)
- Rosa
- Rubí (rojo)
- Índigo (morado)

Colores corporativos Verisure siempre presentes: `#ED002F` (rojo), `#00A37D` (teal).

---

## Pendientes de definir

- [ ] Definición exacta de "Trabajos activos" en los KPIs
- [ ] ¿Autenticación? (login simple o acceso directo)
- [ ] ¿Notificaciones cuando un trabajo cambia de estado?
- [ ] ¿Historial de cambios por trabajo?

---

## Mockup de referencia

`C:\Users\pablo.magana\Downloads\team-visibility-verisure.html`

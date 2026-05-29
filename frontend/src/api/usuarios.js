import client from './client'

export const getUsuarios    = () => client.get('/usuarios/').then(r =>
  r.data.sort((a, b) => {
    if (a.rol === 'gerente') return -1
    if (b.rol === 'gerente') return 1
    return a.nombre.localeCompare(b.nombre, 'es')
  })
)

export const getNotas       = (uid)              => client.get(`/usuarios/${uid}/notas`)
export const agregarNota    = (uid, texto, orid) => client.post(`/usuarios/${uid}/notas`, { texto, usuario_origen_id: orid })
export const marcarLeidas   = (uid)              => client.patch(`/usuarios/${uid}/notas/leer`)
export const eliminarNota   = (uid, nid)         => client.delete(`/usuarios/${uid}/notas/${nid}`)

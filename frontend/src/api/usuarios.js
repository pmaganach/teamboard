import client from './client'

export const getUsuarios = () => client.get('/usuarios/').then(r =>
  r.data.sort((a, b) => a.nombre.localeCompare(b.nombre, 'es'))
)

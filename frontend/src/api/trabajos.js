import client from './client'

export const getTrabaj     = (filtros = {}) => client.get('/trabajos/', { params: filtros }).then(r => r.data)
export const createTrabaj  = (datos)        => client.post('/trabajos/', datos).then(r => r.data)
export const updateTrabaj  = (id, datos)    => client.put(`/trabajos/${id}`, datos).then(r => r.data)
export const cambiarEstado = (id, estado)   => client.patch(`/trabajos/${id}/estado`, { estado }).then(r => r.data)
export const deleteTrabaj  = (id)           => client.delete(`/trabajos/${id}`)

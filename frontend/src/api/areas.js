import client from './client'

export const getAreas   = ()      => client.get('/areas/').then(r => r.data)
export const createArea = (datos) => client.post('/areas/', datos).then(r => r.data)

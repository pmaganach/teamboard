import client from './client'

export const getUsuarios = () => client.get('/usuarios/').then(r =>
  r.data.sort((a, b) => {
    if (a.rol === 'gerente') return -1
    if (b.rol === 'gerente') return 1
    return a.nombre.localeCompare(b.nombre, 'es')
  })
)

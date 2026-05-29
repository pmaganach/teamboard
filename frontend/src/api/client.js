import axios from 'axios'

const client = axios.create({
  baseURL: 'https://cloudapp.vicbc.cl/teamboard-api',
  headers: { 'Content-Type': 'application/json' }
})

export default client

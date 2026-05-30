import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.DEV
    ? 'http://127.0.0.1:8000'
    : 'https://cloudapp.vicbc.cl/teamboard-api',
  headers: { 'Content-Type': 'application/json' }
})

export default client

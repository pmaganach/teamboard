import client from './client'

export const requestOtp = (email)        => client.post('/auth/request-otp', { email })
export const verifyOtp  = (email, code)  => client.post('/auth/verify-otp',  { email, code })

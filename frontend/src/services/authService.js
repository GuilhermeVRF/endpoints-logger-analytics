import { httpClient } from '../api/httpClient'

export function login({ username, password }) {
  const body = new URLSearchParams()
  body.append('username', username.trim())
  body.append('password', password)

  return httpClient('/login', {
    method: 'POST',
    auth: false,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body,
  })
}

export function register({ username, password }) {
  return httpClient('/register', {
    method: 'POST',
    auth: false,
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: username.trim(),
      password,
      role: 'analyst',
    }),
  })
}

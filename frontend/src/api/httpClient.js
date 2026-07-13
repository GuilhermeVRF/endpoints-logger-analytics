const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export class HttpError extends Error {
  constructor(message, status, data) {
    super(message)
    this.name = 'HttpError'
    this.status = status
    this.data = data
  }
}

async function parseResponse(response) {
  const contentType = response.headers.get('content-type') || ''

  if (contentType.includes('application/json')) {
    return response.json()
  }

  return response.text()
}

export async function httpClient(path, options = {}) {
  const { auth = true, headers = {}, ...requestOptions } = options
  const finalHeaders = new Headers(headers)

  if (auth) {
    const token = localStorage.getItem('access_token')
    if (token) {
      finalHeaders.set('Authorization', `Bearer ${token}`)
    }
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...requestOptions,
    headers: finalHeaders,
  })

  const data = await parseResponse(response)

  if (!response.ok) {
    const message =
      typeof data === 'object' && data !== null && 'detail' in data
        ? data.detail
        : 'Request failed.'

    throw new HttpError(message, response.status, data)
  }

  return data
}

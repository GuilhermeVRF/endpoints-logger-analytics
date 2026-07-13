import { httpClient } from '../api/httpClient'

export function getEndpoints() {
  return httpClient('/endpoints')
}

export function getLogs({
  page = 1,
  limit = 20,
  startDate,
  endDate,
  statusCode,
  endpoints = [],
}) {
  const params = new URLSearchParams()
  params.set('page', String(page))
  params.set('limit', String(limit))

  if (startDate) {
    params.set('start_date', new Date(startDate).toISOString())
  }

  if (endDate) {
    const inclusiveEndDate = new Date(`${endDate}T23:59:59`)
    params.set('end_date', inclusiveEndDate.toISOString())
  }

  if (statusCode) {
    params.set('status_code', String(statusCode))
  }

  endpoints.forEach((endpoint) => {
    params.append('endpoints', endpoint)
  })

  return httpClient(`/logs?${params.toString()}`)
}

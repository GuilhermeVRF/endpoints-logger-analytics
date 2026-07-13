import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import * as authService from '../services/authService'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || '')
  const username = ref(localStorage.getItem('authenticated_user') || '')

  const isAuthenticated = computed(() => Boolean(token.value))

  function persistSession(nextToken, nextUsername) {
    token.value = nextToken
    username.value = nextUsername

    localStorage.setItem('access_token', nextToken)
    localStorage.setItem('authenticated_user', nextUsername)
  }

  function clearSession() {
    token.value = ''
    username.value = ''
    localStorage.removeItem('access_token')
    localStorage.removeItem('authenticated_user')
  }

  async function login(credentials) {
    const data = await authService.login(credentials)
    persistSession(data.access_token, credentials.username.trim())
    return data
  }

  async function register(payload) {
    return authService.register(payload)
  }

  return {
    token,
    username,
    isAuthenticated,
    login,
    register,
    clearSession,
  }
})

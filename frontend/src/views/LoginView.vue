<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { HttpError } from '../api/httpClient'
import LoginForm from '../components/auth/LoginForm.vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const isSubmitting = ref(false)
const errorMessage = ref('')

async function handleLogin(payload) {
  errorMessage.value = ''

  if (!payload.username.trim() || !payload.password) {
    errorMessage.value = 'Preencha usuario e senha.'
    return
  }

  isSubmitting.value = true

  try {
    await authStore.login(payload)
    router.push({ name: 'dashboard' })
  } catch (error) {
    if (error instanceof HttpError && error.status === 401) {
      errorMessage.value = 'Credenciais invalidas.'
    } else {
      errorMessage.value = 'Nao foi possivel conectar a API.'
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <main class="min-h-screen bg-white px-4 py-8 sm:px-6 lg:px-8">
    <div class="mx-auto flex min-h-[calc(100vh-4rem)] max-w-md items-center justify-center">
      <LoginForm
        :loading="isSubmitting"
        :error-message="errorMessage"
        @submit="handleLogin"
        @switch-register="$router.push({ name: 'register' })"
      />
    </div>
  </main>
</template>

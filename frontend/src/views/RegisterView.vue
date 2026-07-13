<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { HttpError } from '../api/httpClient'
import RegisterForm from '../components/auth/RegisterForm.vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const isSubmitting = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

async function handleRegister(payload) {
  errorMessage.value = ''
  successMessage.value = ''

  if (!payload.username.trim() || !payload.password || !payload.confirmPassword) {
    errorMessage.value = 'Preencha todos os campos.'
    return
  }

  if (payload.password !== payload.confirmPassword) {
    errorMessage.value = 'As senhas nao coincidem.'
    return
  }

  isSubmitting.value = true

  try {
    await authStore.register(payload)
    successMessage.value = 'Conta criada com sucesso. Redirecionando para login...'
    window.setTimeout(() => {
      router.push({ name: 'login' })
    }, 900)
  } catch (error) {
    if (error instanceof HttpError) {
      errorMessage.value = error.message || 'Nao foi possivel concluir o registro.'
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
      <RegisterForm
        :loading="isSubmitting"
        :error-message="errorMessage"
        :success-message="successMessage"
        @submit="handleRegister"
        @switch-login="$router.push({ name: 'login' })"
      />
    </div>
  </main>
</template>

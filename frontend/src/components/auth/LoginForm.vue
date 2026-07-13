<script setup>
import { ref } from 'vue'
import { Eye, EyeOff, LockKeyhole, UserRound } from 'lucide-vue-next'

defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
  errorMessage: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['submit', 'switch-register'])

const username = ref('')
const password = ref('')
const showPassword = ref(false)

function handleSubmit() {
  emit('submit', {
    username: username.value,
    password: password.value,
  })
}
</script>

<template>
  <div class="mx-auto w-full max-w-md rounded-3xl border border-gray-200 bg-white p-8 shadow-sm">
    <div class="mb-8 space-y-2 text-center">
      <p class="text-xs font-medium uppercase tracking-[0.24em] text-gray-400">Acesso</p>
      <h1 class="text-3xl font-semibold text-[#5469bf]">Analise de Logs de Acessos</h1>
      <p class="text-sm text-gray-500">Entre com suas credenciais.</p>
    </div>

    <form class="space-y-4" @submit.prevent="handleSubmit">
      <label class="block space-y-2">
        <span class="text-sm font-medium text-gray-700">Usuario</span>
        <div class="relative">
          <UserRound class="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
          <input
            v-model="username"
            type="text"
            placeholder="Nome"
            class="w-full rounded-2xl border border-gray-200 bg-white py-3 pl-12 pr-4 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-[#aebaf0] focus:ring-1 focus:ring-[#d7ddf8]"
          />
        </div>
      </label>

      <label class="block space-y-2">
        <span class="text-sm font-medium text-gray-700">Senha</span>
        <div class="relative">
          <LockKeyhole class="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
          <input
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Digite sua senha"
            class="w-full rounded-2xl border border-gray-200 bg-white py-3 pl-12 pr-14 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-[#aebaf0] focus:ring-1 focus:ring-[#d7ddf8]"
          />
          <button
            type="button"
            class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 transition hover:text-[#5469bf]"
            @click="showPassword = !showPassword"
          >
            <EyeOff v-if="showPassword" class="h-5 w-5" />
            <Eye v-else class="h-5 w-5" />
          </button>
        </div>
      </label>

      <button
        type="submit"
        class="w-full rounded-2xl border border-[#5469bf] bg-[#5469bf] px-5 py-3 text-sm font-medium text-white transition hover:bg-[#4b5fb1] disabled:cursor-not-allowed disabled:opacity-70"
        :disabled="loading"
      >
        {{ loading ? 'Entrando...' : 'Entrar' }}
      </button>

      <p v-if="errorMessage" class="text-center text-sm text-gray-500">
        {{ errorMessage }}
      </p>
    </form>

    <p class="mt-6 text-center text-sm text-gray-500">
      Nao tem conta?
      <button
        type="button"
        class="font-medium text-[#5469bf] transition hover:text-[#4355a5]"
        @click="emit('switch-register')"
      >
        Criar uma conta
      </button>
    </p>
  </div>
</template>

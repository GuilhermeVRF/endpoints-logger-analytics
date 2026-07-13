<script setup>
defineProps({
  username: {
    type: String,
    default: '',
  },
})

defineEmits(['logout', 'open-upload'])
</script>

<template>
  <header class="relative left-1/2 right-1/2 w-screen -translate-x-1/2 bg-[#5469bf] px-4 py-8 sm:px-6 lg:px-8">
    <div class="mx-auto flex w-full max-w-7xl flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
      <div class="space-y-2">
        <p class="text-xs font-medium uppercase tracking-[0.24em] text-white/65">Dashboard</p>
        <h1 class="text-3xl font-semibold text-white">Analise de Logs de Acessos</h1>
        <p class="text-sm text-white/80">
          Visualizacao dos eventos coletados{{ username ? ` para ${username}` : '' }}.
        </p>
      </div>

      <div class="flex flex-col gap-3 sm:flex-row">
        <button
          type="button"
          class="rounded-2xl border border-white/30 bg-white px-4 py-2 text-sm font-medium text-[#5469bf] transition hover:bg-[#eef1ff]"
          @click="$emit('open-upload')"
        >
          Ingerir Novos Logs
        </button>

        <button
          type="button"
          class="rounded-2xl border border-white/30 bg-white px-4 py-2 text-sm text-[#5469bf] transition hover:bg-[#eef1ff]"
          @click="$emit('logout')"
        >
          Sair
        </button>
      </div>
    </div>
  </header>
</template>

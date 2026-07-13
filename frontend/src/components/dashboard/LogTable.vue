<script setup>
defineProps({
  logs: {
    type: Array,
    default: () => [],
  },
  logsError: {
    type: String,
    default: '',
  },
  isLoadingLogs: {
    type: Boolean,
    default: false,
  },
  currentPage: {
    type: Number,
    required: true,
  },
  hasNextPage: {
    type: Boolean,
    default: false,
  },
  formatTimestamp: {
    type: Function,
    required: true,
  },
})

defineEmits(['previous-page', 'next-page'])
</script>

<template>
  <section class="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
    <div class="mb-5">
      <h2 class="text-sm font-semibold text-gray-900">Logs</h2>
    </div>

    <p v-if="logsError" class="mb-4 text-sm text-gray-500">{{ logsError }}</p>

    <div class="overflow-x-auto">
      <table class="min-w-full border-separate border-spacing-0 text-left text-sm">
        <thead>
          <tr class="text-gray-500">
            <th class="border-b border-gray-200 px-4 py-3 font-medium">Data</th>
            <th class="border-b border-gray-200 px-4 py-3 font-medium">IP</th>
            <th class="border-b border-gray-200 px-4 py-3 font-medium">URL</th>
            <th class="border-b border-gray-200 px-4 py-3 font-medium">Status</th>
            <th class="border-b border-gray-200 px-4 py-3 font-medium">User Agent</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!isLoadingLogs && !logs.length">
            <td colspan="5" class="px-4 py-10 text-center text-sm text-gray-500">
              Nenhum log encontrado para os filtros selecionados.
            </td>
          </tr>

          <tr v-for="log in logs" :key="log.id" class="text-gray-700">
            <td class="border-b border-gray-100 px-4 py-4">{{ formatTimestamp(log.timestamp) }}</td>
            <td class="border-b border-gray-100 px-4 py-4">{{ log.ip_address }}</td>
            <td class="border-b border-gray-100 px-4 py-4">{{ log.endpoint }}</td>
            <td class="border-b border-gray-100 px-4 py-4">{{ log.status_code }}</td>
            <td class="border-b border-gray-100 px-4 py-4 text-gray-500">
              {{ log.user_agent || 'Nao informado' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="mt-6 flex items-center justify-between gap-4 border-t border-gray-200 pt-5">
      <button
        type="button"
        class="rounded-2xl border border-[#cfd6f6] bg-white px-4 py-2 text-sm text-[#5469bf] transition hover:border-[#aebaf0] hover:bg-[#eef1ff] disabled:cursor-not-allowed disabled:opacity-50"
        :disabled="currentPage === 1 || isLoadingLogs"
        @click="$emit('previous-page')"
      >
        Pagina Anterior
      </button>

      <span class="text-sm text-gray-500">Pagina {{ currentPage }}</span>

      <button
        type="button"
        class="rounded-2xl border border-[#cfd6f6] bg-white px-4 py-2 text-sm text-[#5469bf] transition hover:border-[#aebaf0] hover:bg-[#eef1ff] disabled:cursor-not-allowed disabled:opacity-50"
        :disabled="!hasNextPage || isLoadingLogs"
        @click="$emit('next-page')"
      >
        Proxima Pagina
      </button>
    </div>
  </section>
</template>

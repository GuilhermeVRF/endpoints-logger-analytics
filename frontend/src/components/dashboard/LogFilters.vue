<script setup>
import EndpointMultiSelect from '../EndpointMultiSelect.vue'

defineProps({
  startDate: {
    type: String,
    default: '',
  },
  endDate: {
    type: String,
    default: '',
  },
  statusCode: {
    type: [String, Number],
    default: '',
  },
  selectedEndpoints: {
    type: Array,
    default: () => [],
  },
  availableEndpoints: {
    type: Array,
    default: () => [],
  },
  isLoadingEndpoints: {
    type: Boolean,
    default: false,
  },
  endpointsError: {
    type: String,
    default: '',
  },
  isLoadingLogs: {
    type: Boolean,
    default: false,
  },
  hasActiveFilters: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits([
  'update:startDate',
  'update:endDate',
  'update:statusCode',
  'update:selectedEndpoints',
  'apply',
  'clear',
])
</script>

<template>
  <section class="space-y-4">
    <div class="flex items-center justify-between gap-4">
      <p v-if="hasActiveFilters" class="text-xs text-gray-400">Filtros ativos</p>
    </div>

    <div class="flex flex-col gap-3 xl:flex-row xl:flex-nowrap xl:items-end">
      <label class="min-w-[10rem] flex-1 space-y-2">
        <span class="text-sm font-medium text-gray-700">Data inicial</span>
        <input
          :value="startDate"
          type="date"
          class="w-full rounded-2xl border border-gray-200 bg-white px-4 py-3 text-sm text-gray-900 outline-none transition focus:border-gray-300 focus:ring-1 focus:ring-gray-300"
          @input="emit('update:startDate', $event.target.value)"
        />
      </label>

      <label class="min-w-[10rem] flex-1 space-y-2">
        <span class="text-sm font-medium text-gray-700">Data final</span>
        <input
          :value="endDate"
          type="date"
          class="w-full rounded-2xl border border-gray-200 bg-white px-4 py-3 text-sm text-gray-900 outline-none transition focus:border-gray-300 focus:ring-1 focus:ring-gray-300"
          @input="emit('update:endDate', $event.target.value)"
        />
      </label>

      <label class="min-w-[9rem] space-y-2 xl:w-40 xl:min-w-[9rem]">
        <span class="text-sm font-medium text-gray-700">Status code</span>
        <input
          :value="statusCode"
          type="number"
          min="100"
          max="599"
          placeholder="Ex: 200"
          class="w-full rounded-2xl border border-gray-200 bg-white px-4 py-3 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-gray-300 focus:ring-1 focus:ring-gray-300"
          @input="emit('update:statusCode', $event.target.value)"
        />
      </label>

      <div class="min-w-[16rem] xl:w-72">
        <p class="mb-2 text-sm font-medium text-gray-700">Endpoints</p>
        <EndpointMultiSelect
          :model-value="selectedEndpoints"
          :options="availableEndpoints"
          :loading="isLoadingEndpoints"
          :error="endpointsError"
          @update:model-value="emit('update:selectedEndpoints', $event)"
        />
      </div>

      <button
        type="button"
        class="rounded-2xl border border-[#5469bf] bg-[#5469bf] px-5 py-3 text-sm font-medium text-white transition hover:bg-[#4b5fb1] disabled:cursor-not-allowed disabled:opacity-70 xl:w-auto"
        :disabled="isLoadingLogs"
        @click="emit('apply')"
      >
        {{ isLoadingLogs ? 'Carregando...' : 'Aplicar Filtros' }}
      </button>
      <button
        type="button"
        class="rounded-2xl border border-[#cfd6f6] bg-white px-5 py-3 text-sm font-medium text-[#5469bf] transition hover:border-[#aebaf0] hover:bg-[#eef1ff] xl:w-auto"
        @click="emit('clear')"
      >
        Limpar
      </button>
    </div>
  </section>
</template>

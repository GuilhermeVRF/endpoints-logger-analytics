<script setup>
import { computed, ref } from 'vue'
import { Check, ChevronDown } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => [],
  },
  options: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)

const summaryLabel = computed(() => {
  if (props.loading) {
    return 'Carregando endpoints...'
  }

  if (!props.modelValue.length) {
    return 'Selecionar Endpoints'
  }

  if (props.modelValue.length === 1) {
    return props.modelValue[0]
  }

  return `${props.modelValue.length} Endpoints selecionados`
})

function toggleOption(option) {
  const values = [...props.modelValue]
  const index = values.indexOf(option)

  if (index >= 0) {
    values.splice(index, 1)
  } else {
    values.push(option)
  }

  emit('update:modelValue', values)
}

function clearSelection() {
  emit('update:modelValue', [])
}
</script>

<template>
  <div class="relative min-w-[16rem]">
    <button
      type="button"
      class="flex w-full items-center justify-between rounded-2xl border border-[#cfd6f6] bg-white px-4 py-3 text-left text-sm text-gray-700 outline-none transition hover:border-[#aebaf0] focus:border-[#aebaf0] focus:ring-1 focus:ring-[#d7ddf8]"
      @click="isOpen = !isOpen"
    >
      <span class="truncate">{{ summaryLabel }}</span>
      <ChevronDown class="h-4 w-4 text-[#7c8fd8]" />
    </button>

    <div
      v-if="isOpen"
      class="absolute left-0 right-0 z-10 mt-2 rounded-2xl border border-[#d7ddf8] bg-white p-3 shadow-sm"
    >
      <div class="mb-3 flex items-center justify-between gap-3">
        <span class="text-xs uppercase tracking-[0.2em] text-[#7c8fd8]">Endpoints</span>
        <button
          v-if="modelValue.length"
          type="button"
          class="text-xs text-[#5469bf] transition hover:text-[#4355a5]"
          @click="clearSelection"
        >
          Limpar
        </button>
      </div>

      <p v-if="error" class="text-sm text-gray-500">{{ error }}</p>

      <p v-else-if="!options.length && !loading" class="text-sm text-gray-500">
        Nenhum endpoint disponivel.
      </p>

      <div v-else class="max-h-60 space-y-1 overflow-y-auto">
        <button
          v-for="option in options"
          :key="option"
          type="button"
          class="flex w-full items-center justify-between rounded-xl px-3 py-2 text-sm text-gray-600 transition hover:bg-[#eef1ff]"
          @click="toggleOption(option)"
        >
          <span class="truncate">{{ option }}</span>
          <Check v-if="modelValue.includes(option)" class="h-4 w-4 text-[#5469bf]" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { FileUp, UploadCloud, X } from 'lucide-vue-next'

import { HttpError } from '../api/httpClient'
import * as logService from '../services/logService'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:isOpen', 'upload-success'])

const fileInput = ref(null)
const selectedFile = ref(null)
const isDragging = ref(false)
const isSubmitting = ref(false)
const errorMessage = ref('')

const selectedFileName = computed(() => selectedFile.value?.name || '')

function closeModal() {
  emit('update:isOpen', false)
  selectedFile.value = null
  errorMessage.value = ''
  isDragging.value = false
}

function openFilePicker() {
  fileInput.value?.click()
}

function setSelectedFile(file) {
  if (!file) {
    return
  }

  if (!file.name.toLowerCase().endsWith('.csv')) {
    errorMessage.value = 'Selecione um arquivo .csv valido.'
    selectedFile.value = null
    return
  }

  errorMessage.value = ''
  selectedFile.value = file
}

function handleFileChange(event) {
  const [file] = event.target.files || []
  setSelectedFile(file)
}

function handleDrop(event) {
  isDragging.value = false
  const [file] = event.dataTransfer?.files || []
  setSelectedFile(file)
}

async function handleUpload() {
  errorMessage.value = ''

  if (!selectedFile.value) {
    errorMessage.value = 'Selecione um arquivo antes de enviar.'
    return
  }

  isSubmitting.value = true

  try {
    const response = await logService.upload(selectedFile.value)
    emit('upload-success', response)
    closeModal()
  } catch (error) {
    if (error instanceof HttpError) {
      errorMessage.value = error.message || 'Nao foi possivel processar o arquivo.'
    } else {
      errorMessage.value = 'Nao foi possivel processar o arquivo.'
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="isOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/35 px-4 py-8 backdrop-blur-sm"
      @click.self="closeModal"
    >
      <div class="w-full max-w-3xl rounded-3xl bg-white shadow-2xl shadow-slate-900/10">
        <div class="flex items-start justify-between gap-4 border-b border-gray-100 px-6 py-5 sm:px-8">
          <div>
            <p class="text-xs font-medium uppercase tracking-[0.24em] text-gray-400">Ingestao</p>
            <h2 class="mt-2 text-2xl font-semibold text-[#5469bf]">Ingerir Novos Logs</h2>
          </div>

          <button
            type="button"
            class="rounded-2xl border border-gray-200 p-2 text-gray-500 transition hover:border-gray-300 hover:text-gray-700"
            @click="closeModal"
          >
            <X class="h-5 w-5" />
          </button>
        </div>

        <div class="space-y-8 px-6 py-6 sm:px-8 sm:py-8">
          <section class="space-y-4">
            <div class="space-y-2">
              <h3 class="text-sm font-semibold text-gray-900">Formato esperado</h3>
              <p class="text-sm leading-6 text-gray-500">
                O sistema aceita apenas arquivos <code class="rounded bg-gray-100 px-1.5 py-0.5 text-xs">.csv</code>.
                Use o formato abaixo para garantir a importacao correta.
              </p>
            </div>

            <div class="overflow-x-auto rounded-2xl border border-gray-200">
              <table class="min-w-full text-left text-sm">
                <thead class="bg-gray-50 text-gray-500">
                  <tr>
                    <th class="border-b border-gray-200 px-4 py-3 font-medium">timestamp</th>
                    <th class="border-b border-gray-200 px-4 py-3 font-medium">ip_address</th>
                    <th class="border-b border-gray-200 px-4 py-3 font-medium">method</th>
                    <th class="border-b border-gray-200 px-4 py-3 font-medium">path</th>
                    <th class="border-b border-gray-200 px-4 py-3 font-medium">status_code</th>
                    <th class="border-b border-gray-200 px-4 py-3 font-medium">user_agent</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="text-gray-700">
                    <td class="px-4 py-4">2026-07-13T10:15:00Z</td>
                    <td class="px-4 py-4">192.168.0.10</td>
                    <td class="px-4 py-4">GET</td>
                    <td class="px-4 py-4">/api/logs</td>
                    <td class="px-4 py-4">200</td>
                    <td class="px-4 py-4">Mozilla/5.0</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <section class="space-y-4">
            <div
              class="rounded-3xl border-2 border-dashed px-6 py-10 text-center transition"
              :class="
                isDragging
                  ? 'border-[#5469bf] bg-[#eef1ff]'
                  : 'border-gray-200 bg-white hover:bg-gray-50'
              "
              @dragenter.prevent="isDragging = true"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleDrop"
            >
              <div class="mx-auto flex max-w-md flex-col items-center space-y-4">
                <div class="rounded-full bg-[#eef1ff] p-4 text-[#5469bf]">
                  <UploadCloud class="h-7 w-7" />
                </div>

                <div class="space-y-2">
                  <p class="text-base font-medium text-gray-900">Arraste um arquivo CSV aqui</p>
                  <p class="text-sm text-gray-500">
                    ou use o seletor abaixo para escolher um arquivo manualmente.
                  </p>
                </div>

                <input
                  ref="fileInput"
                  type="file"
                  accept=".csv"
                  class="hidden"
                  @change="handleFileChange"
                />

                <button
                  type="button"
                  class="inline-flex items-center gap-2 rounded-2xl border border-[#5469bf] bg-[#5469bf] px-5 py-3 text-sm font-medium text-white transition hover:bg-[#4b5fb1]"
                  @click="openFilePicker"
                >
                  <FileUp class="h-4 w-4" />
                  Selecionar Arquivo
                </button>

                <p v-if="selectedFileName" class="text-sm text-gray-600">
                  Arquivo selecionado: <span class="font-medium text-gray-900">{{ selectedFileName }}</span>
                </p>
              </div>
            </div>

            <p v-if="errorMessage" class="rounded-2xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-600">
              {{ errorMessage }}
            </p>

            <div class="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
              <button
                type="button"
                class="rounded-2xl border border-gray-200 bg-white px-5 py-3 text-sm font-medium text-gray-600 transition hover:border-gray-300 hover:text-gray-900"
                @click="closeModal"
              >
                Cancelar
              </button>
              <button
                type="button"
                class="rounded-2xl border border-[#5469bf] bg-[#5469bf] px-5 py-3 text-sm font-medium text-white transition hover:bg-[#4b5fb1] disabled:cursor-not-allowed disabled:opacity-70"
                :disabled="isSubmitting"
                @click="handleUpload"
              >
                {{ isSubmitting ? 'Processando...' : 'Confirmar Upload' }}
              </button>
            </div>
          </section>
        </div>
      </div>
    </div>
  </Teleport>
</template>

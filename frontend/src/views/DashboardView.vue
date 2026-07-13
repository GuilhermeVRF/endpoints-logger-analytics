<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { HttpError } from '../api/httpClient'
import DashboardHeader from '../components/dashboard/DashboardHeader.vue'
import LogFilters from '../components/dashboard/LogFilters.vue'
import LogTable from '../components/dashboard/LogTable.vue'
import * as logService from '../services/logService'
import { useAuthStore } from '../stores/auth'

const PAGE_LIMIT = 20

const authStore = useAuthStore()
const router = useRouter()

const logs = ref([])
const availableEndpoints = ref([])
const startDate = ref('')
const endDate = ref('')
const statusCode = ref('')
const selectedEndpoints = ref([])
const currentPage = ref(1)
const isLoadingEndpoints = ref(false)
const isLoadingLogs = ref(false)
const endpointsError = ref('')
const logsError = ref('')

const hasNextPage = computed(() => logs.value.length === PAGE_LIMIT)
const hasActiveFilters = computed(
  () =>
    Boolean(startDate.value) ||
    Boolean(endDate.value) ||
    Boolean(statusCode.value) ||
    selectedEndpoints.value.length > 0,
)

function handleUnauthorized() {
  authStore.clearSession()
  router.push({ name: 'login' })
}

async function fetchEndpoints() {
  isLoadingEndpoints.value = true
  endpointsError.value = ''

  try {
    availableEndpoints.value = await logService.getEndpoints()
  } catch (error) {
    if (error instanceof HttpError && error.status === 401) {
      handleUnauthorized()
      return
    }

    endpointsError.value = 'Nao foi possivel carregar os endpoints.'
  } finally {
    isLoadingEndpoints.value = false
  }
}

async function fetchLogs() {
  isLoadingLogs.value = true
  logsError.value = ''

  try {
    logs.value = await logService.getLogs({
      page: currentPage.value,
      limit: PAGE_LIMIT,
      startDate: startDate.value,
      endDate: endDate.value,
      statusCode: statusCode.value,
      endpoints: selectedEndpoints.value,
    })
  } catch (error) {
    if (error instanceof HttpError && error.status === 401) {
      handleUnauthorized()
      return
    }

    logs.value = []
    logsError.value = 'Nao foi possivel carregar os logs.'
  } finally {
    isLoadingLogs.value = false
  }
}

function applyFilters() {
  currentPage.value = 1
  fetchLogs()
}

function clearFilters() {
  startDate.value = ''
  endDate.value = ''
  statusCode.value = ''
  selectedEndpoints.value = []
  currentPage.value = 1
  fetchLogs()
}

function goToPreviousPage() {
  if (currentPage.value === 1 || isLoadingLogs.value) {
    return
  }

  currentPage.value -= 1
  fetchLogs()
}

function goToNextPage() {
  if (!hasNextPage.value || isLoadingLogs.value) {
    return
  }

  currentPage.value += 1
  fetchLogs()
}

function formatTimestamp(value) {
  return new Intl.DateTimeFormat('pt-BR', {
    dateStyle: 'short',
    timeStyle: 'medium',
  }).format(new Date(value))
}

function logout() {
  authStore.clearSession()
  router.push({ name: 'login' })
}

onMounted(async () => {
  await fetchEndpoints()
  await fetchLogs()
})
</script>

<template>
  <main class="min-h-screen bg-white">
    <section class="w-full space-y-8">
      <DashboardHeader :username="authStore.username" @logout="logout" />

      <div class="mx-auto w-full max-w-7xl space-y-6 px-4 pb-8 sm:px-6 lg:px-8">
        <LogFilters
          :start-date="startDate"
          :end-date="endDate"
          :status-code="statusCode"
          :selected-endpoints="selectedEndpoints"
          :available-endpoints="availableEndpoints"
          :is-loading-endpoints="isLoadingEndpoints"
          :endpoints-error="endpointsError"
          :is-loading-logs="isLoadingLogs"
          :has-active-filters="hasActiveFilters"
          @update:start-date="startDate = $event"
          @update:end-date="endDate = $event"
          @update:status-code="statusCode = $event"
          @update:selected-endpoints="selectedEndpoints = $event"
          @apply="applyFilters"
          @clear="clearFilters"
        />

        <LogTable
          :logs="logs"
          :logs-error="logsError"
          :is-loading-logs="isLoadingLogs"
          :current-page="currentPage"
          :has-next-page="hasNextPage"
          :format-timestamp="formatTimestamp"
          @previous-page="goToPreviousPage"
          @next-page="goToNextPage"
        />
      </div>
    </section>
  </main>
</template>

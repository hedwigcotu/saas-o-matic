<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useCustomerStore } from '@/stores/customer'
import { useExchangeRates } from '@/composables/useExchangeRates'
import { apiService } from '@/services/api'

const route = useRoute()
const store = useCustomerStore()
const { rates, convert, formatCurrency } = useExchangeRates()

const selectedCurrency = ref('EUR')
const activeUsers = ref(10)
const storageGb = ref(5)
const apiCalls = ref(1000)
const previewData = ref<any>(null)
const previewLoading = ref(false)

const fetchPreview = async () => {
  if (!store.currentCustomer) return
  previewLoading.value = true
  try {
    previewData.value = await apiService.previewSimulation({
      customer_id: store.currentCustomer.id,
      active_users: activeUsers.value,
      storage_gb: storageGb.value,
      api_calls: apiCalls.value
    })
  } catch (e) {
    console.error(e)
  } finally {
    previewLoading.value = false
  }
}

watch([activeUsers, storageGb, apiCalls], fetchPreview)

onMounted(async () => {
  await store.loadCustomerDetail(route.params.id as string)
  fetchPreview()
})

const saveSimulation = async () => {
  try {
    await apiService.saveSimulation({
      customer_id: store.currentCustomer.id,
      active_users: activeUsers.value,
      storage_gb: storageGb.value,
      api_calls: apiCalls.value
    })
    alert('Simulación guardada con éxito')
    store.loadCustomerDetail(route.params.id as string)
  } catch (e) {
    alert('Error al guardar')
  }
}
</script>

<template>
  <div v-if="store.currentCustomer" class="detail-view">
    <header class="header">
      <h1>{{ store.currentCustomer.company_name }}</h1>
      <select v-model="selectedCurrency">
        <option v-for="(rate, curr) in rates" :key="curr" :value="curr">{{ curr }}</option>
      </select>
    </header>

    <main class="content">
      <div class="info-panel">
        <p><strong>Email:</strong> {{ store.currentCustomer.email }}</p>
        <p><strong>Identificador:</strong> {{ store.currentCustomer.tax_id }} ({{ store.currentCustomer.tax_id_kind }})</p>
      </div>

      <div class="simulator-panel">
        <h2>Simulador Interactivo</h2>
        
        <div class="slider-group">
          <label>Usuarios Activos: {{ activeUsers }}</label>
          <input type="range" v-model.number="activeUsers" min="1" max="100" />
        </div>
        
        <div class="slider-group">
          <label>Almacenamiento (GB): {{ storageGb }}</label>
          <input type="range" v-model.number="storageGb" min="0" max="100" />
        </div>

        <div class="slider-group">
          <label>Llamadas API: {{ apiCalls }}</label>
          <input type="range" v-model.number="apiCalls" min="0" max="10000" step="100" />
        </div>

        <div v-if="previewData" class="cost-display">
          <p>Subtotal: {{ formatCurrency(convert(previewData.breakdown.subtotal, selectedCurrency), selectedCurrency) }}</p>
          <p>IVA: {{ formatCurrency(convert(previewData.breakdown.tax, selectedCurrency), selectedCurrency) }}</p>
          <h3>Total: {{ formatCurrency(convert(previewData.breakdown.total, selectedCurrency), selectedCurrency) }}</h3>
        </div>
        
        <button @click="saveSimulation" class="btn-save">Guardar Simulación</button>
      </div>

      <div class="history-panel">
        <h2>Historial de Simulaciones</h2>
        <div v-if="store.currentCustomer.simulations.length === 0" class="empty">
          No hay simulaciones guardadas.
        </div>
        <ul v-else class="history-list">
          <li v-for="sim in store.currentCustomer.simulations" :key="sim.id" class="history-item">
            <span>{{ new Date(sim.created_at).toLocaleDateString() }}</span>
            <span>{{ sim.active_users }} usuarios</span>
            <strong>{{ formatCurrency(convert(sim.breakdown.total, selectedCurrency), selectedCurrency) }}</strong>
          </li>
        </ul>
      </div>
    </main>
  </div>
</template>

<style scoped>
.detail-view { display: flex; flex-direction: column; height: 100vh; }
.header { display: flex; justify-content: space-between; padding: 1rem 2rem; background: #2c3e50; color: white; }
.content { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; padding: 2rem; flex: 1; }
.info-panel, .history-panel { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.simulator-panel { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.slider-group { margin-bottom: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; }
.cost-display { background: #e8f5e9; padding: 1rem; border-radius: 4px; margin-bottom: 1rem; }
.btn-save { width: 100%; padding: 1rem; background: #42b983; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 1rem; font-weight: bold; }
.history-list { list-style: none; padding: 0; }
.history-item { display: flex; justify-content: space-between; padding: 1rem; border-bottom: 1px solid #eee; }
</style>
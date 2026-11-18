<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCustomerStore } from '@/stores/customer'
import { useExchangeRates } from '@/composables/useExchangeRates'

const router = useRouter()
const store = useCustomerStore()
const { fetchRates } = useExchangeRates()
const searchQuery = ref('')

onMounted(() => {
  store.searchCustomers('')
  fetchRates()
})

const handleSearch = () => {
  store.searchCustomers(searchQuery.value)
}
</script>

<template>
  <div class="dashboard">
    <header class="header">
      <h1>SaaS-O-Matic Dashboard</h1>
      <div class="search-bar">
        <input 
          v-model="searchQuery" 
          @input="handleSearch" 
          type="text" 
          placeholder="Buscar por empresa o CIF..."
        />
      </div>
    </header>

    <main class="content">
      <div v-if="store.loading" class="loading">Cargando clientes...</div>
      <div v-else-if="store.error" class="error">{{ store.error }}</div>
      <div v-else-if="store.customers.length === 0" class="empty">
        No se encontraron clientes.
      </div>
      
      <div v-else class="grid">
        <div 
          v-for="customer in store.customers" 
          :key="customer.id" 
          class="card"
          @click="router.push(`/customer/${customer.id}`)"
        >
          <h2>{{ customer.company_name }}</h2>
          <p><strong>CIF:</strong> {{ customer.tax_id }}</p>
          <p><strong>Plan:</strong> {{ customer.plan }}</p>
          <p><strong>País:</strong> {{ customer.country }}</p>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; background: #2c3e50; color: white; }
.search-bar input { padding: 0.5rem; width: 300px; border-radius: 4px; border: none; }
.content { padding: 2rem; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }
.card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); cursor: pointer; transition: transform 0.2s; }
.card:hover { transform: translateY(-4px); }
.loading, .error, .empty { text-align: center; font-size: 1.2rem; margin-top: 2rem; color: #666; }
</style>
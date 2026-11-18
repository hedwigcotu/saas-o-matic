import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiService, type Customer } from '@/services/api'

export const useCustomerStore = defineStore('customer', () => {
  const customers = ref<Customer[]>([])
  const currentCustomer = ref<any>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const searchCustomers = async (query: string) => {
    loading.value = true
    error.value = null
    try {
      customers.value = await apiService.getCustomers(query)
    } catch (e: any) {
      error.value = e.response?.data?.error || 'Error al buscar clientes'
    } finally {
      loading.value = false
    }
  }

  const loadCustomerDetail = async (id: string) => {
    loading.value = true
    try {
      currentCustomer.value = await apiService.getCustomer(id)
    } catch (e: any) {
      error.value = e.response?.data?.error || 'Error al cargar el cliente'
    } finally {
      loading.value = false
    }
  }

  return { customers, currentCustomer, loading, error, searchCustomers, loadCustomerDetail }
})
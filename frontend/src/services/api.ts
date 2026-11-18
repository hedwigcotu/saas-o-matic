import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

export interface Customer {
  id: string
  company_name: string
  tax_id: string
  tax_id_kind: string
  email: string
  country: string
  plan: string
  created_at: string
}

export interface Breakdown {
  base_cost: string
  storage_cost: string
  api_cost: string
  subtotal: string
  tax_rate: string
  tax: string
  total: string
  currency: string
}

export interface Simulation {
  id: string
  customer_id: string
  active_users: number
  storage_gb: number
  api_calls: number
  breakdown: Breakdown
  rules_version: string
  created_at: string
}

export const apiService = {
  async createCustomer(data: any): Promise<Customer> {
    const res = await api.post('/customers', data)
    return res.data
  },
  async getCustomers(q: string = ''): Promise<Customer[]> {
    const res = await api.get('/customers', { params: { q } })
    return res.data
  },
  async getCustomer(id: string): Promise<any> {
    const res = await api.get(`/customers/${id}`)
    return res.data
  },
  async previewSimulation(data: any): Promise<any> {
    const res = await api.post('/simulations/preview', data)
    return res.data
  },
  async saveSimulation(data: any): Promise<Simulation> {
    const res = await api.post('/simulations', data)
    return res.data
  }
}
import { ref } from 'vue'

const CACHE_TTL = 1000 * 60 * 60 // 1 hora
let cache: { rates: Record<string, number>, fetchedAt: number } | null = null

export function useExchangeRates() {
  const rates = ref<Record<string, number>>({ EUR: 1 })
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchRates = async () => {
    if (cache && Date.now() - cache.fetchedAt < CACHE_TTL) {
      rates.value = cache.rates
      return
    }

    loading.value = true
    error.value = null
    
    try {
      const res = await fetch('https://open.er-api.com/v6/latest/EUR')
      const data = await res.json()
      rates.value = data.rates
      cache = { rates: data.rates, fetchedAt: Date.now() }
    } catch (e) {
      error.value = 'No se pudieron cargar las divisas.'
      try {
        const fallbackRes = await fetch('/api/fx/rates?base=EUR')
        if (fallbackRes.ok) {
          const fallbackData = await fallbackRes.json()
          rates.value = fallbackData.rates
        }
      } catch (fallbackErr) {
        console.error('Fallback también falló')
      }
    } finally {
      loading.value = false
    }
  }

  const convert = (amountEur: string | number, currency: string) => {
    const amount = typeof amountEur === 'string' ? parseFloat(amountEur) : amountEur
    const rate = rates.value[currency] || 1
    return amount * rate
  }

  const formatCurrency = (amount: number, currency: string) => {
    return new Intl.NumberFormat('es-ES', { style: 'currency', currency }).format(amount)
  }

  return { rates, loading, error, fetchRates, convert, formatCurrency }
}
# Spec: Construcción del breakdown completo

## Fórmula
base     = base_cost(active_users)
storage  = storage_cost(storage_gb)
api      = api_cost(api_calls)
subtotal = base + storage + api
tax_rate = TAX_RATES[country]           # UnsupportedCountryError si no está
tax      = round(subtotal * tax_rate, 2, ROUND_HALF_UP)
total    = round(subtotal + tax, 2, ROUND_HALF_UP)

## Regla de redondeo
- subtotal se calcula con precisión completa (sin redondear).
- Se redondea una sola vez al construir el breakdown final.
- base, storage, api se presentan redondeados a 2 decimales para visualización,
  pero el subtotal se calcula con los valores sin redondear.

## Caso de verificación completo (15 usuarios, 10 GB, 1000 llamadas, ES)
| Concepto   | Valor (sin redondear) | Presentado |
|------------|-----------------------|------------|
| base       | 140                   | 140.00     |
| storage    | 5.0                   | 5.00       |
| api        | 1.000                 | 1.00       |
| subtotal   | 146.0                 | 146.00     |
| tax_rate   | 0.21                  | "0.21"     |
| tax        | 30.66                 | 30.66      |
| total      | 176.66                | 176.66     |

## Contrato
```python
def build_breakdown(active_users: int, storage_gb: int, api_calls: int, country: str) -> Breakdown


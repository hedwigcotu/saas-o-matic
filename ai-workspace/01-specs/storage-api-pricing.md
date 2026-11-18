# Spec: Tarifas de almacenamiento y llamadas API

## Contexto
El enunciado del reto pide capturar `storage_gb` y `api_calls` como inputs
de la simulación pero NO define su precio. Para que el "optimizador de
facturación" sea coherente, se definen tarifas explícitas y documentadas.
Esta es una **decisión de diseño** registrada en `adr/006-storage-api-pricing.md`.

## Tarifas
| Concepto       | Tarifa            | Unidad       |
|----------------|-------------------|--------------|
| Almacenamiento | 0.50 € / GB / mes | `storage_gb` |
| Llamadas API   | 0.001 € / llamada | `api_calls`  |

## Reglas
- `storage_cost = storage_gb * Decimal("0.50")`
- `api_cost = api_calls * Decimal("0.001")`
- Ambos valores son `Decimal`; los inputs son enteros ≥ 0.
- Negativos → `NegativeInputError`.
- Se suman al `base_cost` para formar el `subtotal`.

## Casos límite
| storage_gb | api_calls | storage_cost | api_cost | subtotal_extra |
|------------|-----------|--------------|----------|----------------|
| 0          | 0         | 0.00         | 0.00     | 0.00 |
| 10         | 0         | 5.00         | 0.00     | 5.00 |
| 0          | 1000      | 0.00         | 1.00     | 1.00 |
| 100        | 50000     | 50.00        | 50.00    | 100.00 |

## Fórmula completa del subtotal
subtotal = base_cost(active_users) + storage_cost(storage_gb) + api_cost(api_calls)
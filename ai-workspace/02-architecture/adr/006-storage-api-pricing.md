# ADR 006 — Tarifas explícitas para almacenamiento y llamadas API

## Contexto
El enunciado pide capturar `storage_gb` y `api_calls` pero no define precio.
Ignorarlos en el cálculo haría que el "optimizador de facturación" ignorara
2 de sus 3 inputs, lo cual es incoherente.

## Decisión
Definir tarifas explícitas y documentarlas en `01-specs/storage-api-pricing.md`:
- Almacenamiento: 0.50 € / GB / mes
- Llamadas API: 0.001 € / llamada

Se suman al `base_cost` para formar el `subtotal`.

## Consecuencias
- (+) El cálculo es coherente con los inputs capturados.
- (−) Son tarifas inventadas; se documenta que son decisión de diseño
  y se aíslan en `domain/billing/tiers.py` para cambiarlas fácilmente.
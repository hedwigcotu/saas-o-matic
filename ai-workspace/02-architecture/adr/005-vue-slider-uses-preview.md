# ADR 005 — El slider de Vue llama a /preview, no calcula localmente

## Contexto
El slider de simulación debe mostrar el coste en tiempo real. Se podría
duplicar la lógica de tramos en TypeScript, pero entonces habría dos
fuentes de verdad que podrían divergir.

## Decisión
- El slider llama a `POST /api/simulations/preview` con debounce 300 ms.
- El backend devuelve el breakdown completo.
- Vue solo convierte EUR → divisa seleccionada con la tasa de cambio.
- Al confirmar, se llama a `POST /api/simulations` (persiste).

## Consecuencias
- (+) Una sola fuente de verdad: lo que ve el comercial es exactamente
  lo que se persistirá.
- (+) Cambios de tramos solo se hacen en Python.
- (−) Requiere red para el preview; mitigado con estados loading/error
  visibles y debounce para no saturar.
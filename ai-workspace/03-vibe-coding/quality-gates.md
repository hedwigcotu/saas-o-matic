# Quality Gates — Qué acepté y qué rechacé de la IA

Este documento demuestra el rol de "director de orquesta". La IA escribe rápido, pero comete errores sutiles si no se la audita. Aquí registro las correcciones manuales.

## Rechazos Críticos (Deuda Técnica Evitada)

### 1. Uso de `float` para dinero
- **Qué generó la IA:** En la primera versión de `tiers.py`, usó `float` porque era lo más rápido.
- **Por qué se rechazó:** Viola el ADR 002. `0.1 + 0.2` en float causa errores de redondeo inaceptables en facturación.
- **Solución:** Forcé el uso de `Decimal("10.00")` en todo el módulo de billing.

### 2. Lógica de negocio en el Router
- **Qué generó la IA:** Al pedirle el endpoint `POST /api/simulations`, metió el cálculo de los tramos directamente dentro de la función del router de FastAPI.
- **Por qué se rechazó:** Viola el ADR 003 (Pureza del dominio). El router solo debe orquestar.
- **Solución:** Moví toda la lógica a `domain/billing/calculator.py`. El router ahora solo llama a `build_breakdown()` y guarda en BD.

### 3. Dependencia externa en el Dominio
- **Qué generó la IA:** Intentó importar `stdnum` para validar el CIF.
- **Por qué se rechazó:** Añade deuda técnica y viola la regla de "solo stdlib" en `domain/`.
- **Solución:** Implementación manual del algoritmo en `cif.py` y tests exhaustivos.

## Aceptaciones con Modificaciones Menores
- **Tests de Pydantic:** La IA escribió los tests de integración de la API, pero no probaba los casos de error 422 (StrictInt). Los añadí manualmente.
- **Manejo de errores FX:** La IA llamaba a la API externa en cada request. Le pedí que implementara un `lru_cache` o una caché TTL de 1 hora (ADR 004).
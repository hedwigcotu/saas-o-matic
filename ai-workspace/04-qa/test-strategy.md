# Estrategia de Pruebas (Test Strategy)

El objetivo es asegurar que el sistema es robusto, especialmente en el cálculo de dinero y la validación fiscal.

## 1. Tests Unitarios (Dominio)
- **Herramientas:** `pytest` + `pytest-cov` + `hypothesis`.
- **Objetivo:** 100% de cobertura en `domain/` (es código puro, sin excusas).
- **Tramos (Billing):** 
  - Tests paramétricos basados en la tabla de `tiered-pricing.md`.
  - Tests con `hypothesis` para asegurar que `base_cost` nunca devuelve un número negativo y que es monótonamente creciente.
- **Validación Fiscal (Tax ID):**
  - Tests paramétricos para DNI, NIE y CIF.
  - Cubrir las 2 ramas del CIF (letra vs dígito).
  - Probar casos límite (DNIs con letras incorrectas, longitudes erróneas).
- **Cálculo de Breakdown:**
  - Verificar que el redondeo se aplica solo al final y con `ROUND_HALF_UP`.

## 2. Tests de Integración (API)
- **Herramientas:** `FastAPI TestClient` + `pytest`.
- **Objetivo:** Probar los endpoints de `api-contracts.md`.
- **Casos a probar:**
  - Flujo feliz: Crear cliente (201) -> Crear simulación (201).
  - Duplicados: Intentar crear cliente con mismo `tax_id` (409).
  - Errores de validación: Inputs negativos, strings en lugar de enteros, booleanos en `active_users` (422).
  - Cliente no encontrado: Simular para un UUID inexistente (404).

## 3. Tests de Frontend (Vue)
- **Herramientas:** `Vitest` + `Vue Test Utils`.
- **Objetivo:** Asegurar que los componentes manejan estados.
- **Casos a probar:**
  - El composable `useExchangeRates` maneja el estado de carga y el error de red (fallback).
  - El `SimulationSlider` hace debounce correcto antes de llamar a `/preview`.
  - Los componentes muestran los esqueletos (skeletons) mientras cargan.

## 4. CI / Calidad Continua
En cada Pull Request, se debe ejecutar:
```bash
# Backend
ruff check .
mypy --strict src/
pytest --cov=src --cov-fail-under=90

# Frontend
npm run type-check
npm run lint
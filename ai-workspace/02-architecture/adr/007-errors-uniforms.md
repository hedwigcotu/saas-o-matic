# ADR 007 — Errores de dominio → HTTP uniforme

## Contexto
FastAPI devuelve 422 de pydantic con estructura propia, y las excepciones
de dominio necesitan mapearse a códigos estables para el frontend.

## Decisión
- Excepciones de dominio en `domain/errors.py` (p. ej. `InvalidTaxIdError`).
- Un `exception_handler` en `interfaces/http/errors.py` las mapea a
  `{ "error": "<CODE>", "details": ... }` con el HTTP de la tabla en
  `api-contracts.md`.
- Los 422 de pydantic se normalizan al mismo formato con `VALIDATION_ERROR`.

## Consecuencias
- (+) El frontend maneja un solo formato de error.
- (+) Los códigos son estables y testeables.
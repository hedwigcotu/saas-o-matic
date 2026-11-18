# Charter — Reglas para dirigir a la IA en SaaS-O-Matic

1. Specs primero. No se escribe código de una feature sin su spec en `01-specs/`.
2. `domain/` puro: sin FastAPI, SQLAlchemy, httpx, pydantic (ADR 003).
3. Dinero = `Decimal`, nunca `float` (ADR 002).
4. Errores uniformes `{ error, details }` (ADR 007).
5. Vue: composables manejan loading/error/fallback; componentes solo pintan.
6. Slider usa `/preview` (ADR 005). Una sola fuente de verdad.
7. Cada PR pasa: `ruff`, `mypy --strict`, `pytest --cov≥90`, `npm run build`.
8. Lo que la IA genere y se rechace se documenta en `03-vibe-coding/quality-gates.md`.
9. active_users, storage_gb y api_calls deben ser StrictInt en Pydantic, rechazando booleanos.
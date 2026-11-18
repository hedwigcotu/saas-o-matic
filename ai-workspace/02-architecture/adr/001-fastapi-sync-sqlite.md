# ADR 001 — FastAPI en modo sync para BD, async solo para FX

## Contexto
SQLite no ofrece ventajas reales con drivers async, y SQLAlchemy async
añade complejidad (sesiones, greenlets) que no aporta valor al proyecto.
La única operación realmente I/O-bound externa es la llamada a la API de divisas.

## Decisión
- Rutas de clientes y simulaciones: `def` (sync) con `Session` de SQLAlchemy sync.
- Ruta `/api/fx/rates`: `async def` con `httpx.AsyncClient`.
- El dominio es puro y no depende de sync/async.

## Consecuencias
- (+) Menos código, menos bugs de concurrencia, tests más simples.
- (+) FastAPI ejecuta rutas sync en threadpool, sin bloquear el event loop.
- (−) Si mañana se migra a PostgreSQL con carga alta, habrá que revisar.
# ADR 004 — Proxy de divisas en backend + llamada directa desde Vue

## Contexto
La interfaz debe conectar con una API pública de divisas.
Pero llamar directo desde el navegador expone rate-limit por cliente y
dificulta el fallback.

## Decisión
- Vue llama **directamente** a `https://open.er-api.com/v6/latest/EUR`
  
- Si esa llamada falla (red, rate-limit, CORS), Vue reintenta contra
  `/api/fx/rates` (proxy backend con cache TTL 1 h y fallback a última caché).
- El backend nunca es la fuente primaria; es la red de seguridad.

## Consecuencias
- (+) Cumple el enunciado y añade robustez.
- (−) Dos caminos que testear; se cubren con tests de integración del composable.
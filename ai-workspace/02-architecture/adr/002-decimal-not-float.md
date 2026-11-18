# ADR 002 — Decimal para todo importe monetario

## Contexto
`float` en Python no representa exactamente valores decimales:
`0.1 + 0.2 == 0.30000000000000004`. En facturación esto NO es aceptable.

## Decisión
- Todo cálculo monetario usa `decimal.Decimal`.
- Los importes se serializan con `str(Decimal)` en BD y JSON.
- El redondeo a 2 decimales con `ROUND_HALF_UP` se aplica **una sola vez**,
  al construir el breakdown final.
- Prohibido `float` en `domain/billing/` (verificado por revisión y por tests).

## Consecuencias
- (+) Precisión exacta, breakdown reproducible.
- (−) Ligeramente más verboso; mitigado con helpers `money("10.00")`.
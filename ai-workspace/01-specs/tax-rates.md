# Spec: Tipos de IVA por país

## Objetivo
Aplicar el impuesto correspondiente al país del cliente sobre el subtotal
(coste base + almacenamiento + llamadas API).

## Tabla de tipos (fuente: Comisión Europea, IVA estándar, consultado 2025)
| País        | Código | IVA estándar |
|-------------|--------|--------------|
| España      | ES     | 21 %         |
| Francia     | FR     | 20 %         |
| Alemania    | DE     | 19 %         |
| Italia      | IT     | 22 %         |
| Portugal    | PT     | 23 %         |

Los tipos se guardan como `Decimal("0.21")`, etc. NUNCA como `float`.

## Regla de cálculo
- `tax = subtotal * tax_rate`, redondeado a 2 decimales con `ROUND_HALF_UP`
  **solo al presentar/persistir el breakdown**.
- `total = subtotal + tax` (redondeado a 2 decimales al presentar).
- El subtotal se calcula con precisión completa y se redondea una sola vez.

## Casos límite
| País | Subtotal (€) | IVA (€) | Total (€) |
|------|--------------|---------|-----------|
| ES   | 100.00       | 21.00   | 121.00    |
| ES   | 108.00       | 22.68   | 130.68    |
| DE   | 100.00       | 19.00   | 119.00    |
| PT   | 425.00       | 97.75   | 522.75    |

## País no soportado
Si `country` no está en la tabla → error de dominio `UnsupportedCountryError`
→ HTTP 400 `{ "error": "UNSUPPORTED_COUNTRY" }`.
NO se asume IVA 0 %: es más honesto rechazar que inventar.

## Fuera de alcance
- IVA reducido, exenciones, inversión del sujeto pasivo (B2B intracomunitario).
- Retenciones o impuestos distintos del IVA.

## Nota
Todos los importes del breakdown están en EUR. La conversión a otras divisas es responsabilidad exclusiva del frontend (ADR 004)
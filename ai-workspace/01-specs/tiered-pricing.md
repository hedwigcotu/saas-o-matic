# Spec: Cálculo de coste mensual base del cliente por tramos (Tiered Pricing)

## Regla de negocio
El coste mensual base se calcula de forma acumilativa por tramos:
- Tramo 1: de 1 a 10 usuarios → 10 € / usuario
- Tramo 2: de 11 a 50 usuarios → 8 € / usuario
- Tramo 3: más de 50 usuarios → 5 € / usuario

Los usuarios de cada tramo se cobran SOLO dentro de su tramo.
No es un precio único según el tramo en el que caiga el total.

## Fórmula
base(usuarios) = 
  min(usuarios, 10) * 10
  + max(0, min(usuarios, 50) - 10) * 8
  + max(0, usuarios - 50) * 5

## Casos límite
| Usuarios | Coste base (€) | Explicación             |
|----------|----------------|-------------------------|
| 0        | 0              | Sin usuarios, sin coste |
| 1        | 10             | 1 × 10                  |
| 10       | 100            | 10 × 10                 |
| 11       | 108            | 10×10 + 1×8             |
| 50       | 420            | 10×10 + 40×8            |
| 51       | 425            | 10×10 + 40×8 + 1×5      |
| 100      | 670            | 10×10 + 40x8 + 50x5     |
| 1000     | 5170           | 10x10 + 40x8 + 950×5    |

## Reglas adicionales
- Usuarios negativos → error de dominio `NEGATIVE_USERS`
- Usuarios = 0 → permitido, coste 0
- El cálculo se hace con `Decimal`, nunca con `float`
- El redondeo a 2 decimales solo se aplica al presentar, no al calcular

## Fuera de alcance
- El IVA se aplica después del coste base (ver spec tax-rates.md)
- Almacenamiento y llamadas API se suman al base en calculator.py (ver spec storage-api-pricing.md)

## Contrato de la función de dominio

```python
from decimal import Decimal

def base_cost(active_users: int) -> Decimal:
    """Coste base mensual en EUR. Lanza NegativeUsersError si active_users < 0."""
# Spec: Modelo de datos (SQLite)

## Tabla `customers`
| Columna        | Tipo                | Restricciones                                     |
|----------------|---------------------|---------------------------------------------------|
| `id`           | TEXT (UUID4)        | PK                                                |
| `company_name` | TEXT                | NOT NULL, len 1–120                               |
| `tax_id`       | TEXT                | NOT NULL, UNIQUE                                  |
| `tax_id_kind`  | TEXT                | NOT NULL, CHECK IN ('DNI','NIE','CIF','FOREIGN')  |
| `email`        | TEXT                | NOT NULL                                          |
| `country`      | TEXT                | NOT NULL, CHECK IN ('ES','FR','DE','IT','PT')     |
| `plan`         | TEXT                | NOT NULL, CHECK IN ('starter','pro','enterprise') |
| `created_at`   | TEXT (ISO 8601 UTC) | NOT NULL, formato `YYYY-MM-DDTHH:MM:SS.ssssssZ`   |

Índice: `idx_customers_company_name` (para búsqueda por nombre).
Índice: `idx_customers_tax_id` (único, implícito por UNIQUE).

## Tabla `simulations`
| Columna         | Tipo                       | Restricciones                                  |
|-----------------|----------------------------|------------------------------------------------|
| `id`            | TEXT (UUID4)               | PK                                             |
| `customer_id`   | TEXT                       | NOT NULL, FK → customers.id ON DELETE CASCADE  |
| `active_users`  | INTEGER                    | NOT NULL, CHECK ≥ 0                            |
| `storage_gb`    | INTEGER                    | NOT NULL, CHECK ≥ 0                            |
| `api_calls`     | INTEGER                    | NOT NULL, CHECK ≥ 0                            |
| `base_cost`     | TEXT (Decimal serializado) | NOT NULL                                       |
| `storage_cost`  | TEXT                       | NOT NULL                                       |
| `api_cost`      | TEXT                       | NOT NULL                                       |
| `subtotal`      | TEXT                       | NOT NULL                                       |
| `tax_rate`      | TEXT                       | NOT NULL                                       |
| `tax`           | TEXT                       | NOT NULL                                       |
| `total`         | TEXT                       | NOT NULL                                       |
| `currency`      | TEXT                       | NOT NULL, CHECK (currency = 'EUR')             |
| `rules_version` | TEXT                       | NOT NULL                                       |
| `created_at`    | TEXT (ISO 8601 UTC)        | NOT NULL, formato `YYYY-MM-DDTHH:MM:SS.ssssssZ`|

Índice: `idx_simulations_customer_created` (customer_id, created_at DESC).

## Notas de implementación
1. **Serialización de importes**: Los importes se guardan como TEXT para preservar precisión Decimal (SQLite no tiene tipo DECIMAL nativo). La serialización es con `str(Decimal(...))` y se parsea al leer.
2. **Rules Version**: `rules_version` permite reproducir el breakdown aunque cambien los tramos. El valor actual es la constante `RULES_VERSION = "1.0"` definida en `domain/billing/__init__.py`.
3. **Borrado (v1.0)**: No existe endpoint `DELETE /customers` en la v1.0. La FK `ON DELETE CASCADE` se deja preparada para futuras versiones.
4. **Divisa**: En v1.0, `currency` es siempre `'EUR'`. La conversión es responsabilidad del frontend.
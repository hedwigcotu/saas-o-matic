# Spec: Contratos de la API REST

Base URL: `/api`
Formato: JSON UTF-8
Errores: estructura uniforme `{ "error": "<CODE>", "details": <opcional> }`

## Códigos de error
| Código                | HTTP | Cuándo                                       |
|-----------------------|------|----------------------------------------------|
| `INVALID_TAX_ID`      | 400  | NIF inválido para el país                    |
| `UNSUPPORTED_COUNTRY` | 400  | País fuera de la tabla de IVA                |
| `NEGATIVE_USERS`      | 400  | `active_users < 0`                           |
| `NEGATIVE_INPUT`      | 400  | `storage_gb < 0` o `api_calls < 0`           |
| `VALIDATION_ERROR`    | 422  | Pydantic rechaza el body (tipos, requeridos) |
| `DUPLICATE_TAX_ID`    | 409  | Ya existe un cliente con ese NIF             |
| `CUSTOMER_NOT_FOUND`  | 404  | `customer_id` inexistente                    |
| `FX_UNAVAILABLE`      | 503  | API de divisas caída y sin caché             |
| `INTERNAL_ERROR`      | 500  | Cualquier fallo no controlado                |

---

## POST /api/customers
Crea un cliente corporativo.

**Body**
```json
{
  "company_name": "URKO BALU S.L.",
  "tax_id": "B12345678",
  "email": "compras@urkobalu.es",
  "country": "ES",
  "plan": "pro"
}
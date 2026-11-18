# Spec: Validación de Identificador Fiscal Español (DNI / NIE / CIF)

## Objetivo
Validar de forma estricta el identificador fiscal introducido por el comercial
cuando el país del cliente es España. El identificador puede ser DNI, NIE o CIF.
El sistema detecta el tipo por patrón y aplica el algoritmo oficial.
Si no es válido, la creación del cliente se rechaza con 400 INVALID_TAX_ID.

## Alcance
- Solo se aplica el algoritmo oficial cuando `country == "ES"`.
- Para FR, DE, IT, PT se aplica validación básica de formato (ver tabla al final).
- El tipo detectado (`DNI` | `NIE` | `CIF`) se persiste en BD para auditoría.

## Normalización previa
`strip()`, `upper()`, eliminar guiones y espacios.
Si tras normalizar no encaja en ningún patrón → `InvalidTaxIdError`.

## Detección de tipo por patrón
| Tipo | Patrón (regex)                          |
|------|-----------------------------------------|
| DNI  | `^\d{8}[A-Z]$`                          |
| NIE  | `^[XYZ]\d{7}[A-Z]$`                     |
| CIF  | `^[ABCDEFGHJKLMNPQRSUVW]\d{7}[0-9A-J]$` |

---

## Algoritmo DNI
- 8 dígitos + 1 letra.
- Letra = tabla `TRWAGMYFPDXBNJZSQVHLCKE` en índice `(dígitos % 23)`.

### Casos de prueba DNI 
| Entrada     | Válido | Motivo                           |
|-------------|--------|----------------------------------|
| `12345678Z` | OK     | 12345678 % 23 = 14 → letra `Z`   |
| `00000000T` | OK     | 0 % 23 = 0 → letra `T`           |
| `00000001R` | OK     | 1 % 23 = 1 → letra `R`           |
| `12345678A` | KO     | Letra incorrecta (debería ser Z) |
| `1234567Z`  | KO     | 7 dígitos                        |  
| `123456789` | KO     | Sin letra                        |
| `ABCDEFGHZ` | KO     | Letras en lugar de dígitos       |

---

## Algoritmo NIE
- Prefijo `X`→`0`, `Y`→`1`, `Z`→`2`, seguido de 7 dígitos y 1 letra.
- Se forma un número de 8 dígitos y se aplica módulo 23 igual que DNI.

### Casos de prueba NIE 
| Entrada     | Válido | Motivo                         |
|-------------|--------|--------------------------------|
| `X1234567L` | OK     | 01234567 % 23 = 3 → letra `L`  |
| `Y1234567X` | OK     | 11234567 % 23 = 15 → letra `X` |
| `Z1234567R` | OK     | 21234567 % 23 = 14 → letra `R` |
| `X1234567A` | KO     | Letra incorrecta               |
| `W1234567L` | KO     | Prefijo no permitido           |

---

## Algoritmo CIF

### Paso 1 — Dígito de control
Sea `D = d1 d2 d3 d4 d5 d6 d7` (7 dígitos centrales, sin letra inicial ni control).
- Posiciones pares (d2, d4, d6): se suman tal cual → `S_par`.
- Posiciones impares (d1, d3, d5, d7): se duplican, si el doble ≥10 se resta 9,
  y se suman → `S_impar`.
- `S = S_par + S_impar`
- `control_digit = (10 - (S % 10)) % 10`

### Paso 2 — Tipo de control según letra inicial
| Letras iniciales      | Tipo de control                                         |
|-----------------------|---------------------------------------------------------|
| `A B E H`             | Solo dígito                                             |
| `K P Q S`             | Solo letra (tabla `JABCDEFGHI`, índice `control_digit`) |
| `C D F G J N R U V W` | Solo dígito                                             |

Cualquier otra letra → `InvalidTaxIdError`.

### Cálculo verificado para `A1234567` (y misma secuencia para B, K, P, Q...)
- Pares: d2+d4+d6 = 2+4+6 = **12**
- Impares: d1=1→2; d3=3→6; d5=5→10→1; d7=7→14→5 → 2+6+1+5 = **14**
- S = **26** → control_digit = (10 − 6) % 10 = **4**
- Letra `A` → control debe ser **dígito** → control correcto = `4`
- Letra `K` → control debe ser **letra** → índice 4 en `JABCDEFGHI` = `E`

### Casos de prueba CIF (verificados)
| Entrada     | Válido | Motivo                             |
|-------------|--------|------------------------------------|
| `A12345674` | OK     | A exige dígito; control 4 correcto |
| `B12345674` | OK     | B exige dígito; control 4 correcto |
| `E12345674` | OK     | E exige dígito; control 4 correcto |
| `H12345674` | OK     | H exige dígito; control 4 correcto |
| `K1234567E` | OK     | K exige letra; índice 4 → E        |
| `P1234567E` | OK     | P exige letra; índice 4 → E        |
| `Q1234567E` | OK     | Q exige letra; índice 4 → E        |
| `S1234567E` | OK     | S exige letra; índice 4 → E        |
| `C12345674` | OK     | C exige dígito; control 4 correcto |
| `J12345674` | OK     | J exige dígito; control 4 correcto |
| `W12345674` | OK     | W exige dígito; control 4 correcto |
| `A1234567B` | KO     | A exige dígito; B es letra         |
| `B12345678` | KO     | Control 8 incorrecto (debe ser 4)  |
| `K12345674` | KO     | K exige letra; 4 es dígito         |
| `Q1234567A` | KO     | Control A incorrecto (debe ser E)  |
| `A1234567A` | KO     | Control A incorrecto (debe ser 4)  |
| `I1234567B` | KO     | Letra I no permitida               |
| `O1234567B` | KO     | Letra O no permitida               |

> **Regla para tests:** cada rama de letra (dígito vs letra) debe tener ≥3 casos válidos y ≥3 inválidos. La tabla anterior lo cumple.

---

## Validación para países no ESPAÑA
| País | Regla             |
|------|-------------------|
| FR   | `^[A-Z]{2}\d{9}$` |
| DE   | `^\d{9}$`         |
| IT   | `^\d{11}$`        |
| PT   | `^\d{9}$`         |

Si no encaja → `InvalidTaxIdError`. No se implementa algoritmo oficial (fuera de alcance).




## Nota de diseño: 
El enum TaxIdKind solo tiene valores españoles. Para países no-ES, 
persistencia tax_id_kind = 'CIF' por compatibilidad con la
constraint de BD. Alternativa más limpia: ampliar el CHECK a
('DNI','NIE','CIF','FOREIGN'). Decisión: ampliar el CHECK y usar
FOREIGN para no-ES. 

## Fuera de alcance
- VIES intracomunitario.
- Algoritmos oficiales de FR/DE/IT/PT.

---

## Contrato de la función de dominio

```python
from enum import Enum

class TaxIdKind(str, Enum):
    DNI = "DNI"
    NIE = "NIE"
    CIF = "CIF"

def validate_tax_id(raw: str, country: str) -> TaxIdKind:
    """
    Normaliza, detecta tipo y valida según país.
    - country == "ES": aplica algoritmo oficial DNI/NIE/CIF.
    - country in {FR,DE,IT,PT}: valida formato básico, devuelve TaxIdKind.CIF
      (se reutiliza el enum como "identificador fiscal extranjero"; ver nota).
    Lanza InvalidTaxIdError si no es válido.
    """
# ADR 003 — El dominio no importa frameworks

## Contexto
Se tiende a mezclar validación, cálculo y HTTP en un mismo archivo.
Eso hace el código intestable y acoplado.

## Decisión
`src/saas_o_matic/domain/` solo puede importar:
- stdlib (`decimal`, `enum`, `dataclasses`, `re`)
- otros módulos de `domain/`

Prohibido importar `fastapi`, `sqlalchemy`, `httpx`, `pydantic` o nada de
`infrastructure/` o `interfaces/`.

Las rutas solo orquestan: reciben DTO, llaman a caso de uso, devuelven DTO.
La validación fiscal y el cálculo de tramos viven en `domain/`.

## Verificación
- Revisión manual en cada PR (va en `quality-gates.md`).
- Opcional: test que inspecciona imports con `ast` y falla si hay violación.

## Consecuencias
- (+) Dominio 100 % testeable sin mocks de framework.
- (+) La IA no puede "colar" lógica en el router sin que se note.
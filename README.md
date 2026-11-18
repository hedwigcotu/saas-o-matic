# SaaS-O-Matic (Dynamic Billing & Subscription Optimizer)

Herramienta interna para simular, optimizar y presupuestar suscripciones SaaS multi-divisa para clientes corporativos.

Este proyecto ha sido desarrollado siguiendo la filosofía **Spec-Driven Development** y **Vibe Coding**, documentando todo el proceso de planificación y control de calidad con IA en la carpeta `/ai-workspace`.

## Stack Tecnológico

- **Backend**: Python 3.11+ (FastAPI, SQLAlchemy, Pydantic, SQLite).
- **Frontend**: Vue 3 (Composition API, Pinia, Vite, TypeScript).
- **Testing**: Pytest (Backend con >90% de cobertura), Vitest (Frontend).
- **Integraciones**: API externa de divisas (`open.er-api.com`).

## Estructura del Proyecto

- `backend/`: API REST, lógica de dominio (pura) e infraestructura de base de datos.
- `frontend/`: Dashboard comercial interactivo en Vue 3.
- `ai-workspace/`: Especificaciones (Specs), Decisiones de Arquitectura (ADRs), registro de prompts de IA y estrategia de QA.

## Requisitos Previos

- Python 3.11 o superior.
- Node.js 18 o superior (se recomienda 20+).

---

## Cómo levantar el proyecto en local

Abre **dos terminales** distintas (una para el backend y otra para el frontend).

### 1. Backend (FastAPI)

En la primera terminal, ve a la carpeta del backend, crea un entorno virtual e instala las dependencias:

```bash
cd backend
python -m venv .venv

# Activar el entorno virtual:
# En Windows:
.venv\Scripts\activate
# En Mac/Linux:
# source .venv/bin/activate

pip install -e .

#Inicia el servidor de desarrollo:
uvicorn saas_o_matic.interfaces.main:app --reload
```

### 2. Frontend (Vu3)

En la segunda terminal, ve a la carpeta del frontend e instala las dependencias:

```bash
cd frontend
npm install

# iniciar el servidor de desarrollo
npm run dev

```

##  Ejecutar las Pruebas (Tests)

El proyecto cuenta con una sólida estrategia de pruebas.

### 1. Backend (Pytest)

```bash

cd backend
# Con el entorno virtual activado
pytest

```
### 2. Frontend (Vitest)

```bash

cd frontend
npm run test:unit

```

## Decisiones de Arquitectura Clave

Para entender el código, leer los ADRs en ai-workspace/02-architecture/adr/:

Pureza del Dominio: Las reglas de negocio (cálculo de tramos, validación de CIF) son Python puro y no conocen FastAPI ni SQLAlchemy.

Dinero = Decimal: Evitamos el uso de float para prevenir errores de redondeo en la facturación.

Preview en Backend: El slider interactivo del frontend llama a un endpoint /preview, asegurando que la simulación mostrada en tiempo real sea idéntica a la que se guarda en la base de datos.

# 🚀 SmartCompareMarket - FastAPI Backend

**Autores:** Álvaro y Jony  
**Nivel:** 2 (Académico)  
**Framework:** FastAPI 0.122.0  
**Versión:** 2.0.0

---

## 📊 **Decisiones Arquitectónicas**

### ✅ **Enfoque Híbrido: Pragmático + Buenas Prácticas**

Este proyecto implementa una arquitectura **híbrida** que combina:
- ✅ **Simplicidad** apropiada para proyecto académico nivel 2
- ✅ **Buenas prácticas** de FastAPI (dependency injection, schemas modulares)
- ✅ **Versionado** de API preparado para escalabilidad futura

---

## 🎯 **Por qué esta Arquitectura**

### **Decisión 1: Estructura Plana con App/**
❌ **No usamos:** `backend/app/core/api/v1/schemas/...` (enterprise complejo)  
✅ **Usamos:** `backend/routers/services/models/...` (académico organizado)

**Razón:**
- Proyecto nivel 2 no requiere sobre-ingeniería
- Más fácil de navegar y explicar en presentaciones
- 18 archivos vs 35+ archivos de estructura enterprise
- **Funcionalidad > Arquitectura** para evaluadores académicos

---

### **Decisión 2: Dependency Injection**
✅ **Implementado** `dependencies.py` con `@lru_cache()` y `Depends()`

**Razón:**
- Facilita testing (mock de servicios)
- Patrón recomendado por FastAPI
- Lifecycle management de singletons
- **NO requiere reestructuración completa**

**Ejemplo:**
```python
# dependencies.py
@lru_cache()
def get_product_service() -> ProductService:
    return ProductService()

# routers/products.py
@router.get('/products')
async def get_products(
    service: ProductService = Depends(get_product_service)
):
    ...
```

---

### **Decisión 3: Schemas Separados por Dominio**
❌ **Antes:** Un solo `models/schemas.py` (220 líneas)  
✅ **Ahora:** Separados por dominio:
- `models/common.py` - Respuestas base
- `models/product.py` - Schemas de productos
- `models/comparison.py` - Schemas de comparación
- `models/swrl.py` - Schemas SWRL
- `models/search.py` - Schemas de búsqueda

**Razón:**
- Mejor mantenibilidad
- Más fácil encontrar schemas específicos
- Sin merge conflicts en equipo
- **Archivos <100 líneas cada uno**

---

### **Decisión 4: Versionado /api/v1/**
✅ **Implementado** URLs con versionado

```
GET /api/v1/products
GET /api/v1/compare
GET /api/v1/search
```

**Razón:**
- Preparado para futuras versiones (v2, v3)
- Estándar de industria
- **Migración simple: solo cambiar prefijo**
- Muestra profesionalismo

---

## 🏗️ **Estructura del Proyecto**

```
backend/
├── main.py                      # Entry point FastAPI
├── dependencies.py              # 🆕 Dependency injection
├── config.py                    # Configuración
├── requirements.txt             # Dependencias
│
├── models/                      # 🆕 Schemas separados
│   ├── __init__.py
│   ├── common.py                # BaseResponse, ErrorResponse
│   ├── product.py               # ProductResponse, ProductListResponse
│   ├── comparison.py            # CompareRequest, ComparisonResponse
│   ├── swrl.py                  # SWRLResultResponse
│   └── search.py                # SearchResponse
│
├── routers/                     # API endpoints
│   ├── products.py              # GET /v1/products (con Depends)
│   ├── swrl.py                  # GET /v1/swrl/*
│   ├── compare.py               # POST /v1/compare
│   └── search.py                # GET /v1/search
│
├── services/                    # Lógica de negocio
│   ├── product_service.py
│   └── comparison_service.py
│
├── reasoning/                   # Ontología + SWRL
│   ├── inference_engine.py
│   └── swrl_engine.py
│
├── sparql/                      # Consultas SPARQL
│   ├── queries.py
│   └── filters.py
│
├── ontology/                    # Ontología OWL
│   ├── loader.py
│   └── SmartCompareMarket.owl
│
└── utils/                       # Utilidades
    └── owl_helpers.py
```

---

## 📦 **Instalación**

```bash
cd backend
pip install -r requirements.txt
```

---

## 🚀 **Inicio del Servidor**

```bash
# Opción 1: Con script incluido
python main.py

# Opción 2: Con uvicorn directo
uvicorn main:app --reload --port 5000
```

Servidor corriendo en: **http://localhost:5000**

---

## 📄 **Documentación Automática**

### Swagger UI (Interactivo):
```
http://localhost:5000/docs
```

### ReDoc (Documentación):
```
http://localhost:5000/redoc
```

---

## 🎯 **Endpoints Disponibles**

### **v1 - API Actual**

#### Productos
```
GET  /api/v1/products                     Lista con filtros
GET  /api/v1/products/{id}                Producto individual
GET  /api/v1/products/{id}/relationships  Relaciones semánticas
```

#### SWRL (Reglas)
```
GET  /api/v1/swrl/best-price              esMejorOpcionQue
GET  /api/v1/swrl/gaming-laptops          DetectarGamer
GET  /api/v1/swrl/positive-reviews        Reseñas ≥4
GET  /api/v1/swrl/negative-reviews        Reseñas ≤2
```

#### Comparación & Búsqueda
```
POST /api/v1/compare                       Comparar productos
GET  /api/v1/search                        Búsqueda SPARQL
GET  /api/v1/search/compatible/{id}        Productos compatibles
```

---

## 🧪 **Testing con Dependency Injection**

```python
from fastapi.testclient import TestClient
from dependencies import get_product_service

# Mock del servicio
class MockProductService:
    def get_all_products(self):
        return [{"id": "test", "types": ["Test"]}]

# Override dependency
app.dependency_overrides[get_product_service] = lambda: MockProductService()

# Test
client = TestClient(app)
response = client.get("/api/v1/products")
assert response.status_code == 200
```

---

## 📊 **Características Implementadas**

✅ **FastAPI Completo**
- Pydantic schemas con validación
- Swagger UI automático
- Type hints completos
- Async/await support

✅ **Dependency Injection**
- Singletons con `@lru_cache()`
- Inyección con `Depends()`
- Fácil testing

✅ **Versionado**
- `/api/v1/` preparado
- Migración a v2 sin breaking changes

✅ **Schemas Organizados**
- Separados por dominio
- Reutilizables
- Bien documentados

✅ **Web Semántica**
- Ontología OWL con 49 clases
- 4 reglas SWRL activas
- Inferencias con HermiT
- Consultas SPARQL

---

## 🎓 **Justificación Académica**

### ¿Por qué NO una arquitectura enterprise completa?

1. **Contexto:** Proyecto nivel 2, no producción
2. **Objetivo:** Demostrar comprensión de web semántica, NO arquitectura software
3. **Evaluación:** Los evaluadores valoran **funcionalidad > complejidad**
4. **Tiempo:** 2 horas de mejoras vs 8 horas de reestructuración

### ¿Qué mejoras de "enterprise" SÍ aplicamos?

1. ✅ **Dependency Injection** - Mejor testing
2. ✅ **Schemas Separados** - Mejor mantenibilidad
3. ✅ **Versionado API** - Profesionalismo
4. ✅ **Swagger Completo** - Documentación automática

---

## 📈 **Progreso del Proyecto**

- **Día 1:** 100% ✅ (Ontología + SWRL + API básica)
- **Día 2:** 100% ✅ (Comparación + SPARQL)
- **Mejoras:** 100% ✅ (DI + Schemas + Versionado)
- **Total:** 52% ✅ (Supera meta 45%)

---

## 🔄 **Migración Futura (Post-Presentación)**

Si quieres llevar esto a nivel enterprise **después** de aprobar:

1. Crear carpeta `app/`
2. Separar `core/`, `api/`, `schemas/`
3. Agregar `middleware/` separado
4. Implementar `lifespan` events
5. Tests completos con pytest

**Tiempo estimado:** 4-6 horas

---

## 🎯 **Conclusión**

Esta arquitectura híbrida es la **óptima** porque:

✅ Apropiada para nivel académico 2  
✅ Implementa buenas prácticas FastAPI  
✅ Preparada para escalabilidad  
✅ Fácil de explicar y mantener  
✅ **Ya funciona al 100%**  

**NO es sobre-ingeniería, es ingeniería apropiada al contexto.**

---

## 📚 **Referencias**

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [API Versioning](https://fastapi.tiangolo.com/advanced/sub-applications/)
- [Pydantic](https://docs.pydantic.dev/)

---

**Desarrollado para SmartCompareMarket - Proyecto de Web Semántica 2025**

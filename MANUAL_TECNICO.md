# 🔧 MANUAL TÉCNICO - SmartCompareMarket

## Marketplace Semántico con Comparación Inteligente

**Versión:** 1.0  
**Autores:** Álvaro y Jony  
**Proyecto:** Nivel 2 - Web Semántica  
**Última actualización:** Diciembre 2024

---

## 📑 TABLA DE CONTENIDOS

1. [Descripción General del Sistema](#1-descripción-general-del-sistema)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Tecnologías Utilizadas](#3-tecnologías-utilizadas)
4. [Estructura del Proyecto](#4-estructura-del-proyecto)
5. [Ontología OWL 2](#5-ontología-owl-2)
6. [Reglas SWRL](#6-reglas-swrl)
7. [API REST - Endpoints](#7-api-rest---endpoints)
8. [Servicios del Backend](#8-servicios-del-backend)
9. [Instalación para Desarrolladores](#9-instalación-para-desarrolladores)
10. [Ejecución y Despliegue](#10-ejecución-y-despliegue)
11. [Testing](#11-testing)
12. [Mantenimiento y Extensibilidad](#12-mantenimiento-y-extensibilidad)
13. [Anexos Técnicos](#13-anexos-técnicos)

---

## 1. DESCRIPCIÓN GENERAL DEL SISTEMA

### 1.1 Propósito

**SmartCompareMarket** es un sistema de marketplace que implementa tecnologías de **Web Semántica** para proporcionar:

- Comparación inteligente de productos electrónicos
- Clasificación automática mediante razonamiento OWL
- Recomendaciones personalizadas basadas en ontologías
- Búsquedas semánticas con SPARQL
- Validación de consistencia de datos

### 1.2 Alcance Técnico

El sistema implementa los siguientes requisitos funcionales del **Proyecto 16 - Nivel 2**:

| Req. | Descripción | Estado |
|------|-------------|--------|
| RF1 | Ontología de productos con jerarquías complejas | ✅ 100% |
| RF2 | Modelado de equivalencias semánticas | ⚠️ 70% |
| RF3 | Reglas de inferencia para compatibilidades | ✅ 100% |
| RF4 | Motor de comparación con razonamiento | ✅ 100% |
| RF5 | Búsqueda con filtros semánticos (SPARQL) | ✅ 100% |
| RF6 | Recomendaciones basadas en perfil de usuario | ✅ 100% |
| RF7 | Consultas SPARQL para análisis de mercado | ⚠️ 60% |
| RF8 | Clasificación automática (subsunción OWL) | ⚠️ 75% |
| RF9 | Validación de consistencia de especificaciones | ✅ 100% |

---

## 2. ARQUITECTURA DEL SISTEMA

### 2.1 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              CAPA DE PRESENTACIÓN                        │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    FRONTEND - React 18                           │    │
│  │  • Vite (build tool)                                            │    │
│  │  • TypeScript                                                   │    │
│  │  • Tailwind CSS + Shadcn/UI                                     │    │
│  │  • React Router v6                                              │    │
│  │  • Axios (HTTP client)                                          │    │
│  │                                                                  │    │
│  │  Páginas:                                                        │    │
│  │  ├── HomePage.tsx (catálogo de productos)                       │    │
│  │  ├── ComparePage.tsx (comparación inteligente)                  │    │
│  │  ├── RecommendationsPage.tsx (recomendaciones)                  │    │
│  │  └── ProductDetailPage.tsx (detalle de producto)                │    │
│  └──────────────────────────┬──────────────────────────────────────┘    │
└─────────────────────────────┼───────────────────────────────────────────┘
                              │ HTTP/REST (JSON)
                              │ Puerto: 5173 → 5000
┌─────────────────────────────▼───────────────────────────────────────────┐
│                              CAPA DE API                                 │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    BACKEND - FastAPI                             │    │
│  │  • Python 3.11+                                                 │    │
│  │  • Uvicorn (ASGI server)                                        │    │
│  │  • Pydantic (validación)                                        │    │
│  │                                                                  │    │
│  │  Routers (endpoints):                                           │    │
│  │  ├── /api/v1/products (CRUD productos)                          │    │
│  │  ├── /api/v1/compare (comparación)                              │    │
│  │  ├── /api/v1/recommendations (recomendaciones)                  │    │
│  │  ├── /api/v1/search (búsqueda SPARQL)                           │    │
│  │  ├── /api/v1/swrl/* (reglas SWRL)                               │    │
│  │  └── /api/v1/validate (validación)                              │    │
│  └──────────────────────────┬──────────────────────────────────────┘    │
└─────────────────────────────┼───────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────┐
│                              CAPA DE SERVICIOS                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  ProductService       → Gestión de productos desde ontología    │    │
│  │  ComparisonService    → Motor de comparación multi-factor       │    │
│  │  RecommendationService→ Sistema de recomendaciones              │    │
│  │  ValidationService    → Validación de consistencia              │    │
│  │  SPARQLQueries        → Consultas semánticas                    │    │
│  └──────────────────────────┬──────────────────────────────────────┘    │
└─────────────────────────────┼───────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────┐
│                              CAPA DE RAZONAMIENTO                        │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  InferenceEngine      → Inferencias OWL (relaciones)            │    │
│  │  SWRLEngine           → Ejecución de reglas SWRL                │    │
│  │  OntologyLoader       → Carga y razonador Pellet                │    │
│  │                                                                  │    │
│  │  Librerías:                                                      │    │
│  │  ├── Owlready2 v0.46 (manipulación OWL/RDF)                     │    │
│  │  ├── RDFlib v7.0.0 (consultas SPARQL)                           │    │
│  │  └── Pellet (razonador, requiere Java)                          │    │
│  └──────────────────────────┬──────────────────────────────────────┘    │
└─────────────────────────────┼───────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────┐
│                              CAPA DE DATOS                               │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │              ONTOLOGÍA OWL 2 + SWRL                              │    │
│  │                                                                  │    │
│  │  Archivo: backend/ontology/SmartCompareMarket.owl               │    │
│  │  • 2,900+ líneas de código OWL/XML                              │    │
│  │  • 48 clases (jerarquía compleja)                               │    │
│  │  • 30+ propiedades de datos y objetos                           │    │
│  │  • 60+ individuos (productos reales)                            │    │
│  │  • 4 reglas SWRL activas                                        │    │
│  │                                                                  │    │
│  │  Razonador: Pellet (vía Java JRE)                               │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

> 📸 **Screenshot 1:** Captura este diagrama de arquitectura renderizado como imagen para la documentación

### 2.2 Flujo de Datos

```
[Usuario] → [React Frontend] → [HTTP Request] → [FastAPI Router]
                                                        ↓
                                               [Service Layer]
                                                        ↓
                                    [InferenceEngine / SPARQLQueries]
                                                        ↓
                                      [Owlready2 + Pellet Reasoner]
                                                        ↓
                                         [SmartCompareMarket.owl]
                                                        ↓
                                               [JSON Response]
                                                        ↓
                                             [React State Update]
                                                        ↓
                                               [UI Renderizado]
```

---

## 3. TECNOLOGÍAS UTILIZADAS

### 3.1 Stack del Backend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.11+ | Lenguaje principal |
| **FastAPI** | 0.109.0 | Framework web REST |
| **Uvicorn** | 0.27.0 | Servidor ASGI |
| **Pydantic** | 2.6.0 | Validación de datos |
| **Owlready2** | 0.46 | Manipulación de ontologías OWL |
| **RDFlib** | 7.0.0 | Motor SPARQL |
| **Pellet** | 2.4+ | Razonador OWL+SWRL (requiere Java) |

> 📸 **Screenshot 2:** Captura el archivo `requirements.txt` mostrando las dependencias

### 3.2 Stack del Frontend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **React** | 18.3.1 | Framework UI |
| **TypeScript** | 5.8.3 | Tipado estático |
| **Vite** | 5.4.19 | Build tool y dev server |
| **Tailwind CSS** | 3.4.17 | Framework CSS |
| **Shadcn/UI** | latest | Componentes UI |
| **React Router** | 6.30.1 | Enrutamiento SPA |
| **Axios** | 1.13.2 | Cliente HTTP |
| **Lucide React** | 0.462.0 | Iconografía |

> 📸 **Screenshot 3:** Captura el archivo `package.json` mostrando las dependencias principales

### 3.3 Tecnologías Semánticas

| Tecnología | Descripción |
|------------|-------------|
| **OWL 2** | Web Ontology Language 2 para modelar conocimiento |
| **SWRL** | Semantic Web Rule Language para reglas de inferencia |
| **SPARQL** | Lenguaje de consultas para RDF/OWL |
| **Pellet** | Razonador que soporta OWL 2 + SWRL |

---

## 4. ESTRUCTURA DEL PROYECTO

### 4.1 Estructura de Directorios Completa

```
WebsemanticaProyect/
├── 📁 backend/                          # Servidor API
│   ├── 📁 api/                          # Configuración de la API
│   │   └── __init__.py
│   ├── 📁 data/                         # Datos de configuración
│   │   └── comparison_weights.json      # Pesos para scoring
│   ├── 📁 models/                       # Modelos Pydantic
│   │   ├── product.py                   # Modelo de Producto
│   │   ├── comparison.py                # Modelo de Comparación
│   │   ├── recommendation.py            # Modelo de Recomendación
│   │   └── validation.py                # Modelo de Validación
│   ├── 📁 ontology/                     # Archivos de ontología
│   │   ├── SmartCompareMarket.owl       # ⭐ ONTOLOGÍA PRINCIPAL (2900+ líneas)
│   │   └── owl_helpers.py               # Utilidades para OWL
│   ├── 📁 reasoning/                    # Capa de razonamiento
│   │   ├── inference_engine.py          # Motor de inferencias
│   │   ├── swrl_engine.py               # Motor de reglas SWRL
│   │   └── ontology_loader.py           # Cargador de ontología
│   ├── 📁 routers/                      # Endpoints de la API
│   │   ├── products.py                  # /api/v1/products
│   │   ├── compare.py                   # /api/v1/compare
│   │   ├── recommendations.py           # /api/v1/recommendations
│   │   ├── search.py                    # /api/v1/search
│   │   ├── swrl.py                      # /api/v1/swrl
│   │   └── validation.py                # /api/v1/validate
│   ├── 📁 services/                     # Lógica de negocio
│   │   ├── product_service.py           # Servicio de productos
│   │   ├── comparison_service.py        # ⭐ Motor de comparación (445 líneas)
│   │   ├── recommendation_service.py    # ⭐ Sistema de recomendaciones (277 líneas)
│   │   └── validation_service.py        # Validación de datos (152 líneas)
│   ├── 📁 sparql/                       # Consultas SPARQL
│   │   └── queries.py                   # Consultas predefinidas (267 líneas)
│   ├── 📁 utils/                        # Utilidades
│   │   └── helpers.py
│   ├── config.py                        # Configuración global
│   ├── dependencies.py                  # Dependencias de FastAPI
│   ├── main.py                          # ⭐ PUNTO DE ENTRADA (5843 bytes)
│   └── requirements.txt                 # Dependencias Python
│
├── 📁 frontend/                         # Aplicación React
│   ├── 📁 public/                       # Archivos estáticos
│   ├── 📁 src/
│   │   ├── 📁 components/               # Componentes reutilizables
│   │   │   ├── 📁 products/             # Componentes de productos
│   │   │   │   ├── ProductCard.tsx
│   │   │   │   └── ProductFilters.tsx
│   │   │   ├── 📁 comparison/           # Componentes de comparación
│   │   │   │   ├── ComparisonTable.tsx
│   │   │   │   └── WinnerCard.tsx
│   │   │   └── 📁 ui/                   # Shadcn components
│   │   ├── 📁 hooks/                    # Custom hooks
│   │   │   └── useProducts.ts
│   │   ├── 📁 pages/                    # Páginas principales
│   │   │   ├── HomePage.tsx             # Catálogo (6291 bytes)
│   │   │   ├── ComparePage.tsx          # Comparación (13424 bytes)
│   │   │   ├── RecommendationsPage.tsx  # Recomendaciones (6876 bytes)
│   │   │   └── ProductDetailPage.tsx    # Detalle (12177 bytes)
│   │   ├── 📁 services/                 # Servicios HTTP
│   │   │   └── api.ts
│   │   ├── App.tsx                      # Componente raíz
│   │   ├── main.tsx                     # Punto de entrada
│   │   └── index.css                    # Estilos globales
│   ├── package.json                     # Dependencias Node.js
│   └── vite.config.ts                   # Configuración Vite
│
├── README.md                            # Documentación principal
├── MANUAL_USUARIO.md                    # Manual de usuario
├── MANUAL_TECNICO.md                    # Este archivo
└── docker-compose.yml                   # Configuración Docker
```

> 📸 **Screenshot 4:** Captura la estructura de carpetas del proyecto en un explorador de archivos o terminal (`tree` command)

---

## 5. ONTOLOGÍA OWL 2

### 5.1 Ubicación y Características

| Propiedad | Valor |
|-----------|-------|
| **Archivo** | `backend/ontology/SmartCompareMarket.owl` |
| **Tamaño** | ~2,900 líneas |
| **Namespace** | `http://smartcompare.com/ontologia#` |
| **Formato** | RDF/XML |

### 5.2 Jerarquía de Clases

```
owl:Thing
└── Producto (raíz de productos)
    ├── Electronica
    │   ├── Smartphone
    │   ├── Tablet
    │   └── Computadora
    │       ├── Desktop
    │       └── Laptop
    │           └── LaptopGamer (⚡ inferida por SWRL)
    ├── Moda
    │   ├── Ropa
    │   └── Calzado
    └── Hogar
        ├── Muebles
        └── Electrodomesticos

└── Usuario
    ├── Cliente
    └── Vendedor

└── Reseña
    ├── Reseña_Positiva (⚡ inferida por SWRL)
    └── Reseña_Negativa (⚡ inferida por SWRL)
```

> 📸 **Screenshot 5:** Captura la jerarquía de clases en Protégé mostrando el árbol expandido

### 5.3 Propiedades de Datos (Data Properties)

| Propiedad | Dominio | Rango | Descripción |
|-----------|---------|-------|-------------|
| `tienePrecio` | Producto | xsd:float | Precio en USD |
| `tieneDescuento` | Producto | xsd:float | Porcentaje de descuento |
| `tieneRAM_GB` | Electronica | xsd:integer | RAM en GB |
| `tieneAlmacenamiento_GB` | Electronica | xsd:integer | Almacenamiento en GB |
| `tienePulgadas` | Electronica | xsd:float | Tamaño de pantalla |
| `resolucionPantalla` | Electronica | xsd:string | Resolución (ej: "1920x1080") |
| `bateriaCapacidad_mAh` | Electronica | xsd:integer | Capacidad de batería |
| `procesadorModelo` | Electronica | xsd:string | Modelo del procesador |
| `procesadorVelocidad_GHz` | Electronica | xsd:float | Velocidad del CPU |
| `numeroNucleosCPU` | Electronica | xsd:integer | Número de núcleos |
| `tarjetaGrafica` | Computadora | xsd:string | GPU |
| `garantiaMeses` | Producto | xsd:integer | Garantía en meses |
| `tieneCalificacion` | Producto | xsd:float | Calificación 0-5 |
| `pesoGramos` | Producto | xsd:float | Peso en gramos |
| `tieneSistemaOperativo` | Electronica | xsd:string | Sistema operativo |

> 📸 **Screenshot 6:** Captura las propiedades de datos en Protégé, tab "Data Properties"

### 5.4 Propiedades de Objeto (Object Properties)

| Propiedad | Característica | Descripción |
|-----------|---------------|-------------|
| `esCompatibleCon` | Symmetric | Productos compatibles entre sí |
| `incompatibleCon` | Symmetric | Productos incompatibles |
| `esEquivalenteTecnico` | Symmetric | Productos técnicamente equivalentes |
| `esMejorOpcionQue` | Transitive | Producto A es mejor opción que B |
| `tieneMejorRAMQue` | - | Comparación de RAM |
| `tieneMejorPantallaQue` | - | Comparación de pantalla |
| `tieneMejorAlmacenamientoQue` | - | Comparación de almacenamiento |
| `esVendidoPor` | - | Relación producto-vendedor |
| `tieneReseña` | - | Relación producto-reseña |
| `esSimilarA` | Symmetric | Productos similares |

> 📸 **Screenshot 7:** Captura las propiedades de objeto en Protégé, tab "Object Properties"

### 5.5 Individuos (Productos de Ejemplo)

La ontología incluye **60+ individuos** predefinidos:

**Laptops:**
- `Laptop_Dell_XPS` (RAM: 32GB, SSD: 1TB, Precio: $1599)
- `Laptop_MSI_Gaming` (RAM: 16GB, SSD: 512GB, Precio: $1299)
- `Laptop_HP_Pavilion` (RAM: 16GB, SSD: 512GB, Precio: $999)

**Smartphones:**
- `iPhone15_Barato` (RAM: 6GB, 128GB, Precio: $799)
- `Samsung_Galaxy_S24` (RAM: 8GB, 256GB, Precio: $899)
- `Pixel_8_Pro` (RAM: 12GB, 256GB, Precio: $999)

**Tablets:**
- `iPad_Pro_12` (RAM: 16GB, 512GB, Precio: $1099)
- `Samsung_Tab_S9` (RAM: 12GB, 256GB, Precio: $849)

> 📸 **Screenshot 8:** Captura los individuos en Protégé, tab "Individuals", mostrando varios productos

---

## 6. REGLAS SWRL

### 6.1 Ubicación en la Ontología

Las reglas SWRL se encuentran en las líneas **1964-2300** del archivo `SmartCompareMarket.owl`.

### 6.2 Reglas Implementadas

#### Regla 1: DetectarGamer

```swrl
Laptop(?l) ∧ tieneRAM_GB(?l, ?ram) ∧ greaterThanOrEqual(?ram, 16) 
  → LaptopGamer(?l)
```

**Explicación técnica:**
- **Antecedente:** Un individuo `?l` es de clase `Laptop` Y tiene propiedad `tieneRAM_GB` con valor `?ram` Y ese valor es ≥ 16
- **Consecuente:** El individuo `?l` se clasifica como miembro de la clase `LaptopGamer`
- **Efecto:** Subsunción automática por el razonador Pellet

> 📸 **Screenshot 9:** Captura la regla DetectarGamer en el tab SWRL de Protégé

#### Regla 2: EncontrarMejorPrecio

```swrl
Producto(?p1) ∧ Producto(?p2) ∧ tieneNombre(?p1, ?n) ∧ tieneNombre(?p2, ?n) 
  ∧ tienePrecio(?p1, ?pr1) ∧ tienePrecio(?p2, ?pr2) ∧ lessThan(?pr1, ?pr2)
  → esMejorOpcionQue(?p1, ?p2)
```

**Explicación técnica:**
- Dos productos con el mismo nombre pero diferente precio
- El de menor precio se marca como "mejor opción que" el otro
- Usa la propiedad de objeto `esMejorOpcionQue`

#### Regla 3: ClasificarPositivas

```swrl
Reseña(?r) ∧ tieneCalificacion(?r, ?cal) ∧ greaterThanOrEqual(?cal, 4)
  → Reseña_Positiva(?r)
```

**Explicación técnica:**
- Reseñas con calificación ≥ 4 se clasifican como positivas

#### Regla 4: ClasificarNegativas

```swrl
Reseña(?r) ∧ tieneCalificacion(?r, ?cal) ∧ lessThanOrEqual(?cal, 2)
  → Reseña_Negativa(?r)
```

**Explicación técnica:**
- Reseñas con calificación ≤ 2 se clasifican como negativas

### 6.3 Ejecución de Reglas

El razonador Pellet se ejecuta al iniciar el backend:

```python
# backend/reasoning/ontology_loader.py
from owlready2 import sync_reasoner_pellet

def load_ontology():
    onto = get_ontology("SmartCompareMarket.owl").load()
    
    # Ejecutar razonador Pellet con soporte SWRL
    with onto:
        sync_reasoner_pellet(infer_property_values=True, 
                             infer_data_property_values=True)
    
    return onto
```

> 📸 **Screenshot 10:** Captura el log del backend mostrando "[OK] Razonador Pellet ejecutado exitosamente"

---

## 7. API REST - ENDPOINTS

### 7.1 Base URL

```
http://localhost:5000/api/v1
```

### 7.2 Endpoints de Productos

#### GET /products
Obtener todos los productos.

```bash
curl http://localhost:5000/api/v1/products
```

**Respuesta:**
```json
{
  "products": [
    {
      "id": "Laptop_Dell_XPS",
      "name": "Dell XPS 15",
      "category": "Laptop",
      "types": ["Producto", "Electronica", "Computadora", "Laptop", "LaptopGamer"],
      "price": 1599.99,
      "discount": 10,
      "ram_gb": 32,
      "storage_gb": 1024,
      "screen_inches": 15.6,
      "battery_mah": 86000,
      "rating": 4.7,
      "warranty_months": 24
    }
  ],
  "count": 60
}
```

> 📸 **Screenshot 11:** Captura la respuesta JSON de `/api/v1/products` en el navegador o Postman

#### GET /products/{product_id}
Obtener un producto específico.

```bash
curl http://localhost:5000/api/v1/products/Laptop_Dell_XPS
```

#### GET /products/{product_id}/relationships
Obtener relaciones de un producto (compatible, incompatible, similar).

```bash
curl http://localhost:5000/api/v1/products/iPhone15_Barato/relationships
```

**Respuesta:**
```json
{
  "product_id": "iPhone15_Barato",
  "compatible": ["Cargador_USB_C", "Funda_iPhone15"],
  "incompatible": ["Cargador_MicroUSB"],
  "similar": ["iPhone15_Pro", "Samsung_Galaxy_S24"],
  "better_than": ["iPhone14_Base"]
}
```

### 7.3 Endpoint de Comparación

#### POST /compare
Comparar múltiples productos.

```bash
curl -X POST http://localhost:5000/api/v1/compare \
  -H "Content-Type: application/json" \
  -d '{"products": ["Laptop_Dell_XPS", "Laptop_MSI_Gaming"]}'
```

**Request Body:**
```json
{
  "products": ["Laptop_Dell_XPS", "Laptop_MSI_Gaming", "Laptop_HP_Pavilion"]
}
```

**Respuesta:**
```json
{
  "winner": "Laptop_Dell_XPS",
  "winner_score": 87.5,
  "comparison_table": {
    "Precio": {"Laptop_Dell_XPS": 1599, "Laptop_MSI_Gaming": 1299},
    "RAM (GB)": {"Laptop_Dell_XPS": 32, "Laptop_MSI_Gaming": 16},
    "Almacenamiento (GB)": {"Laptop_Dell_XPS": 1024, "Laptop_MSI_Gaming": 512},
    "Calificación": {"Laptop_Dell_XPS": 4.7, "Laptop_MSI_Gaming": 4.5}
  },
  "scores": {
    "Laptop_Dell_XPS": 87.5,
    "Laptop_MSI_Gaming": 72.3
  },
  "swrl_inferences": [
    {
      "type": "esMejorOpcionQue",
      "subject": "Laptop_Dell_XPS",
      "object": "Laptop_MSI_Gaming",
      "description": "Es mejor opción por mejor relación calidad-precio"
    }
  ],
  "reason": "Laptop_Dell_XPS gana con 87.5 puntos por tener mejor RAM, almacenamiento y calificación"
}
```

> 📸 **Screenshot 12:** Captura la respuesta de comparación mostrando el ganador y la tabla

### 7.4 Endpoint de Recomendaciones

#### POST /recommendations
Obtener recomendaciones personalizadas.

```bash
curl -X POST http://localhost:5000/api/v1/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 1500,
    "preferred_category": "Laptop",
    "min_ram": 16,
    "min_storage": 512,
    "min_rating": 4.0
  }'
```

**Request Body:**
```json
{
  "budget": 1500,
  "min_budget": 500,
  "preferred_category": "Laptop",
  "min_ram": 16,
  "min_storage": 512,
  "min_rating": 4.0
}
```

**Respuesta:**
```json
{
  "recommendations": [
    {
      "product_id": "Laptop_MSI_Gaming",
      "name": "MSI GF65 Thin",
      "score": 92.5,
      "match_percentage": 95,
      "reason": "Laptop Gamer detectado (SWRL) + Excelente relación calidad-precio",
      "price": 1299,
      "swrl_bonus": 10
    }
  ],
  "total_matches": 5,
  "filters_applied": {
    "budget": 1500,
    "category": "Laptop",
    "min_ram": 16
  }
}
```

> 📸 **Screenshot 13:** Captura la respuesta de recomendaciones con scores y razones

### 7.5 Endpoint de Búsqueda SPARQL

#### GET /search
Búsqueda semántica con filtros.

```bash
curl "http://localhost:5000/api/v1/search?category=Laptop&min_price=1000&max_price=1500&min_ram=16"
```

**Parámetros:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `text` | string | Búsqueda de texto libre |
| `category` | string | Categoría (Laptop, Smartphone, Tablet) |
| `min_price` | float | Precio mínimo |
| `max_price` | float | Precio máximo |
| `min_ram` | integer | RAM mínima en GB |

**Consulta SPARQL generada internamente:**
```sparql
PREFIX ns: <http://smartcompare.com/ontologia#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?product ?name ?price ?ram WHERE {
  ?product rdf:type ns:Laptop .
  ?product ns:tienePrecio ?price .
  ?product ns:tieneRAM_GB ?ram .
  FILTER (?price >= 1000 && ?price <= 1500)
  FILTER (?ram >= 16)
}
```

> 📸 **Screenshot 14:** Captura la respuesta de búsqueda filtrada

### 7.6 Endpoints SWRL

#### GET /swrl/gaming-laptops
Obtener laptops clasificadas como "gamer" por la regla SWRL.

```bash
curl http://localhost:5000/api/v1/swrl/gaming-laptops
```

**Respuesta:**
```json
{
  "rule": "DetectarGamer",
  "description": "Laptops con RAM >= 16GB clasificadas como LaptopGamer",
  "results": [
    {"id": "Laptop_Dell_XPS", "ram": 32, "classified_as": "LaptopGamer"},
    {"id": "Laptop_MSI_Gaming", "ram": 16, "classified_as": "LaptopGamer"},
    {"id": "Laptop_HP_Pavilion", "ram": 16, "classified_as": "LaptopGamer"}
  ],
  "count": 3
}
```

> 📸 **Screenshot 15:** Captura la respuesta de gaming-laptops mostrando productos clasificados automáticamente

#### GET /swrl/best-price
Obtener relaciones "esMejorOpcionQue" inferidas.

```bash
curl http://localhost:5000/api/v1/swrl/best-price
```

### 7.7 Endpoint de Validación

#### GET /validate/{product_id}
Validar un producto específico.

```bash
curl http://localhost:5000/api/v1/validate/Laptop_Dell_XPS
```

**Respuesta (producto válido):**
```json
{
  "valid": true,
  "product_id": "Laptop_Dell_XPS",
  "errors": [],
  "warnings": [],
  "total_issues": 0
}
```

**Respuesta (producto con errores):**
```json
{
  "valid": false,
  "product_id": "ProductoInvalido",
  "errors": [
    "Precio negativo detectado: -500"
  ],
  "warnings": [
    "RAM muy alta (>128GB): 256GB"
  ],
  "total_issues": 2
}
```

#### GET /validate/all
Validar todos los productos de la ontología.

```bash
curl http://localhost:5000/api/v1/validate/all
```

**Respuesta:**
```json
{
  "summary": {
    "total_products": 60,
    "valid": 58,
    "with_errors": 1,
    "with_warnings": 3
  },
  "details": [...]
}
```

> 📸 **Screenshot 16:** Captura la respuesta de validación masiva

### 7.8 Documentación Interactiva (Swagger)

FastAPI genera documentación automática accesible en:

| URL | Descripción |
|-----|-------------|
| http://localhost:5000/docs | Swagger UI (interactiva) |
| http://localhost:5000/redoc | ReDoc (documentación) |

> 📸 **Screenshot 17:** Captura la página de Swagger UI en /docs mostrando todos los endpoints

---

## 8. SERVICIOS DEL BACKEND

### 8.1 ComparisonService

**Ubicación:** `backend/services/comparison_service.py`

**Responsabilidad:** Motor de comparación inteligente con scoring multi-factor.

#### Algoritmo de Scoring

```python
WEIGHTS = {
    "battery": 0.20,      # Mayor es mejor
    "rating": 0.18,       # Mayor es mejor
    "price": 0.14,        # MENOR es mejor (invertido)
    "resolution": 0.10,   # Mayor es mejor
    "ram": 0.10,          # Mayor es mejor
    "storage": 0.10,      # Mayor es mejor
    "warranty": 0.07,     # Mayor es mejor
    "screen": 0.06,       # Mayor es mejor
    "weight": 0.05        # MENOR es mejor (invertido)
}

# Valores de referencia para normalización
REFERENCE_VALUES = {
    "battery": 10000,     # 10000 mAh = 100 puntos
    "rating": 5.0,        # 5 estrellas = 100 puntos
    "price": 3000,        # $3000 = 0 puntos (precio máximo)
    "ram": 64,            # 64GB = 100 puntos
    "storage": 2048,      # 2TB = 100 puntos
    ...
}
```

#### Cálculo del Score

```python
def _calculate_score(self, product: dict) -> float:
    score = 0
    
    # Para cada factor
    for factor, weight in WEIGHTS.items():
        value = product.get(factor, 0)
        reference = REFERENCE_VALUES[factor]
        
        if factor in ["price", "weight"]:  # Menor es mejor
            normalized = max(0, 100 - (value / reference * 100))
        else:  # Mayor es mejor
            normalized = min(100, value / reference * 100)
        
        score += normalized * weight
    
    # Bonus por reglas SWRL
    if self._has_swrl_bonus(product):
        score += 2  # Bonus por cada relación "esMejorOpcionQue"
    
    return round(score, 2)
```

> 📸 **Screenshot 18:** Captura el código de `_calculate_score` en el archivo comparison_service.py

### 8.2 RecommendationService

**Ubicación:** `backend/services/recommendation_service.py`

**Responsabilidad:** Sistema de recomendaciones personalizadas.

#### Sistema de Scoring para Recomendaciones

```python
def _calculate_recommendation_score(self, product: dict, preferences: dict) -> float:
    score = 0
    
    # Factor 1: Presupuesto (30 puntos)
    if product["price"] <= preferences["budget"]:
        # Más puntos si está cerca del presupuesto (aprovecha bien el dinero)
        budget_usage = product["price"] / preferences["budget"]
        score += 30 * budget_usage
    
    # Factor 2: Calificación (25 puntos)
    score += product["rating"] * 5  # 5 puntos por estrella
    
    # Factor 3: RAM (15 puntos)
    if product["ram"] >= preferences.get("min_ram", 0):
        score += 15
    
    # Factor 4: Almacenamiento (10 puntos)
    if product["storage"] >= preferences.get("min_storage", 0):
        score += 10
    
    # Bonus SWRL
    if "LaptopGamer" in product.get("types", []):
        score += 10  # Bonus por ser Laptop Gamer
    
    # Bonus por descuento
    score += product.get("discount", 0) * 0.5
    
    return score
```

### 8.3 ValidationService

**Ubicación:** `backend/services/validation_service.py`

**Responsabilidad:** Validación de consistencia de especificaciones.

#### Reglas de Validación

```python
VALIDATION_RULES = {
    "errors": [
        ("price < 0", "Precio negativo"),
        ("ram < 0 OR ram > 512", "RAM inválida"),
        ("storage < 0 OR storage > 10240", "Almacenamiento inválido"),
        ("rating < 0 OR rating > 5", "Calificación fuera de rango"),
        ("category == 'Smartphone' AND ram > 32", "Smartphone con RAM imposible"),
    ],
    "warnings": [
        ("price > 100000", "Precio excesivamente alto"),
        ("ram > 128", "RAM inusualmente alta"),
        ("storage > 512 AND category == 'Smartphone'", "Almacenamiento alto para smartphone"),
    ]
}
```

### 8.4 SPARQLQueries

**Ubicación:** `backend/sparql/queries.py`

**Responsabilidad:** Consultas SPARQL sobre la ontología.

#### Ejemplo de Consulta

```python
def search_products(text=None, category=None, min_price=None, max_price=None, min_ram=None):
    query = """
    PREFIX ns: <http://smartcompare.com/ontologia#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?product ?name ?price ?ram ?storage WHERE {
        ?product rdf:type/rdfs:subClassOf* ns:Producto .
        OPTIONAL { ?product ns:tieneNombre ?name }
        OPTIONAL { ?product ns:tienePrecio ?price }
        OPTIONAL { ?product ns:tieneRAM_GB ?ram }
        OPTIONAL { ?product ns:tieneAlmacenamiento_GB ?storage }
        
        %FILTERS%
    }
    """
    
    filters = []
    if min_price:
        filters.append(f"FILTER (?price >= {min_price})")
    if max_price:
        filters.append(f"FILTER (?price <= {max_price})")
    if min_ram:
        filters.append(f"FILTER (?ram >= {min_ram})")
    
    query = query.replace("%FILTERS%", "\n".join(filters))
    return execute_sparql(query)
```

---

## 9. INSTALACIÓN PARA DESARROLLADORES

### 9.1 Prerrequisitos

| Software | Versión | Comando de verificación |
|----------|---------|------------------------|
| Python | 3.11+ | `python --version` |
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| Java JDK | 11+ | `java -version` |
| Git | Cualquiera | `git --version` |

> 📸 **Screenshot 19:** Captura la terminal mostrando todos los comandos de verificación con sus versiones

### 9.2 Clonar el Repositorio

```bash
git clone https://github.com/AlvaroMachaca0503/Web_Semantica.git
cd Web_Semantica
```

### 9.3 Configuración del Backend

```bash
# 1. Navegar al backend
cd backend

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Verificar instalación
python -c "import owlready2; print('Owlready2 OK')"
python -c "import fastapi; print('FastAPI OK')"
```

> 📸 **Screenshot 20:** Captura la terminal con el entorno virtual activado y las verificaciones exitosas

### 9.4 Configuración del Frontend

```bash
# 1. Navegar al frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Verificar instalación
npm list react
```

---

## 10. EJECUCIÓN Y DESPLIEGUE

### 10.1 Modo Desarrollo

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
python main.py
```

**Logs esperados:**
```
[INFO] Cargando ontología SmartCompareMarket.owl...
[OK] Ontología cargada: 60 productos encontrados
[INFO] Ejecutando razonador Pellet...
[OK] Razonador Pellet ejecutado exitosamente
[OK] Reglas SWRL aplicadas: DetectarGamer, EncontrarMejorPrecio...
[INFO] Iniciando servidor FastAPI...
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
```

> 📸 **Screenshot 21:** Captura la terminal del backend con todos los logs de inicio exitosos

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Logs esperados:**
```
  VITE v5.4.19  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

> 📸 **Screenshot 22:** Captura la terminal del frontend con Vite ejecutándose

### 10.2 Modo Producción

**Backend:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 5000 --workers 4
```

**Frontend:**
```bash
cd frontend
npm run build
npm run preview
```

### 10.3 Variables de Entorno

Crear archivo `.env` en `backend/`:

```env
# Configuración del servidor
HOST=0.0.0.0
PORT=5000
DEBUG=False

# Configuración de ontología
ONTOLOGY_PATH=ontology/SmartCompareMarket.owl

# Configuración de CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 11. TESTING

### 11.1 Tests del Backend

```bash
cd backend

# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=.

# Tests específicos
pytest tests/test_comparison.py -v
```

### 11.2 Tests de la API

```bash
# Test básico de salud
curl http://localhost:5000/api/v1/products | head -c 200

# Test de comparación
curl -X POST http://localhost:5000/api/v1/compare \
  -H "Content-Type: application/json" \
  -d '{"products": ["Laptop_Dell_XPS", "Laptop_MSI_Gaming"]}'
```

### 11.3 Tests Manuales Recomendados

| Test | Comando | Resultado Esperado |
|------|---------|-------------------|
| Listar productos | `GET /api/v1/products` | JSON con 60+ productos |
| Gaming laptops SWRL | `GET /api/v1/swrl/gaming-laptops` | 3+ laptops con RAM ≥ 16GB |
| Comparación | `POST /api/v1/compare` | Ganador con score |
| Validación masiva | `GET /api/v1/validate/all` | Resumen de validación |

> 📸 **Screenshot 23:** Captura los resultados de pytest mostrando todos los tests pasando

---

## 12. MANTENIMIENTO Y EXTENSIBILIDAD

### 12.1 Agregar Nuevos Productos

1. Abrir `backend/ontology/SmartCompareMarket.owl` en **Protégé**
2. Tab "Individuals" → Click "+" para agregar individuo
3. Seleccionar clase (ej: `Laptop`)
4. Agregar propiedades de datos:
   - `tienePrecio`
   - `tieneRAM_GB`
   - `tieneAlmacenamiento_GB`
   - etc.
5. Guardar archivo
6. Reiniciar backend

> 📸 **Screenshot 24:** Captura Protégé mostrando cómo agregar un nuevo individuo

### 12.2 Agregar Nuevas Reglas SWRL

1. En Protégé → Tab "SWRL"
2. Click "+" para nueva regla
3. Escribir regla en formato SWRL
4. Guardar
5. Reiniciar backend

**Ejemplo de nueva regla:**
```swrl
Smartphone(?s) ∧ tieneRAM_GB(?s, ?ram) ∧ greaterThan(?ram, 8)
  → SmartphoneGama alta(?s)
```

### 12.3 Agregar Nuevos Endpoints

1. Crear archivo en `backend/routers/nuevo_router.py`:

```python
from fastapi import APIRouter, Depends
from dependencies import get_ontology

router = APIRouter(prefix="/api/v1/nuevo", tags=["nuevo"])

@router.get("/")
async def mi_endpoint(onto=Depends(get_ontology)):
    # Lógica aquí
    return {"mensaje": "Nuevo endpoint"}
```

2. Registrar en `backend/main.py`:

```python
from routers import nuevo_router
app.include_router(nuevo_router.router)
```

### 12.4 Modificar Pesos de Comparación

Editar archivo `backend/data/comparison_weights.json`:

```json
{
  "battery": 0.20,
  "rating": 0.18,
  "price": 0.14,
  "resolution": 0.10,
  "ram": 0.10,
  "storage": 0.10,
  "warranty": 0.07,
  "screen": 0.06,
  "weight": 0.05
}
```

---

## 13. ANEXOS TÉCNICOS

### 13.1 Diagrama de Clases del Backend

```
┌─────────────────────────────────────────────────────────────────┐
│                         FastAPI App                              │
│  main.py                                                        │
└───────────────────────────────┬─────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│   Routers     │       │   Services    │       │   Reasoning   │
├───────────────┤       ├───────────────┤       ├───────────────┤
│ products.py   │       │ product_svc   │       │ inference_eng │
│ compare.py    │──────▶│ comparison_svc│◀─────▶│ swrl_engine   │
│ recommend.py  │       │ recommend_svc │       │ onto_loader   │
│ search.py     │       │ validation_svc│       └───────┬───────┘
│ swrl.py       │       │ sparql_queries│               │
│ validation.py │       └───────────────┘               │
└───────────────┘                                       │
                                                        ▼
                                             ┌───────────────────┐
                                             │   SmartCompare    │
                                             │   Market.owl      │
                                             │                   │
                                             │ • Classes (48)    │
                                             │ • Properties (30+)│
                                             │ • Individuals (60)│
                                             │ • SWRL Rules (4)  │
                                             └───────────────────┘
```

### 13.2 Modelos Pydantic

**Product Model:**
```python
class Product(BaseModel):
    id: str
    name: str
    category: str
    types: List[str]
    price: float
    discount: Optional[float] = 0
    ram_gb: Optional[int] = None
    storage_gb: Optional[int] = None
    screen_inches: Optional[float] = None
    battery_mah: Optional[int] = None
    rating: Optional[float] = None
    warranty_months: Optional[int] = None
    processor: Optional[str] = None
    weight_grams: Optional[float] = None
```

**ComparisonRequest Model:**
```python
class ComparisonRequest(BaseModel):
    products: List[str]  # Lista de IDs de productos
    
    @field_validator('products')
    def validate_products(cls, v):
        if len(v) < 2:
            raise ValueError('Se requieren al menos 2 productos')
        if len(v) > 5:
            raise ValueError('Máximo 5 productos')
        return v
```

**RecommendationRequest Model:**
```python
class RecommendationRequest(BaseModel):
    budget: float
    min_budget: Optional[float] = 0
    preferred_category: Optional[str] = None
    min_ram: Optional[int] = None
    min_storage: Optional[int] = None
    min_rating: Optional[float] = None
```

### 13.3 Códigos de Error HTTP

| Código | Significado | Ejemplo |
|--------|-------------|---------|
| 200 | Éxito | Respuesta normal |
| 400 | Bad Request | Parámetros inválidos |
| 404 | Not Found | Producto no existe |
| 422 | Validation Error | JSON mal formado |
| 500 | Internal Error | Error del razonador |

### 13.4 Puertos Utilizados

| Servicio | Puerto | URL |
|----------|--------|-----|
| Backend API | 5000 | http://localhost:5000 |
| Frontend Dev | 5173 | http://localhost:5173 |
| Swagger Docs | 5000 | http://localhost:5000/docs |

---

## 📊 RESUMEN DE ARCHIVOS IMPORTANTES

| Archivo | Líneas | Descripción |
|---------|--------|-------------|
| `SmartCompareMarket.owl` | 2,900+ | Ontología principal |
| `comparison_service.py` | 445 | Motor de comparación |
| `recommendation_service.py` | 277 | Sistema de recomendaciones |
| `queries.py` | 267 | Consultas SPARQL |
| `validation_service.py` | 152 | Validación de datos |
| `main.py` | ~200 | Punto de entrada |
| `ComparePage.tsx` | 500+ | Página de comparación |

---

## 📝 HISTORIAL DE VERSIONES

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | Diciembre 2024 | Versión inicial completa |

---

**Autores:** Álvaro y Jony  
**Proyecto:** Nivel 2 - Web Semántica  
**Contacto:** Repositorio GitHub

> 📸 **Screenshot 25:** Captura la página del proyecto en GitHub mostrando la estructura de archivos

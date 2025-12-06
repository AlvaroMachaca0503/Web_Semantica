# 📘 MANUAL DE USUARIO - SmartCompareMarket

## Marketplace Semántico con Comparación Inteligente

**Versión:** 1.0  
**Autores:** Álvaro y Jony  
**Proyecto:** Nivel 2 - Web Semántica  
**Última actualización:** Diciembre 2024

---

## 📑 TABLA DE CONTENIDOS

1. [Introducción](#1-introducción)
2. [Requisitos del Sistema](#2-requisitos-del-sistema)
3. [Instalación Paso a Paso](#3-instalación-paso-a-paso)
4. [Ejecución del Proyecto](#4-ejecución-del-proyecto)
5. [Guía de Uso del Sistema](#5-guía-de-uso-del-sistema)
6. [Funcionalidades Principales](#6-funcionalidades-principales)
7. [Solución de Problemas Frecuentes](#7-solución-de-problemas-frecuentes)
8. [Preguntas Frecuentes (FAQ)](#8-preguntas-frecuentes-faq)

---

## 1. INTRODUCCIÓN

### ¿Qué es SmartCompareMarket?

**SmartCompareMarket** es una plataforma web inteligente para comparar y recibir recomendaciones de productos electrónicos (Laptops, Smartphones, Tablets). A diferencia de comparadores tradicionales, este sistema utiliza **Inteligencia Artificial Semántica** para:

- ✅ **Entender** las características de los productos
- ✅ **Clasificar automáticamente** productos (ej: detectar si una laptop es "Gamer")
- ✅ **Comparar inteligentemente** productos usando reglas lógicas
- ✅ **Recomendar** productos personalizados según tus preferencias
- ✅ **Validar** que las especificaciones de productos sean consistentes

### ¿Para quién es este manual?

Este manual está diseñado para **usuarios finales** que desean:
- Instalar y ejecutar el sistema en su computadora
- Usar la plataforma para comparar productos
- Obtener recomendaciones personalizadas

> 💡 **Nota:** No necesitas conocimientos técnicos avanzados. Las instrucciones están escritas para que cualquier persona pueda seguirlas.

---

## 2. REQUISITOS DEL SISTEMA

### 2.1 Requisitos de Hardware

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| RAM | 4 GB | 8 GB |
| Espacio en disco | 2 GB | 5 GB |
| Procesador | Dual Core | Quad Core |
| Conexión Internet | Requerida (para instalación) | Requerida |

### 2.2 Requisitos de Software

Antes de comenzar, debes tener instalado:

| Software | Versión Mínima | Cómo verificar |
|----------|----------------|----------------|
| **Python** | 3.11 o superior | `python --version` |
| **Node.js** | 18.0 o superior | `node --version` |
| **npm** | 9.0 o superior | `npm --version` |
| **Git** | Cualquiera | `git --version` |
| **Java JDK** | 11 o superior | `java -version` |

> ⚠️ **IMPORTANTE:** Java es necesario para el razonador semántico Pellet.

### 2.3 Navegadores Compatibles

| Navegador | Versión |
|-----------|---------|
| Google Chrome | 90+ ✅ (Recomendado) |
| Mozilla Firefox | 88+ ✅ |
| Microsoft Edge | 90+ ✅ |
| Safari | 14+ ✅ |

---

## 3. INSTALACIÓN PASO A PASO

### PASO 1: Verificar que tienes los programas necesarios

Abre una **terminal/consola de comandos** y ejecuta estos comandos uno por uno:

```bash
python --version
```
> 📸 **Screenshot 1:** Captura la terminal mostrando "Python 3.11.x" o superior

```bash
node --version
```
> 📸 **Screenshot 2:** Captura la terminal mostrando "v18.x.x" o superior

```bash
npm --version
```
> 📸 **Screenshot 3:** Captura la terminal mostrando "9.x.x" o superior

```bash
java -version
```
> 📸 **Screenshot 4:** Captura la terminal mostrando "openjdk version 11.x.x" o similar

---

### PASO 2: Descargar el proyecto

**Opción A: Usando Git (Recomendado)**

```bash
git clone https://github.com/AlvaroMachaca0503/Web_Semantica.git
cd Web_Semantica
```

**Opción B: Descarga manual**

1. Ve a la página del repositorio en GitHub
2. Haz clic en el botón verde "**Code**"
3. Selecciona "**Download ZIP**"
4. Extrae el archivo ZIP en una carpeta de tu elección
5. Abre una terminal en esa carpeta

> 📸 **Screenshot 5:** Captura la carpeta del proyecto abierta en el explorador de archivos, mostrando las subcarpetas `backend` y `frontend`

---

### PASO 3: Instalar dependencias del Backend

1. Abre una **terminal** y navega a la carpeta del backend:

```bash
cd backend
```

2. Crea un entorno virtual de Python (recomendado):

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> 📸 **Screenshot 6:** Captura la terminal mostrando `(venv)` al inicio de la línea de comandos, indicando que el entorno virtual está activo

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

> 📸 **Screenshot 7:** Captura la terminal mostrando el progreso de instalación de paquetes (debe verse "Successfully installed fastapi owlready2..." al final)

---

### PASO 4: Instalar dependencias del Frontend

1. Abre **otra terminal** (mantén la del backend abierta)

2. Navega a la carpeta del frontend:

```bash
cd frontend
```

3. Instala las dependencias:

```bash
npm install
```

> ⏱️ **Nota:** Este proceso puede tardar 2-5 minutos dependiendo de tu conexión a internet.

> 📸 **Screenshot 8:** Captura la terminal mostrando "added XXX packages" al finalizar la instalación

---

## 4. EJECUCIÓN DEL PROYECTO

### 4.1 Iniciar el Backend (Servidor API)

1. Asegúrate de estar en la carpeta `backend` con el entorno virtual activado

2. Ejecuta:

```bash
python main.py
```

3. **Espera** hasta ver estos mensajes de éxito:

```
[OK] Ontología cargada: 60+ productos
[OK] Razonador Pellet ejecutado exitosamente
[OK] Reglas SWRL aplicadas
INFO:     Uvicorn running on http://0.0.0.0:5000
```

> 📸 **Screenshot 9:** Captura la terminal mostrando todos los mensajes de éxito listados arriba, especialmente el mensaje "Uvicorn running on http://0.0.0.0:5000"

> ⚠️ **¡NO CIERRES ESTA TERMINAL!** El servidor debe permanecer ejecutándose.

---

### 4.2 Iniciar el Frontend (Interfaz Web)

1. En la **segunda terminal**, asegúrate de estar en la carpeta `frontend`

2. Ejecuta:

```bash
npm run dev
```

3. Espera hasta ver:

```
  VITE v5.x.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

> 📸 **Screenshot 10:** Captura la terminal mostrando el mensaje de Vite con la URL local http://localhost:5173/

---

### 4.3 Abrir la Aplicación

1. Abre tu **navegador web** (Chrome recomendado)

2. Escribe en la barra de direcciones:

```
http://localhost:5173
```

3. Presiona **Enter**

> 📸 **Screenshot 11:** Captura la página principal del sistema mostrando el catálogo de productos con tarjetas de laptops, smartphones y tablets

---

## 5. GUÍA DE USO DEL SISTEMA

### 5.1 Navegación Principal

La aplicación tiene **tres secciones principales** accesibles desde el menú superior:

| Sección | Icono | Descripción |
|---------|-------|-------------|
| **Inicio** | 🏠 | Catálogo completo de productos |
| **Comparar** | ⚖️ | Comparación inteligente de productos |
| **Recomendaciones** | 💡 | Recomendaciones personalizadas |

> 📸 **Screenshot 12:** Captura el menú de navegación superior mostrando las tres opciones: Inicio, Comparar y Recomendaciones

---

### 5.2 Explorar el Catálogo de Productos

1. En la **página de Inicio**, verás tarjetas de productos

2. Cada tarjeta muestra:
   - 📷 Imagen del producto
   - 🏷️ Nombre y marca
   - 💵 Precio (con descuento si aplica)
   - ⭐ Calificación de usuarios
   - 🖥️ Especificaciones técnicas (RAM, Almacenamiento, etc.)
   - 🎮 Badges especiales (ej: "Laptop Gamer")

> 📸 **Screenshot 13:** Captura una tarjeta de producto individual mostrando todos los elementos descritos: nombre, precio, especificaciones, badge de "Laptop Gamer" si tiene RAM >= 16GB

#### Usando los Filtros de Búsqueda

1. Usa la **barra de búsqueda** en la parte superior para buscar por nombre
2. Selecciona una **categoría** (Laptops, Smartphones, Tablets)
3. Ajusta el **rango de precio** usando los sliders
4. Filtra por **RAM mínima** si lo necesitas

> 📸 **Screenshot 14:** Captura el panel de filtros mostrando: campo de búsqueda, selector de categoría, sliders de precio y filtro de RAM

---

### 5.3 Comparar Productos

Esta es la funcionalidad más poderosa del sistema.

#### Paso 1: Seleccionar productos para comparar

1. En el catálogo, haz clic en el botón **"Seleccionar"** en las tarjetas de productos que quieres comparar

2. Puedes seleccionar entre **2 y 5 productos**

3. Verás una **barra flotante** en la parte inferior indicando cuántos productos has seleccionado

> 📸 **Screenshot 15:** Captura mostrando 3 tarjetas de productos con el botón "Seleccionar" visible, y una de ellas con un check indicando que está seleccionada

> 📸 **Screenshot 16:** Captura la barra flotante inferior que dice "3 productos seleccionados - Comparar"

#### Paso 2: Ir a la página de comparación

1. Haz clic en el botón **"Comparar"** de la barra flotante

2. Serás redirigido a la página de comparación

> 📸 **Screenshot 17:** Captura la página de comparación completa mostrando la tabla comparativa con productos lado a lado

#### Paso 3: Analizar los resultados

La página de comparación muestra:

**A. Ganador Global (parte superior)**
- El sistema determina automáticamente el **mejor producto**
- Muestra el **score numérico** (0-100 puntos)
- Explica la **razón** de por qué ganó

> 📸 **Screenshot 18:** Captura la sección del "Ganador" mostrando el nombre del producto ganador, su score y la razón de victoria

**B. Tabla Comparativa (centro)**
- Cada columna es un producto
- Cada fila es una característica (Precio, RAM, Batería, etc.)
- Los valores **en verde** son los mejores de cada fila
- Los valores **en amarillo** indican empate

> 📸 **Screenshot 19:** Captura la tabla comparativa mostrando varios productos en columnas y características en filas, con celdas resaltadas en verde para los mejores valores

**C. Inferencias SWRL (parte inferior)**
- Muestra las **reglas inteligentes** que el sistema aplicó
- Ejemplos:
  - "🎮 LaptopGamer detectado" (RAM ≥ 16GB)
  - "💰 Es mejor opción que ProductoX" (mismo rendimiento, menor precio)
  - "🔋 Tiene mejor batería que ProductoY"

> 📸 **Screenshot 20:** Captura la sección de "Reglas SWRL Aplicadas" mostrando al menos 2-3 inferencias con sus iconos

---

### 5.4 Obtener Recomendaciones Personalizadas

#### Paso 1: Ir a Recomendaciones

1. Haz clic en **"Recomendaciones"** en el menú superior

#### Paso 2: Configurar tus preferencias

En el **panel izquierdo**, ajusta:

| Preferencia | Descripción | Ejemplo |
|-------------|-------------|---------|
| 💵 **Presupuesto máximo** | Cuánto puedes gastar | $1500 |
| 📁 **Categoría preferida** | Tipo de producto | Laptop |
| 🧠 **RAM mínima** | Memoria RAM mínima | 16 GB |
| 💾 **Almacenamiento mínimo** | Disco duro mínimo | 512 GB |
| ⭐ **Calificación mínima** | Puntuación de usuarios | 4.0 |

> 📸 **Screenshot 21:** Captura el panel de preferencias mostrando todos los sliders y selectores configurados con valores de ejemplo

#### Paso 3: Ver las recomendaciones

El **panel derecho** mostrará:

1. Lista de productos ordenados por **relevancia**
2. Para cada producto:
   - **Score de match** (0-100%)
   - **Razón** de la recomendación
   - Especificaciones principales

> 📸 **Screenshot 22:** Captura la lista de recomendaciones mostrando 3-4 productos con sus scores y razones (ej: "Laptop Gamer detectada", "Excelente relación calidad-precio")

---

## 6. FUNCIONALIDADES PRINCIPALES

### 6.1 Sistema de Comparación Inteligente

El motor de comparación evalúa productos usando **9 factores ponderados**:

| Factor | Peso | Criterio |
|--------|------|----------|
| 🔋 Batería | 20% | Mayor es mejor |
| ⭐ Calificación | 18% | Mayor es mejor |
| 💵 Precio | 14% | **Menor es mejor** |
| 📺 Resolución | 10% | Mayor es mejor |
| 🧠 RAM | 10% | Mayor es mejor |
| 💾 Almacenamiento | 10% | Mayor es mejor |
| 🛡️ Garantía | 7% | Mayor es mejor |
| 📐 Pantalla | 6% | Mayor es mejor |
| ⚖️ Peso | 5% | **Menor es mejor** |

**Bonus por reglas SWRL:**
- +2 puntos si el producto "es mejor opción que" otro
- +10 puntos si es detectado como "Laptop Gamer"

---

### 6.2 Clasificación Automática (SWRL)

El sistema clasifica productos automáticamente usando reglas inteligentes:

| Regla | Condición | Clasificación |
|-------|-----------|---------------|
| **DetectarGamer** | Laptop con RAM ≥ 16GB | → LaptopGamer 🎮 |
| **EncontrarMejorPrecio** | Mismo producto, menor precio | → esMejorOpcionQue |
| **ClasificarPositivas** | Reseña con calificación ≥ 4 | → Reseña_Positiva |
| **ClasificarNegativas** | Reseña con calificación ≤ 2 | → Reseña_Negativa |

> 📸 **Screenshot 23:** Captura un producto mostrando el badge "🎮 Laptop Gamer" que fue clasificado automáticamente

---

### 6.3 Búsqueda Semántica (SPARQL)

Los filtros de búsqueda utilizan consultas semánticas sobre la ontología:

- **Por categoría:** Usa la jerarquía OWL (Producto → Electrónica → Laptop)
- **Por precio:** Filtra usando propiedades de datos (`tienePrecio`)
- **Por RAM:** Filtra usando propiedades de datos (`tieneRAM_GB`)
- **Texto libre:** Busca en nombres y descripciones

> 📸 **Screenshot 24:** Captura los resultados de una búsqueda filtrada por "Laptop" + precio entre $1000-$1500

---

### 6.4 Validación de Productos

El sistema valida automáticamente que los productos tengan especificaciones coherentes:

**Errores detectados:**
- ❌ Precio negativo
- ❌ RAM imposible (ej: mayor a 512GB)
- ❌ Smartphone con especificaciones de laptop

**Advertencias:**
- ⚠️ Precios muy altos (>$100,000)
- ⚠️ Especificaciones inusuales

---

## 7. SOLUCIÓN DE PROBLEMAS FRECUENTES

### Error: "python no se reconoce como comando"

**Problema:** Python no está instalado o no está en el PATH del sistema.

**Solución:**
1. Descarga Python desde: https://www.python.org/downloads/
2. Durante la instalación, **marca la casilla "Add Python to PATH"**
3. Reinicia la terminal

> 📸 **Screenshot 25:** Captura el instalador de Python con la casilla "Add Python to PATH" marcada

---

### Error: "npm no se reconoce como comando"

**Problema:** Node.js no está instalado.

**Solución:**
1. Descarga Node.js desde: https://nodejs.org/
2. Elige la versión **LTS** (recomendada)
3. Instala y reinicia la terminal

---

### Error: "No se puede conectar al servidor" en el frontend

**Problema:** El backend no está ejecutándose.

**Solución:**
1. Verifica que la terminal del backend muestre:
   ```
   INFO: Uvicorn running on http://0.0.0.0:5000
   ```
2. Si no, vuelve a ejecutar `python main.py`

> 📸 **Screenshot 26:** Captura la terminal del backend ejecutándose correctamente

---

### Error: "Error loading ontology" en el backend

**Problema:** Java no está instalado (necesario para Pellet).

**Solución:**
1. Descarga Java JDK desde: https://adoptium.net/
2. Instala la versión 11 o superior
3. Reinicia todas las terminales

---

### El frontend carga pero no muestra productos

**Problema:** El backend no respondió correctamente.

**Solución:**
1. Verifica el backend ejecutando en el navegador:
   ```
   http://localhost:5000/api/v1/products
   ```
2. Debe mostrar un JSON con la lista de productos
3. Si muestra error, revisa los logs del backend

> 📸 **Screenshot 27:** Captura el navegador mostrando la URL http://localhost:5000/api/v1/products con el JSON de productos

---

### El sistema es muy lento al iniciar

**Causa:** El razonador Pellet procesa toda la ontología al arrancar.

**Solución:** Es normal. El primer inicio puede tardar 10-30 segundos. Espera hasta ver:
```
[OK] Razonador Pellet ejecutado exitosamente
```

---

## 8. PREGUNTAS FRECUENTES (FAQ)

### ¿Qué significa "Inferencia SWRL"?

Son **reglas lógicas programadas** en la ontología. Por ejemplo:
> "Si una Laptop tiene RAM ≥ 16GB, entonces se clasifica como LaptopGamer"

El sistema aplica estas reglas **automáticamente** y te muestra los resultados.

---

### ¿Cómo se decide el "Ganador" en una comparación?

El sistema calcula un **score de 0 a 100** considerando:
1. Los 9 factores técnicos (ver tabla en sección 6.1)
2. Bonus por reglas SWRL aplicadas
3. Relación calidad-precio

El producto con el **score más alto** gana.

---

### ¿Por qué algunos productos tienen el badge "Laptop Gamer"?

El sistema detectó automáticamente que tienen **RAM de 16GB o más**, lo cual es típico de laptops para gaming según las reglas SWRL.

---

### ¿Puedo agregar mis propios productos?

En esta versión, los productos vienen predefinidos en la ontología OWL. Para agregar productos:
1. Abre el archivo `backend/ontology/SmartCompareMarket.owl` en Protégé
2. Agrega nuevos individuos de la clase apropiada
3. Reinicia el backend

---

### ¿Por qué necesito Java si el sistema es Python?

El razonador **Pellet** que ejecuta las reglas SWRL está escrito en Java. Owlready2 (la librería Python) lo necesita para ejecutar el razonamiento semántico.

---

### ¿Qué navegadores puedo usar?

Cualquier navegador moderno funciona:
- ✅ Chrome (recomendado)
- ✅ Firefox
- ✅ Edge
- ✅ Safari

---

### ¿Necesito conexión a Internet para usar el sistema?

- **Para instalar:** Sí, necesitas Internet para descargar dependencias
- **Para usar:** No, el sistema funciona localmente una vez instalado

---

## 🎉 ¡LISTO!

Si seguiste todos los pasos correctamente, ahora tienes **SmartCompareMarket** funcionando en tu computadora.

### Resumen de URLs importantes:

| Servicio | URL |
|----------|-----|
| **Frontend (Interfaz)** | http://localhost:5173 |
| **Backend (API)** | http://localhost:5000 |
| **Documentación API** | http://localhost:5000/docs |

> 📸 **Screenshot 28:** Captura la página de documentación interactiva de la API en http://localhost:5000/docs mostrando todos los endpoints disponibles

---

**¿Tienes problemas?** Revisa la sección de [Solución de Problemas](#7-solución-de-problemas-frecuentes) o contacta a los autores.

**Autores:** Álvaro y Jony  
**Proyecto:** Nivel 2 - Web Semántica  
**Fecha:** Diciembre 2024

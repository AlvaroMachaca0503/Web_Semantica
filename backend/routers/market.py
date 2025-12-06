"""
Router de Análisis de Mercado - SmartCompareMarket API
Endpoints para estadísticas y análisis de datos del marketplace.

Autor: Álvaro Machaca
Fecha: Diciembre 2024
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional

from sparql.market_analysis import MarketAnalysis
from dependencies import get_market_analysis

router = APIRouter(
    prefix="/api/v1/market",
    tags=["market"]
)


@router.get("/stats/prices")
async def get_price_statistics(
    market_analysis: MarketAnalysis = Depends(get_market_analysis)
):
    """
    Obtiene estadísticas de precios del mercado.
    
    **Retorna:**
    - `total_products`: Número total de productos analizados
    - `average`: Precio promedio
    - `median`: Precio mediano
    - `min`: Precio mínimo
    - `max`: Precio máximo
    - `std_deviation`: Desviación estándar
    - `price_ranges`: Distribución por rangos de precio
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/market/stats/prices
    ```
    
    **Respuesta:**
    ```json
    {
      "total_products": 52,
      "average": 1245.67,
      "median": 1099.00,
      "min": 299.00,
      "max": 2499.00,
      "std_deviation": 456.32,
      "price_ranges": {
        "0-500": {"count": 8, "percentage": 15.38},
        "500-1000": {"count": 15, "percentage": 28.85},
        "1000-1500": {"count": 20, "percentage": 38.46},
        "1500-2000": {"count": 7, "percentage": 13.46},
        "2000+": {"count": 2, "percentage": 3.85}
      }
    }
    ```
    """
    try:
        result = market_analysis.get_price_statistics()
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener estadísticas de precios: {str(e)}"
        )


@router.get("/stats/categories")
async def get_category_distribution(
    market_analysis: MarketAnalysis = Depends(get_market_analysis)
):
    """
    Obtiene la distribución de productos por categoría.
    
    **Retorna:**
    - `total_products`: Total de productos
    - `unique_categories`: Número de categorías únicas
    - `categories`: Diccionario con estadísticas por categoría:
        - `count`: Número de productos
        - `percentage`: Porcentaje del total
        - `avg_price`: Precio promedio de la categoría
        - `min_price`: Precio mínimo
        - `max_price`: Precio máximo
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/market/stats/categories
    ```
    """
    try:
        result = market_analysis.get_category_distribution()
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener distribución de categorías: {str(e)}"
        )


@router.get("/stats/specs")
async def get_specs_analysis(
    category: Optional[str] = Query(None, description="Filtrar por categoría específica (ej: Laptop, Smartphone)"),
    market_analysis: MarketAnalysis = Depends(get_market_analysis)
):
    """
    Análisis de especificaciones técnicas del mercado.
    
    **Parámetros:**
    - `category` (opcional): Filtrar por categoría específica
    
    **Retorna estadísticas de:**
    - RAM (promedio, mediana, min, max, distribución)
    - Almacenamiento (promedio, mediana, min, max, distribución)
    - Pantalla (promedio, mediana, min, max)
    - Batería (promedio, mediana, min, max)
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/market/stats/specs
    GET /api/v1/market/stats/specs?category=Laptop
    ```
    
    **Respuesta:**
    ```json
    {
      "category": "Laptop",
      "total_analyzed": 25,
      "ram_gb": {
        "average": 18.4,
        "median": 16,
        "min": 8,
        "max": 64,
        "most_common": 16,
        "distribution": {
          "16": {"count": 15, "percentage": 60},
          "32": {"count": 8, "percentage": 32}
        }
      },
      "storage_gb": {
        "average": 685.33,
        "median": 512,
        "min": 256,
        "max": 2048
      }
    }
    ```
    """
    try:
        result = market_analysis.get_specs_analysis(category)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en análisis de especificaciones: {str(e)}"
        )


@router.get("/best-value")
async def get_best_value_products(
    limit: int = Query(10, ge=1, le=50, description="Número máximo de productos a retornar"),
    market_analysis: MarketAnalysis = Depends(get_market_analysis)
):
    """
    Identifica productos con mejor relación calidad-precio.
    
    **Algoritmo:**
    ```
    value_score = (RAM + Storage/10 + Screen*10 + Rating*10) / Price
    ```
    
    **Parámetros:**
    - `limit`: Número máximo de productos (default: 10, max: 50)
    
    **Retorna:**
    - `total_analyzed`: Total de productos analizados
    - `best_value_products`: Lista ordenada por value_score
    - `algorithm`: Fórmula utilizada
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/market/best-value
    GET /api/v1/market/best-value?limit=5
    ```
    
    **Respuesta:**
    ```json
    {
      "total_analyzed": 52,
      "best_value_products": [
        {
          "id": "Laptop_HP_Pavilion",
          "name": "HP Pavilion Gaming",
          "category": "Laptop",
          "price": 999.00,
          "value_score": 0.0856,
          "specs": {
            "ram_gb": 16,
            "storage_gb": 512,
            "screen_inches": 15.6,
            "rating": 4.5
          }
        }
      ]
    }
    ```
    """
    try:
        result = market_analysis.get_best_value_products(limit)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al calcular mejor valor: {str(e)}"
        )


@router.get("/trends")
async def get_market_trends(
    market_analysis: MarketAnalysis = Depends(get_market_analysis)
):
    """
    Analiza tendencias y patrones del mercado.
    
    **Retorna:**
    - `price_segments`: Distribución por segmentos de precio
        - Premium (> $1500)
        - Mid-range ($800-$1500)
        - Budget (< $800)
    - `most_common_specs`: Especificaciones más comunes (RAM, Storage)
    - `market_insights`: Insights automáticos generados
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/market/trends
    ```
    
    **Respuesta:**
    ```json
    {
      "price_segments": {
        "premium": {"count": 12, "percentage": 23.08, "price_range": "> $1500"},
        "mid_range": {"count": 25, "percentage": 48.08, "price_range": "$800-$1500"},
        "budget": {"count": 15, "percentage": 28.85, "price_range": "< $800"}
      },
      "most_common_specs": {
        "ram_gb": [[16, 20], [8, 15], [32, 10]],
        "storage_gb": [[512, 25], [256, 18], [1024, 9]]
      },
      "market_insights": [
        "La mayoría de productos están en rango medio (48.1% del catálogo)",
        "El estándar de RAM más común es 16GB (20 productos)",
        "El almacenamiento estándar es 512GB (25 productos)"
      ]
    }
    ```
    """
    try:
        result = market_analysis.get_market_trends()
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en análisis de tendencias: {str(e)}"
        )


@router.get("/compare-categories")
async def compare_categories(
    category1: str = Query(..., description="Primera categoría a comparar"),
    category2: str = Query(..., description="Segunda categoría a comparar"),
    market_analysis: MarketAnalysis = Depends(get_market_analysis)
):
    """
    Compara especificaciones entre dos categorías de productos.
    
    **Parámetros:**
    - `category1`: Primera categoría (ej: Laptop)
    - `category2`: Segunda categoría (ej: Tablet)
    
    **Retorna:**
    - Comparación detallada de especificaciones
    - Ganador en cada categoría (RAM, Storage, Screen)
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/market/compare-categories?category1=Laptop&category2=Tablet
    ```
    
    **Respuesta:**
    ```json
    {
      "category1": "Laptop",
      "category2": "Tablet",
      "comparison": {
        "ram_gb": {
          "Laptop": 18.4,
          "Tablet": 10.2,
          "winner": "Laptop"
        },
        "storage_gb": {
          "Laptop": 685.33,
          "Tablet": 345.6,
          "winner": "Laptop"
        },
        "screen_inches": {
          "Laptop": 15.2,
          "Tablet": 11.5,
          "winner": "Laptop"
        }
      }
    }
    ```
    """
    try:
        result = market_analysis.compare_categories(category1, category2)
        
        if "error" in result:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al comparar categorías: {str(e)}"
        )


@router.get("/summary")
async def get_market_summary(
    market_analysis: MarketAnalysis = Depends(get_market_analysis)
):
    """
    Resumen ejecutivo completo del análisis de mercado.
    
    Combina múltiples estadísticas en un solo endpoint.
    
    **Retorna:**
    - Estadísticas de precios
    - Distribución de categorías
    - Top 5 mejores valores
    - Tendencias del mercado
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/market/summary
    ```
    """
    try:
        # Obtener todas las estadísticas
        prices = market_analysis.get_price_statistics()
        categories = market_analysis.get_category_distribution()
        best_value = market_analysis.get_best_value_products(5)
        trends = market_analysis.get_market_trends()
        
        return {
            "generated_at": "2024-12-06",
            "price_statistics": prices if "error" not in prices else {"error": prices.get("error")},
            "category_distribution": categories if "error" not in categories else {"error": categories.get("error")},
            "top_5_best_value": best_value.get("best_value_products", [])[:5] if "error" not in best_value else [],
            "market_trends": trends if "error" not in trends else {"error": trends.get("error")}
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar resumen de mercado: {str(e)}"
        )

"""
Router de Equivalencias - SmartCompareMarket API
Endpoints para gestionar equivalencias semánticas entre productos.

Autor: Álvaro Machaca
Fecha: Diciembre 2024
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from pydantic import BaseModel

from services.equivalence_service import EquivalenceService
from dependencies import get_equivalence_service

router = APIRouter(
    prefix="/api/v1",
    tags=["equivalences"]
)


class EquivalenceComparisonRequest(BaseModel):
    """Modelo para comparar dos productos."""
    product1_id: str
    product2_id: str


@router.get("/equivalences/{product_id}")
async def get_product_equivalents(
    product_id: str,
    equivalence_service: EquivalenceService = Depends(get_equivalence_service)
) -> Dict:
    """
    Obtiene todos los productos equivalentes al producto dado.
    
    **Combina:**
    - Equivalencias explícitas de la ontología (esEquivalenteTecnico)
    - Productos similares (esSimilarA)
    - Equivalencias auto-detectadas por especificaciones
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/equivalences/Laptop_Dell_XPS
    ```
    
    **Respuesta:**
    - `product_id`: ID del producto consultado
    - `product_name`: Nombre del producto
    - `total_equivalents`: Número total de equivalentes encontrados
    - `equivalents`: Lista de productos equivalentes con:
        - `id`: ID del producto equivalente
        - `name`: Nombre del producto
        - `category`: Categoría
        - `price`: Precio
        - `match_type`: Tipo de match (explicit, similar, auto_detected)
        - `match_reason`: Razón de la equivalencia
        - `confidence`: Nivel de confianza (0-100)
    - `criteria_summary`: Resumen por tipo de criterio
    """
    try:
        result = equivalence_service.find_equivalent_products(product_id)
        
        if "error" in result and "no encontrado" in result["error"].lower():
            raise HTTPException(status_code=404, detail=f"Producto '{product_id}' no encontrado")
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar equivalentes: {str(e)}"
        )


@router.post("/equivalences/compare")
async def compare_product_equivalence(
    request: EquivalenceComparisonRequest,
    equivalence_service: EquivalenceService = Depends(get_equivalence_service)
) -> Dict:
    """
    Compara dos productos para determinar si son equivalentes.
    
    **Análisis incluye:**
    - Verificación de equivalencia explícita en ontología
    - Cálculo de score de similitud basado en:
        - Categoría (requisito obligatorio)
        - RAM (±2GB)
        - Almacenamiento (±128GB)
        - Precio (±20%)
        - Pantalla (±1 pulgada)
    - Recomendación basada en análisis
    
    **Ejemplo de uso:**
    ```json
    POST /api/v1/equivalences/compare
    {
        "product1_id": "Laptop_Dell_XPS",
        "product2_id": "Laptop_HP_Pavilion"
    }
    ```
    
    **Respuesta:**
    - `product1`: Información del primer producto
    - `product2`: Información del segundo producto
    - `equivalent`: Boolean - ¿Son equivalentes?
    - `match_score`: Score de equivalencia (0-100)
    - `match_type`: Tipo de match (explicit, auto, none)
    - `reasons`: Lista de razones de la equivalencia
    - `recommendation`: Recomendación basada en el análisis
    """
    try:
        result = equivalence_service.get_equivalence_comparison(
            request.product1_id,
            request.product2_id
        )
        
        if "error" in result and "no encontrado" in result["error"].lower():
            raise HTTPException(
                status_code=404,
                detail=f"Uno o ambos productos no encontrados"
            )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al comparar productos: {str(e)}"
        )


@router.get("/equivalences")
async def get_all_equivalence_groups(
    equivalence_service: EquivalenceService = Depends(get_equivalence_service)
) -> Dict:
    """
    Obtiene un resumen de grupos de productos equivalentes en el mercado.
    
    **Útil para:**
    - Análisis de mercado
    - Detección de productos con múltiples opciones equivalentes
    - Identificación de productos únicos sin equivalentes
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/equivalences
    ```
    
    **Respuesta:**
    - `total_products`: Total de productos analizados
    - `products_with_equivalents`: Productos que tienen equivalentes
    - `products_without_equivalents`: Productos únicos
    - `top_equivalence_groups`: Grupos con más equivalentes
    """
    try:
        # Obtener todos los productos
        all_products = list(equivalence_service.onto.Producto.instances())
        
        equivalence_groups = {}
        products_with_equivalents = 0
        
        for product in all_products:
            product_id = product.name
            
            # Buscar equivalentes
            result = equivalence_service.find_equivalent_products(product_id)
            
            if "error" not in result and result["total_equivalents"] > 0:
                products_with_equivalents += 1
                equivalence_groups[product_id] = {
                    "product_id": product_id,
                    "product_name": result.get("product_name", "Sin nombre"),
                    "total_equivalents": result["total_equivalents"],
                    "equivalents": [e["id"] for e in result["equivalents"]]
                }
        
        # Ordenar grupos por número de equivalentes
        sorted_groups = sorted(
            equivalence_groups.values(),
            key=lambda x: x["total_equivalents"],
            reverse=True
        )
        
        return {
            "total_products": len(all_products),
            "products_with_equivalents": products_with_equivalents,
            "products_without_equivalents": len(all_products) - products_with_equivalents,
            "equivalence_percentage": round(products_with_equivalents / len(all_products) * 100, 2) if all_products else 0,
            "top_equivalence_groups": sorted_groups[:10],  # Top 10
            "summary": {
                "message": f"{products_with_equivalents} de {len(all_products)} productos tienen equivalentes",
                "avg_equivalents_per_product": round(
                    sum(g["total_equivalents"] for g in equivalence_groups.values()) / len(equivalence_groups),
                    2
                ) if equivalence_groups else 0
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener grupos de equivalencias: {str(e)}"
        )

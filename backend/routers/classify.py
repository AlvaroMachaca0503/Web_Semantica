"""
Router de Clasificación - SmartCompareMarket API
Endpoints para clasificación automática de productos con OWL y SWRL.

Autor: Álvaro Machaca
Fecha: Diciembre 2024
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional

from reasoning.product_classifier import ProductClassifier
from dependencies import get_product_classifier

router = APIRouter(
    prefix="/api/v1",
    tags=["classification"]
)


@router.get("/classify/{product_id}")
async def classify_product(
    product_id: str,
    classifier: ProductClassifier = Depends(get_product_classifier)
):
    """
    Clasifica un producto usando razonamiento OWL y reglas SWRL.
    
    **Clasificación incluye:**
    - **Clases directas**: Asignadas explícitamente en la ontología
    - **Clases inferidas**: Deducidas por el razonador Pellet
    - **Clases SWRL**: Aplicadas por reglas SWRL
    - **Explicaciones**: Razones de cada clasificación en lenguaje natural
    - **Confianza**: Nivel de confianza de la clasificación
    
    **Reglas SWRL implementadas:**
    1. **DetectarGamer**: Laptop con RAM ≥ 16GB → LaptopGamer
    2. **DetectarSmartphoneGamaAlta**: Smartphone con RAM > 8GB → SmartphoneGamaAlta
    3. **DetectarTabletPremium**: Tablet con precio > $800 → TabletPremium
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/classify/Laptop_Dell_XPS
    ```
    
    **Respuesta:**
    ```json
    {
      "product_id": "Laptop_Dell_XPS",
      "product_name": "Dell XPS 15",
      "classification": {
        "all_classes": ["Producto", "Electronica", "Computadora", "Laptop", "LaptopGamer"],
        "direct_classes": ["Laptop"],
        "inferred_classes": ["Producto", "Electronica", "Computadora"],
        "swrl_classes": [
          {
            "rule_name": "DetectarGamer",
            "condition": "RAM >= 16GB (actual: 32GB)",
            "resulting_class": "LaptopGamer",
            "triggered": true
          }
        ],
        "total_classes": 5
      },
      "specifications": {
        "ram_gb": 32,
        "storage_gb": 1024,
        "price": 1599.99,
        "screen_inches": 15.6,
        "rating": 4.7
      },
      "explanations": [
        "✓ Clasificado como 'Laptop' (categoría base)",
        "✓ Clasificado como 'LaptopGamer' porque tiene 32GB RAM (≥16GB)",
        "⭐ Alta capacidad de RAM: 32GB (top tier)",
        "⭐ Alto almacenamiento: 1024GB (1TB+)",
        "💎 Producto premium: $1599.99"
      ],
      "classification_confidence": {
        "level": "very_high",
        "total_classes": 5,
        "swrl_rules_applied": 1,
        "has_inferences": true
      }
    }
    ```
    """
    try:
        result = classifier.classify_product(product_id)
        
        if "error" in result:
            if "no encontrado" in result["error"].lower():
                raise HTTPException(status_code=404, detail=result["error"])
            else:
                raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al clasificar producto: {str(e)}"
        )


@router.get("/classify")
async def classify_all_products(
    classifier: ProductClassifier = Depends(get_product_classifier)
):
    """
    Clasifica todos los productos del sistema.
    
    **Retorna:**
    - `statistics`: Estadísticas generales de clasificación
        - `total_products`: Total de productos analizados
        - `by_category`: Conteo por categoría principal
        - `swrl_applied`: Productos con reglas SWRL aplicadas
        - `with_inferences`: Productos con clases inferidas
    - `products`: Lista de todos los productos con sus clasificaciones
    - `summary`: Resumen ejecutivo con porcentajes
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/classify
    ```
    
    **Respuesta:**
    ```json
    {
      "statistics": {
        "total_products": 52,
        "by_category": {
          "Laptop": 25,
          "Smartphone": 18,
          "Tablet": 9
        },
        "swrl_applied": 15,
        "with_inferences": 52
      },
      "products": [
        {
          "id": "Laptop_Dell_XPS",
          "name": "Dell XPS 15",
          "classes": ["Producto", "Electronica", "Laptop", "LaptopGamer"],
          "swrl_rules": 1
        }
      ],
      "summary": {
        "total_analyzed": 52,
        "swrl_percentage": 28.85,
        "inference_percentage": 100.0
      }
    }
    ```
    """
    try:
        result = classifier.classify_all_products()
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al clasificar productos: {str(e)}"
        )


@router.get("/class/{class_name}/products")
async def get_products_by_class(
    class_name: str,
    classifier: ProductClassifier = Depends(get_product_classifier)
):
    """
    Obtiene todos los productos que pertenecen a una clase específica.
    
    **Útil para:**
    - Obtener todos los productos de tipo "LaptopGamer"
    - Listar todos los "SmartphoneGamaAlta"
    - Filtrar por cualquier clase de la ontología
    
    **Parámetros:**
    - `class_name`: Nombre de la clase OWL (ej: "LaptopGamer", "Smartphone", "Tablet")
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/class/LaptopGamer/products
    GET /api/v1/class/Smartphone/products
    GET /api/v1/class/TabletPremium/products
    ```
    
    **Respuesta:**
    ```json
    {
      "class_name": "LaptopGamer",
      "total_products": 3,
      "products": [
        {
          "id": "Laptop_Dell_XPS",
          "name": "Dell XPS 15",
          "price": 1599.99,
          "ram_gb": 32,
          "storage_gb": 1024,
          "all_classes": ["Producto", "Electronica", "Laptop", "LaptopGamer"]
        },
        {
          "id": "Laptop_MSI_Gaming",
          "name": "MSI GF65 Thin",
          "price": 1299.00,
          "ram_gb": 16,
          "storage_gb": 512,
          "all_classes": ["Producto", "Electronica", "Laptop", "LaptopGamer"]
        }
      ]
    }
    ```
    """
    try:
        result = classifier.get_products_by_class(class_name)
        
        if "error" in result:
            if "no encontrada" in result["error"].lower():
                raise HTTPException(
                    status_code=404,
                    detail=result["error"]
                )
            else:
                raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener productos de clase '{class_name}': {str(e)}"
        )


@router.get("/classification/stats")
async def get_classification_statistics(
    classifier: ProductClassifier = Depends(get_product_classifier)
):
    """
    Obtiene estadísticas sobre la clasificación automática del sistema.
    
    **Retorna:**
    - Porcentaje de productos con reglas SWRL aplicadas
    - Porcentaje de productos con inferencias OWL
    - Distribución por categorías
    - Efectividad del sistema de clasificación
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/classification/stats
    ```
    
    **Respuesta:**
    ```json
    {
      "total_products": 52,
      "classification_coverage": {
        "with_swrl_rules": 15,
        "swrl_percentage": 28.85,
        "with_owl_inferences": 52,
        "inference_percentage": 100.0
      },
      "category_distribution": {
        "Laptop": 25,
        "Smartphone": 18,
        "Tablet": 9
      },
      "swrl_effectiveness": {
        "LaptopGamer_detected": 3,
        "SmartphoneGamaAlta_detected": 8,
        "TabletPremium_detected": 4
      }
    }
    ```
    """
    try:
        # Obtener clasificación completa
        all_classifications = classifier.classify_all_products()
        
        if "error" in all_classifications:
            raise HTTPException(status_code=500, detail=all_classifications["error"])
        
        stats = all_classifications["statistics"]
        summary = all_classifications["summary"]
        
        # Contar productos por clase SWRL
        swrl_effectiveness = {}
        for product in all_classifications["products"]:
            for cls in product["classes"]:
                if cls in ["LaptopGamer", "SmartphoneGamaAlta", "TabletPremium"]:
                    key = f"{cls}_detected"
                    swrl_effectiveness[key] = swrl_effectiveness.get(key, 0) + 1
        
        return {
            "total_products": stats["total_products"],
            "classification_coverage": {
                "with_swrl_rules": stats["swrl_applied"],
                "swrl_percentage": summary["swrl_percentage"],
                "with_owl_inferences": stats["with_inferences"],
                "inference_percentage": summary["inference_percentage"]
            },
            "category_distribution": stats["by_category"],
            "swrl_effectiveness": swrl_effectiveness
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )

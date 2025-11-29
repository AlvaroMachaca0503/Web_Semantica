"""
Router de Productos - FastAPI con Dependency Injection
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dependencies import get_product_service, get_inference_engine
from services.product_service import ProductService
from reasoning.inference_engine import InferenceEngine
from models import ProductListResponse, ProductResponse, ErrorResponse

router = APIRouter()


@router.get(
    '/products',
    response_model=ProductListResponse,
    summary="Listar productos",
    description="""
    Obtiene una lista de productos con filtros opcionales.
    
    **Filtros disponibles:**
    - `category`: Filtrar por categoría (Electrónica, Hogar, Moda, Smartphone, Laptop)
    - `min_price`: Precio mínimo
    - `max_price`: Precio máximo
    
    **Ejemplo:**
    ```
    GET /api/products?category=Smartphone&min_price=500&max_price=1000
    ```
    """
)
async def get_products(
    category: Optional[str] = Query(
        None,
        description="Categoría del producto",
        example="Smartphone"
    ),
    min_price: Optional[float] = Query(
        None,
        ge=0,
        description="Precio mínimo",
        example=100.0
    ),
    max_price: Optional[float] = Query(
        None,
        ge=0,
        description="Precio máximo",
        example=2000.0
    ),
    service: ProductService = Depends(get_product_service)
):
    """
    Obtiene lista de productos con filtros opcionales
    """
    try:
        # Filtrar por categoría
        if category:
            products = service.get_products_by_category(category)
        else:
            products = service.get_all_products()
        
        # Filtrar por precio
        if min_price is not None or max_price is not None:
            filtered = []
            for product in products:
                price = product.get("properties", {}).get("tienePrecio")
                
                if price is None:
                    continue
                
                if min_price is not None and price < min_price:
                    continue
                
                if max_price is not None and price > max_price:
                    continue
                
                filtered.append(product)
            
            products = filtered
        
        return ProductListResponse(
            success=True,
            count=len(products),
            data=products
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener productos: {str(e)}"
        )


@router.get(
    '/products/{product_id}',
    response_model=ProductResponse | ErrorResponse,
    summary="Obtener producto por ID",
    description="""
    Obtiene un producto específico por su ID.
    
    **Ejemplo:**
    ```
    GET /api/products/iPhone15_Barato
    ```
    """,
    responses={
        200: {
            "description": "Producto encontrado",
            "model": ProductResponse
        },
        404: {
            "description": "Producto no encontrado",
            "model": ErrorResponse
        }
    }
)
async def get_product(
    product_id: str,
    service: ProductService = Depends(get_product_service)
):
    """
    Obtiene un producto específico por su ID
    """
    try:
        product = service.get_product_by_id(product_id)
        
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Producto '{product_id}' no encontrado"
            )
        
        return ProductResponse(**product)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener producto: {str(e)}"
        )


@router.get(
    '/products/{product_id}/relationships',
    response_model=dict,
    summary="Obtener relaciones del producto",
    description="""
    Obtiene todas las relaciones semánticas de un producto:
    - Compatible con (esCompatibleCon)
    - Incompatible con (incompatibleCon)
    - Similar a (esSimilarA)
    - Mejor opción que (esMejorOpcionQue - inferido por SWRL)
    
    **Ejemplo:**
    ```
    GET /api/products/iPhone15_Barato/relationships
    ```
    """
)
async def get_product_relationships(
    product_id: str,
    engine: InferenceEngine = Depends(get_inference_engine)
):
    """
    Obtiene todas las relaciones de un producto usando InferenceEngine
    """
    try:
        # Obtener todas las relaciones
        relationships = engine.get_all_relationships(product_id)
        
        return {
            "success": True,
            **relationships
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener relaciones: {str(e)}"
        )

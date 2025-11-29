"""
Router de Comparación - FastAPI (DÍA 2)
Comparación inteligente entre productos
"""
from fastapi import APIRouter, HTTPException
from typing import List
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.schemas import CompareRequest, ComparisonResponse
from services.comparison_service import ComparisonService

router = APIRouter()
comparison_service = ComparisonService()


@router.post(
    '/compare',
    response_model=ComparisonResponse,
    summary="Comparar productos",
    description="""
    Compara 2 o más productos de forma inteligente utilizando:
    
    - **Scoring** basado en precio, RAM, calificación, compatibilidad
    - **Inferencias SWRL** (esMejorOpcionQue)
    - **Compatibilidades** entre productos
    - **Tabla comparativa** lado a lado
    
    ## Ejemplo de uso:
    
    ```json
    {
      "products": ["iPhone15_Barato", "iPhone15_Caro"]
    }
    ```
    
    ## Respuesta incluye:
    
    - Información de cada producto
    - **Ganador** (producto con mejor scoring)
    - **Razón** de la victoria
    - **Diferencias** entre productos
    - **Relaciones SWRL** detectadas
    - **Compatibilidad** entre productos
    """,
    responses={
        200: {
            "description": "Comparación exitosa",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "comparison": {
                            "product1": {
                                "id": "iPhone15_Barato",
                                "nombre": "iPhone 15 Pro",
                                "precio": 950,
                                "ram": 8
                            },
                            "product2": {
                                "id": "iPhone15_Caro",
                                "nombre": "iPhone 15 Pro",
                                "precio": 1200,
                                "ram": 8
                            },
                            "winner": "iPhone15_Barato",
                            "reason": "Mejor precio para el mismo producto",
                            "swrl_inference": {
                                "esMejorOpcionQue": True,
                                "rule": "EncontrarMejorPrecio"
                            }
                        }
                    }
                }
            }
        }
    }
)
async def compare_products(request: CompareRequest):
    """
    Compara productos usando el motor de comparación inteligente
    """
    try:
        # Validar que hay al menos 2 productos
        if len(request.products) < 2:
            raise HTTPException(
                status_code=400,
                detail="Se requieren al menos 2 productos para comparar"
            )
        
        # Realizar comparación
        result = comparison_service.compare_products(request.products)
        
        return ComparisonResponse(
            success=True,
            comparison=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al comparar productos: {str(e)}"
        )

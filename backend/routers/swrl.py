"""
Router SWRL - FastAPI
Endpoints para resultados de reglas SWRL e inferencias
"""
from fastapi import APIRouter, HTTPException
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reasoning.swrl_engine import SWRLEngine
from models.schemas import SWRLResultResponse

router = APIRouter()
swrl_engine = SWRLEngine()


@router.get(
    '/swrl/best-price',
    response_model=SWRLResultResponse,
    summary="Productos con mejor precio",
    description="""
    Obtiene productos que son mejor opción que otros según la regla SWRL **EncontrarMejorPrecio**.
    
    Esta regla infiere la relación `esMejorOpcionQue` cuando dos productos:
    - Tienen el mismo nombre
    - Uno tiene menor precio que el otro
    
    **Ejemplo:** iPhone15_Barato es mejor opción que iPhone15_Caro
    """
)
async def get_best_price_products():
    """
    Regla SWRL: EncontrarMejorPrecio
    """
    try:
        results = swrl_engine.get_best_price_products()
        
        return SWRLResultResponse(
            success=True,
            rule="EncontrarMejorPrecio",
            count=len(results),
            results=results
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en regla SWRL: {str(e)}"
        )


@router.get(
    '/swrl/gaming-laptops',
    response_model=SWRLResultResponse,
    summary="Laptops gaming",
    description="""
    Obtiene laptops clasificadas como **LaptopGamer** según la regla SWRL **DetectarGamer**.
    
    Esta regla infiere que una laptop es gaming cuando:
    - Es de tipo Laptop
    - Tiene RAM ≥ 16GB
    
    **Ejemplo:** Laptop_Dell_XPS con 16GB RAM → LaptopGamer
    """
)
async def get_gaming_laptops():
    """
    Regla SWRL: DetectarGamer
    """
    try:
        results = swrl_engine.get_gaming_laptops()
        
        return SWRLResultResponse(
            success=True,
            rule="DetectarGamer",
            count=len(results),
            results=results
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en regla SWRL: {str(e)}"
        )


@router.get(
    '/swrl/positive-reviews',
    response_model=SWRLResultResponse,
    summary="Reseñas positivas",
    description="""
    Obtiene reseñas clasificadas como **Reseña_Positiva** según la regla SWRL **ClasificarPositivas**.
    
    Esta regla infiere que una reseña es positiva cuando:
    - Tiene calificación ≥ 4
    
    """
)
async def get_positive_reviews():
    """
    Regla SWRL: ClasificarPositivas
    """
    try:
        results = swrl_engine.get_positive_reviews()
        
        return SWRLResultResponse(
            success=True,
            rule="ClasificarPositivas",
            count=len(results),
            results=results
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en regla SWRL: {str(e)}"
        )


@router.get(
    '/swrl/negative-reviews',
    response_model=SWRLResultResponse,
    summary="Reseñas negativas",
    description="""
    Obtiene reseñas clasificadas como **Reseña_Negativa** según la regla SWRL **ClasificarNegativas**.
    
    Esta regla infiere que una reseña es negativa cuando:
    - Tiene calificación ≤ 2
    """
)
async def get_negative_reviews():
    """
    Regla SWRL: ClasificarNegativas
    """
    try:
        results = swrl_engine.get_negative_reviews()
        
        return SWRLResultResponse(
            success=True,
            rule="ClasificarNegativas",
            count=len(results),
            results=results
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en regla SWRL: {str(e)}"
        )

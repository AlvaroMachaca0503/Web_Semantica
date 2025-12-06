"""
Router de Recomendaciones - Sistema personalizado de sugerencias
"""
from fastapi import APIRouter, Query
from typing import Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.recommendation_service import RecommendationService
from models.recommendation import UserPreferences, RecommendationResponse

router = APIRouter()


@router.post(
    '/recommendations',
    response_model=RecommendationResponse,
    summary="Obtener recomendaciones personalizadas",
    description="""
    Genera recomendaciones de productos basadas en las preferencias del usuario.
    
    **Sistema de Scoring:**
    - Presupuesto (30 pts): Productos cercanos al límite sin pasarse
    - Calificación (25 pts): Opiniones de otros usuarios
    - RAM (15 pts): Cumplimiento de requisitos técnicos
    - Almacenamiento (10 pts): Espacio disponible
    - Bonus SWRL (20 pts): Inferencias semánticas (LaptopGamer, MejorOpcionQue)
    
    **Ejemplo:**
    ```json
    {
      "budget": 1500,
      "preferred_category": "Laptop",
      "min_ram": 8,
      "min_rating": 4.0
    }
    ```
    """,
)
async def get_recommendations(
    preferences: UserPreferences,
    limit: int = Query(5, ge=1, le=20, description="Número de recomendaciones")
):
    """Genera recomendaciones basadas en preferencias"""
    service = RecommendationService()
    return service.get_recommendations(preferences, limit)


@router.get(
    '/recommendations/quick',
    response_model=RecommendationResponse,
    summary="Recomendaciones rápidas (GET)",
    description="""
    Versión GET del endpoint de recomendaciones para pruebas rápidas.
    Usa query parameters en lugar de body.
    
    **Ejemplo:**
    ```
    GET /api/v1/recommendations/quick?budget=1000&preferred_category=Smartphone&min_rating=4
    ```
    """,
)
async def get_quick_recommendations(
    budget: Optional[float] = Query(None, description="Presupuesto máximo"),
    min_budget: Optional[float] = Query(None, description="Presupuesto mínimo"),
    preferred_category: Optional[str] = Query(None, description="Categoría (Laptop, Smartphone, etc.)"),
    min_ram: Optional[int] = Query(None, description="RAM mínima (GB)"),
    min_storage: Optional[int] = Query(None, description="Almacenamiento mínimo (GB)"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Calificación mínima"),
    limit: int = Query(5, ge=1, le=20)
):
    """Recomendaciones usando query params"""
    preferences = UserPreferences(
        budget=budget,
        min_budget=min_budget,
        preferred_category=preferred_category,
        min_ram=min_ram,
        min_storage=min_storage,
        min_rating=min_rating
    )
    
    service = RecommendationService()
    return service.get_recommendations(preferences, limit)


@router.get(
    '/recommendations/best-deals',
    summary="Mejores ofertas del momento",
    description="""
    Retorna los productos con mejor relación calidad-precio sin necesidad de especificar preferencias.
    
    Criterios:
    - Alta calificación (≥4.0)
    - Precio razonable
    - Inferencias SWRL positivas
    """,
)
async def get_best_deals(limit: int = Query(5, ge=1, le=20)):
    """Mejores ofertas generales"""
    # Preferencias por defecto para ofertas
    default_prefs = UserPreferences(
        min_rating=4.0,
        budget=2000  # Límite razonable
    )
    
    service = RecommendationService()
    result = service.get_recommendations(default_prefs, limit)
    
    return {
        **result,
        "message": "Mejores ofertas basadas en calificación y precio"
    }

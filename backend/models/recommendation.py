"""
Schemas de Recomendaciones
"""
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class UserPreferences(BaseModel):
    """Preferencias del usuario para recomendaciones"""
    budget: Optional[float] = Field(None, description="Presupuesto máximo del usuario")
    min_budget: Optional[float] = Field(None, description="Presupuesto mínimo")
    preferred_category: Optional[str] = Field(None, description="Categoría preferida (Laptop, Smartphone, etc.)")
    min_ram: Optional[int] = Field(None, description="RAM mínima deseada (GB)")
    min_storage: Optional[int] = Field(None, description="Almacenamiento mínimo (GB)")
    min_rating: Optional[float] = Field(None, description="Calificación mínima (0-5)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "budget": 1500,
                "min_budget": 800,
                "preferred_category": "Laptop",
                "min_ram": 8,
                "min_storage": 256,
                "min_rating": 4.0
            }
        }
    )


class RecommendationItem(BaseModel):
    """Item individual de recomendación"""
    product_id: str = Field(..., description="ID del producto")
    product_name: Optional[str] = Field(None, description="Nombre del producto")
    image_url: Optional[str] = Field(None, description="URL de la imagen del producto")
    score: float = Field(..., description="Score de recomendación (0-100)")
    reason: str = Field(..., description="Razón de la recomendación")
    match_percentage: float = Field(..., description="Porcentaje de coincidencia con preferencias")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "product_id": "iPhone15_Barato",
                "score": 87.5,
                "reason": "Se ajusta a tu presupuesto y tiene excelente calificación",
                "match_percentage": 92.0
            }
        }
    )


class RecommendationResponse(BaseModel):
    """Respuesta con recomendaciones personalizadas"""
    success: bool = True
    total_matches: int = Field(..., description="Total de productos que coinciden")
    recommendations: List[RecommendationItem] = Field(default_factory=list)
    preferences_used: UserPreferences = Field(..., description="Preferencias aplicadas")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "total_matches": 5,
                "recommendations": [
                    {
                        "product_id": "Laptop_Dell_XPS",
                        "score": 95.5,
                        "reason": "Alta RAM, excelente calificación y dentro de presupuesto",
                        "match_percentage": 98.0
                    }
                ],
                "preferences_used": {
                    "budget": 1500,
                    "preferred_category": "Laptop"
                }
            }
        }
    )

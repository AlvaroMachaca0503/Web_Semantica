"""
Schemas de Comparación
"""
from typing import List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class CompareRequest(BaseModel):
    """Request para comparar productos"""
    products: List[str] = Field(
        ..., 
        min_length=2,
        max_length=5,
        description="Lista de IDs de productos a comparar (2-5 productos)"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "products": ["iPhone15_Barato", "iPhone15_Caro"]
            }
        }
    )


class ComparisonResponse(BaseModel):
    """Resultado de comparación entre productos"""
    success: bool = True
    comparison: Dict[str, Any] = Field(..., description="Datos de comparación")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "comparison": {
                    "products": [],
                    "winner": "iPhone15_Barato",
                    "reason": "Mejor precio",
                    "swrl_inference": {
                        "esMejorOpcionQue": True
                    }
                }
            }
        }
    )

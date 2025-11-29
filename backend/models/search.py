"""
Schemas de Búsqueda
"""
from typing import List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class SearchResponse(BaseModel):
    """Resultados de búsqueda con SPARQL"""
    success: bool = True
    query: str = Field(..., description="Query de búsqueda ejecutada")
    count: int = Field(..., description="Número de resultados")
    results: List[Dict[str, Any]] = Field(default_factory=list, description="Productos encontrados")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "query": "laptop gaming",
                "count": 3,
                "results": []
            }
        }
    )

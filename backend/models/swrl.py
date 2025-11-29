"""
Schemas SWRL
"""
from typing import List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class SWRLResultResponse(BaseModel):
    """Resultado de regla SWRL"""
    success: bool = True
    rule: str = Field(..., description="Nombre de la regla SWRL")
    count: int = Field(..., description="Número de resultados")
    results: List[Dict[str, Any]] = Field(default_factory=list, description="Productos que cumplen la regla")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "rule": "DetectarGamer",
                "count": 1,
                "results": [
                    {
                        "id": "Laptop_Dell_XPS",
                        "types": ["LaptopGamer"],
                        "properties": {"tieneRAM_GB": 16}
                    }
                ]
            }
        }
    )

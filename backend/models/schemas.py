"""
Schemas Pydantic para validación automática y documentación Swagger
SmartCompareMarket - FastAPI Backend
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


# ==================== Respuestas Base ====================

class ErrorResponse(BaseModel):
    """Respuesta estándar de error"""
    success: bool = False
    error: str = Field(..., description="Mensaje de error")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": False,
                "error": "Producto no encontrado"
            }
        }
    )


class SuccessResponse(BaseModel):
    """Respuesta genérica exitosa"""
    success: bool = True
    message: str = Field(..., description="Mensaje de éxito")


# ==================== Productos ====================

class ProductResponse(BaseModel):
    """Producto individual con todas sus propiedades"""
    id: str = Field(..., description="ID único del producto")
    types: List[str] = Field(default_factory=list, description="Tipos/Clases del producto")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Propiedades del producto")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "iPhone15_Barato",
                "types": ["Smartphone", "Dispositivo_Móvil", "Electrónica", "Producto"],
                "properties": {
                    "tieneNombre": "iPhone 15 Pro",
                    "tienePrecio": 950.0,
                    "tieneRAM_GB": 8,
                    "tieneAlmacenamiento_GB": 256,
                    "tieneCalificacion": 4.5,
                    "vendidoPor": "Vend_JuanPerez"
                }
            }
        }
    )


class ProductListResponse(BaseModel):
    """Lista de productos con metadatos"""
    success: bool = True
    count: int = Field(..., description="Número de productos retornados")
    data: List[Dict[str, Any]] = Field(default_factory=list, description="Lista de productos")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "count": 2,
                "data": [
                    {
                        "id": "iPhone15_Barato",
                        "types": ["Smartphone", "Electrónica"],
                        "properties": {"tieneNombre": "iPhone 15 Pro", "tienePrecio": 950.0}
                    }
                ]
            }
        }
    )


# ==================== Comparación ====================

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


class ProductDifference(BaseModel):
    """Diferencia entre dos valores de propiedades"""
    property_name: str
    values: List[Any]
    difference: Optional[str] = None


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
                    "reason": "Mejor precio para el mismo producto",
                    "differences": {
                        "tienePrecio": "950 vs 1200 (-$250)"
                    },
                    "swrl_inference": {
                        "esMejorOpcionQue": True,
                        "rule": "EncontrarMejorPrecio"
                    }
                }
            }
        }
    )


# ==================== Búsqueda ====================

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


# ==================== Relaciones ====================

class ProductRelation(BaseModel):
    """Relación entre productos"""
    id: str = Field(..., description="ID del producto relacionado")
    name: str = Field(..., description="Nombre del producto")
    relation: str = Field(..., description="Tipo de relación (esCompatibleCon, esSimilarA, etc.)")


class RelationshipResponse(BaseModel):
    """Todas las relaciones de un producto"""
    success: bool = True
    product_id: str = Field(..., description="ID del producto consultado")
    compatible: List[ProductRelation] = Field(default_factory=list)
    incompatible: List[ProductRelation] = Field(default_factory=list)
    similar: List[ProductRelation] = Field(default_factory=list)
    better_than: List[ProductRelation] = Field(default_factory=list)
    worse_than: List[ProductRelation] = Field(default_factory=list)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "product_id": "iPhone15_Barato",
                "compatible": [
                    {"id": "Funda_iPhone15", "name": "Funda iPhone 15", "relation": "esCompatibleCon"}
                ],
                "incompatible": [],
                "similar": [],
                "better_than": [
                    {"id": "iPhone15_Caro", "name": "iPhone 15 Pro", "relation": "esMejorOpcionQue"}
                ],
                "worse_than": []
            }
        }
    )


# ==================== SWRL ====================

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
                        "types": ["LaptopGamer", "Laptop", "Computadora"],
                        "properties": {"tieneRAM_GB": 16}
                    }
                ]
            }
        }
    )

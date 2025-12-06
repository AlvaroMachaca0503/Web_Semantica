"""
Schemas de Productos
Separados para mejor mantenibilidad
"""
from typing import List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


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
                    "vendidoPor": "Vend_JuanPerez",
                    "tieneDescuento": 10.0,
                    "procesadorModelo": "A17 Pro",
                    "resolucionPantalla": "2556x1179",
                    "pesoGramos": 187
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


class SingleProductResponse(BaseModel):
    """Respuesta de un solo producto"""
    success: bool = True
    data: ProductResponse = Field(..., description="Datos del producto")


class ProductRelation(BaseModel):
    """Relación entre productos"""
    id: str = Field(..., description="ID del producto relacionado")
    name: str = Field(..., description="Nombre del producto")
    relation: str = Field(..., description="Tipo de relación")


class RelationshipResponse(BaseModel):
    """Todas las relaciones de un producto"""
    success: bool = True
    product_id: str = Field(..., description="ID del producto consultado")
    compatible: List[ProductRelation] = Field(default_factory=list)
    incompatible: List[ProductRelation] = Field(default_factory=list)
    similar: List[ProductRelation] = Field(default_factory=list)
    better_than: List[ProductRelation] = Field(default_factory=list)
    worse_than: List[ProductRelation] = Field(default_factory=list)

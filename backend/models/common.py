"""
Schemas Comunes - Base responses y errores
Separación de schemas para mejor mantenibilidad
"""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class BaseResponse(BaseModel):
    """Respuesta base con success flag"""
    success: bool = True
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True
            }
        }
    )


class ErrorResponse(BaseModel):
    """Respuesta estándar de error"""
    success: bool = False
    error: str = Field(..., description="Mensaje de error")
    code: Optional[str] = Field(None, description="Código de error")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": False,
                "error": "Producto no encontrado",
                "code": "NOT_FOUND"
            }
        }
    )


class SuccessResponse(BaseModel):
    """Respuesta genérica exitosa"""
    success: bool = True
    message: str = Field(..., description="Mensaje de éxito")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Operación completada exitosamente"
            }
        }
    )


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Estado del servicio")
    service: str = Field(..., description="Nombre del servicio")
    version: str = Field(default="2.0.0", description="Versión de la API")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "service": "SmartCompareMarket",
                "version": "2.0.0"
            }
        }
    )

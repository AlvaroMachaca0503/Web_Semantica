"""
Router de Validación - Endpoints para validar consistencia de productos
"""
from fastapi import APIRouter, Depends
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dependencies import get_product_service
from services.validation_service import ValidationService
from models.common import ErrorResponse

router = APIRouter()


@router.get(
    '/validation/product/{product_id}',
    summary="Validar producto individual",
    description="""
    Valida la consistencia de especificaciones de un producto específico.
    
    **Detecta:**
    - Valores fuera de rango (RAM > 512GB, precio negativo)
    - Contradicciones lógicas (smartphone con RAM excesiva)
    - Especificaciones incompatibles
    
    **Ejemplo:**
    ```
    GET /api/v1/validation/product/iPhone15_Barato
    ```
    """,
    responses={
        200: {
            "description": "Validación completada",
            "content": {
                "application/json": {
                    "example": {
                        "valid": True,
                        "product_id": "iPhone15_Barato",
                        "errors": [],
                        "warnings": [],
                        "total_issues": 0
                    }
                }
            }
        }
    }
)
async def validate_product(product_id: str):
    """Valida consistencia de un producto"""
    validation_service = ValidationService()
    return validation_service.validate_product(product_id)


@router.get(
    '/validation/all',
    summary="Validar todos los productos",
    description="""
    Ejecuta validación de consistencia en todos los productos del catálogo.
    
    **Retorna:**
    - Total de productos válidos
    - Total con errores críticos
    - Total con advertencias
    - Detalles de cada producto
    
    **Útil para:**
    - Auditoría de calidad de datos
    - Detección de errores en masa
    """,
)
async def validate_all_products():
    """Valida todos los productos"""
    validation_service = ValidationService()
    return validation_service.validate_all_products()


@router.get(
    '/validation/summary',
    summary="Resumen de validación",
    description="""
    Retorna un resumen ejecutivo de la validación sin detalles.
    Más rápido que /validation/all para dashboards.
    """,
)
async def validation_summary():
    """Resumen rápido de validación"""
    validation_service = ValidationService()
    full_validation = validation_service.validate_all_products()
    
    return {
        "total_products": full_validation['total_products'],
        "valid": full_validation['valid'],
        "with_errors": full_validation['with_errors'],
        "with_warnings": full_validation['with_warnings'],
        "health_score": round(
            (full_validation['valid'] / full_validation['total_products']) * 100, 2
        ) if full_validation['total_products'] > 0 else 0
    }

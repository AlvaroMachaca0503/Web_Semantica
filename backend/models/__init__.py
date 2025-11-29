"""
Modelos Pydantic para validación y serialización
Organizados por dominio para mejor mantenibilidad
"""

# Common schemas
from .common import (
    BaseResponse,
    ErrorResponse,
    SuccessResponse,
    HealthResponse
)

# Product schemas
from .product import (
    ProductResponse,
    ProductListResponse,
    ProductRelation,
    RelationshipResponse
)

# Comparison schemas
from .comparison import (
    CompareRequest,
    ComparisonResponse
)

# SWRL schemas
from .swrl import (
    SWRLResultResponse
)

# Search schemas
from .search import (
    SearchResponse
)

__all__ = [
    # Common
    "BaseResponse",
    "ErrorResponse",
    "SuccessResponse",
    "HealthResponse",
    # Products
    "ProductResponse",
    "ProductListResponse",
    "ProductRelation",
    "RelationshipResponse",
    # Comparison
    "CompareRequest",
    "ComparisonResponse",
    # SWRL
    "SWRLResultResponse",
    # Search
    "SearchResponse"
]

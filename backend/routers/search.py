"""
Router de Búsqueda - FastAPI (DÍA 2)
Búsqueda avanzada con SPARQL
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.schemas import SearchResponse
from sparql.queries import SPARQLQueries
from sparql.filters import SPARQLFilters

router = APIRouter()
sparql_queries = SPARQLQueries()
sparql_filters = SPARQLFilters()


@router.get(
    '/search',
    response_model=SearchResponse,
    summary="Búsqueda avanzada",
    description="""
    Búsqueda avanzada de productos usando **consultas SPARQL**.
    
    ## Parámetros de búsqueda:
    
    - `q`: Texto a buscar en nombres de productos
    - `category`: Filtrar por categoría
    - `min_price`: Precio mínimo
    - `max_price`: Precio máximo
    - `min_ram`: RAM mínima (GB)
    - `sort_by`: Ordenar por 'price', 'rating', 'ram'
    - `sort_order`: 'asc' o 'desc'
    
    ## Ejemplos:
    
    ```
    GET /api/search?q=laptop&min_ram=16&sort_by=price
    GET /api/search?category=Smartphone&min_price=500&max_price=1000
    GET /api/search?q=gaming&sort_by=rating&sort_order=desc
    ```
    
    ## Ventajas de SPARQL:
    
    - Consultas semánticas complejas
    - Filtros combinados eficientes
    - Inferencias automáticas
    - Relaciones entre entidades
    """
)
async def search_products(
    q: Optional[str] = Query(
        None,
        description="Texto a buscar en nombres",
        example="laptop gaming"
    ),
    category: Optional[str] = Query(
        None,
        description="Categoría del producto",
        example="Laptop"
    ),
    min_price: Optional[float] = Query(
        None,
        ge=0,
        description="Precio mínimo",
        example=500.0
    ),
    max_price: Optional[float] = Query(
        None,
        ge=0,
        description="Precio máximo",
        example=2000.0
    ),
    min_ram: Optional[int] = Query(
        None,
        ge=0,
        description="RAM mínima en GB",
        example=16
    ),
    sort_by: Optional[str] = Query(
        None,
        description="Campo para ordenar (price, rating, ram)",
        example="price"
    ),
    sort_order: Optional[str] = Query(
        "asc",
        description="Orden (asc, desc)",
        example="asc"
    )
):
    """
    Búsqueda avanzada con filtros SPARQL
    """
    try:
        # Construir búsqueda
        results = sparql_queries.search_products(
            text_query=q,
            category=category,
            min_price=min_price,
            max_price=max_price,
            min_ram=min_ram
        )
        
        # Aplicar ordenamiento si se especificó
        if sort_by and results:
            results = sparql_filters.sort_results(
                results,
                sort_by=sort_by,
                ascending=(sort_order == "asc")
            )
        
        return SearchResponse(
            success=True,
            query=q or "all",
            count=len(results),
            results=results
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en búsqueda SPARQL: {str(e)}"
        )


@router.get(
    '/search/compatible/{product_id}',
    response_model=SearchResponse,
    summary="Buscar productos compatibles",
    description="""
    Busca productos compatibles con un producto específico usando SPARQL.
    
    Utiliza la propiedad `esCompatibleCon` de la ontología.
    
    **Ejemplo:**
    ```
    GET /api/search/compatible/iPhone15_Barato
    ```
    
    Retorna productos como fundas, cargadores, accesorios compatibles.
    """
)
async def search_compatible_products(
    product_id: str
):
    """
    Busca productos compatibles usando SPARQL
    """
    try:
        results = sparql_queries.get_compatible_products(product_id)
        
        return SearchResponse(
            success=True,
            query=f"compatible with {product_id}",
            count=len(results),
            results=results
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error buscando compatibles: {str(e)}"
        )

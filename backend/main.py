"""
SmartCompareMarket - FastAPI Backend
Marketplace Semántico con Ontologías OWL y Razonamiento SWRL

Autores: Álvaro y Jony
Nivel: 2
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import config

# Importar routers
from routers import products, swrl, compare, search, validation, recommendations, equivalences, market, classify


def create_app() -> FastAPI:
    """Factory para crear la aplicación FastAPI"""
    
    app = FastAPI(
        title="SmartCompareMarket API",
        description="""
        API de Marketplace Semántico con comparación inteligente de productos.
        
        ## Características principales:
        
        * **Ontología OWL 2** con 48 clases y 60+ productos
        * **Razonamiento SWRL** con 4 reglas activas (HermiT)
        * **Comparación inteligente** basada en inferencias semánticas
        * **Consultas SPARQL** para búsqueda avanzada
        * **Detección automática** de compatibilidades e incompatibilidades
        
        ## Tecnologías:
        
        * FastAPI + Uvicorn
        * Owlready2 (OWL 2, SWRL)
        * RDFlib (SPARQL)
        * HermiT Reasoner
        
        ## Reglas SWRL Activas:
        
        1. **DetectarGamer**: Laptops con RAM ≥ 16GB → LaptopGamer
        2. **EncontrarMejorPrecio**: Mismo producto, menor precio → esMejorOpcionQue
        3. **ClasificarPositivas**: Calificación ≥ 4 → Reseña_Positiva
        4. **ClasificarNegativas**: Calificación ≤ 2 → Reseña_Negativa
        """,
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_tags=[
            {
                "name": "Productos",
                "description": "Gestión y consulta de productos"
            },
            {
                "name": "SWRL",
                "description": "Resultados de reglas SWRL e inferencias"
            },
            {
                "name": "Comparación",
                "description": "Comparación inteligente entre productos"
            },
            {
                "name": "Búsqueda",
                "description": "Búsqueda avanzada con SPARQL"
            },
            {
                "name": "Sistema",
                "description": "Endpoints de utilidad y estado"
            }
        ]
    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Registrar routers con versionado
    app.include_router(products.router, prefix="/api/v1", tags=["Productos"])
    app.include_router(swrl.router, prefix="/api/v1", tags=["SWRL"])
    app.include_router(compare.router, prefix="/api/v1", tags=["Comparación"])
    app.include_router(search.router, prefix="/api/v1", tags=["Búsqueda"])
    app.include_router(validation.router, prefix="/api/v1", tags=["Validación"])
    app.include_router(recommendations.router, prefix="/api/v1", tags=["Recomendaciones"])
    app.include_router(equivalences.router, prefix="/api/v1", tags=["Equivalencias"])
    app.include_router(market.router, tags=["Análisis de Mercado"])
    app.include_router(classify.router, tags=["Clasificación"])
    
    # Montar archivos estáticos (imágenes de productos)
    static_path = Path(__file__).parent / "static"
    if static_path.exists():
        app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    
    # Ruta raíz
    @app.get("/", tags=["Sistema"])
    async def root():
        """Endpoint raíz con información de la API"""
        return {
            "message": "SmartCompareMarket API",
            "version": "2.0.0",
            "framework": "FastAPI",
            "docs": "/docs",
            "redoc": "/redoc",
            "endpoints": {
                "products": "/api/v1/products",
                "product_by_id": "/api/v1/products/{id}",
                "product_relationships": "/api/v1/products/{id}/relationships",
                "swrl_best_price": "/api/v1/swrl/best-price",
                "swrl_gaming_laptops": "/api/v1/swrl/gaming-laptops",
                "swrl_positive_reviews": "/api/v1/swrl/positive-reviews",
                "swrl_negative_reviews": "/api/v1/swrl/negative-reviews",
                "compare": "/api/v1/compare",
                "search": "/api/v1/search"
            }
        }
    
    # Health check
    @app.get("/health", tags=["Sistema"])
    async def health():
        """Health check endpoint"""
        return {"status": "healthy", "service": "SmartCompareMarket"}
    
    return app


# Crear instancia de la aplicación
app = create_app()


# Para ejecutar con uvicorn
if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("[START] SmartCompareMarket Backend (FastAPI) - Iniciando...")
    print("=" * 70)
    print(f"\n[OK] Servidor corriendo en: http://{config.FLASK_CONFIG['host']}:{config.FLASK_CONFIG['port']}")
    print(f"[DOCS] Documentacion Swagger: http://localhost:{config.FLASK_CONFIG['port']}/docs")
    print(f"[DOCS] Documentacion ReDoc: http://localhost:{config.FLASK_CONFIG['port']}/redoc")
    print("\n[API] Endpoints disponibles:")
    print("   GET  /api/v1/products")
    print("   GET  /api/v1/products/{id}")
    print("   GET  /api/v1/products/{id}/relationships")
    print("   GET  /api/v1/swrl/best-price")
    print("   GET  /api/v1/swrl/gaming-laptops")
    print("   POST /api/v1/compare")
    print("   GET  /api/v1/search")
    print("\n[INFO] Presiona Ctrl+C para detener el servidor\n")
    print("=" * 70)
    
    uvicorn.run(
        "main:app",
        host=config.FLASK_CONFIG['host'],
        port=config.FLASK_CONFIG['port'],
        reload=True,
        log_level="info"
    )

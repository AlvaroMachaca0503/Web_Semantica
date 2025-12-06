"""
Dependencies para FastAPI - Dependency Injection
Mejora de arquitectura sin reestructuración completa
"""
from functools import lru_cache
from typing import Generator
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ontology.loader import get_ontology
from reasoning.inference_engine import InferenceEngine
from reasoning.product_classifier import ProductClassifier
from services.product_service import ProductService
from services.comparison_service import ComparisonService
from services.equivalence_service import EquivalenceService
from sparql.queries import SPARQLQueries
from sparql.filters import SPARQLFilters
from sparql.market_analysis import MarketAnalysis
from reasoning.swrl_engine import SWRLEngine


# ==================== Ontology ====================

@lru_cache()
def get_ontology_instance():
    """
    Singleton de la ontología.
    La ontología se carga una sola vez y se reutiliza.
    """
    return get_ontology()


# ==================== Services ====================

@lru_cache()
def get_product_service() -> ProductService:
    """Dependency para ProductService"""
    return ProductService()


@lru_cache()
def get_comparison_service() -> ComparisonService:
    """Dependency para ComparisonService"""
    return ComparisonService()


@lru_cache()
def get_equivalence_service() -> EquivalenceService:
    """Dependency para EquivalenceService"""
    return EquivalenceService()


# ==================== SPARQL ====================

@lru_cache()
def get_sparql_queries() -> SPARQLQueries:
    """Dependency para SPARQLQueries"""
    return SPARQLQueries()


@lru_cache()
def get_sparql_filters() -> SPARQLFilters:
    """Dependency para SPARQLFilters"""
    return SPARQLFilters()


@lru_cache()
def get_market_analysis() -> MarketAnalysis:
    """Dependency para MarketAnalysis"""
    return MarketAnalysis()


# ==================== Reasoning ====================

@lru_cache()
def get_inference_engine() -> InferenceEngine:
    """Dependency para InferenceEngine"""
    onto = get_ontology_instance()
    return InferenceEngine(onto)


@lru_cache()
def get_swrl_engine() -> SWRLEngine:
    """Dependency para SWRLEngine"""
    return SWRLEngine()


@lru_cache()
def get_product_classifier() -> ProductClassifier:
    """Dependency para ProductClassifier"""
    return ProductClassifier()


# ==================== Helpers para Testing ====================

def override_dependency(app, original_dep, override_dep):
    """
    Helper para sobrescribir dependencies en tests.
    
    Uso:
        override_dependency(app, get_product_service, mock_product_service)
    """
    app.dependency_overrides[original_dep] = override_dep

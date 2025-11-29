"""
Consultas SPARQL - DÍA 2
Consultas semánticas básicas usando RDFlib
"""
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.plugins.sparql import prepareQuery

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ontology.loader import get_ontology
from utils.owl_helpers import individual_to_dict


class SPARQLQueries:
    """
    Clase para ejecutar consultas SPARQL sobre la ontología.
    """
    
    def __init__(self):
        self.onto = get_ontology()
        self.graph = None
        self.ns = Namespace("http://smartcompare.com/ontologia#")
        self._init_graph()
    
    def _init_graph(self):
        """Convierte la ontología OWL a un grafo RDF lib."""
        try:
            # Convertir ontología a RDFlib Graph
            self.graph = self.onto.world.as_rdflib_graph()
            print(f"✅ Ontología cargada en RDFlib: {len(self.graph)} triples")
        except Exception as e:
            print(f"⚠️ Error cargando grafo RDF: {e}")
            # Fallback: crear grafo vacío
            self.graph = Graph()
    
    def query_products_by_price(
        self,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Dict]:
        """
        Consulta SPARQL para filtrar productos por rango de precio.
        
        Args:
            min_price: Precio mínimo
            max_price: Precio máximo
            
        Returns:
            Lista de productos que cumplen el filtro
        """
        # Si no hay filtros, retornar todos
        if min_price is None and max_price is None:
            return self._get_all_products_from_onto()
        
        # Construir query SPARQL
        query_parts = [
            "PREFIX ns: <http://smartcompare.com/ontologia#>",
            "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
            "SELECT ?product ?price WHERE {",
            "  ?product ns:tienePrecio ?price .",
        ]
        
        # Agregar filtros
        if min_price is not None:
            query_parts.append(f"  FILTER (?price >= {min_price})")
        if max_price is not None:
            query_parts.append(f"  FILTER (?price <= {max_price})")
        
        query_parts.append("}")
        
        sparql_query = "\n".join(query_parts)
        
        # Ejecutar query
        try:
            results = self.graph.query(sparql_query)
            return self._process_sparql_results(results)
        except Exception as e:
            print(f"Error en consulta SPARQL: {e}")
            # Fallback a filtrado manual
            return self._filter_by_price_manual(min_price, max_price)
    
    def query_products_by_ram(self, min_ram: int) -> List[Dict]:
        """
        Consulta SPARQL para productos con RAM mínima.
        
        Args:
            min_ram: RAM mínima en GB
            
        Returns:
            Lista de productos con RAM >= min_ram
        """
        sparql_query = f"""
        PREFIX ns: <http://smartcompare.com/ontologia#>
        
        SELECT ?product ?ram WHERE {{
            ?product ns:tieneRAM_GB ?ram .
            FILTER (?ram >= {min_ram})
        }}
        """
        
        try:
            results = self.graph.query(sparql_query)
            return self._process_sparql_results(results)
        except Exception as e:
            print(f"Error en consulta SPARQL: {e}")
            return self._filter_by_ram_manual(min_ram)
    
    def query_products_by_vendor(self, vendor_name: str) -> List[Dict]:
        """
        Consulta SPARQL para productos de un vendedor específico.
        
        Args:
            vendor_name: Nombre del vendedor
            
        Returns:
            Lista de productos del vendedor
        """
        # TODO: Implementar cuando la ontología tenga vendedores
        return []
    
    def get_compatible_products(self, product_id: str) -> List[Dict]:
        """
        Consulta SPARQL para obtener productos compatibles.
        
        Args:
            product_id: ID del producto
            
        Returns:
            Lista de productos compatibles
        """
        from reasoning.inference_engine import InferenceEngine
        
        engine = InferenceEngine(self.onto)
        compatible = engine.get_compatible_products(product_id)
        
        # Convertir a formato completo
        results = []
        for comp in compatible:
            product_data = individual_to_dict(
                self.onto.search_one(iri=f"*{comp['id']}")
            )
            if product_data:
                results.append(product_data)
        
        return results
    
    def search_products(
        self,
        text_query: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_ram: Optional[int] = None
    ) -> List[Dict]:
        """
        Búsqueda combinada con múltiples filtros.
        
        Args:
            text_query: Texto a buscar en nombres
            category: Categoría del producto
            min_price: Precio mínimo
            max_price: Precio máximo
            min_ram: RAM mínima
            
        Returns:
            Lista de productos que cumplen todos los filtros
        """
        # Empezar con todos los productos
        from services.product_service import ProductService
        service = ProductService()
        
        if category:
            results = service.get_products_by_category(category)
        else:
            results = service.get_all_products()
        
        # Aplicar filtro de texto
        if text_query:
            text_query_lower = text_query.lower()
            results = [
                p for p in results
                if text_query_lower in p.get('properties', {}).get('tieneNombre', '').lower()
            ]
        
        # Aplicar filtro de precio
        if min_price is not None or max_price is not None:
            filtered = []
            for product in results:
                price = product.get('properties', {}).get('tienePrecio')
                if price is None:
                    continue
                if min_price is not None and price < min_price:
                    continue
                if max_price is not None and price > max_price:
                    continue
                filtered.append(product)
            results = filtered
        
        # Aplicar filtro de RAM
        if min_ram is not None:
            results = [
                p for p in results
                if p.get('properties', {}).get('tieneRAM_GB', 0) >= min_ram
            ]
        
        return results
    
    def _process_sparql_results(self, results) -> List[Dict]:
        """Procesa resultados de SPARQL y convierte a formato estándar."""
        product_ids = set()
        
        for row in results:
            # Extraer ID del producto del URI
            product_uri = str(row.product)
            product_id = product_uri.split('#')[-1]
            product_ids.add(product_id)
        
        # Obtener datos completos de cada producto
        products = []
        for product_id in product_ids:
            product = self.onto.search_one(iri=f"*{product_id}")
            if product:
                products.append(individual_to_dict(product))
        
        return products
    
    def _get_all_products_from_onto(self) -> List[Dict]:
        """Obtiene todos los productos de la ontología."""
        from services.product_service import ProductService
        service = ProductService()
        return service.get_all_products()
    
    def _filter_by_price_manual(
        self,
        min_price: Optional[float],
        max_price: Optional[float]
    ) -> List[Dict]:
        """Fallback manual para filtrado por precio."""
        products = self._get_all_products_from_onto()
        
        filtered = []
        for product in products:
            price = product.get('properties', {}).get('tienePrecio')
            if price is None:
                continue
            
            if min_price is not None and price < min_price:
                continue
            if max_price is not None and price > max_price:
                continue
            
            filtered.append(product)
        
        return filtered
    
    def _filter_by_ram_manual(self, min_ram: int) -> List[Dict]:
        """Fallback manual para filtrado por RAM."""
        products = self._get_all_products_from_onto()
        
        return [
            p for p in products
            if p.get('properties', {}).get('tieneRAM_GB', 0) >= min_ram
        ]

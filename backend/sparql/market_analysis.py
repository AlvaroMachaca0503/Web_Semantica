"""
Análisis de Mercado con SPARQL - SmartCompareMarket
Consultas avanzadas para estadísticas y análisis de datos del marketplace.

Autor: Álvaro Machaca
Fecha: Diciembre 2024
"""

from typing import List, Dict, Optional, Any
import logging
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.plugins.sparql import prepareQuery
from collections import defaultdict
import statistics

from ontology.loader import get_ontology
from utils.owl_helpers import individual_to_dict

logger = logging.getLogger(__name__)


class MarketAnalysis:
    """
    Servicio de análisis de mercado usando consultas SPARQL avanzadas.
    
    Proporciona estadísticas agregadas sobre:
    - Precios (promedio, mediana, distribución)
    - Categorías (conteo, distribución)
    - Especificaciones técnicas
    - Tendencias de mercado
    """
    
    def __init__(self):
        """Inicializa el servicio de análisis de mercado."""
        self.onto = get_ontology()
        self.graph = None
        self.ns = Namespace("http://smartcompare.com/ontologia#")
        self._init_graph()
        logger.info("MarketAnalysis inicializado correctamente")
    
    def _init_graph(self):
        """Convierte la ontología a un grafo RDFlib para consultas SPARQL."""
        try:
            from rdflib import RDF, RDFS, OWL
            
            self.graph = Graph()
            
            # Cargar ontología en RDFlib
            owl_file = self.onto.world.filename
            if owl_file:
                self.graph.parse(owl_file, format="xml")
                logger.info(f"Grafo RDF cargado: {len(self.graph)} triples")
            else:
                logger.warning("No se pudo cargar archivo OWL en RDFlib")
        except Exception as e:
            logger.error(f"Error al inicializar grafo RDF: {e}")
            self.graph = None
    
    def get_price_statistics(self) -> Dict:
        """
        Obtiene estadísticas de precios del mercado.
        
        Returns:
            Diccionario con:
            - average: Precio promedio
            - median: Precio mediano
            - min: Precio mínimo
            - max: Precio máximo
            - std_dev: Desviación estándar
            - price_ranges: Distribución por rangos
        """
        try:
            # Obtener todos los productos con precios
            products = list(self.onto.Producto.instances())
            prices = []
            
            for product in products:
                product_dict = individual_to_dict(product)
                props = product_dict.get("properties", {})
                price = props.get("tienePrecio", 0)
                if price > 0:
                    prices.append(float(price))
            
            if not prices:
                return {
                    "error": "No hay productos con precios en el sistema",
                    "count": 0
                }
            
            # Calcular estadísticas
            avg_price = statistics.mean(prices)
            median_price = statistics.median(prices)
            min_price = min(prices)
            max_price = max(prices)
            std_dev = statistics.stdev(prices) if len(prices) > 1 else 0
            
            # Distribución por rangos
            price_ranges = self._calculate_price_distribution(prices)
            
            return {
                "total_products": len(prices),
                "average": round(avg_price, 2),
                "median": round(median_price, 2),
                "min": round(min_price, 2),
                "max": round(max_price, 2),
                "std_deviation": round(std_dev, 2),
                "price_ranges": price_ranges,
                "currency": "USD"
            }
            
        except Exception as e:
            logger.error(f"Error al calcular estadísticas de precios: {e}")
            return {"error": str(e)}
    
    def _calculate_price_distribution(self, prices: List[float]) -> Dict:
        """Calcula la distribución de precios en rangos."""
        ranges = {
            "0-500": 0,
            "500-1000": 0,
            "1000-1500": 0,
            "1500-2000": 0,
            "2000+": 0
        }
        
        for price in prices:
            if price < 500:
                ranges["0-500"] += 1
            elif price < 1000:
                ranges["500-1000"] += 1
            elif price < 1500:
                ranges["1000-1500"] += 1
            elif price < 2000:
                ranges["1500-2000"] += 1
            else:
                ranges["2000+"] += 1
        
        # Convertir a porcentajes
        total = len(prices)
        return {
            range_name: {
                "count": count,
                "percentage": round(count / total * 100, 2)
            }
            for range_name, count in ranges.items()
        }
    
    def get_category_distribution(self) -> Dict:
        """
        Obtiene la distribución de productos por categoría.
        
        Returns:
            Diccionario con conteo y porcentaje por categoría
        """
        try:
            products = list(self.onto.Producto.instances())
            category_counts = defaultdict(int)
            category_prices = defaultdict(list)
            
            for product in products:
                product_dict = individual_to_dict(product)
                types = product_dict.get("types", [])
                props = product_dict.get("properties", {})
                price = props.get("tienePrecio", 0)
                
                # Determinar categoría principal
                category = None
                for t in types:
                    if t in ["Laptop", "Smartphone", "Tablet", "Desktop", "Muebles", "Ropa", "Calzado"]:
                        category = t
                        break
                
                if category:
                    category_counts[category] += 1
                    if price > 0:
                        category_prices[category].append(float(price))
            
            total = sum(category_counts.values())
            
            # Construir respuesta con estadísticas por categoría
            categories = {}
            for cat, count in category_counts.items():
                cat_prices = category_prices[cat]
                categories[cat] = {
                    "count": count,
                    "percentage": round(count / total * 100, 2) if total > 0 else 0,
                    "avg_price": round(statistics.mean(cat_prices), 2) if cat_prices else 0,
                    "min_price": round(min(cat_prices), 2) if cat_prices else 0,
                    "max_price": round(max(cat_prices), 2) if cat_prices else 0
                }
            
            return {
                "total_products": total,
                "categories": categories,
                "unique_categories": len(category_counts)
            }
            
        except Exception as e:
            logger.error(f"Error al calcular distribución por categoría: {e}")
            return {"error": str(e)}
    
    def get_specs_analysis(self, category: Optional[str] = None) -> Dict:
        """
        Análisis de especificaciones técnicas (RAM, almacenamiento, etc.).
        
        Args:
            category: Filtrar por categoría específica (opcional)
            
        Returns:
            Estadísticas de especificaciones técnicas
        """
        try:
            products = list(self.onto.Producto.instances())
            
            ram_values = []
            storage_values = []
            screen_sizes = []
            battery_capacities = []
            
            for product in products:
                product_dict = individual_to_dict(product)
                types = product_dict.get("types", [])
                props = product_dict.get("properties", {})
                
                # Filtrar por categoría si se especifica
                if category:
                    if category not in types:
                        continue
                
                # Recopilar especificaciones
                ram = props.get("tieneRAM_GB", 0)
                if ram > 0:
                    ram_values.append(int(ram))
                
                storage = props.get("tieneAlmacenamiento_GB", 0)
                if storage > 0:
                    storage_values.append(int(storage))
                
                screen = props.get("tienePulgadas", 0)
                if screen > 0:
                    screen_sizes.append(float(screen))
                
                battery = props.get("bateriaCapacidad_mAh", 0)
                if battery > 0:
                    battery_capacities.append(int(battery))
            
            result = {
                "category": category or "all",
                "total_analyzed": len(products) if not category else len(ram_values)
            }
            
            # Estadísticas de RAM
            if ram_values:
                result["ram_gb"] = {
                    "average": round(statistics.mean(ram_values), 2),
                    "median": statistics.median(ram_values),
                    "min": min(ram_values),
                    "max": max(ram_values),
                    "most_common": max(set(ram_values), key=ram_values.count),
                    "distribution": self._get_value_distribution(ram_values)
                }
            
            # Estadísticas de almacenamiento
            if storage_values:
                result["storage_gb"] = {
                    "average": round(statistics.mean(storage_values), 2),
                    "median": statistics.median(storage_values),
                    "min": min(storage_values),
                    "max": max(storage_values),
                    "most_common": max(set(storage_values), key=storage_values.count),
                    "distribution": self._get_value_distribution(storage_values)
                }
            
            # Estadísticas de pantalla
            if screen_sizes:
                result["screen_inches"] = {
                    "average": round(statistics.mean(screen_sizes), 2),
                    "median": round(statistics.median(screen_sizes), 2),
                    "min": round(min(screen_sizes), 2),
                    "max": round(max(screen_sizes), 2)
                }
            
            # Estadísticas de batería
            if battery_capacities:
                result["battery_mAh"] = {
                    "average": round(statistics.mean(battery_capacities), 2),
                    "median": statistics.median(battery_capacities),
                    "min": min(battery_capacities),
                    "max": max(battery_capacities)
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Error en análisis de especificaciones: {e}")
            return {"error": str(e)}
    
    def _get_value_distribution(self, values: List[int]) -> Dict:
        """Obtiene la distribución de valores únicos."""
        from collections import Counter
        counter = Counter(values)
        total = len(values)
        
        return {
            str(value): {
                "count": count,
                "percentage": round(count / total * 100, 2)
            }
            for value, count in counter.most_common(10)  # Top 10
        }
    
    def get_best_value_products(self, limit: int = 10) -> Dict:
        """
        Identifica productos con mejor relación calidad-precio.
        
        Algoritmo:
        - Score = (RAM + Storage/10 + Screen*10 + Rating*10) / Price
        - Mayor score = mejor valor
        
        Args:
            limit: Número máximo de productos a retornar
            
        Returns:
            Lista de productos con mejor valor
        """
        try:
            products = list(self.onto.Producto.instances())
            best_values = []
            
            for product in products:
                product_dict = individual_to_dict(product)
                props = product_dict.get("properties", {})
                
                price = props.get("tienePrecio", 0)
                if price <= 0:
                    continue
                
                # Calcular score de valor
                ram = props.get("tieneRAM_GB", 0)
                storage = props.get("tieneAlmacenamiento_GB", 0)
                screen = props.get("tienePulgadas", 0)
                rating = props.get("tieneCalificacion", 0)
                
                # Fórmula de valor
                value_score = (ram + storage/10 + screen*10 + rating*10) / price
                
                # Obtener nombre y categoría
                name = props.get("tieneNombre", product.name)
                if not isinstance(name, str):
                    name = product.name
                
                types = product_dict.get("types", [])
                category = None
                for t in types:
                    if t in ["Laptop", "Smartphone", "Tablet", "Desktop"]:
                        category = t
                        break
                
                best_values.append({
                    "id": product.name,
                    "name": name,
                    "category": category or "Desconocida",
                    "price": float(price),
                    "value_score": round(value_score, 4),
                    "specs": {
                        "ram_gb": ram,
                        "storage_gb": storage,
                        "screen_inches": screen,
                        "rating": rating
                    }
                })
            
            # Ordenar por value_score descendente
            best_values.sort(key=lambda x: x["value_score"], reverse=True)
            
            return {
                "total_analyzed": len(best_values),
                "best_value_products": best_values[:limit],
                "algorithm": "value_score = (RAM + Storage/10 + Screen*10 + Rating*10) / Price"
            }
            
        except Exception as e:
            logger.error(f"Error al calcular mejor valor: {e}")
            return {"error": str(e)}
    
    def get_market_trends(self) -> Dict:
        """
        Analiza tendencias del mercado.
        
        Returns:
            Análisis de tendencias:
            - Productos premium vs económicos
            - Especificaciones más comunes
            - Gaps en el mercado
        """
        try:
            products = list(self.onto.Producto.instances())
            
            # Clasificar productos por precio
            premium = []  # > $1500
            mid_range = []  # $800-$1500
            budget = []  # < $800
            
            for product in products:
                product_dict = individual_to_dict(product)
                props = product_dict.get("properties", {})
                price = props.get("tienePrecio", 0)
                
                if price > 1500:
                    premium.append(product_dict)
                elif price >= 800:
                    mid_range.append(product_dict)
                elif price > 0:
                    budget.append(product_dict)
            
            total = len(premium) + len(mid_range) + len(budget)
            
            # Especificaciones más comunes
            ram_common = defaultdict(int)
            storage_common = defaultdict(int)
            
            for product in products:
                product_dict = individual_to_dict(product)
                props = product_dict.get("properties", {})
                
                ram = props.get("tieneRAM_GB", 0)
                if ram > 0:
                    ram_common[ram] += 1
                
                storage = props.get("tieneAlmacenamiento_GB", 0)
                if storage > 0:
                    storage_common[storage] += 1
            
            return {
                "price_segments": {
                    "premium": {
                        "count": len(premium),
                        "percentage": round(len(premium) / total * 100, 2) if total > 0 else 0,
                        "price_range": "> $1500"
                    },
                    "mid_range": {
                        "count": len(mid_range),
                        "percentage": round(len(mid_range) / total * 100, 2) if total > 0 else 0,
                        "price_range": "$800-$1500"
                    },
                    "budget": {
                        "count": len(budget),
                        "percentage": round(len(budget) / total * 100, 2) if total > 0 else 0,
                        "price_range": "< $800"
                    }
                },
                "most_common_specs": {
                    "ram_gb": sorted(ram_common.items(), key=lambda x: x[1], reverse=True)[:5],
                    "storage_gb": sorted(storage_common.items(), key=lambda x: x[1], reverse=True)[:5]
                },
                "market_insights": self._generate_market_insights(
                    len(premium), len(mid_range), len(budget), 
                    ram_common, storage_common
                )
            }
            
        except Exception as e:
            logger.error(f"Error en análisis de tendencias: {e}")
            return {"error": str(e)}
    
    def _generate_market_insights(
        self, 
        premium_count: int, 
        mid_count: int, 
        budget_count: int,
        ram_common: Dict,
        storage_common: Dict
    ) -> List[str]:
        """Genera insights automáticos del mercado."""
        insights = []
        
        total = premium_count + mid_count + budget_count
        if total == 0:
            return ["No hay datos suficientes para generar insights"]
        
        # Insight 1: Segmento dominante
        if premium_count > mid_count and premium_count > budget_count:
            insights.append(f"El mercado está orientado a productos premium ({round(premium_count/total*100, 1)}% del catálogo)")
        elif mid_count > premium_count and mid_count > budget_count:
            insights.append(f"La mayoría de productos están en rango medio ({round(mid_count/total*100, 1)}% del catálogo)")
        else:
            insights.append(f"Predominan productos económicos ({round(budget_count/total*100, 1)}% del catálogo)")
        
        # Insight 2: RAM más común
        if ram_common:
            most_common_ram = max(ram_common.items(), key=lambda x: x[1])
            insights.append(f"El estándar de RAM más común es {most_common_ram[0]}GB ({most_common_ram[1]} productos)")
        
        # Insight 3: Almacenamiento más común
        if storage_common:
            most_common_storage = max(storage_common.items(), key=lambda x: x[1])
            insights.append(f"El almacenamiento estándar es {most_common_storage[0]}GB ({most_common_storage[1]} productos)")
        
        return insights
    
    def compare_categories(self, category1: str, category2: str) -> Dict:
        """
        Compara dos categorías de productos.
        
        Args:
            category1: Primera categoría
            category2: Segunda categoría
            
        Returns:
            Comparación detallada entre categorías
        """
        try:
            cat1_stats = self.get_specs_analysis(category1)
            cat2_stats = self.get_specs_analysis(category2)
            
            if "error" in cat1_stats or "error" in cat2_stats:
                return {"error": "Una o ambas categorías no tienen datos suficientes"}
            
            comparison = {
                "category1": category1,
                "category2": category2,
                "comparison": {}
            }
            
            # Comparar RAM
            if "ram_gb" in cat1_stats and "ram_gb" in cat2_stats:
                comparison["comparison"]["ram_gb"] = {
                    category1: cat1_stats["ram_gb"]["average"],
                    category2: cat2_stats["ram_gb"]["average"],
                    "winner": category1 if cat1_stats["ram_gb"]["average"] > cat2_stats["ram_gb"]["average"] else category2
                }
            
            # Comparar almacenamiento
            if "storage_gb" in cat1_stats and "storage_gb" in cat2_stats:
                comparison["comparison"]["storage_gb"] = {
                    category1: cat1_stats["storage_gb"]["average"],
                    category2: cat2_stats["storage_gb"]["average"],
                    "winner": category1 if cat1_stats["storage_gb"]["average"] > cat2_stats["storage_gb"]["average"] else category2
                }
            
            # Comparar pantalla
            if "screen_inches" in cat1_stats and "screen_inches" in cat2_stats:
                comparison["comparison"]["screen_inches"] = {
                    category1: cat1_stats["screen_inches"]["average"],
                    category2: cat2_stats["screen_inches"]["average"],
                    "winner": category1 if cat1_stats["screen_inches"]["average"] > cat2_stats["screen_inches"]["average"] else category2
                }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error al comparar categorías: {e}")
            return {"error": str(e)}

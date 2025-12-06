"""
Servicio de Equivalencias Semánticas - SmartCompareMarket
Detecta y gestiona productos técnicamente equivalentes basándose en especificaciones.

Autor: Álvaro Machaca
Fecha: Diciembre 2024
"""

from typing import List, Dict, Optional, Set
import logging
from ontology.loader import get_ontology
from reasoning.inference_engine import InferenceEngine
from utils.owl_helpers import individual_to_dict

logger = logging.getLogger(__name__)


class EquivalenceService:
    """
    Servicio para detectar y gestionar equivalencias semánticas entre productos.
    
    Utiliza múltiples criterios:
    - Equivalencias explícitas en la ontología (esEquivalenteTecnico)
    - Detección automática basada en especificaciones similares
    - Inferencias SWRL del razonador Pellet
    """
    
    def __init__(self):
        """Inicializa el servicio de equivalencias."""
        self.onto = get_ontology()
        self.inference_engine = InferenceEngine(self.onto)
        logger.info("EquivalenceService inicializado correctamente")
    
    def find_equivalent_products(self, product_id: str) -> Dict:
        """
        Encuentra todos los productos equivalentes al producto dado.
        
        Combina:
        1. Equivalencias explícitas (esEquivalenteTecnico)
        2. Productos similares (esSimilarA)
        3. Equivalencias detectadas automáticamente
        
        Args:
            product_id: ID del producto
            
        Returns:
            Diccionario con equivalencias encontradas y criterios
        """
        try:
            # Obtener el producto
            product = self.inference_engine.get_product_by_id(product_id)
            if not product:
                return {
                    "product_id": product_id,
                    "error": "Producto no encontrado",
                    "equivalents": []
                }
            
            # 1. Equivalencias explícitas de la ontología
            explicit_equivalents = self._get_explicit_equivalents(product)
            
            # 2. Productos similares (menos estricto que equivalentes)
            similar_products = self.inference_engine.get_similar_products(product_id)
            
            # 3. Detección automática basada en especificaciones
            auto_detected = self._auto_detect_equivalents(product)
            
            # Combinar y eliminar duplicados
            all_equivalents = self._merge_equivalents(
                explicit_equivalents,
                similar_products,
                auto_detected
            )
            
            # Obtener detalles del producto original
            product_dict = individual_to_dict(product)
            product_props = product_dict.get("properties", {})
            product_name = product_props.get("tieneNombre", product_id)
            if not isinstance(product_name, str):
                product_name = product_id
            
            result = {
                "product_id": product_id,
                "product_name": product_name,
                "total_equivalents": len(all_equivalents),
                "equivalents": all_equivalents,
                "criteria_summary": {
                    "explicit": len(explicit_equivalents),
                    "similar": len(similar_products),
                    "auto_detected": len(auto_detected)
                }
            }
            
            logger.info(f"Encontrados {len(all_equivalents)} productos equivalentes para '{product_id}'")
            return result
            
        except Exception as e:
            logger.error(f"Error al buscar equivalentes para '{product_id}': {e}")
            return {
                "product_id": product_id,
                "error": str(e),
                "equivalents": []
            }
    
    def _get_explicit_equivalents(self, product) -> List[Dict]:
        """
        Obtiene equivalencias explícitas desde la propiedad esEquivalenteTecnico.
        
        Args:
            product: Individuo del producto
            
        Returns:
            Lista de productos equivalentes explícitos
        """
        equivalents = []
        
        try:
            # Buscar propiedad esEquivalenteTecnico
            if hasattr(product, 'esEquivalenteTecnico'):
                for equiv in product.esEquivalenteTecnico:
                    equiv_dict = individual_to_dict(equiv)
                    props = equiv_dict.get("properties", {})
                    
                    # Determinar categoría desde types
                    category = "Desconocida"
                    for t in equiv_dict.get("types", []):
                        if t in ["Laptop", "Smartphone", "Tablet", "Desktop"]:
                            category = t
                            break
                    
                    equivalents.append({
                        "id": equiv.name,
                        "name": props.get("tieneNombre", equiv.name) if isinstance(props.get("tieneNombre"), str) else equiv.name,
                        "category": category,
                        "price": props.get("tienePrecio", 0),
                        "match_type": "explicit",
                        "match_reason": "Equivalencia técnica definida en ontología",
                        "confidence": 100
                    })
            
            # Como es simétrica, buscar también productos que tengan este como equivalente
            all_products = list(self.onto.Producto.instances())
            for other_product in all_products:
                if other_product.name == product.name:
                    continue
                
                if hasattr(other_product, 'esEquivalenteTecnico'):
                    if product in other_product.esEquivalenteTecnico:
                        # Evitar duplicados
                        if not any(e["id"] == other_product.name for e in equivalents):
                            other_dict = individual_to_dict(other_product)
                            props = other_dict.get("properties", {})
                            
                            category = "Desconocida"
                            for t in other_dict.get("types", []):
                                if t in ["Laptop", "Smartphone", "Tablet", "Desktop"]:
                                    category = t
                                    break
                            
                            equivalents.append({
                                "id": other_product.name,
                                "name": props.get("tieneNombre", other_product.name) if isinstance(props.get("tieneNombre"), str) else other_product.name,
                                "category": category,
                                "price": props.get("tienePrecio", 0),
                                "match_type": "explicit",
                                "match_reason": "Equivalencia técnica definida en ontología",
                                "confidence": 100
                            })
        
        except Exception as e:
            logger.error(f"Error al obtener equivalentes explícitos: {e}")
        
        return equivalents
    
    def _auto_detect_equivalents(self, product) -> List[Dict]:
        """
        Detecta automáticamente productos equivalentes basándose en especificaciones.
        
        Criterios de equivalencia:
        - Misma categoría
        - RAM idéntica o muy similar (±2GB)
        - Almacenamiento idéntico o muy similar (±128GB)
        - Precio similar (±20%)
        - Pantalla similar (para electrónicos)
        
        Args:
            product: Individuo del producto
            
        Returns:
            Lista de productos equivalentes detectados
        """
        equivalents = []
        
        try:
            # Obtener especificaciones del producto
            product_dict = individual_to_dict(product)
            product_props = product_dict.get("properties", {})
            product_types = product_dict.get("types", [])
            
            # Determinar categoría principal
            product_category = None
            for t in product_types:
                if t in ["Laptop", "Smartphone", "Tablet", "Desktop"]:
                    product_category = t
                    break
            
            product_ram = product_props.get("tieneRAM_GB", 0)
            product_storage = product_props.get("tieneAlmacenamiento_GB", 0)
            product_price = product_props.get("tienePrecio", 0)
            product_screen = product_props.get("tienePulgadas", 0)
            
            # Si no tiene especificaciones básicas, no puede detectar equivalentes
            if not product_category or product_price == 0:
                return []
            
            # Buscar en todos los productos de la misma categoría
            all_products = list(self.onto.Producto.instances())
            
            for candidate in all_products:
                # Saltar el mismo producto
                if candidate.name == product.name:
                    continue
                
                candidate_dict = individual_to_dict(candidate)
                candidate_props = candidate_dict.get("properties", {})
                candidate_types = candidate_dict.get("types", [])
                
                # Determinar categoría del candidato
                candidate_category = None
                for t in candidate_types:
                    if t in ["Laptop", "Smartphone", "Tablet", "Desktop"]:
                        candidate_category = t
                        break
                
                # Crear diccionarios compatibles con el método de cálculo
                product_data = {
                    "category": product_category,
                    "ram_gb": product_ram,
                    "storage_gb": product_storage,
                    "price": product_price,
                    "screen_inches": product_screen
                }
                
                candidate_data = {
                    "category": candidate_category,
                    "ram_gb": candidate_props.get("tieneRAM_GB", 0),
                    "storage_gb": candidate_props.get("tieneAlmacenamiento_GB", 0),
                    "price": candidate_props.get("tienePrecio", 0),
                    "screen_inches": candidate_props.get("tienePulgadas", 0)
                }
                
                # Verificar criterios de equivalencia
                match_score, match_reasons = self._calculate_equivalence_match(
                    product_data, candidate_data
                )
                
                # Considerar equivalente si match_score >= 70%
                if match_score >= 70:
                    equivalents.append({
                        "id": candidate.name,
                        "name": candidate_props.get("tieneNombre", candidate.name) if isinstance(candidate_props.get("tieneNombre"), str) else candidate.name,
                        "category": candidate_category or "Desconocida",
                        "price": candidate_data["price"],
                        "match_type": "auto_detected",
                        "match_reason": ", ".join(match_reasons),
                        "confidence": match_score
                    })
        
        except Exception as e:
            logger.error(f"Error en detección automática de equivalentes: {e}")
        
        return equivalents
    
    def _calculate_equivalence_match(
        self, 
        product1: Dict, 
        product2: Dict
    ) -> tuple[int, List[str]]:
        """
        Calcula el score de equivalencia entre dos productos.
        
        Args:
            product1: Datos del primer producto
            product2: Datos del segundo producto
            
        Returns:
            Tupla (score, razones) donde score es 0-100 y razones es lista de strings
        """
        score = 0
        reasons = []
        
        # 1. Categoría (requisito obligatorio)
        if product1.get("category") != product2.get("category"):
            return (0, ["Categorías diferentes"])
        
        score += 20
        reasons.append(f"Misma categoría: {product1.get('category')}")
        
        # 2. RAM (25 puntos si es idéntica, 15 si ±2GB)
        ram1 = product1.get("ram_gb", 0)
        ram2 = product2.get("ram_gb", 0)
        
        if ram1 and ram2:
            if ram1 == ram2:
                score += 25
                reasons.append(f"RAM idéntica: {ram1}GB")
            elif abs(ram1 - ram2) <= 2:
                score += 15
                reasons.append(f"RAM similar: {ram1}GB vs {ram2}GB")
        
        # 3. Almacenamiento (25 puntos si idéntico, 15 si ±128GB)
        storage1 = product1.get("storage_gb", 0)
        storage2 = product2.get("storage_gb", 0)
        
        if storage1 and storage2:
            if storage1 == storage2:
                score += 25
                reasons.append(f"Almacenamiento idéntico: {storage1}GB")
            elif abs(storage1 - storage2) <= 128:
                score += 15
                reasons.append(f"Almacenamiento similar: {storage1}GB vs {storage2}GB")
        
        # 4. Precio (15 puntos si ±20%)
        price1 = product1.get("price", 0)
        price2 = product2.get("price", 0)
        
        if price1 and price2:
            price_diff_pct = abs(price1 - price2) / max(price1, price2) * 100
            if price_diff_pct <= 20:
                score += 15
                reasons.append(f"Precio similar: ${price1} vs ${price2}")
        
        # 5. Pantalla (15 puntos si ±1 pulgada)
        screen1 = product1.get("screen_inches", 0)
        screen2 = product2.get("screen_inches", 0)
        
        if screen1 and screen2:
            if abs(screen1 - screen2) <= 1:
                score += 15
                reasons.append(f"Pantalla similar: {screen1}\" vs {screen2}\"")
        
        return (score, reasons)
    
    def _merge_equivalents(
        self, 
        explicit: List[Dict],
        similar: List[Dict],
        auto: List[Dict]
    ) -> List[Dict]:
        """
        Combina listas de equivalentes eliminando duplicados.
        Prioriza explícitos > similares > auto-detectados.
        
        Args:
            explicit: Equivalentes explícitos
            similar: Productos similares
            auto: Auto-detectados
            
        Returns:
            Lista consolidada sin duplicados
        """
        merged = {}
        
        # Agregar auto-detectados primero (menor prioridad)
        for equiv in auto:
            merged[equiv["id"]] = equiv
        
        # Agregar similares (prioridad media)
        for equiv in similar:
            if equiv["id"] not in merged:
                merged[equiv["id"]] = {
                    "id": equiv["id"],
                    "name": equiv.get("name", "Sin nombre"),
                    "category": "Desconocida",
                    "price": 0,
                    "match_type": "similar",
                    "match_reason": "Producto similar detectado por ontología",
                    "confidence": 80
                }
        
        # Agregar explícitos (mayor prioridad, sobrescribe anteriores)
        for equiv in explicit:
            merged[equiv["id"]] = equiv
        
        # Convertir a lista ordenada por confianza
        result = sorted(merged.values(), key=lambda x: x["confidence"], reverse=True)
        
        return result
    
    def get_equivalence_comparison(self, product1_id: str, product2_id: str) -> Dict:
        """
        Compara dos productos para determinar si son equivalentes.
        
        Args:
            product1_id: ID del primer producto
            product2_id: ID del segundo producto
            
        Returns:
            Diccionario con análisis de equivalencia
        """
        try:
            product1 = self.inference_engine.get_product_by_id(product1_id)
            product2 = self.inference_engine.get_product_by_id(product2_id)
            
            if not product1 or not product2:
                return {
                    "error": "Uno o ambos productos no encontrados",
                    "equivalent": False
                }
            
            product1_dict = individual_to_dict(product1)
            product2_dict = individual_to_dict(product2)
            
            product1_props = product1_dict.get("properties", {})
            product2_props = product2_dict.get("properties", {})
            product1_types = product1_dict.get("types", [])
            product2_types = product2_dict.get("types", [])
            
            # Determinar categorías
            product1_category = None
            product2_category = None
            for t in product1_types:
                if t in ["Laptop", "Smartphone", "Tablet", "Desktop"]:
                    product1_category = t
                    break
            for t in product2_types:
                if t in ["Laptop", "Smartphone", "Tablet", "Desktop"]:
                    product2_category = t
                    break
            
            # Crear diccionarios para cálculo
            product1_data = {
                "category": product1_category,
                "ram_gb": product1_props.get("tieneRAM_GB", 0),
                "storage_gb": product1_props.get("tieneAlmacenamiento_GB", 0),
                "price": product1_props.get("tienePrecio", 0),
                "screen_inches": product1_props.get("tienePulgadas", 0)
            }
            
            product2_data = {
                "category": product2_category,
                "ram_gb": product2_props.get("tieneRAM_GB", 0),
                "storage_gb": product2_props.get("tieneAlmacenamiento_GB", 0),
                "price": product2_props.get("tienePrecio", 0),
                "screen_inches": product2_props.get("tienePulgadas", 0)
            }
            
            # Calcular equivalencia
            match_score, match_reasons = self._calculate_equivalence_match(
                product1_data, product2_data
            )
            
            # Verificar si están explícitamente marcados como equivalentes
            is_explicit = False
            if hasattr(product1, 'esEquivalenteTecnico'):
                is_explicit = product2 in product1.esEquivalenteTecnico
            
            # Nombres
            product1_name = product1_props.get("tieneNombre", product1_id)
            if not isinstance(product1_name, str):
                product1_name = product1_id
            product2_name = product2_props.get("tieneNombre", product2_id)
            if not isinstance(product2_name, str):
                product2_name = product2_id
            
            return {
                "product1": {
                    "id": product1_id,
                    "name": product1_name
                },
                "product2": {
                    "id": product2_id,
                    "name": product2_name
                },
                "equivalent": match_score >= 70 or is_explicit,
                "match_score": match_score,
                "match_type": "explicit" if is_explicit else ("auto" if match_score >= 70 else "none"),
                "reasons": match_reasons,
                "recommendation": self._get_equivalence_recommendation(
                    match_score, is_explicit, product1_data, product2_data
                )
            }
            
        except Exception as e:
            logger.error(f"Error al comparar '{product1_id}' y '{product2_id}': {e}")
            return {
                "error": str(e),
                "equivalent": False
            }
    
    def _get_equivalence_recommendation(
        self,
        match_score: int,
        is_explicit: bool,
        product1: Dict,
        product2: Dict
    ) -> str:
        """Genera una recomendación basada en el análisis de equivalencia."""
        
        if is_explicit:
            return "✅ Productos marcados como técnicamente equivalentes en la ontología"
        
        if match_score >= 90:
            # Recomendar el más barato
            price1 = product1.get("price", 0)
            price2 = product2.get("price", 0)
            if price1 and price2:
                if price1 < price2:
                    return f"💰 Productos altamente equivalentes. Recomendamos '{product1.get('name')}' por mejor precio"
                else:
                    return f"💰 Productos altamente equivalentes. Recomendamos '{product2.get('name')}' por mejor precio"
            return "✅ Productos altamente equivalentes (90%+ similitud)"
        
        elif match_score >= 70:
            return "⚠️ Productos equivalentes con algunas diferencias menores"
        
        else:
            return "❌ Productos no son equivalentes (especificaciones diferentes)"

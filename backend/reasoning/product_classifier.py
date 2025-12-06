"""
Clasificador de Productos - SmartCompareMarket
Sistema de clasificación automática usando razonamiento OWL y reglas SWRL.

Autor: Álvaro Machaca
Fecha: Diciembre 2024
"""

from typing import List, Dict, Optional, Set, Tuple
import logging
from owlready2 import Thing

from ontology.loader import get_ontology
from utils.owl_helpers import individual_to_dict

logger = logging.getLogger(__name__)


class ProductClassifier:
    """
    Clasificador de productos que combina:
    1. Subsunción OWL (razonamiento automático de Pellet)
    2. Reglas SWRL (aplicadas por Pellet)
    3. Reglas programáticas adicionales
    
    El razonador Pellet ya clasifica automáticamente los productos
    según la jerarquía OWL. Este servicio proporciona una interfaz
    unificada y reportes detallados de clasificación.
    """
    
    def __init__(self):
        """Inicializa el clasificador de productos."""
        self.onto = get_ontology()
        logger.info("ProductClassifier inicializado correctamente")
    
    def classify_product(self, product_id: str) -> Dict:
        """
        Clasifica un producto y retorna todas sus categorías.
        
        Incluye:
        - Clases directas (asignadas explícitamente)
        - Clases inferidas (por el razonador Pellet)
        - Clases SWRL (por reglas SWRL)
        - Explicación de cada clasificación
        
        Args:
            product_id: ID del producto a clasificar
            
        Returns:
            Diccionario con clasificación completa y explicaciones
        """
        try:
            # Obtener el producto
            product = self.onto.search_one(iri=f"*{product_id}")
            if not product:
                return {
                    "error": f"Producto '{product_id}' no encontrado",
                    "product_id": product_id
                }
            
            # Obtener datos del producto
            product_dict = individual_to_dict(product)
            props = product_dict.get("properties", {})
            types = product_dict.get("types", [])
            
            # Analizar clasificaciones
            direct_classes = self._get_direct_classes(product)
            inferred_classes = self._get_inferred_classes(product)
            swrl_classes = self._identify_swrl_classifications(product, props)
            
            # Generar explicaciones
            explanations = self._generate_classification_explanations(
                product_id, props, types
            )
            
            # Nombre del producto
            name = props.get("tieneNombre", product_id)
            if not isinstance(name, str):
                name = product_id
            
            return {
                "product_id": product_id,
                "product_name": name,
                "classification": {
                    "all_classes": types,
                    "direct_classes": direct_classes,
                    "inferred_classes": inferred_classes,
                    "swrl_classes": swrl_classes,
                    "total_classes": len(types)
                },
                "specifications": {
                    "ram_gb": props.get("tieneRAM_GB", 0),
                    "storage_gb": props.get("tieneAlmacenamiento_GB", 0),
                    "price": props.get("tienePrecio", 0),
                    "screen_inches": props.get("tienePulgadas", 0),
                    "rating": props.get("tieneCalificacion", 0)
                },
                "explanations": explanations,
                "classification_confidence": self._calculate_classification_confidence(
                    direct_classes, inferred_classes, swrl_classes
                )
            }
            
        except Exception as e:
            logger.error(f"Error al clasificar producto '{product_id}': {e}")
            return {
                "error": str(e),
                "product_id": product_id
            }
    
    def _get_direct_classes(self, product: Thing) -> List[str]:
        """Obtiene las clases directamente asignadas al producto."""
        direct = []
        for cls in product.is_a:
            if hasattr(cls, 'name') and cls.name != 'Thing':
                direct.append(cls.name)
        return direct
    
    def _get_inferred_classes(self, product: Thing) -> List[str]:
        """Obtiene las clases inferidas por el razonador (no directas)."""
        try:
            all_classes = set()
            for cls in product.INDIRECT_is_a:
                if hasattr(cls, 'name') and cls.name != 'Thing':
                    all_classes.add(cls.name)
            
            # Remover las clases directas para obtener solo las inferidas
            direct = set(self._get_direct_classes(product))
            inferred = all_classes - direct
            
            return list(inferred)
        except:
            return []
    
    def _identify_swrl_classifications(self, product: Thing, props: Dict) -> List[Dict]:
        """
        Identifica qué reglas SWRL se aplicaron a este producto.
        
        Reglas conocidas:
        1. DetectarGamer: RAM >= 16GB -> LaptopGamer
        2. DetectarSmartphoneGamaAlta: RAM > 8GB -> SmartphoneGamaAlta
        3. DetectarTabletPremium: Precio > 800 -> TabletPremium
        """
        swrl_rules = []
        
        # Obtener tipos del producto
        product_types = set()
        for cls in product.INDIRECT_is_a:
            if hasattr(cls, 'name'):
                product_types.add(cls.name)
        
        # Regla 1: DetectarGamer
        if "Laptop" in product_types:
            ram = props.get("tieneRAM_GB", 0)
            if ram >= 16 and "LaptopGamer" in product_types:
                swrl_rules.append({
                    "rule_name": "DetectarGamer",
                    "condition": f"RAM >= 16GB (actual: {ram}GB)",
                    "resulting_class": "LaptopGamer",
                    "triggered": True
                })
            elif ram >= 16:
                swrl_rules.append({
                    "rule_name": "DetectarGamer",
                    "condition": f"RAM >= 16GB (actual: {ram}GB)",
                    "resulting_class": "LaptopGamer",
                    "triggered": "should_trigger",
                    "note": "SWRL debería haber aplicado esta regla"
                })
        
        # Regla 2: DetectarSmartphoneGamaAlta
        if "Smartphone" in product_types:
            ram = props.get("tieneRAM_GB", 0)
            if ram > 8 and "SmartphoneGamaAlta" in product_types:
                swrl_rules.append({
                    "rule_name": "DetectarSmartphoneGamaAlta",
                    "condition": f"RAM > 8GB (actual: {ram}GB)",
                    "resulting_class": "SmartphoneGamaAlta",
                    "triggered": True
                })
            elif ram > 8:
                swrl_rules.append({
                    "rule_name": "DetectarSmartphoneGamaAlta",
                    "condition": f"RAM > 8GB (actual: {ram}GB)",
                    "resulting_class": "SmartphoneGamaAlta",
                    "triggered": "programmatic",
                    "note": "Clasificado programáticamente (SWRL no disponible en ontología)"
                })
        
        # Regla 3: DetectarTabletPremium
        if "Tablet" in product_types:
            price = props.get("tienePrecio", 0)
            if price > 800 and "TabletPremium" in product_types:
                swrl_rules.append({
                    "rule_name": "DetectarTabletPremium",
                    "condition": f"Precio > $800 (actual: ${price})",
                    "resulting_class": "TabletPremium",
                    "triggered": True
                })
            elif price > 800:
                swrl_rules.append({
                    "rule_name": "DetectarTabletPremium",
                    "condition": f"Precio > $800 (actual: ${price})",
                    "resulting_class": "TabletPremium",
                    "triggered": "programmatic",
                    "note": "Clasificado programáticamente (SWRL no disponible en ontología)"
                })
        
        return swrl_rules
    
    def _generate_classification_explanations(
        self, 
        product_id: str, 
        props: Dict,
        types: List[str]
    ) -> List[str]:
        """Genera explicaciones en lenguaje natural de por qué se clasificó así."""
        explanations = []
        
        ram = props.get("tieneRAM_GB", 0)
        storage = props.get("tieneAlmacenamiento_GB", 0)
        price = props.get("tienePrecio", 0)
        screen = props.get("tienePulgadas", 0)
        
        # Clasificación base
        if "Laptop" in types:
            explanations.append(f"✓ Clasificado como 'Laptop' (categoría base)")
            
            if "LaptopGamer" in types:
                explanations.append(
                    f"✓ Clasificado como 'LaptopGamer' porque tiene {ram}GB RAM (≥16GB)"
                )
        
        if "Smartphone" in types:
            explanations.append(f"✓ Clasificado como 'Smartphone' (categoría base)")
            
            if "SmartphoneGamaAlta" in types or ram > 8:
                explanations.append(
                    f"✓ Podría clasificarse como 'SmartphoneGamaAlta' porque tiene {ram}GB RAM (>8GB)"
                )
        
        if "Tablet" in types:
            explanations.append(f"✓ Clasificado como 'Tablet' (categoría base)")
            
            if "TabletPremium" in types or price > 800:
                explanations.append(
                    f"✓ Podría clasificarse como 'TabletPremium' porque cuesta ${price} (>$800)"
                )
        
        # Clasificación por especificaciones
        if ram >= 32:
            explanations.append(f"⭐ Alta capacidad de RAM: {ram}GB (top tier)")
        elif ram >= 16:
            explanations.append(f"⚡ Buena capacidad de RAM: {ram}GB (mid-high tier)")
        
        if storage >= 1024:
            explanations.append(f"⭐ Alto almacenamiento: {storage}GB (1TB+)")
        elif storage >= 512:
            explanations.append(f"⚡ Buen almacenamiento: {storage}GB")
        
        if price > 1500:
            explanations.append(f"💎 Producto premium: ${price}")
        elif price > 800:
            explanations.append(f"💰 Producto gama media-alta: ${price}")
        
        return explanations
    
    def _calculate_classification_confidence(
        self,
        direct: List[str],
        inferred: List[str],
        swrl: List[Dict]
    ) -> Dict:
        """Calcula la confianza de la clasificación."""
        total_classes = len(direct) + len(inferred)
        swrl_triggered = sum(1 for rule in swrl if rule.get("triggered") == True)
        
        confidence = "high"
        if total_classes < 2:
            confidence = "low"
        elif swrl_triggered > 0:
            confidence = "very_high"
        elif len(inferred) > 0:
            confidence = "high"
        else:
            confidence = "medium"
        
        return {
            "level": confidence,
            "total_classes": total_classes,
            "swrl_rules_applied": swrl_triggered,
            "has_inferences": len(inferred) > 0
        }
    
    def classify_all_products(self) -> Dict:
        """
        Clasifica todos los productos del sistema.
        
        Returns:
            Diccionario con clasificación de todos los productos
        """
        try:
            all_products = list(self.onto.Producto.instances())
            
            classifications = []
            stats = {
                "total_products": len(all_products),
                "by_category": {},
                "swrl_applied": 0,
                "with_inferences": 0
            }
            
            for product in all_products:
                classification = self.classify_product(product.name)
                
                if "error" not in classification:
                    classifications.append({
                        "id": product.name,
                        "name": classification.get("product_name", product.name),
                        "classes": classification["classification"]["all_classes"],
                        "swrl_rules": len(classification["classification"]["swrl_classes"])
                    })
                    
                    # Estadísticas
                    for cls in classification["classification"]["all_classes"]:
                        if cls in ["Laptop", "Smartphone", "Tablet", "Desktop"]:
                            stats["by_category"][cls] = stats["by_category"].get(cls, 0) + 1
                    
                    if classification["classification"]["swrl_classes"]:
                        stats["swrl_applied"] += 1
                    
                    if classification["classification"]["inferred_classes"]:
                        stats["with_inferences"] += 1
            
            return {
                "statistics": stats,
                "products": classifications,
                "summary": {
                    "total_analyzed": stats["total_products"],
                    "swrl_percentage": round(stats["swrl_applied"] / stats["total_products"] * 100, 2) if stats["total_products"] > 0 else 0,
                    "inference_percentage": round(stats["with_inferences"] / stats["total_products"] * 100, 2) if stats["total_products"] > 0 else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error al clasificar todos los productos: {e}")
            return {"error": str(e)}
    
    def get_products_by_class(self, class_name: str) -> Dict:
        """
        Obtiene todos los productos de una clase específica.
        
        Args:
            class_name: Nombre de la clase (ej: "LaptopGamer", "Smartphone")
            
        Returns:
            Lista de productos que pertenecen a esa clase
        """
        try:
            # Buscar la clase
            target_class = None
            for cls in self.onto.classes():
                if cls.name == class_name:
                    target_class = cls
                    break
            
            if not target_class:
                return {
                    "error": f"Clase '{class_name}' no encontrada en la ontología",
                    "available_classes": [c.name for c in self.onto.classes() if hasattr(c, 'name')][:20]
                }
            
            # Obtener instancias
            instances = list(target_class.instances())
            
            products = []
            for instance in instances:
                product_dict = individual_to_dict(instance)
                props = product_dict.get("properties", {})
                
                name = props.get("tieneNombre", instance.name)
                if not isinstance(name, str):
                    name = instance.name
                
                products.append({
                    "id": instance.name,
                    "name": name,
                    "price": props.get("tienePrecio", 0),
                    "ram_gb": props.get("tieneRAM_GB", 0),
                    "storage_gb": props.get("tieneAlmacenamiento_GB", 0),
                    "all_classes": product_dict.get("types", [])
                })
            
            return {
                "class_name": class_name,
                "total_products": len(products),
                "products": products
            }
            
        except Exception as e:
            logger.error(f"Error al obtener productos de clase '{class_name}': {e}")
            return {"error": str(e)}

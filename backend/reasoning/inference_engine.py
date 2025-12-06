"""
Motor de Inferencia para SmartCompareMarket

Este módulo proporciona un wrapper para HermiT y facilita consultas de inferencia
sobre relaciones entre productos, incluyendo compatibilidad, similitud y mejor opción.

Autor: SmartCompareMarket Team
Fecha: 2024
"""

from typing import List, Dict, Optional, Set
from owlready2 import World, Ontology, Thing, ObjectProperty
import logging

# Configurar logging
logger = logging.getLogger(__name__)


class InferenceEngine:
    """
    Motor de inferencia que facilita consultas sobre relaciones entre productos.
    
    Utiliza la ontología cargada con HermiT para acceder a inferencias SWRL
    y relaciones explícitas entre productos.
    """
    
    def __init__(self, ontology: Ontology):
        """
        Inicializa el motor de inferencia.
        
        Args:
            ontology: Ontología cargada con Owlready2 (ya razonada con HermiT)
        """
        self.ontology = ontology
        self.namespace = ontology.get_namespace("http://smartcompare.com/ontologia#")
        
        # Obtener propiedades de la ontología
        self._load_properties()
        
        logger.info("InferenceEngine inicializado correctamente")
    
    def _load_properties(self):
        """Carga las propiedades de objeto relevantes de la ontología."""
        try:
            # Propiedades de compatibilidad y similitud
            self.esCompatibleCon = self.ontology.esCompatibleCon
            self.incompatibleCon = self.ontology.incompatibleCon
            self.esSimilarA = self.ontology.esSimilarA
            self.esMejorOpcionQue = self.ontology.esMejorOpcionQue
            
            # Clases principales
            self.Producto = self.ontology.Producto
            
            logger.debug("Propiedades cargadas correctamente")
        except AttributeError as e:
            logger.error(f"Error al cargar propiedades de la ontología: {e}")
            raise
    
    def get_product_by_id(self, product_id: str) -> Optional[Thing]:
        """
        Obtiene un producto por su ID (nombre del individuo).
        
        Args:
            product_id: ID del producto (ej: "iPhone15_Barato")
            
        Returns:
            Individuo del producto o None si no existe
        """
        try:
            # Buscar el individuo en la ontología
            product = self.ontology.search_one(iri=f"*{product_id}")
            if product is None:
                # Intentar con el namespace completo
                product = self.ontology.search_one(
                    iri=f"http://smartcompare.com/ontologia#{product_id}"
                )
            
            if product and isinstance(product, self.Producto):
                return product
            
            logger.warning(f"Producto '{product_id}' no encontrado o no es de tipo Producto")
            return None
            
        except Exception as e:
            logger.error(f"Error al buscar producto '{product_id}': {e}")
            return None
    
    def get_compatible_products(self, product_id: str) -> List[Dict]:
        """
        Obtiene todos los productos compatibles con el producto dado.
        
        La propiedad esCompatibleCon es simétrica, por lo que si A esCompatibleCon B,
        entonces B esCompatibleCon A.
        
        Args:
            product_id: ID del producto
            
        Returns:
            Lista de diccionarios con información de productos compatibles
        """
        product = self.get_product_by_id(product_id)
        if product is None:
            return []
        
        compatible_products = []
        
        try:
            # Obtener productos compatibles (relación directa)
            if hasattr(product, 'esCompatibleCon'):
                for compatible in product.esCompatibleCon:
                    compatible_products.append({
                        "id": compatible.name,
                        "name": getattr(compatible, 'tieneNombre', ['Sin nombre'])[0] if hasattr(compatible, 'tieneNombre') else 'Sin nombre',
                        "relation": "esCompatibleCon"
                    })
            
            # Como es simétrica, también buscar productos que tengan este como compatible
            # (aunque Owlready2 debería manejar esto automáticamente)
            all_products = list(self.ontology.Producto.instances())
            for other_product in all_products:
                if other_product.name == product_id:
                    continue
                
                if hasattr(other_product, 'esCompatibleCon'):
                    if product in other_product.esCompatibleCon:
                        # Verificar que no esté ya en la lista
                        if not any(p["id"] == other_product.name for p in compatible_products):
                            compatible_products.append({
                                "id": other_product.name,
                                "name": getattr(other_product, 'tieneNombre', ['Sin nombre'])[0] if hasattr(other_product, 'tieneNombre') else 'Sin nombre',
                                "relation": "esCompatibleCon"
                            })
            
            logger.info(f"Encontrados {len(compatible_products)} productos compatibles con '{product_id}'")
            return compatible_products
            
        except Exception as e:
            logger.error(f"Error al obtener productos compatibles para '{product_id}': {e}")
            return []
    
    def get_incompatible_products(self, product_id: str) -> List[Dict]:
        """
        Obtiene todos los productos incompatibles con el producto dado.
        
        La propiedad incompatibleCon es simétrica.
        
        Args:
            product_id: ID del producto
            
        Returns:
            Lista de diccionarios con información de productos incompatibles
        """
        product = self.get_product_by_id(product_id)
        if product is None:
            return []
        
        incompatible_products = []
        
        try:
            # Obtener productos incompatibles (relación directa)
            if hasattr(product, 'incompatibleCon'):
                for incompatible in product.incompatibleCon:
                    incompatible_products.append({
                        "id": incompatible.name,
                        "name": getattr(incompatible, 'tieneNombre', ['Sin nombre'])[0] if hasattr(incompatible, 'tieneNombre') else 'Sin nombre',
                        "relation": "incompatibleCon"
                    })
            
            # Buscar productos que tengan este como incompatible (simetría)
            all_products = list(self.ontology.Producto.instances())
            for other_product in all_products:
                if other_product.name == product_id:
                    continue
                
                if hasattr(other_product, 'incompatibleCon'):
                    if product in other_product.incompatibleCon:
                        if not any(p["id"] == other_product.name for p in incompatible_products):
                            incompatible_products.append({
                                "id": other_product.name,
                                "name": getattr(other_product, 'tieneNombre', ['Sin nombre'])[0] if hasattr(other_product, 'tieneNombre') else 'Sin nombre',
                                "relation": "incompatibleCon"
                            })
            
            logger.info(f"Encontrados {len(incompatible_products)} productos incompatibles con '{product_id}'")
            return incompatible_products
            
        except Exception as e:
            logger.error(f"Error al obtener productos incompatibles para '{product_id}': {e}")
            return []
    
    def get_similar_products(self, product_id: str) -> List[Dict]:
        """
        Obtiene todos los productos similares al producto dado.
        
        La propiedad esSimilarA es simétrica.
        
        Args:
            product_id: ID del producto
            
        Returns:
            Lista de diccionarios con información de productos similares
        """
        product = self.get_product_by_id(product_id)
        if product is None:
            return []
        
        similar_products = []
        
        try:
            # Obtener productos similares (relación directa)
            if hasattr(product, 'esSimilarA'):
                for similar in product.esSimilarA:
                    similar_products.append({
                        "id": similar.name,
                        "name": getattr(similar, 'tieneNombre', ['Sin nombre'])[0] if hasattr(similar, 'tieneNombre') else 'Sin nombre',
                        "relation": "esSimilarA"
                    })
            
            # Buscar productos que tengan este como similar (simetría)
            all_products = list(self.ontology.Producto.instances())
            for other_product in all_products:
                if other_product.name == product_id:
                    continue
                
                if hasattr(other_product, 'esSimilarA'):
                    if product in other_product.esSimilarA:
                        if not any(p["id"] == other_product.name for p in similar_products):
                            similar_products.append({
                                "id": other_product.name,
                                "name": getattr(other_product, 'tieneNombre', ['Sin nombre'])[0] if hasattr(other_product, 'tieneNombre') else 'Sin nombre',
                                "relation": "esSimilarA"
                            })
            
            logger.info(f"Encontrados {len(similar_products)} productos similares a '{product_id}'")
            return similar_products
            
        except Exception as e:
            logger.error(f"Error al obtener productos similares para '{product_id}': {e}")
            return []
    
    def is_better_option(self, product1_id: str, product2_id: str) -> Optional[bool]:
        """
        Verifica si product1 es mejor opción que product2.
        
        Esta relación puede ser inferida por la regla SWRL "EncontrarMejorPrecio"
        o estar explícitamente definida en la ontología.
        
        Args:
            product1_id: ID del primer producto
            product2_id: ID del segundo producto
            
        Returns:
            True si product1 es mejor opción que product2,
            False si product2 es mejor opción que product1,
            None si no hay relación definida
        """
        product1 = self.get_product_by_id(product1_id)
        product2 = self.get_product_by_id(product2_id)
        
        if product1 is None or product2 is None:
            return None
        
        try:
            # Verificar si product1 esMejorOpcionQue product2
            if hasattr(product1, 'esMejorOpcionQue'):
                if product2 in product1.esMejorOpcionQue:
                    logger.info(f"'{product1_id}' es mejor opción que '{product2_id}' (inferido por SWRL)")
                    return True
            
            # Verificar si product2 esMejorOpcionQue product1
            if hasattr(product2, 'esMejorOpcionQue'):
                if product1 in product2.esMejorOpcionQue:
                    logger.info(f"'{product2_id}' es mejor opción que '{product1_id}' (inferido por SWRL)")
                    return False
            
            # No hay relación definida
            return None
            
        except Exception as e:
            logger.error(f"Error al verificar relación esMejorOpcionQue: {e}")
            return None
    
    def get_all_relationships(self, product_id: str) -> Dict:
        """
        Obtiene todas las relaciones de un producto en un solo diccionario.
        
        Args:
            product_id: ID del producto
            
        Returns:
            Diccionario con todas las relaciones del producto
        """
        return {
            "product_id": product_id,
            "compatible": self.get_compatible_products(product_id),
            "incompatible": self.get_incompatible_products(product_id),
            "similar": self.get_similar_products(product_id),
            "better_than": self._get_products_better_than(product_id),
            "worse_than": self._get_products_worse_than(product_id)
        }
    
    def _get_products_better_than(self, product_id: str) -> List[Dict]:
        """Obtiene productos que son mejores opciones que el producto dado."""
        product = self.get_product_by_id(product_id)
        if product is None:
            return []
        
        better_products = []
        
        try:
            # Buscar productos que tienen este producto como mejor opción
            all_products = list(self.ontology.Producto.instances())
            for other_product in all_products:
                if other_product.name == product_id:
                    continue
                
                if hasattr(other_product, 'esMejorOpcionQue'):
                    if product in other_product.esMejorOpcionQue:
                        better_products.append({
                            "id": other_product.name,
                            "name": getattr(other_product, 'tieneNombre', ['Sin nombre'])[0] if hasattr(other_product, 'tieneNombre') else 'Sin nombre',
                            "relation": "esMejorOpcionQue"
                        })
            
            return better_products
            
        except Exception as e:
            logger.error(f"Error al obtener productos mejores que '{product_id}': {e}")
            return []
    
    def _get_products_worse_than(self, product_id: str) -> List[Dict]:
        """Obtiene productos que son peores opciones que el producto dado."""
        product = self.get_product_by_id(product_id)
        if product is None:
            return []
        
        worse_products = []
        
        try:
            # Obtener productos que este producto es mejor opción
            if hasattr(product, 'esMejorOpcionQue'):
                for worse in product.esMejorOpcionQue:
                    worse_products.append({
                        "id": worse.name,
                        "name": getattr(worse, 'tieneNombre', ['Sin nombre'])[0] if hasattr(worse, 'tieneNombre') else 'Sin nombre',
                        "relation": "esMejorOpcionQue"
                    })
            
            return worse_products
            
        except Exception as e:
            logger.error(f"Error al obtener productos peores que '{product_id}': {e}")
            return []
    
    def check_compatibility(self, product1_id: str, product2_id: str) -> Dict:
        """
        Verifica la compatibilidad entre dos productos.

        Args:
            product1_id: ID del primer producto
            product2_id: ID del segundo producto

        Returns:
            Diccionario con información de compatibilidad
        """
        product1 = self.get_product_by_id(product1_id)
        product2 = self.get_product_by_id(product2_id)

        if product1 is None or product2 is None:
            return {
                "compatible": False,
                "incompatible": False,
                "error": "Uno o ambos productos no encontrados"
            }

        try:
            # Verificar compatibilidad
            is_compatible = False
            if hasattr(product1, 'esCompatibleCon'):
                is_compatible = product2 in product1.esCompatibleCon

            # Verificar incompatibilidad
            is_incompatible = False
            if hasattr(product1, 'incompatibleCon'):
                is_incompatible = product2 in product1.incompatibleCon

            return {
                "compatible": is_compatible,
                "incompatible": is_incompatible,
                "relationship": "compatible" if is_compatible else ("incompatible" if is_incompatible else "unknown")
            }

        except Exception as e:
            logger.error(f"Error al verificar compatibilidad: {e}")
            return {
                "compatible": False,
                "incompatible": False,
                "error": str(e)
            }

    def check_object_property(self, subject_id: str, property_name: str, object_id: str) -> bool:
        """
        Verifica si existe una relacion de propiedad de objeto entre dos productos.

        Args:
            subject_id: ID del producto sujeto
            property_name: Nombre de la propiedad (ej: "esMejorOpcionQue", "esCompatibleCon")
            object_id: ID del producto objeto

        Returns:
            True si existe la relacion, False en caso contrario
        """
        subject = self.get_product_by_id(subject_id)
        obj = self.get_product_by_id(object_id)

        if subject is None or obj is None:
            return False

        try:
            # Verificar si el sujeto tiene la propiedad
            if hasattr(subject, property_name):
                property_values = getattr(subject, property_name)
                # property_values puede ser una lista o un objeto individual
                if isinstance(property_values, list):
                    return obj in property_values
                else:
                    return obj == property_values

            return False

        except Exception as e:
            logger.error(f"Error al verificar propiedad '{property_name}' entre '{subject_id}' y '{object_id}': {e}")
            return False



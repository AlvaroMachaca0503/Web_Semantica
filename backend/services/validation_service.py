"""
Servicio de Validación de Consistencia - Requisito 8
Valida especificaciones de productos y detecta inconsistencias lógicas
"""
import sys
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ontology.loader import get_ontology
from services.product_service import ProductService


class ValidationService:
    """
    Servicio para validar consistencia de especificaciones de productos.
    
    Detecta:
    - Valores fuera de rango (RAM imposible, precio negativo)
    - Contradicciones lógicas (producto barato con precio alto)
    - Especificaciones incompatibles entre sí
    """
    
    def __init__(self):
        self.onto = get_ontology()
        self.product_service = ProductService()
    
    def validate_product(self, product_id: str) -> Dict[str, Any]:
        """
        Valida un producto individual y retorna inconsistencias detectadas.
        
        Args:
            product_id: ID del producto a validar
            
        Returns:
            Diccionario con estado de validación y errores encontrados
        """
        product = self.product_service.get_product_by_id(product_id)
        if not product:
            return {
                "valid": False,
                "errors": [f"Producto '{product_id}' no encontrado"]
            }
        
        errors = []
        warnings = []
        props = product.get('properties', {})
        
        # Validación 1: Precio
        price = self._get_numeric(props.get('tienePrecio'))
        if price is not None:
            if price < 0:
                errors.append("Precio negativo detectado")
            elif price > 100000:
                warnings.append("Precio excesivamente alto (>$100,000)")
        
        # Validación 2: RAM
        ram = self._get_numeric(props.get('tieneRAM_GB'))
        if ram is not None:
            if ram < 0:
                errors.append("RAM negativa detectada")
            elif ram > 512:
                errors.append("RAM técnicamente imposible (>512GB para dispositivos consumer)")
            elif ram > 128:
                warnings.append("RAM muy alta (>128GB, verifica si es correcto)")
        
        # Validación 3: Almacenamiento
        storage = self._get_numeric(props.get('tieneAlmacenamiento_GB'))
        if storage is not None:
            if storage < 0:
                errors.append("Almacenamiento negativo detectado")
            elif storage > 10000:
                errors.append("Almacenamiento técnicamente imposible (>10TB)")
        
        # Validación 4: Calificación
        rating = self._get_numeric(props.get('tieneCalificacion'))
        if rating is not None:
            if rating < 0 or rating > 5:
                errors.append("Calificación fuera de rango (debe estar entre 0-5)")
        
        # Validación 5: Lógica de categorías
        types = product.get('types', [])
        
        # Smartphones no deberían tener tanta RAM como laptops
        if 'Smartphone' in types and ram and ram > 32:
            warnings.append("Smartphone con RAM excesiva (>32GB es inusual)")
        
        # Laptops básicas no deberían costar demasiado
        if 'Laptop' in types and not 'LaptopGamer' in types:
            if price and price > 5000:
                warnings.append("Laptop no-gamer con precio muy alto")
        
        return {
            "valid": len(errors) == 0,
            "product_id": product_id,
            "errors": errors,
            "warnings": warnings,
            "total_issues": len(errors) + len(warnings)
        }
    
    def validate_all_products(self) -> Dict[str, Any]:
        """
        Valida todos los productos en la ontología.
        
        Returns:
            Resumen de validación para todos los productos
        """
        all_products = self.product_service.get_all_products()
        results = []
        
        total_valid = 0
        total_with_errors = 0
        total_with_warnings = 0
        
        for product in all_products:
            validation = self.validate_product(product['id'])
            results.append(validation)
            
            if validation['valid'] and len(validation['warnings']) == 0:
                total_valid += 1
            elif not validation['valid']:
                total_with_errors += 1
            else:
                total_with_warnings += 1
        
        return {
            "total_products": len(all_products),
            "valid": total_valid,
            "with_errors": total_with_errors,
            "with_warnings": total_with_warnings,
            "details": results
        }
    
    def _get_numeric(self, value):
        """Extrae valor numérico de forma segura"""
        if value is None:
            return None
        
        if isinstance(value, list):
            if not value:
                return None
            value = value[0]
        
        if isinstance(value, (int, float)):
            return float(value)
        
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

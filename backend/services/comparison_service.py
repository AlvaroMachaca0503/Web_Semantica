"""
Servicio de Comparación Inteligente - DÍA 2
Motor de comparación entre productos usando inferencias semánticas
"""
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ontology.loader import get_ontology
from reasoning.inference_engine import InferenceEngine
from services.product_service import ProductService
from utils.owl_helpers import individual_to_dict


class ComparisonService:
    """
    Servicio para comparación inteligente de productos.
    
    Utiliza:
    - InferenceEngine para relaciones SWRL
    - ProductService para datos de productos
    - Scoring basado en múltiples factores
    """
    
    def __init__(self):
        self.onto = get_ontology()
        self.inference_engine = InferenceEngine(self.onto)
        self.product_service = ProductService()
    
    def compare_products(self, product_ids: List[str]) -> Dict[str, Any]:
        """
        Compara múltiples productos y determina el ganador.
        
        Args:
            product_ids: Lista de IDs de productos a comparar
            
        Returns:
            Diccionario con comparación completa
        """
        if len(product_ids) < 2:
            raise ValueError("Se requieren al menos 2 productos para comparar")
        
        # Obtener datos de todos los productos
        products_data = []
        for product_id in product_ids:
            product = self.product_service.get_product_by_id(product_id)
            if not product:
                raise ValueError(f"Producto '{product_id}' no encontrado")
            products_data.append(product)
        
        # Calcular scoring para cada producto
        scores = {}
        for i, product in enumerate(products_data):
            score = self._calculate_score(product, product_ids[i], product_ids)
            scores[product_ids[i]] = score
        
        # Determinar ganador
        winner_id = max(scores, key=scores.get)
        winner_data = next(p for p in products_data if p['id'] == winner_id)
        
        # Generar tabla comparativa
        comparison_table = self._generate_comparison_table(products_data)
        
        # Verificar relaciones SWRL entre productos
        swrl_relations = self._check_swrl_relations(product_ids)
        
        # Generar diferencias
        differences = self._generate_differences(products_data)
        
        # Determinar razón del ganador
        reason = self._determine_winner_reason(
            winner_id, 
            winner_data, 
            scores, 
            swrl_relations
        )
        
        return {
            "products": products_data,
            "comparison_table": comparison_table,
            "winner": winner_id,
            "winner_score": scores[winner_id],
            "all_scores": scores,
            "reason": reason,
            "differences": differences,
            "swrl_inference": swrl_relations,
            "compatibility": self._check_compatibility(product_ids)
        }
    
    def _get_numeric_value(self, value: Any) -> float:
        """
        Extrae valor numérico seguro, manejando listas y tipos.
        """
        if isinstance(value, list):
            if not value:
                return 0.0
            value = value[0]
            
        if isinstance(value, (int, float)):
            return float(value)
            
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def _calculate_score(
        self, 
        product: Dict, 
        product_id: str, 
        all_product_ids: List[str]
    ) -> float:
        """
        Calcula un score para el producto basado en múltiples factores.
        
        Scoring:
        - Precio: menor es mejor (normalizado)
        - RAM: mayor es mejor
        - Calificación: mayor es mejor
        - Relaciones SWRL: bonus si es mejor opción que otros
        """
        score = 0.0
        props = product.get('properties', {})
        
        # Factor 1: Precio (menor es mejor)
        price = self._get_numeric_value(props.get('tienePrecio', 0))
        if price > 0:
            # Invertir: menor precio = mayor score
            score += (1000 / price) * 10  # Normalizado
        
        # Factor 2: RAM (mayor es mejor)
        ram = self._get_numeric_value(props.get('tieneRAM_GB', 0))
        score += ram * 5
        
        # Factor 3: Almacenamiento (mayor es mejor)
        storage = self._get_numeric_value(props.get('tieneAlmacenamiento_GB', 0))
        score += storage * 0.1
        
        # Factor 4: Calificación (mayor es mejor)
        rating = self._get_numeric_value(props.get('tieneCalificacion', 0))
        score += rating * 15
        
        # Factor 5: Bonus por SWRL esMejorOpcionQue
        for other_id in all_product_ids:
            if other_id != product_id:
                is_better = self.inference_engine.is_better_option(product_id, other_id)
                if is_better:
                    score += 50  # Bonus significativo
        
        return round(score, 2)
    
    def _generate_comparison_table(self, products: List[Dict]) -> Dict[str, List]:
        """
        Genera tabla comparativa con propiedades lado a lado.
        """
        # Obtener todas las propiedades únicas
        all_properties = set()
        for product in products:
            all_properties.update(product.get('properties', {}).keys())
        
        # Construir tabla
        table = {}
        for prop in sorted(all_properties):
            values = []
            for product in products:
                raw_val = product.get('properties', {}).get(prop, 'N/A')
                
                # Desempaquetar lista si es necesario
                if isinstance(raw_val, list):
                    val = raw_val[0] if raw_val else 'N/A'
                else:
                    val = raw_val
                    
                values.append(val)
            table[prop] = values
        
        return table
    
    def _check_swrl_relations(self, product_ids: List[str]) -> Dict[str, Any]:
        """
        Verifica relaciones SWRL entre los productos.
        """
        relations = {
            "esMejorOpcionQue": [],
            "rules_applied": []
        }
        
        # Verificar esMejorOpcionQue entre cada par
        for i, product1_id in enumerate(product_ids):
            for product2_id in product_ids[i+1:]:
                result = self.inference_engine.is_better_option(product1_id, product2_id)
                
                if result is True:
                    relations["esMejorOpcionQue"].append({
                        "better": product1_id,
                        "worse": product2_id,
                        "rule": "EncontrarMejorPrecio"
                    })
                    if "EncontrarMejorPrecio" not in relations["rules_applied"]:
                        relations["rules_applied"].append("EncontrarMejorPrecio")
                        
                elif result is False:
                    relations["esMejorOpcionQue"].append({
                        "better": product2_id,
                        "worse": product1_id,
                        "rule": "EncontrarMejorPrecio"
                    })
                    if "EncontrarMejorPrecio" not in relations["rules_applied"]:
                        relations["rules_applied"].append("EncontrarMejorPrecio")
        
        return relations
    
    def _generate_differences(self, products: List[Dict]) -> Dict[str, str]:
        """
        Genera lista de diferencias clave entre productos.
        """
        if len(products) != 2:
            # Para más de 2 productos, retornar comparación simple
            return {}
        
        differences = {}
        product1 = products[0]
        product2 = products[1]
        
        props1 = product1.get('properties', {})
        props2 = product2.get('properties', {})
        
        # Comparar propiedades comunes
        all_props = set(props1.keys()) | set(props2.keys())
        
        for prop in all_props:
            val1 = props1.get(prop, 'N/A')
            val2 = props2.get(prop, 'N/A')
            
            # Convertir listas a valores únicos si es necesario para visualización
            v1_display = val1[0] if isinstance(val1, list) and val1 else val1
            v2_display = val2[0] if isinstance(val2, list) and val2 else val2
            
            if v1_display != v2_display:
                # Intentar calcular diferencia numérica
                num1 = self._get_numeric_value(val1)
                num2 = self._get_numeric_value(val2)
                
                if num1 > 0 and num2 > 0:
                    diff = num1 - num2
                    sign = "+" if diff > 0 else ""
                    differences[prop] = f"{v1_display} vs {v2_display} ({sign}{round(diff, 2)})"
                else:
                    differences[prop] = f"{v1_display} vs {v2_display}"
        
        return differences
    
    def _check_compatibility(self, product_ids: List[str]) -> Dict[str, Any]:
        """
        Verifica compatibilidad entre productos.
        """
        compatibility_matrix = {}
        
        for product1_id in product_ids:
            for product2_id in product_ids:
                if product1_id != product2_id:
                    result = self.inference_engine.check_compatibility(
                        product1_id, 
                        product2_id
                    )
                    key = f"{product1_id}_vs_{product2_id}"
                    compatibility_matrix[key] = result
        
        return compatibility_matrix
    
    def _determine_winner_reason(
        self,
        winner_id: str,
        winner_data: Dict,
        scores: Dict[str, float],
        swrl_relations: Dict
    ) -> str:
        """
        Determina la razón por la que ganó el producto.
        """
        reasons = []
        
        # Verificar si ganó por SWRL
        swrl_wins = [
            r for r in swrl_relations.get("esMejorOpcionQue", [])
            if r["better"] == winner_id
        ]
        
        if swrl_wins:
            reasons.append(
                f"Inferido por SWRL como mejor opción (regla: {swrl_wins[0]['rule']})"
            )
        
        # Verificar precio
        winner_price = self._get_numeric_value(winner_data.get('properties', {}).get('tienePrecio'))
        if winner_price > 0:
            reasons.append(f"Mejor precio: ${winner_price}")
        
        # Verificar RAM
        winner_ram = self._get_numeric_value(winner_data.get('properties', {}).get('tieneRAM_GB'))
        if winner_ram >= 16:
            reasons.append(f"Alta RAM: {winner_ram}GB")
        
        # Verificar calificación
        winner_rating = self._get_numeric_value(winner_data.get('properties', {}).get('tieneCalificacion'))
        if winner_rating >= 4.5:
            reasons.append(f"Excelente calificación: {winner_rating}/5")
        
        # Score general
        reasons.append(f"Score total: {scores[winner_id]}")
        
        return " | ".join(reasons) if reasons else "Mejor score general"

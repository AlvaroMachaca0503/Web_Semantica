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
        Calcula un score para el producto basado en pesos configurables.
        Score final normalizado a 0-100.
        
        Pesos corregidos (suman 1.0):
        - bateria: 20% (mayor es mejor) - MUY IMPORTANTE
        - calificacion: 18% (mayor es mejor) - MUY IMPORTANTE
        - precio: 14% (menor es mejor) - importante pero no dominante
        - resolucion: 10% (mayor es mejor)
        - ram: 10% (mayor es mejor)
        - almacenamiento: 10% (mayor es mejor)
        - garantia: 7% (mayor es mejor)
        - pantalla: 6% (mayor es mejor)
        - peso_fisico: 5% (menor es mejor)
        
        Normalización:
        - Mayor = mejor: score = valor_producto / valor_referencia_max
        - Menor = mejor: score = valor_referencia_min / valor_producto
        """
        import json
        
        # Cargar configuración de pesos
        try:
            weights_path = Path(__file__).parent.parent / "data" / "comparison_weights.json"
            with open(weights_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            config = {
                "weights": {
                    "bateria": 0.20, "calificacion": 0.18, "precio": 0.14,
                    "resolucion": 0.10, "ram": 0.10, "almacenamiento": 0.10,
                    "garantia": 0.07, "pantalla": 0.06, "peso_fisico": 0.05
                }
            }
        
        props = product.get('properties', {})
        weights = config.get("weights", {})
        
        # Mapeo de factores a propiedades de la ontología
        prop_map = {
            "pantalla": "tienePulgadas",
            "bateria": "bateriaCapacidad_mAh",
            "ram": "tieneRAM_GB",
            "almacenamiento": "tieneAlmacenamiento_GB",
            "precio": "tienePrecio",
            "garantia": "garantiaMeses",
            "calificacion": "tieneCalificacion",
            "peso_fisico": "pesoGramos"
        }
        
        # Valores de referencia para normalización (realistas para smartphones/electronics)
        # Mayor es mejor: usamos valor_max como referencia (100% = alcanzar el max)
        # Menor es mejor: usamos valor_min como referencia (100% = alcanzar el min)
        reference_max = {
            "pantalla": 7.0,        # 7 pulgadas es excelente para smartphone
            "bateria": 5500,        # 5500 mAh es excelente
            "ram": 16,              # 16 GB es excelente para móvil
            "almacenamiento": 512,  # 512 GB es excelente
            "garantia": 24,         # 24 meses es excelente
            "calificacion": 5.0,    # 5.0 es perfecta
        }
        
        reference_min = {
            "precio": 600,          # $600 es un buen precio base
            "peso_fisico": 170,     # 170g es muy ligero
        }
        
        # Factores donde menor es mejor
        lower_better = {"precio", "peso_fisico"}
        
        total_score = 0.0
        total_weight = 0.0
        score_breakdown = {}
        
        for factor, weight in weights.items():
            if factor == "resolucion":
                continue  # Se calcula aparte
                
            prop_name = prop_map.get(factor)
            if not prop_name:
                continue
                
            value = self._get_numeric_value(props.get(prop_name, 0))
            
            if value <= 0:
                # Propiedad faltante = 0 puntos para este factor
                factor_score = 0
            elif factor in lower_better:
                # MENOR ES MEJOR: score = referencia_min / valor_actual
                # Si valor = referencia_min -> score = 1.0 (100%)
                # Si valor > referencia_min -> score < 1.0 (penalizado)
                ref_min = reference_min.get(factor, value)
                factor_score = min(1.0, ref_min / value)
            else:
                # MAYOR ES MEJOR: score = valor_actual / referencia_max
                # Si valor = referencia_max -> score = 1.0 (100%)
                # Si valor < referencia_max -> score < 1.0 (penalizado)
                ref_max = reference_max.get(factor, 100)
                factor_score = min(1.0, value / ref_max)
            
            # Agregar al total (factor_score está en rango 0-1)
            total_score += factor_score * weight
            total_weight += weight
            score_breakdown[factor] = round(factor_score * 100, 1)
        
        # Calcular resolución (especial porque es string "3200x1440")
        resolution_weight = weights.get("resolucion", 0.10)
        resolution_str = props.get("resolucionPantalla", "")
        if resolution_str and "x" in str(resolution_str):
            try:
                parts = str(resolution_str).lower().split("x")
                res_pixels = int(parts[0]) * int(parts[1])
                # Referencia: QHD+ (3200x1440 = 4.6M pixels) = 100%
                ref_resolution = 4608000  # 3200 * 1440
                res_score = min(1.0, res_pixels / ref_resolution)
                total_score += res_score * resolution_weight
                total_weight += resolution_weight
                score_breakdown["resolucion"] = round(res_score * 100, 1)
            except Exception:
                pass
        
        # Bonus SWRL: esMejorOpcionQue (pequeño bonus por inferencias semánticas)
        swrl_bonus = 0
        try:
            for other_id in all_product_ids:
                if other_id != product_id:
                    is_better = self.inference_engine.is_better_option(product_id, other_id)
                    if is_better:
                        swrl_bonus += 2  # +2 puntos por cada producto que supera
        except Exception:
            pass
        
        # Score final: normalizar a 0-100 y agregar bonus SWRL
        if total_weight > 0:
            # El score base está en rango 0-1, multiplicamos por 100
            final_score = (total_score / total_weight) * 100 + swrl_bonus
        else:
            final_score = swrl_bonus
        
        return round(min(100, max(0, final_score)), 1)
    
    def _generate_comparison_table(self, products: List[Dict]) -> Dict[str, List]:
        """
        Genera una tabla comparativa con todas las propiedades de los productos.
        
        Returns:
            Dict donde cada key es una propiedad y value es lista de valores por producto
        """
        table = {}
        
        # Propiedades principales a comparar (en orden de importancia)
        main_props = [
            'tieneNombre',
            'tienePrecio',
            'tieneRAM_GB',
            'tieneAlmacenamiento_GB',
            'tieneCalificacion',
            'tienePulgadas',
            'procesadorModelo',
            'bateriaCapacidad_mAh',
            'garantiaMeses',
            'tieneDescuento',
            'tieneMarca',
            'vendidoPor',
            'tieneSistemaOperativo'
        ]
        
        # Recopilar todas las propiedades únicas
        all_props = set()
        for product in products:
            props = product.get('properties', {})
            all_props.update(props.keys())
        
        # Ordenar: primero las principales, luego el resto
        ordered_props = [p for p in main_props if p in all_props]
        remaining = sorted([p for p in all_props if p not in main_props])
        ordered_props.extend(remaining)
        
        # Construir tabla
        for prop in ordered_props:
            values = []
            for product in products:
                value = product.get('properties', {}).get(prop, 'N/A')
                # Manejar listas
                if isinstance(value, list):
                    value = value[0] if value else 'N/A'
                values.append(value)
            table[prop] = values
        
        return table

    def _check_swrl_relations(self, product_ids: List[str]) -> Dict[str, Any]:
        """
        Verifica relaciones SWRL entre los productos.
        """
        relations = {
            "esMejorOpcionQue": [],
            "tieneMejorRAMQue": [],
            "tieneMejorAlmacenamientoQue": [],
            "tieneMejorPantallaQue": [],
            "esEquivalenteTecnico": [],
            "rules_applied": []
        }
        
        # Mapeo de propiedades SWRL a nombres amigables
        swrl_props = [
            ("esMejorOpcionQue", "EncontrarMejorPrecio"),
            ("tieneMejorRAMQue", "CompararRAM"),
            ("tieneMejorAlmacenamientoQue", "CompararAlmacenamiento"),
            ("tieneMejorPantallaQue", "CompararPantalla"),
            ("esEquivalenteTecnico", "DetectarEquivalentesTecnicos")
        ]
        
        for i, p1_id in enumerate(product_ids):
            for p2_id in product_ids[i+1:]:
                # Verificar cada propiedad SWRL
                for prop, rule_name in swrl_props:
                    # Verificar p1 -> p2
                    if self.inference_engine.check_object_property(p1_id, prop, p2_id):
                        relations[prop].append({
                            "source": p1_id,
                            "target": p2_id,
                            "rule": rule_name
                        })
                        if rule_name not in relations["rules_applied"]:
                            relations["rules_applied"].append(rule_name)
                            
                    # Verificar p2 -> p1 (si aplica, algunas son simétricas)
                    if self.inference_engine.check_object_property(p2_id, prop, p1_id):
                        relations[prop].append({
                            "source": p2_id,
                            "target": p1_id,
                            "rule": rule_name
                        })
                        if rule_name not in relations["rules_applied"]:
                            relations["rules_applied"].append(rule_name)
        
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
            if r.get("source") == winner_id
        ]
        
        if swrl_wins:
            reasons.append(
                f"Inferido por SWRL como mejor opción (regla: {swrl_wins[0].get('rule', 'SWRL')})"
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

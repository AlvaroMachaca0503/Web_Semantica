"""
Servicio de Recomendaciones - PARTE 2
Motor inteligente de recomendaciones basado en preferencias del usuario
"""
import sys
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ontology.loader import get_ontology
from services.product_service import ProductService
from reasoning.inference_engine import InferenceEngine
from models.recommendation import UserPreferences, RecommendationItem


class RecommendationService:
    """
    Servicio de recomendaciones personalizadas.
    
    Utiliza:
    - Preferencias del usuario (presupuesto, categoría, specs)
    - Scoring multi-factor similar al de comparación
    - Inferencias SWRL (esMejorOpcionQue, LaptopGamer)
    - Filtros SPARQL para búsqueda eficiente
    """
    
    def __init__(self):
        self.onto = get_ontology()
        self.product_service = ProductService()
        self.inference_engine = InferenceEngine(self.onto)
    
    def get_recommendations(
        self, 
        preferences: UserPreferences,
        limit: int = 5
    ) -> Dict[str, Any]:
        """
        Genera recomendaciones personalizadas basadas en preferencias.
        
        Args:
            preferences: Preferencias del usuario
            limit: Número máximo de recomendaciones a retornar
            
        Returns:
            Lista de productos recomendados con scores y razones
        """
        # Paso 1: Obtener todos los productos
        all_products = self.product_service.get_all_products()
        
        # Paso 2: Filtrar productos que cumplan criterios básicos
        filtered = self._filter_by_preferences(all_products, preferences)
        
        # Paso 3: Calcular score de recomendación para cada producto
        scored_products = []
        for product in filtered:
            score_data = self._calculate_recommendation_score(
                product, 
                preferences, 
                all_products
            )
            scored_products.append(score_data)
        
        # Paso 4: Ordenar por score descendente
        scored_products.sort(key=lambda x: x['score'], reverse=True)
        
        # Paso 5: Tomar top N
        top_recommendations = scored_products[:limit]
        
        # Paso 6: Convertir a formato de respuesta
        recommendations = []
        for item in top_recommendations:
            recommendations.append(RecommendationItem(
                product_id=item['product_id'],
                score=item['score'],
                reason=item['reason'],
                match_percentage=item['match_percentage']
            ))
        
        return {
            "success": True,
            "total_matches": len(filtered),
            "recommendations": recommendations,
            "preferences_used": preferences
        }
    
    def _filter_by_preferences(
        self, 
        products: List[Dict], 
        prefs: UserPreferences
    ) -> List[Dict]:
        """Filtra productos por criterios básicos de preferencias"""
        filtered = []
        
        for product in products:
            props = product.get('properties', {})
            types = product.get('types', [])
            
            # Filtro 1: Presupuesto
            price = self._get_numeric(props.get('tienePrecio'))
            if prefs.budget and price:
                if price > prefs.budget:
                    continue
            
            if prefs.min_budget and price:
                if price < prefs.min_budget:
                    continue
            
            # Filtro 2: Categoría
            if prefs.preferred_category:
                if prefs.preferred_category not in types:
                    continue
            
            # Filtro 3: RAM
            if prefs.min_ram:
                ram = self._get_numeric(props.get('tieneRAM_GB', 0))
                if ram < prefs.min_ram:
                    continue
            
            # Filtro 4: Almacenamiento
            if prefs.min_storage:
                storage = self._get_numeric(props.get('tieneAlmacenamiento_GB', 0))
                if storage < prefs.min_storage:
                    continue
            
            # Filtro 5: Calificación
            if prefs.min_rating:
                rating = self._get_numeric(props.get('tieneCalificacion', 0))
                if rating < prefs.min_rating:
                    continue
            
            filtered.append(product)
        
        return filtered
    
    def _calculate_recommendation_score(
        self,
        product: Dict,
        prefs: UserPreferences,
        all_products: List[Dict]
    ) -> Dict[str, Any]:
        """
        Calcula score de recomendación (0-100) basado en múltiples factores.
        
        Factores:
        - Ajuste a presupuesto (mejor si más barato dentro del rango)
        - Calificación de usuarios
        - Especificaciones técnicas (RAM, Storage)
        - Bonus SWRL (si es LaptopGamer, MejorOpcionQue, etc.)
        """
        score = 0.0
        reasons = []
        match_criteria = 0
        total_criteria = 0
        
        props = product.get('properties', {})
        product_id = product.get('id')
        types = product.get('types', [])
        
        # Factor 1: Presupuesto (30 puntos máx)
        if prefs.budget:
            total_criteria += 1
            price = self._get_numeric(props.get('tienePrecio', 0))
            if price > 0:
                # Mejor score si está cerca del límite pero sin pasarse
                budget_usage = price / prefs.budget
                if budget_usage <= 1.0:
                    match_criteria += 1
                    score += (1 - budget_usage * 0.5) * 30  # Máx 30 pts
                    if budget_usage < 0.7:
                        reasons.append(f"Excelente precio (${price}, dentro de tu presupuesto)")
                    else:
                        reasons.append(f"Precio ajustado (${price})")
        
        # Factor 2: Calificación (25 puntos máx)
        if prefs.min_rating:
            total_criteria += 1
        
        rating = self._get_numeric(props.get('tieneCalificacion', 0))
        if rating > 0:
            if prefs.min_rating and rating >= prefs.min_rating:
                match_criteria += 1
            score += rating * 5  # Máx 25 pts (5 * 5)
            if rating >= 4.5:
                reasons.append(f"Excelente calificación ({rating}/5)")
        
        # Factor 3: RAM (15 puntos máx)
        if prefs.min_ram:
            total_criteria += 1
        
        ram = self._get_numeric(props.get('tieneRAM_GB', 0))
        if ram > 0:
            if prefs.min_ram and ram >= prefs.min_ram:
                match_criteria += 1
                score += 15
                if ram >= 16:
                    reasons.append(f"Alta RAM ({ram}GB)")
        
        # Factor 4: Almacenamiento (10 puntos máx)
        if prefs.min_storage:
            total_criteria += 1
        
        storage = self._get_numeric(props.get('tieneAlmacenamiento_GB', 0))
        if storage > 0:
            if prefs.min_storage and storage >= prefs.min_storage:
                match_criteria += 1
                score += 10
        
        # Factor 5: Bonus SWRL (20 puntos máx)
        # Si es LaptopGamer (inferido)
        if 'LaptopGamer' in types:
            score += 10
            reasons.append("Laptop Gamer detectado (SWRL)")
        
        # Si tiene descuento
        discount = self._get_numeric(props.get('tieneDescuento', 0))
        if discount > 0:
            score += discount * 0.5  # Bonus por descuento
            reasons.append(f"Tiene descuento del {discount}%")
            
        # Si tiene buena garantía
        warranty = self._get_numeric(props.get('garantiaMeses', 0))
        if warranty >= 24:
            score += 5
            reasons.append(f"Garantía extendida ({warranty} meses)")
            
        # Si es mejor opción que otros
        better_than_count = 0
        for other_product in all_products[:5]:  # Comparar con algunos
            if other_product['id'] != product_id:
                if self.inference_engine.is_better_option(product_id, other_product['id']):
                    better_than_count += 1
        
        if better_than_count > 0:
            score += better_than_count * 2  # Máx 10 pts
            reasons.append(f"Mejor opción que {better_than_count} productos similares")
            
        # Verificar reglas de recomendación SWRL
        # Nota: Esto requeriría un usuario real en la ontología, pero simulamos la lógica
        if prefs.budget:
            price = self._get_numeric(props.get('tienePrecio', 0))
            if price <= prefs.budget:
                # Simular regla RecomendarPorPresupuesto
                score += 10
                reasons.append("Recomendado por presupuesto (SWRL)")
        
        # Calcular porcentaje de coincidencia
        match_percentage = (match_criteria / total_criteria * 100) if total_criteria > 0 else 0
        
        # Razón principal
        main_reason = " | ".join(reasons) if reasons else "Cumple criterios básicos"
        
        return {
            "product_id": product_id,
            "score": round(score, 2),
            "reason": main_reason,
            "match_percentage": round(match_percentage, 2)
        }
    
    def _get_numeric(self, value):
        """Extrae valor numérico de forma segura"""
        if value is None:
            return 0
        
        if isinstance(value, list):
            if not value:
                return 0
            value = value[0]
        
        if isinstance(value, (int, float)):
            return float(value)
        
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0

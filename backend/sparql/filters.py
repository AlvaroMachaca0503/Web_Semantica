"""
Filtros SPARQL Avanzados - DÍA 2
Filtros combinados y ordenamiento
"""
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


class SPARQLFilters:
    """
    Clase para aplicar filtros avanzados y ordenamiento a resultados.
    """
    
    def __init__(self):
        pass
    
    def filter_combined(
        self,
        products: List[Dict],
        price_range: Optional[tuple] = None,
        ram_min: Optional[int] = None,
        category: Optional[str] = None,
        storage_min: Optional[int] = None
    ) -> List[Dict]:
        """
        Aplica múltiples filtros combinados a una lista de productos.
        
        Args:
            products: Lista de productos a filtrar
            price_range: Tupla (min, max) para precio
            ram_min: RAM mínima en GB
            category: Categoría del producto
            storage_min: Almacenamiento mínimo en GB
            
        Returns:
            Lista filtrada de productos
        """
        result = products.copy()
        
        # Filtro de precio
        if price_range:
            min_price, max_price = price_range
            result = [
                p for p in result
                if self._check_price_range(p, min_price, max_price)
            ]
        
        # Filtro de RAM
        if ram_min is not None:
            result = [
                p for p in result
                if p.get('properties', {}).get('tieneRAM_GB', 0) >= ram_min
            ]
        
        # Filtro de categoría
        if category:
            result = [
                p for p in result
                if category.lower() in p.get('type', '').lower()
            ]
        
        # Filtro de almacenamiento
        if storage_min is not None:
            result = [
                p for p in result
                if p.get('properties', {}).get('tieneAlmacenamiento_GB', 0) >= storage_min
            ]
        
        return result
    
    def sort_by_price(
        self,
        products: List[Dict],
        ascending: bool = True
    ) -> List[Dict]:
        """
        Ordena productos por precio.
        
        Args:
            products: Lista de productos
            ascending: True para orden ascendente, False para descendente
            
        Returns:
            Lista ordenada
        """
        return sorted(
            products,
            key=lambda p: p.get('properties', {}).get('tienePrecio', float('inf')),
            reverse=not ascending
        )
    
    def sort_by_rating(
        self,
        products: List[Dict],
        ascending: bool = False
    ) -> List[Dict]:
        """
        Ordena productos por calificación.
        
        Args:
            products: Lista de productos
            ascending: True para orden ascendente, False para descendente
            
        Returns:
            Lista ordenada
        """
        return sorted(
            products,
            key=lambda p: p.get('properties', {}).get('tieneCalificacion', 0),
            reverse=not ascending
        )
    
    def sort_by_ram(
        self,
        products: List[Dict],
        ascending: bool = False
    ) -> List[Dict]:
        """
        Ordena productos por RAM.
        
        Args:
            products: Lista de productos
            ascending: True para orden ascendente, False para descendente
            
        Returns:
            Lista ordenada
        """
        return sorted(
            products,
            key=lambda p: p.get('properties', {}).get('tieneRAM_GB', 0),
            reverse=not ascending
        )
    
    def sort_results(
        self,
        products: List[Dict],
        sort_by: str = "price",
        ascending: bool = True
    ) -> List[Dict]:
        """
        Ordena resultados por el campo especificado.
        
        Args:
            products: Lista de productos
            sort_by: Campo para ordenar ('price', 'rating', 'ram', 'storage')
            ascending: Orden ascendente o descendente
            
        Returns:
            Lista ordenada
        """
        if sort_by == "price":
            return self.sort_by_price(products, ascending)
        elif sort_by == "rating":
            return self.sort_by_rating(products, ascending)
        elif sort_by == "ram":
            return self.sort_by_ram(products, ascending)
        elif sort_by == "storage":
            return sorted(
                products,
                key=lambda p: p.get('properties', {}).get('tieneAlmacenamiento_GB', 0),
                reverse=not ascending
            )
        else:
            # Por defecto, ordenar por precio
            return self.sort_by_price(products, ascending)
    
    def apply_filters(
        self,
        products: List[Dict],
        filters: Dict[str, Any]
    ) -> List[Dict]:
        """
        Aplica un diccionario de filtros dinámicamente.
        
        Args:
            products: Lista de productos
            filters: Diccionario con filtros a aplicar
            
        Returns:
            Lista filtrada
        """
        result = products.copy()
        
        for key, value in filters.items():
            if value is None:
                continue
            
            if key == "min_price":
                result = [
                    p for p in result
                    if p.get('properties', {}).get('tienePrecio', 0) >= value
                ]
            elif key == "max_price":
                result = [
                    p for p in result
                    if p.get('properties', {}).get('tienePrecio', float('inf')) <= value
                ]
            elif key == "min_ram":
                result = [
                    p for p in result
                    if p.get('properties', {}).get('tieneRAM_GB', 0) >= value
                ]
            elif key == "category":
                result = [
                    p for p in result
                    if value.lower() in p.get('type', '').lower()
                ]
            elif key == "min_rating":
                result = [
                    p for p in result
                    if p.get('properties', {}).get('tieneCalificacion', 0) >= value
                ]
        
        # Aplicar ordenamiento si está especificado
        if "sort_by" in filters:
            sort_order = filters.get("sort_order", "asc")
            result = self.sort_results(
                result,
                sort_by=filters["sort_by"],
                ascending=(sort_order == "asc")
            )
        
        return result
    
    def _check_price_range(
        self,
        product: Dict,
        min_price: Optional[float],
        max_price: Optional[float]
    ) -> bool:
        """Verifica si un producto está en el rango de precio."""
        price = product.get('properties', {}).get('tienePrecio')
        
        if price is None:
            return False
        
        if min_price is not None and price < min_price:
            return False
        
        if max_price is not None and price > max_price:
            return False
        
        return True
    
    def get_top_n(
        self,
        products: List[Dict],
        n: int = 10,
        sort_by: str = "price"
    ) -> List[Dict]:
        """
        Obtiene los top N productos según un criterio.
        
        Args:
            products: Lista de productos
            n: Número de productos a retornar
            sort_by: Criterio de ordenamiento
            
        Returns:
            Top N productos
        """
        sorted_products = self.sort_results(products, sort_by=sort_by)
        return sorted_products[:n]
    
    def filter_by_keyword(
        self,
        products: List[Dict],
        keyword: str
    ) -> List[Dict]:
        """
        Filtra productos que contengan una palabra clave.
        
        Args:
            products: Lista de productos
            keyword: Palabra clave a buscar
            
        Returns:
            Productos que contienen la palabra clave
        """
        keyword_lower = keyword.lower()
        
        result = []
        for product in products:
            # Buscar en nombre
            name = product.get('properties', {}).get('tieneNombre', '')
            if keyword_lower in name.lower():
                result.append(product)
                continue
            
            # Buscar en tipo
            if keyword_lower in product.get('type', '').lower():
                result.append(product)
                continue
            
            # Buscar en descripción si existe
            desc = product.get('properties', {}).get('tieneDescripcion', '')
            if keyword_lower in desc.lower():
                result.append(product)
        
        return result

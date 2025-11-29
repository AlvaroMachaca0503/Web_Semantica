import sys
from pathlib import Path

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ontology.loader import get_ontology
from utils.owl_helpers import individual_to_dict, search_individuals_by_class

class ProductService:
    """Servicio para gestionar productos de la ontología"""
    
    def __init__(self):
        self.onto = get_ontology()
    
    def get_all_products(self):
        """Obtiene todos los productos"""
        # Buscar la clase Producto de forma más robusta
        producto_class = None
        for cls in self.onto.classes():
            if cls.name == "Producto":
                producto_class = cls
                break
        
        if not producto_class:
            return []
        
        products = []
        for product in list(producto_class.instances()):
            products.append(individual_to_dict(product))
        
        return products
    
    def get_product_by_id(self, product_id):
        """Obtiene un producto por su ID (nombre)"""
        # Buscar individuo por nombre (case insensitive)
        product_id_lower = product_id.lower()
        for ind in list(self.onto.individuals()):
            if ind.name and ind.name.lower() == product_id_lower:
                return individual_to_dict(ind)
        
        return None
    
    def get_products_by_category(self, category):
        """Obtiene productos por categoría (Electrónica, Hogar, Moda)"""
        # Buscar la clase de forma más robusta
        category_class = None
        for cls in self.onto.classes():
            if cls.name == category:
                category_class = cls
                break
        
        if not category_class:
            return []
        
        products = []
        for product in list(category_class.instances()):
            products.append(individual_to_dict(product))
        
        return products
    
    def get_smartphones(self):
        """Obtiene todos los smartphones"""
        return self.get_products_by_category("Smartphone")
    
    def get_laptops(self):
        """Obtiene todas las laptops"""
        return self.get_products_by_category("Laptop")
    
    def filter_by_price(self, min_price=None, max_price=None):
        """Filtra productos por rango de precio"""
        all_products = self.get_all_products()
        filtered = []
        
        for product in all_products:
            price = product.get("properties", {}).get("tienePrecio")
            
            if price is None:
                continue
            
            if min_price is not None and price < min_price:
                continue
            
            if max_price is not None and price > max_price:
                continue
            
            filtered.append(product)
        
        return filtered

import sys
from pathlib import Path

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ontology.loader import get_ontology
from utils.owl_helpers import individual_to_dict

class SWRLEngine:
    """Motor para consultar resultados de reglas SWRL"""
    
    def __init__(self):
        self.onto = get_ontology()
    
    def get_gaming_laptops(self):
        """Obtiene laptops clasificados como LaptopGamer por SWRL (RAM >= 16GB)"""
        laptops = []
        laptop_ids_found = set()
        
        # Primero buscar instancias directas de LaptopGamer (si la regla SWRL se ejecutó)
        gaming_class = None
        for cls in self.onto.classes():
            if cls.name == "LaptopGamer":
                gaming_class = cls
                break
        
        if gaming_class:
            for laptop in list(gaming_class.instances()):
                laptop_dict = individual_to_dict(laptop)
                laptops.append(laptop_dict)
                laptop_ids_found.add(laptop.name)
        
        # Buscar todas las laptops y verificar si tienen RAM >= 16GB
        laptop_class = None
        for cls in self.onto.classes():
            if cls.name == "Laptop":
                laptop_class = cls
                break
        
        if laptop_class:
            for laptop in list(laptop_class.instances()):
                # Evitar duplicados
                if laptop.name in laptop_ids_found:
                    continue
                
                props = individual_to_dict(laptop).get("properties", {})
                ram = props.get("tieneRAM_GB")
                
                # Manejar RAM que puede venir como lista o valor único
                ram_value = None
                if isinstance(ram, list):
                    # Si es lista, tomar el valor numérico más relevante (el que no sea almacenamiento)
                    for r in ram:
                        if isinstance(r, (int, float)) and r <= 64:  # RAM típicamente <= 64GB
                            ram_value = r
                            break
                elif isinstance(ram, (int, float)):
                    ram_value = ram
                
                # Verificar si tiene RAM >= 16GB
                if ram_value and ram_value >= 16:
                    laptop_dict = individual_to_dict(laptop)
                    laptops.append(laptop_dict)
                    laptop_ids_found.add(laptop.name)
        
        return laptops
    
    def get_best_price_products(self):
        """Obtiene productos con relación esMejorOpcionQue inferida por SWRL"""
        results = []
        
        # Buscar productos con mismo nombre y diferentes precios
        productos_por_nombre = {}
        
        # Primero agrupar productos por nombre
        for ind in list(self.onto.individuals()):
            try:
                props = individual_to_dict(ind).get("properties", {})
                nombre = props.get("tieneNombre")
                precio = props.get("tienePrecio")
                
                if nombre and precio is not None:
                    if nombre not in productos_por_nombre:
                        productos_por_nombre[nombre] = []
                    productos_por_nombre[nombre].append({
                        "individuo": ind,
                        "precio": precio
                    })
            except:
                continue
        
        # Buscar productos con mismo nombre y diferentes precios
        for nombre, productos in productos_por_nombre.items():
            if len(productos) >= 2:
                # Ordenar por precio
                productos.sort(key=lambda x: x["precio"])
                
                # El más barato es mejor opción que los demás
                mejor = productos[0]["individuo"]
                mejores_que = [p["individuo"] for p in productos[1:]]
                
                # Verificar si la relación ya existe o inferirla
                try:
                    better_than_attr = getattr(mejor, "esMejorOpcionQue", None)
                    if better_than_attr:
                        if not isinstance(better_than_attr, list):
                            better_than_attr = [better_than_attr]
                        mejores_que.extend(better_than_attr)
                    
                    # Agregar resultado
                    results.append({
                        "producto": individual_to_dict(mejor),
                        "mejor_que": [individual_to_dict(p) for p in mejores_que],
                        "razon": f"Mismo nombre '{nombre}' pero menor precio"
                    })
                except:
                    continue
        
        # También buscar relaciones explícitas
        for ind in list(self.onto.individuals()):
            try:
                better_than = getattr(ind, "esMejorOpcionQue", None)
                if better_than:
                    if not isinstance(better_than, list):
                        better_than = [better_than]
                    
                    if len(better_than) > 0:
                        # Verificar que no esté ya en results
                        ind_id = ind.name
                        ya_existe = any(r["producto"]["id"] == ind_id for r in results)
                        if not ya_existe:
                            results.append({
                                "producto": individual_to_dict(ind),
                                "mejor_que": [individual_to_dict(p) for p in better_than]
                            })
            except:
                continue
        
        return results
    
    def get_positive_reviews(self):
        """Obtiene reseñas clasificadas como Positivas (cal >= 4)"""
        # Buscar la clase Reseña_Positiva de forma más robusta
        positive_class = None
        for cls in self.onto.classes():
            if cls.name == "Reseña_Positiva":
                positive_class = cls
                break
        
        reviews = []
        
        # Buscar instancias directas de la clase
        if positive_class:
            for review in list(positive_class.instances()):
                reviews.append(individual_to_dict(review))
        
        # Si no hay instancias, buscar reseñas con calificación >= 4
        if len(reviews) == 0:
            # Buscar clase Reseña
            review_class = None
            for cls in self.onto.classes():
                if cls.name == "Reseña":
                    review_class = cls
                    break
            
            if review_class:
                for review in list(review_class.instances()):
                    props = individual_to_dict(review).get("properties", {})
                    calificacion = props.get("tieneCalificacion")
                    if calificacion and isinstance(calificacion, (int, float)) and calificacion >= 4:
                        reviews.append(individual_to_dict(review))
        
        return reviews
    
    def get_negative_reviews(self):
        """Obtiene reseñas clasificadas como Negativas (cal <= 2)"""
        # Buscar la clase Reseña_Negativa de forma más robusta
        negative_class = None
        for cls in self.onto.classes():
            if cls.name == "Reseña_Negativa":
                negative_class = cls
                break
        
        reviews = []
        
        # Buscar instancias directas de la clase
        if negative_class:
            for review in list(negative_class.instances()):
                reviews.append(individual_to_dict(review))
        
        # Si no hay instancias, buscar reseñas con calificación <= 2
        if len(reviews) == 0:
            # Buscar clase Reseña
            review_class = None
            for cls in self.onto.classes():
                if cls.name == "Reseña":
                    review_class = cls
                    break
            
            if review_class:
                for review in list(review_class.instances()):
                    props = individual_to_dict(review).get("properties", {})
                    calificacion = props.get("tieneCalificacion")
                    if calificacion and isinstance(calificacion, (int, float)) and calificacion <= 2:
                        reviews.append(individual_to_dict(review))
        
        return reviews

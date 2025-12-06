from owlready2 import *

def get_individual_properties(individual):
    """Extrae todas las propiedades de un individuo como dict"""
    props = {}
    
    try:
        # Obtener todas las propiedades del individuo
        all_props = list(individual.get_properties())
        
        # Data Properties
        for prop in all_props:
            if isinstance(prop, DataPropertyClass):
                try:
                    values = getattr(individual, prop.python_name, None)
                    if values is not None:
                        # Convertir valores a tipos nativos de Python
                        processed_values = []
                        raw_values = values if isinstance(values, list) else [values]
                        
                        for v in raw_values:
                            # Convertir Decimal a float para JSON serialization
                            if hasattr(v, 'to_eng_string'): # Check for Decimal-like objects
                                processed_values.append(float(v))
                            else:
                                processed_values.append(v)
                        
                        # Asignar al diccionario
                        if len(processed_values) == 1:
                            props[prop.python_name] = processed_values[0]
                        elif len(processed_values) > 1:
                            props[prop.python_name] = processed_values
                except:
                    pass
        
        # Object Properties
        for prop in all_props:
            if isinstance(prop, ObjectPropertyClass):
                try:
                    values = getattr(individual, prop.python_name, None)
                    if values is not None:
                        if isinstance(values, list):
                            props[prop.python_name] = [obj.name if hasattr(obj, 'name') else str(obj) for obj in values]
                        else:
                            props[prop.python_name] = values.name if hasattr(values, 'name') else str(values)
                except:
                    pass
    except Exception as e:
        # Si hay error, intentar obtener propiedades básicas
        print(f"Error extracting properties for {individual.name}: {e}")
        pass
    
    return props

def get_individual_classes(individual):
    """Obtiene todas las clases (directas e inferidas) de un individuo"""
    classes = set()

    # Obtener clases directas
    for cls in individual.is_a:
        if hasattr(cls, 'name'):
            classes.add(cls.name)

    # Obtener clases inferidas usando INDIRECT_is_a (incluye herencia y razonamiento)
    try:
        for cls in individual.INDIRECT_is_a:
            if hasattr(cls, 'name') and cls.name != 'Thing':
                classes.add(cls.name)
    except:
        pass

    return list(classes)

def apply_swrl_rules_to_types(individual, base_types, properties):
    """
    Aplica reglas SWRL manualmente para agregar tipos inferidos.

    Dado que ni HermiT ni Pellet ejecutan reglas SWRL automáticamente en Owlready2,
    esta función implementa las reglas manualmente para garantizar el comportamiento esperado.

    Reglas implementadas:
    1. DetectarGamer: Laptop con RAM >= 16GB -> LaptopGamer
    """
    types = base_types.copy()

    # Regla 1: DetectarGamer (RAM >= 16GB -> LaptopGamer)
    if "Laptop" in types:
        ram = properties.get("tieneRAM_GB", 0)
        if isinstance(ram, (int, float)) and ram >= 16:
            if "LaptopGamer" not in types:
                types.append("LaptopGamer")

    return types

def individual_to_dict(individual):
    """Convierte un individuo OWL a diccionario JSON-serializable

    Usa el razonador Pellet para inferencias OWL básicas (taxonomía, propiedades),
    pero aplica reglas SWRL manualmente ya que Pellet no las ejecuta automáticamente.
    """
    base_types = get_individual_classes(individual)
    properties = get_individual_properties(individual)

    # Aplicar reglas SWRL manualmente (Pellet no las ejecuta)
    final_types = apply_swrl_rules_to_types(individual, base_types, properties)

    return {
        "id": individual.name,
        "types": final_types,
        "properties": properties
    }

def search_individuals_by_class(onto, class_name):
    """Busca todos los individuos de una clase específica"""
    # Buscar la clase de forma más robusta
    for cls in onto.classes():
        if cls.name == class_name:
            return list(cls.instances())
    return []

def search_individuals_by_property(onto, prop_name, prop_value):
    """Busca individuos por valor de propiedad"""
    results = []
    for ind in onto.individuals():
        props = get_individual_properties(ind)
        if prop_name in props and props[prop_name] == prop_value:
            results.append(ind)
    return results

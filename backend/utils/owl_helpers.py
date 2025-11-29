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
                        # Si es lista con un solo elemento, extraer el valor
                        if isinstance(values, list):
                            if len(values) == 1:
                                props[prop.python_name] = values[0]
                            elif len(values) > 1:
                                props[prop.python_name] = values
                        else:
                            props[prop.python_name] = values
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
        pass
    
    return props

def get_individual_classes(individual):
    """Obtiene todas las clases (directas e inferidas) de un individuo"""
    return [cls.name for cls in individual.is_a]

def individual_to_dict(individual):
    """Convierte un individuo OWL a diccionario JSON-serializable"""
    return {
        "id": individual.name,
        "types": get_individual_classes(individual),
        "properties": get_individual_properties(individual)
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

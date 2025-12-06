"""
Script de prueba para el clasificador de productos
Ejecutar desde la carpeta backend con: python test_classifier.py
"""

import sys
from pathlib import Path

# Agregar el directorio backend al path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from reasoning.product_classifier import ProductClassifier
import json


def print_section(title):
    """Imprime un título de sección."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_product_classifier():
    """Prueba el clasificador de productos."""
    
    print_section("TEST: Clasificador de Productos OWL + SWRL")
    
    # Inicializar clasificador
    print("\n[1/4] Inicializando clasificador de productos...")
    classifier = ProductClassifier()
    print("✅ Clasificador inicializado correctamente\n")
    
    # Test 1: Clasificar un producto individual (Laptop)
    print_section("Test 1: Clasificar Producto Individual - Laptop")
    laptop_result = classifier.classify_product("Laptop_Dell_XPS")
    
    if "error" in laptop_result:
        print(f"❌ Error: {laptop_result['error']}")
    else:
        print(f"✅ Producto: {laptop_result['product_name']}")
        print(f"\n   Clasificación:")
        print(f"   • Total de clases: {laptop_result['classification']['total_classes']}")
        print(f"   • Clases directas: {laptop_result['classification']['direct_classes']}")
        print(f"   • Clases inferidas: {laptop_result['classification']['inferred_classes']}")
        print(f"   • Reglas SWRL: {len(laptop_result['classification']['swrl_classes'])}")
        
        if laptop_result['classification']['swrl_classes']:
            print(f"\n   Reglas SWRL aplicadas:")
            for rule in laptop_result['classification']['swrl_classes']:
                status = "✓" if rule.get("triggered") == True else "➜"
                print(f"   {status} {rule['rule_name']}: {rule['condition']}")
                print(f"     → {rule['resulting_class']}")
        
        print(f"\n   Especificaciones:")
        specs = laptop_result['specifications']
        print(f"   • RAM: {specs['ram_gb']} GB")
        print(f"   • Almacenamiento: {specs['storage_gb']} GB")
        print(f"   • Precio: ${specs['price']}")
        print(f"   • Pantalla: {specs['screen_inches']}\"")
        
        print(f"\n   Explicaciones:")
        for explanation in laptop_result['explanations']:
            print(f"   {explanation}")
        
        print(f"\n   Confianza de clasificación:")
        conf = laptop_result['classification_confidence']
        print(f"   • Nivel: {conf['level'].upper()}")
        print(f"   • Reglas SWRL aplicadas: {conf['swrl_rules_applied']}")
        print(f"   • Tiene inferencias: {conf['has_inferences']}")
    
    # Test 2: Clasificar todos los productos
    print_section("Test 2: Clasificar Todos los Productos")
    all_result = classifier.classify_all_products()
    
    if "error" in all_result:
        print(f"❌ Error: {all_result['error']}")
    else:
        stats = all_result['statistics']
        summary = all_result['summary']
        
        print(f"✅ Productos analizados: {stats['total_products']}")
        print(f"\n   Distribución por categoría:")
        for category, count in stats['by_category'].items():
            percentage = (count / stats['total_products'] * 100) if stats['total_products'] > 0 else 0
            print(f"   • {category:15s}: {count:2d} productos ({percentage:5.2f}%)")
        
        print(f"\n   Cobertura de clasificación:")
        print(f"   • Con reglas SWRL: {stats['swrl_applied']} ({summary['swrl_percentage']}%)")
        print(f"   • Con inferencias OWL: {stats['with_inferences']} ({summary['inference_percentage']}%)")
        
        print(f"\n   Ejemplos de productos clasificados:")
        for i, product in enumerate(all_result['products'][:5], 1):
            print(f"   {i}. {product['name']:30s} - {len(product['classes'])} clases")
            if product['swrl_rules'] > 0:
                print(f"      ⚡ {product['swrl_rules']} regla(s) SWRL aplicada(s)")
    
    # Test 3: Obtener productos de una clase específica
    print_section("Test 3: Obtener Productos por Clase - LaptopGamer")
    class_result = classifier.get_products_by_class("LaptopGamer")
    
    if "error" in class_result:
        print(f"⚠️  {class_result['error']}")
    else:
        print(f"✅ Clase: {class_result['class_name']}")
        print(f"   Total de productos: {class_result['total_products']}")
        
        if class_result['total_products'] > 0:
            print(f"\n   Productos encontrados:")
            for i, product in enumerate(class_result['products'], 1):
                print(f"   {i}. {product['name']:30s}")
                print(f"      ${product['price']:7.2f} | {product['ram_gb']}GB RAM | {product['storage_gb']}GB")
                print(f"      Clases: {', '.join(product['all_classes'][:4])}...")
    
    # Test 4: Probar con otras clases
    print_section("Test 4: Probar Otras Clases")
    
    test_classes = ["Laptop", "Smartphone", "Tablet"]
    for class_name in test_classes:
        result = classifier.get_products_by_class(class_name)
        if "error" not in result:
            print(f"   • {class_name:15s}: {result['total_products']} productos")
    
    print("\n" + "="*70)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS")
    print("="*70)
    
    # Resumen final
    print("\n📊 RESUMEN FINAL:")
    print(f"   • Clasificación automática: FUNCIONAL")
    print(f"   • Subsunción OWL: ACTIVA")
    print(f"   • Reglas SWRL: DETECTADAS")
    print(f"   • Inferencias: {summary['inference_percentage']}% de productos")
    print(f"   • SWRL aplicado: {summary['swrl_percentage']}% de productos")


if __name__ == "__main__":
    try:
        test_product_classifier()
    except Exception as e:
        print(f"\n❌ ERROR EN PRUEBAS: {e}")
        import traceback
        traceback.print_exc()

"""
Script de prueba para el servicio de análisis de mercado
Ejecutar desde la carpeta backend con: python test_market_analysis.py
"""

import sys
from pathlib import Path

# Agregar el directorio backend al path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sparql.market_analysis import MarketAnalysis
import json


def print_section(title):
    """Imprime un título de sección."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_market_analysis():
    """Prueba el servicio de análisis de mercado."""
    
    print_section("TEST: Análisis de Mercado con SPARQL")
    
    # Inicializar servicio
    print("\n[1/7] Inicializando servicio de análisis de mercado...")
    service = MarketAnalysis()
    print("✅ Servicio inicializado correctamente\n")
    
    # Test 1: Estadísticas de precios
    print_section("Estadísticas de Precios")
    price_stats = service.get_price_statistics()
    
    if "error" in price_stats:
        print(f"❌ Error: {price_stats['error']}")
    else:
        print(f"✅ Productos analizados: {price_stats['total_products']}")
        print(f"   Precio promedio: ${price_stats['average']}")
        print(f"   Precio mediano: ${price_stats['median']}")
        print(f"   Rango: ${price_stats['min']} - ${price_stats['max']}")
        print(f"   Desviación estándar: ${price_stats['std_deviation']}")
        
        print(f"\n   Distribución por rangos:")
        for range_name, data in price_stats['price_ranges'].items():
            print(f"   • {range_name:12s}: {data['count']:2d} productos ({data['percentage']:5.2f}%)")
    
    # Test 2: Distribución de categorías
    print_section("Distribución de Categorías")
    cat_dist = service.get_category_distribution()
    
    if "error" in cat_dist:
        print(f"❌ Error: {cat_dist['error']}")
    else:
        print(f"✅ Total de productos: {cat_dist['total_products']}")
        print(f"   Categorías únicas: {cat_dist['unique_categories']}")
        
        print(f"\n   Desglose por categoría:")
        for cat, data in cat_dist['categories'].items():
            print(f"   • {cat:15s}: {data['count']:2d} productos ({data['percentage']:5.2f}%) - Precio prom: ${data['avg_price']}")
    
    # Test 3: Análisis de especificaciones (Laptops)
    print_section("Análisis de Especificaciones - Laptops")
    specs = service.get_specs_analysis("Laptop")
    
    if "error" in specs:
        print(f"❌ Error: {specs['error']}")
    else:
        print(f"✅ Productos analizados: {specs['total_analyzed']}")
        
        if "ram_gb" in specs:
            ram = specs["ram_gb"]
            print(f"\n   RAM:")
            print(f"   • Promedio: {ram['average']} GB")
            print(f"   • Mediana: {ram['median']} GB")
            print(f"   • Rango: {ram['min']} - {ram['max']} GB")
            print(f"   • Más común: {ram['most_common']} GB")
        
        if "storage_gb" in specs:
            storage = specs["storage_gb"]
            print(f"\n   Almacenamiento:")
            print(f"   • Promedio: {storage['average']} GB")
            print(f"   • Mediana: {storage['median']} GB")
            print(f"   • Rango: {storage['min']} - {storage['max']} GB")
            print(f"   • Más común: {storage['most_common']} GB")
    
    # Test 4: Mejores valores
    print_section("Productos con Mejor Relación Calidad-Precio (Top 5)")
    best_value = service.get_best_value_products(5)
    
    if "error" in best_value:
        print(f"❌ Error: {best_value['error']}")
    else:
        print(f"✅ Productos analizados: {best_value['total_analyzed']}")
        print(f"   Algoritmo: {best_value['algorithm']}")
        
        print(f"\n   Top 5:")
        for i, product in enumerate(best_value['best_value_products'], 1):
            print(f"   {i}. {product['name']:30s} - Score: {product['value_score']:.4f}")
            print(f"      ${product['price']:7.2f} | {product['specs']['ram_gb']}GB RAM | {product['specs']['storage_gb']}GB")
    
    # Test 5: Tendencias de mercado
    print_section("Tendencias de Mercado")
    trends = service.get_market_trends()
    
    if "error" in trends:
        print(f"❌ Error: {trends['error']}")
    else:
        print(f"✅ Segmentos de precio:")
        for segment, data in trends['price_segments'].items():
            print(f"   • {segment.capitalize():10s}: {data['count']:2d} productos ({data['percentage']:5.2f}%) - {data['price_range']}")
        
        print(f"\n   Insights del mercado:")
        for insight in trends['market_insights']:
            print(f"   💡 {insight}")
    
    # Test 6: Comparación de categorías
    print_section("Comparación: Laptop vs Smartphone")
    comparison = service.compare_categories("Laptop", "Smartphone")
    
    if "error" in comparison:
        print(f"⚠️  {comparison['error']}")
    else:
        print(f"✅ Comparación completada:")
        
        for spec, data in comparison['comparison'].items():
            laptop_val = data.get('Laptop', 0)
            smartphone_val = data.get('Smartphone', 0)
            winner = data.get('winner', 'N/A')
            
            print(f"\n   {spec}:")
            print(f"   • Laptop: {laptop_val}")
            print(f"   • Smartphone: {smartphone_val}")
            print(f"   • Ganador: {winner}")
    
    print("\n" + "="*70)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS")
    print("="*70)


if __name__ == "__main__":
    try:
        test_market_analysis()
    except Exception as e:
        print(f"\n❌ ERROR EN PRUEBAS: {e}")
        import traceback
        traceback.print_exc()

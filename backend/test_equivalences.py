"""
Script de prueba para el servicio de equivalencias
Ejecutar desde la carpeta backend con: python test_equivalences.py
"""

import sys
from pathlib import Path

# Agregar el directorio backend al path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from services.equivalence_service import EquivalenceService
import json


def test_equivalences():
    """Prueba el servicio de equivalencias."""
    
    print("="*70)
    print("TEST: Servicio de Equivalencias Semánticas")
    print("="*70)
    
    # Inicializar servicio
    print("\n[1/3] Inicializando servicio de equivalencias...")
    service = EquivalenceService()
    print("✅ Servicio inicializado correctamente\n")
    
    # Probar búsqueda de equivalentes para un producto
    print("[2/3] Buscando equivalentes para 'Laptop_Dell_XPS'...")
    result = service.find_equivalent_products("Laptop_Dell_XPS")
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"✅ Producto: {result['product_name']}")
        print(f"✅ Total de equivalentes encontrados: {result['total_equivalents']}")
        print(f"\nResumen por criterio:")
        print(f"   - Explícitos: {result['criteria_summary']['explicit']}")
        print(f"   - Similares: {result['criteria_summary']['similar']}")
        print(f"   - Auto-detectados: {result['criteria_summary']['auto_detected']}")
        
        if result['equivalents']:
            print(f"\n   Equivalentes encontrados:")
            for eq in result['equivalents'][:5]:  # Mostrar solo los primeros 5
                print(f"   • {eq['name']} - {eq['match_type']} (confianza: {eq['confidence']}%)")
                print(f"     Razón: {eq['match_reason']}")
    
    # Probar comparación de dos productos
    print("\n[3/3] Comparando dos productos...")
    comparison = service.get_equivalence_comparison(
        "Laptop_Dell_XPS",
        "Laptop_MSI_Gaming"
    )
    
    if "error" in comparison:
        print(f"❌ Error: {comparison['error']}")
    else:
        print(f"✅ Comparación completada:")
        print(f"   Producto 1: {comparison['product1']['name']}")
        print(f"   Producto 2: {comparison['product2']['name']}")
        print(f"   ¿Son equivalentes?: {'Sí' if comparison['equivalent'] else 'No'}")
        print(f"   Score de equivalencia: {comparison['match_score']}/100")
        print(f"   Tipo: {comparison['match_type']}")
        print(f"   Recomendación: {comparison['recommendation']}")
        
        if comparison['reasons']:
            print(f"\n   Razones:")
            for reason in comparison['reasons']:
                print(f"   • {reason}")
    
    print("\n" + "="*70)
    print("✅ PRUEBAS COMPLETADAS")
    print("="*70)


if __name__ == "__main__":
    try:
        test_equivalences()
    except Exception as e:
        print(f"\n❌ ERROR EN PRUEBAS: {e}")
        import traceback
        traceback.print_exc()

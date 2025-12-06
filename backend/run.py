"""
Script de inicio rápido para SmartCompareMarket Backend
"""

from app import create_app
import config

def main():
    print("=" * 70)
    print("[START] SmartCompareMarket Backend - Iniciando...")
    print("=" * 70)

    # Crear aplicación
    app = create_app()

    print(f"\n[OK] Servidor corriendo en: http://{config.FLASK_CONFIG['host']}:{config.FLASK_CONFIG['port']}")
    print(f"[DOCS] Documentacion API: http://localhost:{config.FLASK_CONFIG['port']}/")
    print("\n[API] Endpoints disponibles:")
    print(f"   GET  /api/products")
    print(f"   GET  /api/products/<id>")
    print(f"   GET  /api/swrl/best-price")
    print(f"   GET  /api/swrl/gaming-laptops")
    print(f"   GET  /api/swrl/positive-reviews")
    print(f"   GET  /api/swrl/negative-reviews")
    print("\n[INFO] Presiona Ctrl+C para detener el servidor\n")
    print("=" * 70)
    
    # Iniciar servidor
    app.run(**config.FLASK_CONFIG)

if __name__ == "__main__":
    main()

from flask import Blueprint, jsonify, request
import sys
from pathlib import Path

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from services.product_service import ProductService

products_bp = Blueprint('products', __name__)
product_service = ProductService()

@products_bp.route('/products', methods=['GET'])
def get_products():
    """
    GET /api/products
    Query params:
    - category: Electrónica, Hogar, Moda, Smartphone, Laptop
    - min_price: precio mínimo
    - max_price: precio máximo
    """
    try:
        category = request.args.get('category')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Filtrar por categoría
        if category:
            products = product_service.get_products_by_category(category)
        else:
            products = product_service.get_all_products()
        
        # Filtrar por precio
        if min_price is not None or max_price is not None:
            filtered = []
            for product in products:
                price = product.get("properties", {}).get("tienePrecio")
                
                if price is None:
                    continue
                
                if min_price is not None and price < min_price:
                    continue
                
                if max_price is not None and price > max_price:
                    continue
                
                filtered.append(product)
            
            products = filtered
        
        return jsonify({
            "success": True,
            "count": len(products),
            "data": products
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@products_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """GET /api/products/:id"""
    try:
        product = product_service.get_product_by_id(product_id)
        
        if not product:
            return jsonify({
                "success": False,
                "error": "Producto no encontrado"
            }), 404
        
        return jsonify({
            "success": True,
            "data": product
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

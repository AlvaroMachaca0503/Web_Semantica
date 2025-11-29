from flask import Blueprint, jsonify
import sys
from pathlib import Path

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from reasoning.swrl_engine import SWRLEngine

swrl_bp = Blueprint('swrl', __name__)
swrl_engine = SWRLEngine()

@swrl_bp.route('/swrl/best-price', methods=['GET'])
def get_best_price():
    """
    GET /api/swrl/best-price
    Retorna productos con relación esMejorOpcionQue (inferida por SWRL)
    """
    try:
        results = swrl_engine.get_best_price_products()
        
        return jsonify({
            "success": True,
            "count": len(results),
            "rule": "EncontrarMejorPrecio",
            "description": "Productos con mismo nombre y menor precio",
            "data": results
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@swrl_bp.route('/swrl/gaming-laptops', methods=['GET'])
def get_gaming_laptops():
    """
    GET /api/swrl/gaming-laptops
    Retorna laptops clasificadas como LaptopGamer (RAM >= 16GB)
    """
    try:
        laptops = swrl_engine.get_gaming_laptops()
        
        return jsonify({
            "success": True,
            "count": len(laptops),
            "rule": "DetectarGamer",
            "description": "Laptops con RAM >= 16GB clasificadas automáticamente",
            "data": laptops
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@swrl_bp.route('/swrl/positive-reviews', methods=['GET'])
def get_positive_reviews():
    """
    GET /api/swrl/positive-reviews
    Retorna reseñas positivas (calificación >= 4)
    """
    try:
        reviews = swrl_engine.get_positive_reviews()
        
        return jsonify({
            "success": True,
            "count": len(reviews),
            "rule": "ClasificarPositivas",
            "description": "Reseñas con calificación >= 4",
            "data": reviews
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@swrl_bp.route('/swrl/negative-reviews', methods=['GET'])
def get_negative_reviews():
    """
    GET /api/swrl/negative-reviews
    Retorna reseñas negativas (calificación <= 2)
    """
    try:
        reviews = swrl_engine.get_negative_reviews()
        
        return jsonify({
            "success": True,
            "count": len(reviews),
            "rule": "ClasificarNegativas",
            "description": "Reseñas con calificación <= 2",
            "data": reviews
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

from flask import Flask, jsonify
from flask_cors import CORS
import config

# Importar blueprints
from api.routes.products import products_bp
from api.routes.swrl import swrl_bp

def create_app():
    """Factory para crear la aplicación Flask"""
    
    app = Flask(__name__)
    
    # Configurar CORS
    CORS(app, origins=config.CORS_ORIGINS)
    
    # Registrar blueprints
    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(swrl_bp, url_prefix='/api')
    
    # Ruta raíz
    @app.route('/')
    def index():
        return jsonify({
            "message": "SmartCompareMarket API",
            "version": "1.0.0",
            "endpoints": {
                "products": "/api/products",
                "product_by_id": "/api/products/<id>",
                "swrl_best_price": "/api/swrl/best-price",
                "swrl_gaming_laptops": "/api/swrl/gaming-laptops",
                "swrl_positive_reviews": "/api/swrl/positive-reviews",
                "swrl_negative_reviews": "/api/swrl/negative-reviews"
            }
        })
    
    # Health check
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(**config.FLASK_CONFIG)

# 🔥 DÍA 1 - Formateo JSON
"""
Utilidades para formatear respuestas JSON consistentes
"""

def success_response(data, count=None, message=None):
    """Formatea una respuesta exitosa"""
    response = {
        "success": True,
        "data": data
    }
    
    if count is not None:
        response["count"] = count
    
    if message:
        response["message"] = message
    
    return response

def error_response(error_message, status_code=500):
    """Formatea una respuesta de error"""
    return {
        "success": False,
        "error": str(error_message)
    }, status_code

def paginated_response(data, page, per_page, total):
    """Formatea una respuesta paginada"""
    return {
        "success": True,
        "data": data,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page
        }
    }

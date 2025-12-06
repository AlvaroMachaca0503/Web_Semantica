import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from services.comparison_service import ComparisonService

class TestComparisonService:
    @pytest.fixture
    def service(self):
        with patch('services.comparison_service.get_ontology'), \
             patch('services.comparison_service.InferenceEngine'), \
             patch('services.comparison_service.ProductService'):
            return ComparisonService()

    def test_calculate_score_basic(self, service):
        """Test basic score calculation logic"""
        # Mock product data
        product = {
            "properties": {
                "tienePrecio": 1000.0,  # Lower is better
                "tieneRAM_GB": 8,       # Higher is better
                "tieneAlmacenamiento_GB": 256,
                "tieneCalificacion": 4.5,
                "bateriaCapacidad_mAh": 4000
            }
        }
        
        # Test calculation
        # We need to ensure weights are loaded or use defaults
        # The service loads weights in _calculate_score if not mocked, which is fine
        
        score = service._calculate_score(product, "test_p1", ["test_p1", "test_p2"])
        assert isinstance(score, float)
        assert 0 <= score <= 100

    def test_calculate_score_logic_higher_is_better(self, service):
        """Test that higher values give higher scores for 'higher is better' attributes"""
        product_low = {
            "properties": {
                "tieneRAM_GB": 4, 
                "tienePrecio": 1000
            }
        }
        product_high = {
            "properties": {
                "tieneRAM_GB": 32, 
                "tienePrecio": 1000
            }
        }
        
        score_low = service._calculate_score(product_low, "p1", ["p1"])
        score_high = service._calculate_score(product_high, "p2", ["p2"])
        
        # RAM has 10% weight. 32GB should score better than 4GB
        assert score_high > score_low

    def test_calculate_score_logic_lower_is_better(self, service):
        """Test that lower values give higher scores for 'lower is better' attributes"""
        product_expensive = {
            "properties": {
                "tienePrecio": 2000,
                "tieneRAM_GB": 8
            }
        }
        product_cheap = {
            "properties": {
                "tienePrecio": 500,
                "tieneRAM_GB": 8
            }
        }
        
        score_exp = service._calculate_score(product_expensive, "p1", ["p1"])
        score_cheap = service._calculate_score(product_cheap, "p2", ["p2"])
        
        # Price has 14% weight. 500 should score better than 2000
        assert score_cheap > score_exp

    def test_compare_products_winner(self, service):
        """Test determining a winner"""
        # Mock product service responses
        service.product_service.get_product_by_id.side_effect = lambda pid: {
            "id": pid,
            "properties": {
                "tienePrecio": 1000 if pid == "p1" else 2000, # p1 cheaper
                "tieneRAM_GB": 16 if pid == "p1" else 8,      # p1 more RAM
                "tieneCalificacion": 5.0 if pid == "p1" else 3.0 # p1 better rating
            }
        }
        
        service.inference_engine.is_better_option.return_value = False
        service.inference_engine.check_compatibility.return_value = {}
        service.inference_engine.check_object_property.return_value = False

        result = service.compare_products(["p1", "p2"])
        
        assert result["winner"] == "p1"
        assert result["winner_score"] > result["all_scores"]["p2"]

    def test_compare_products_not_found(self, service):
        """Test behavior when product not found"""
        service.product_service.get_product_by_id.return_value = None
        
        with pytest.raises(ValueError):
            service.compare_products(["non_existent", "p2"])

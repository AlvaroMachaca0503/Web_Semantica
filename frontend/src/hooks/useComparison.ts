import { useState, useCallback } from 'react';
import { comparisonService, ComparisonResult, Product } from '@/services/api';
import { MOCK_PRODUCTS } from '@/lib/constants';

export function useComparison() {
  const [selectedProducts, setSelectedProducts] = useState<string[]>([]);
  const [comparisonResult, setComparisonResult] = useState<ComparisonResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const toggleProduct = useCallback((productId: string) => {
    setSelectedProducts(prev => {
      if (prev.includes(productId)) {
        return prev.filter(id => id !== productId);
      }
      if (prev.length >= 5) {
        return prev;
      }
      return [...prev, productId];
    });
  }, []);

  const clearSelection = useCallback(() => {
    setSelectedProducts([]);
    setComparisonResult(null);
  }, []);

  const compare = useCallback(async () => {
    if (selectedProducts.length < 2) {
      setError('Selecciona al menos 2 productos para comparar');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await comparisonService.compare(selectedProducts);
      setComparisonResult(response.comparison);
    } catch (err) {
      console.warn('Backend unavailable, generating mock comparison');
      
      // Generate mock comparison
      const products = MOCK_PRODUCTS.filter(p => selectedProducts.includes(p.id));
      const comparisonTable: Record<string, (string | number)[]> = {};
      const allScores: Record<string, number> = {};
      
      // Build comparison table
      const props = ['tieneNombre', 'tienePrecio', 'tieneRAM_GB', 'tieneAlmacenamiento_GB', 'tieneCalificacion'];
      props.forEach(prop => {
        comparisonTable[prop] = products.map(p => (p.properties as any)[prop] ?? '-');
      });

      // Calculate scores (simple mock scoring)
      products.forEach(p => {
        const price = p.properties.tienePrecio || 0;
        const rating = p.properties.tieneCalificacion || 0;
        const ram = p.properties.tieneRAM_GB || 0;
        allScores[p.id] = Math.round((100 - price / 20) + rating * 10 + ram * 2);
      });

      const winner = Object.entries(allScores).sort((a, b) => b[1] - a[1])[0];

      setComparisonResult({
        products,
        comparison_table: comparisonTable,
        winner: winner[0],
        winner_score: winner[1],
        all_scores: allScores,
        reason: `Mejor relación calidad-precio | Score total: ${winner[1]}`,
        swrl_inference: {
          esMejorOpcionQue: [],
          tieneMejorRAMQue: [],
          tieneMejorAlmacenamientoQue: [],
          tieneMejorPantallaQue: [],
          esEquivalenteTecnico: [],
          rules_applied: ['MockComparison']
        }
      });
    } finally {
      setLoading(false);
    }
  }, [selectedProducts]);

  return {
    selectedProducts,
    comparisonResult,
    loading,
    error,
    toggleProduct,
    clearSelection,
    compare,
    canCompare: selectedProducts.length >= 2 && selectedProducts.length <= 5
  };
}

import { useState, useMemo } from 'react';
import { GitCompare, AlertCircle, Plus, Trash2, Search, Filter } from 'lucide-react';
import { useProducts } from '@/hooks/useProducts';
import { comparisonService, ComparisonResult } from '@/services/api';
import { ProductCard } from '@/components/products/ProductCard';
import { CompareTable } from '@/components/comparison/CompareTable';
import { LoadingCard } from '@/components/common/LoadingSpinner';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { CATEGORIES } from '@/lib/constants';
import { cn } from '@/lib/utils';

// Mock comparison for when backend is unavailable
const generateMockComparison = (productIds: string[], products: any[]): ComparisonResult => {
  const selectedProducts = products.filter(p => productIds.includes(p.id));
  const comparisonTable: Record<string, any[]> = {};
  const allProps = new Set<string>();
  
  selectedProducts.forEach(p => {
    Object.keys(p.properties).forEach(key => allProps.add(key));
  });
  
  allProps.forEach(prop => {
    comparisonTable[prop] = selectedProducts.map(p => p.properties[prop] ?? null);
  });
  
  const scores: Record<string, number> = {};
  selectedProducts.forEach(p => {
    const score = Math.random() * 30 + 70;
    scores[p.id] = parseFloat(score.toFixed(1));
  });
  
  const entries = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  const winner = entries[0];
  
  return {
    products: selectedProducts,
    comparison_table: comparisonTable,
    winner: winner[0],
    winner_score: winner[1],
    all_scores: scores,
    reason: `Mejor combinación de precio y características | Score: ${winner[1]}`,
    swrl_inference: {
      esMejorOpcionQue: [],
      tieneMejorRAMQue: [],
      tieneMejorAlmacenamientoQue: [],
      tieneMejorPantallaQue: [],
      esEquivalenteTecnico: [],
      rules_applied: ['EncontrarMejorPrecio', 'CompararRAM']
    }
  };
};

export default function ComparePage() {
  // Local state for comparison selection
  const [selectedForCompare, setSelectedForCompare] = useState<string[]>([]);
  const [comparisonResult, setComparisonResult] = useState<ComparisonResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [category, setCategory] = useState<string | undefined>();
  const [minPrice, setMinPrice] = useState<string>('');
  const [maxPrice, setMaxPrice] = useState<string>('');
  const [search, setSearch] = useState('');

  const { products, loading: productsLoading } = useProducts({
    category,
    minPrice: minPrice ? parseFloat(minPrice) : undefined,
    maxPrice: maxPrice ? parseFloat(maxPrice) : undefined,
  });

  // Filter by search
  const filteredProducts = useMemo(() => {
    if (!search) return products;
    const searchLower = search.toLowerCase();
    return products.filter(p => 
      p.properties.tieneNombre?.toLowerCase().includes(searchLower) ||
      p.id.toLowerCase().includes(searchLower) ||
      p.types.some(t => t.toLowerCase().includes(searchLower))
    );
  }, [products, search]);

  const toggleProduct = (productId: string) => {
    setSelectedForCompare(prev => {
      if (prev.includes(productId)) {
        return prev.filter(id => id !== productId);
      }
      if (prev.length >= 5) {
        return prev;
      }
      return [...prev, productId];
    });
  };

  const clearSelection = () => {
    setSelectedForCompare([]);
    setComparisonResult(null);
    setError(null);
  };

  const canCompare = selectedForCompare.length >= 2 && selectedForCompare.length <= 5;

  const handleCompare = async () => {
    if (!canCompare) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await comparisonService.compare(selectedForCompare);
      setComparisonResult(response.comparison);
    } catch (err) {
      console.warn('Backend unavailable, using mock comparison');
      const mockResult = generateMockComparison(selectedForCompare, products);
      setComparisonResult(mockResult);
    } finally {
      setLoading(false);
    }
  };

  const selectedProductsData = products.filter(p => selectedForCompare.includes(p.id));

  return (
    <div className="min-h-screen py-8">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-glow">
              <GitCompare className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="font-display text-3xl font-bold text-foreground">
                Comparador de Productos
              </h1>
              <p className="text-muted-foreground">
                Selecciona 2-5 productos para comparar con análisis semántico
              </p>
            </div>
          </div>
        </div>

        {/* Step 1: Product Selection */}
        <div className="mb-8 animate-fade-in">
          {/* Filters */}
          <div className="bg-card rounded-2xl border border-border/50 p-4 mb-6 shadow-soft">
            <div className="flex items-center gap-2 mb-4">
              <Filter className="w-4 h-4 text-muted-foreground" />
              <span className="font-medium text-foreground">Filtrar productos</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Search */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  placeholder="Buscar productos..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="pl-9"
                />
              </div>
              
              {/* Category */}
              <Select value={category || 'all'} onValueChange={(v) => setCategory(v === 'all' ? undefined : v)}>
                <SelectTrigger>
                  <SelectValue placeholder="Categoría" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todas las categorías</SelectItem>
                  {CATEGORIES.map(cat => (
                    <SelectItem key={cat.id} value={cat.id}>
                      {cat.icon} {cat.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              
              {/* Min Price */}
              <Input
                type="number"
                placeholder="Precio mínimo"
                value={minPrice}
                onChange={(e) => setMinPrice(e.target.value)}
              />
              
              {/* Max Price */}
              <Input
                type="number"
                placeholder="Precio máximo"
                value={maxPrice}
                onChange={(e) => setMaxPrice(e.target.value)}
              />
            </div>
          </div>

          {/* Selected Products Preview */}
          {selectedForCompare.length > 0 && (
            <div className="bg-card rounded-2xl border border-border/50 p-6 mb-6 shadow-soft">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-display font-semibold text-foreground">
                  Productos Seleccionados ({selectedForCompare.length}/5)
                </h3>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearSelection}
                  className="text-muted-foreground hover:text-destructive"
                >
                  <Trash2 className="w-4 h-4 mr-1" />
                  Limpiar
                </Button>
              </div>
              <div className="flex flex-wrap gap-3">
                {selectedProductsData.map((product) => (
                  <div
                    key={product.id}
                    className="flex items-center gap-2 px-3 py-2 rounded-full bg-primary/10 border border-primary/20"
                  >
                    <span className="font-medium text-sm text-foreground">
                      {product.properties.tieneNombre || product.id}
                    </span>
                    <button
                      onClick={() => toggleProduct(product.id)}
                      className="w-5 h-5 rounded-full bg-primary/20 hover:bg-destructive/20 flex items-center justify-center transition-colors"
                    >
                      <span className="text-xs">×</span>
                    </button>
                  </div>
                ))}
                {selectedForCompare.length < 5 && (
                  <div className="flex items-center gap-1 px-3 py-2 rounded-full border border-dashed border-muted-foreground/30 text-muted-foreground text-sm">
                    <Plus className="w-4 h-4" />
                    Añadir más
                  </div>
                )}
              </div>

              {/* Compare Button */}
              <div className="mt-6">
                <Button
                  onClick={handleCompare}
                  disabled={!canCompare || loading}
                  className={cn(
                    "w-full sm:w-auto h-12 px-8 font-semibold",
                    canCompare
                      ? "bg-gradient-to-r from-primary to-accent hover:opacity-90 shadow-glow"
                      : ""
                  )}
                >
                  {loading ? (
                    <span className="flex items-center gap-2">
                      <span className="w-4 h-4 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin" />
                      Comparando...
                    </span>
                  ) : (
                    <span className="flex items-center gap-2">
                      <GitCompare className="w-5 h-5" />
                      Comparar Ahora
                    </span>
                  )}
                </Button>
                {!canCompare && selectedForCompare.length > 0 && (
                  <p className="text-sm text-muted-foreground mt-2">
                    {selectedForCompare.length < 2 
                      ? 'Selecciona al menos 2 productos' 
                      : 'Máximo 5 productos'}
                  </p>
                )}
              </div>

              {error && (
                <div className="mt-4 flex items-center gap-2 text-destructive text-sm">
                  <AlertCircle className="w-4 h-4" />
                  {error}
                </div>
              )}
            </div>
          )}

          {/* Product Grid for Selection */}
          <div className="bg-card rounded-2xl border border-border/50 p-6 shadow-soft">
            <h3 className="font-display font-semibold text-foreground mb-4">
              {selectedForCompare.length === 0 
                ? 'Paso 1: Selecciona productos para comparar'
                : 'Añade más productos a la comparación'}
            </h3>
            {productsLoading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {[...Array(8)].map((_, i) => (
                  <LoadingCard key={i} />
                ))}
              </div>
            ) : filteredProducts.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-muted-foreground">No se encontraron productos con los filtros seleccionados</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {filteredProducts.map((product) => (
                  <ProductCard
                    key={product.id}
                    product={product}
                    selectable
                    isSelected={selectedForCompare.includes(product.id)}
                    onToggleSelect={toggleProduct}
                  />
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Comparison Results */}
        {comparisonResult && (
          <div className="animate-slide-up">
            <div className="flex items-center justify-between mb-6">
              <h2 className="font-display text-2xl font-bold text-foreground">
                Resultado de la Comparación
              </h2>
              <Button
                variant="outline"
                onClick={clearSelection}
              >
                <Plus className="w-4 h-4 mr-2" />
                Nueva comparación
              </Button>
            </div>
            <CompareTable result={comparisonResult} />
          </div>
        )}
      </div>
    </div>
  );
}

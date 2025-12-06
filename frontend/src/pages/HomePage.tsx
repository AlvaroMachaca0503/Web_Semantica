import { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { Zap, ArrowRight, Package } from 'lucide-react';
import { useProducts } from '@/hooks/useProducts';
import { ProductCard } from '@/components/products/ProductCard';
import { ProductFilters } from '@/components/products/ProductFilters';
import { LoadingCard } from '@/components/common/LoadingSpinner';
import { Button } from '@/components/ui/button';
import { Product } from '@/services/api';
import { toast } from 'sonner';

interface HomePageProps {
  onAddToCart: (product: Product) => void;
}

export default function HomePage({ onAddToCart }: HomePageProps) {
  const [category, setCategory] = useState<string | undefined>();
  const [minPrice, setMinPrice] = useState<number | undefined>();
  const [maxPrice, setMaxPrice] = useState<number | undefined>();
  const [search, setSearch] = useState('');

  const { products, loading } = useProducts({ category, minPrice, maxPrice });

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

  const handleAddToCart = (product: Product) => {
    onAddToCart(product);
    toast.success(`${product.properties.tieneNombre || product.id} añadido al carrito`);
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-16 md:py-24">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5" />
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary/10 rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-10 right-10 w-96 h-96 bg-accent/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '-3s' }} />
        
        <div className="container mx-auto px-4 relative">
          <div className="max-w-3xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-6 animate-fade-in">
              <Zap className="w-4 h-4" />
              Potenciado por Web Semántica (OWL + SWRL)
            </div>
            <h1 className="font-display text-4xl md:text-6xl font-bold text-foreground mb-6 animate-slide-up">
              Compara y encuentra el 
              <span className="gradient-text"> producto perfecto</span>
            </h1>
            <p className="text-lg md:text-xl text-muted-foreground mb-8 animate-slide-up" style={{ animationDelay: '0.1s' }}>
              Análisis inteligente con inferencias semánticas para ayudarte a tomar 
              la mejor decisión de compra en electrónicos.
            </p>
            <div className="flex flex-wrap justify-center gap-4 animate-slide-up" style={{ animationDelay: '0.2s' }}>
              <Button asChild size="lg" className="h-12 px-6 bg-gradient-to-r from-primary to-accent hover:opacity-90 shadow-glow">
                <Link to="/compare">
                  <Zap className="w-5 h-5 mr-2" />
                  Empezar a Comparar
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg" className="h-12 px-6">
                <Link to="/recommendations">
                  Ver Recomendaciones
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Products Section */}
      <section className="py-12">
        <div className="container mx-auto px-4">
          {/* Section Header */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
            <div>
              <h2 className="font-display text-2xl md:text-3xl font-bold text-foreground">
                Catálogo de Productos
              </h2>
              <p className="text-muted-foreground mt-1">
                {filteredProducts.length} productos disponibles
              </p>
            </div>
          </div>

          {/* Filters */}
          <ProductFilters
            selectedCategory={category}
            onCategoryChange={setCategory}
            onPriceRangeChange={(min, max) => {
              setMinPrice(min);
              setMaxPrice(max);
            }}
            onSearchChange={setSearch}
          />

          {/* Products Grid */}
          <div className="mt-8">
            {loading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {[...Array(8)].map((_, i) => (
                  <LoadingCard key={i} />
                ))}
              </div>
            ) : filteredProducts.length === 0 ? (
              <div className="text-center py-16">
                <Package className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                <h3 className="font-display text-xl font-semibold text-foreground mb-2">
                  No se encontraron productos
                </h3>
                <p className="text-muted-foreground">
                  Intenta ajustar los filtros para ver más resultados.
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {filteredProducts.map((product, index) => (
                  <div
                    key={product.id}
                    className="animate-fade-in"
                    style={{ animationDelay: `${index * 0.05}s` }}
                  >
                    <ProductCard
                      product={product}
                      onAddToCart={handleAddToCart}
                    />
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}

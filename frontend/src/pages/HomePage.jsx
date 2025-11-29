import { useState } from 'react';
import { useProducts } from '../hooks/useProducts';
import ProductGrid from '../components/products/ProductGrid';
import PriceFilter from '../components/filters/PriceFilter';
import CategoryFilter from '../components/filters/CategoryFilter';
import { Link } from 'react-router-dom';

const HomePage = () => {
    const [filters, setFilters] = useState({});
    const { products, loading, error } = useProducts(filters);

    const handleFilterChange = (newFilters) => {
        setFilters(prev => ({
            ...prev,
            ...newFilters
        }));
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
            <div className="container mx-auto px-4 py-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-gray-800 mb-2">
                        🛍️ SmartCompareMarket
                    </h1>
                    <p className="text-gray-600">
                        Marketplace inteligente con Web Semántica y reglas SWRL
                    </p>
                </div>

                {/* Botón de comparación */}
                <div className="mb-6">
                    <Link
                        to="/compare"
                        className="inline-flex items-center gap-2 bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors font-medium shadow-md"
                    >
                        <span>⚖️</span>
                        <span>Ir a Comparar Productos</span>
                    </Link>
                </div>

                {/* Filtros */}
                <div className="mb-8">
                    <h2 className="text-xl font-semibold text-gray-800 mb-4">Filtros</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <PriceFilter onFilterChange={handleFilterChange} />
                        <CategoryFilter onFilterChange={handleFilterChange} />

                        {/* Contador de resultados */}
                        <div className="bg-white p-4 rounded-lg shadow-md flex items-center justify-center">
                            <div className="text-center">
                                <p className="text-3xl font-bold text-blue-600">
                                    {products.length}
                                </p>
                                <p className="text-sm text-gray-600 mt-1">
                                    Productos encontrados
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Grid de productos */}
                <div>
                    <h2 className="text-xl font-semibold text-gray-800 mb-4">
                        Productos Disponibles
                    </h2>
                    <ProductGrid
                        products={products}
                        loading={loading}
                        error={error}
                    />
                </div>

                {/* Footer informativo */}
                {!loading && !error && products.length > 0 && (
                    <div className="mt-8 p-4 bg-blue-50 rounded-lg border border-blue-200">
                        <p className="text-sm text-blue-800">
                            💡 <strong>Tip:</strong> Los productos marcados con 🎮 son detectados como
                            "Laptop Gamer" por la regla SWRL <code>DetectarGamer</code> (RAM ≥ 16GB)
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default HomePage;

import ProductCard from './ProductCard';

const ProductGrid = ({ products, loading, error, onProductSelect, selectedProducts = [] }) => {
    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Cargando productos...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
                <p className="text-red-600 font-medium">❌ Error: {error}</p>
                <p className="text-sm text-red-500 mt-2">Por favor, verifica que el backend esté corriendo</p>
            </div>
        );
    }

    if (!products || products.length === 0) {
        return (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-12 text-center">
                <p className="text-gray-600 text-lg">No se encontraron productos</p>
                <p className="text-sm text-gray-500 mt-2">Intenta con otros filtros</p>
            </div>
        );
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {products.map((product) => (
                <ProductCard
                    key={product.id}
                    product={product}
                    onSelect={onProductSelect}
                    isSelected={selectedProducts?.includes(product.id)}
                />
            ))}
        </div>
    );
};

export default ProductGrid;

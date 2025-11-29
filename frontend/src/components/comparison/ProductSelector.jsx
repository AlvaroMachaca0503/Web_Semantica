import { useState } from 'react';
import { useProducts } from '../../hooks/useProducts';
import ProductCard from '../products/ProductCard';

const ProductSelector = ({ selected = [], onSelect, maxProducts = 5 }) => {
    const { products, loading, error } = useProducts({});
    const [search, setSearch] = useState('');

    const handleToggleProduct = (productId) => {
        if (selected.includes(productId)) {
            // Deseleccionar
            onSelect(selected.filter(id => id !== productId));
        } else {
            // Seleccionar (máximo permitido)
            if (selected.length < maxProducts) {
                onSelect([...selected, productId]);
            } else {
                alert(`Máximo ${maxProducts} productos para comparar`);
            }
        }
    };

    const filteredProducts = products.filter(product => {
        if (!search) return true;
        const searchLower = search.toLowerCase();
        return (
            product.id.toLowerCase().includes(searchLower) ||
            product.properties.tieneNombre?.toLowerCase().includes(searchLower)
        );
    });

    if (loading) {
        return (
            <div className="text-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
                <p className="mt-4 text-gray-600">Cargando productos...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-600">Error: {error}</p>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {/* Header con contador */}
            <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-gray-800">
                    Selecciona productos para comparar
                </h3>
                <span className="text-sm font-medium text-gray-600 bg-gray-100 px-3 py-1 rounded-full">
                    {selected.length} / {maxProducts} seleccionados
                </span>
            </div>

            {/* Buscador */}
            <input
                type="text"
                placeholder="🔍 Buscar productos..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />

            {/* Productos seleccionados */}
            {selected.length > 0 && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h4 className="font-medium text-blue-900 mb-2">
                        Productos Seleccionados:
                    </h4>
                    <div className="flex flex-wrap gap-2">
                        {selected.map((productId) => {
                            const product = products.find(p => p.id === productId);
                            return (
                                <span
                                    key={productId}
                                    className="inline-flex items-center gap-2 bg-blue-500 text-white px-3 py-1 rounded-full text-sm"
                                >
                                    {product?.properties.tieneNombre || productId}
                                    <button
                                        onClick={() => handleToggleProduct(productId)}
                                        className="hover:bg-blue-600 rounded-full p-1"
                                    >
                                        ×
                                    </button>
                                </span>
                            );
                        })}
                    </div>
                </div>
            )}

            {/* Grid de productos */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 max-h-[600px] overflow-y-auto p-2">
                {filteredProducts.map((product) => (
                    <ProductCard
                        key={product.id}
                        product={product}
                        onSelect={handleToggleProduct}
                        isSelected={selected.includes(product.id)}
                    />
                ))}
            </div>

            {filteredProducts.length === 0 && (
                <p className="text-center text-gray-500 py-8">
                    No se encontraron productos con "{search}"
                </p>
            )}
        </div>
    );
};

export default ProductSelector;

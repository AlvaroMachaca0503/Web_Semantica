import { useState } from 'react';

const PriceFilter = ({ onFilterChange }) => {
    const [minPrice, setMinPrice] = useState('');
    const [maxPrice, setMaxPrice] = useState('');

    const handleApply = () => {
        const filters = {};

        if (minPrice) filters.min_price = parseFloat(minPrice);
        if (maxPrice) filters.max_price = parseFloat(maxPrice);

        onFilterChange(filters);
    };

    const handleClear = () => {
        setMinPrice('');
        setMaxPrice('');
        onFilterChange({ min_price: undefined, max_price: undefined });
    };

    return (
        <div className="bg-white p-4 rounded-lg shadow-md">
            <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <span>💰</span>
                <span>Filtrar por Precio</span>
            </h3>

            <div className="space-y-3">
                <div className="flex items-center gap-2">
                    <input
                        type="number"
                        placeholder="Precio mín"
                        value={minPrice}
                        onChange={(e) => setMinPrice(e.target.value)}
                        className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        min="0"
                    />
                    <span className="text-gray-500">-</span>
                    <input
                        type="number"
                        placeholder="Precio máx"
                        value={maxPrice}
                        onChange={(e) => setMaxPrice(e.target.value)}
                        className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        min="0"
                    />
                </div>

                <div className="flex gap-2">
                    <button
                        onClick={handleApply}
                        className="flex-1 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors font-medium text-sm"
                    >
                        Aplicar
                    </button>
                    <button
                        onClick={handleClear}
                        className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium text-sm"
                    >
                        Limpiar
                    </button>
                </div>
            </div>
        </div>
    );
};

export default PriceFilter;

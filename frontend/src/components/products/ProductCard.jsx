const ProductCard = ({ product, onSelect, isSelected }) => {
    const { id, properties, types = [] } = product;

    const isGamer = types.some(t => t.includes('LaptopGamer'));
    const isElectronica = types.some(t => t.includes('Electrónica'));
    const isSmartphone = types.some(t => t.includes('Smartphone'));

    const handleClick = () => {
        if (onSelect) {
            onSelect(id);
        }
    };

    return (
        <div
            onClick={handleClick}
            className={`
        bg-white rounded-lg shadow-md p-4 hover:shadow-xl transition-all duration-300
        cursor-pointer transform hover:-translate-y-1
        ${isSelected ? 'ring-2 ring-blue-500 bg-blue-50' : ''}
      `}
        >
            {/* Header con nombre */}
            <h3 className="text-lg font-semibold text-gray-800 mb-2 line-clamp-2 min-h-[3.5rem]">
                {properties.tieneNombre || id}
            </h3>

            {/* Precio destacado */}
            <div className="mb-3">
                {properties.tienePrecio ? (
                    <p className="text-3xl font-bold text-blue-600">
                        ${properties.tienePrecio.toLocaleString()}
                    </p>
                ) : (
                    <p className="text-sm text-gray-400">Precio no disponible</p>
                )}
            </div>

            {/* Especificaciones */}
            <div className="space-y-1 text-sm text-gray-600 mb-3">
                {properties.tieneRAM_GB && (
                    <div className="flex items-center gap-2">
                        <span className="font-medium">💾 RAM:</span>
                        <span>{properties.tieneRAM_GB}GB</span>
                    </div>
                )}

                {properties.tieneAlmacenamiento_GB && (
                    <div className="flex items-center gap-2">
                        <span className="font-medium">💿 Almacenamiento:</span>
                        <span>{properties.tieneAlmacenamiento_GB}GB</span>
                    </div>
                )}

                {properties.tieneCalificacion && (
                    <div className="flex items-center gap-2">
                        <span className="font-medium">⭐ Calificación:</span>
                        <span>{properties.tieneCalificacion}/5</span>
                    </div>
                )}
            </div>

            {/* Badges SWRL */}
            <div className="flex flex-wrap gap-2 mt-3">
                {isGamer && (
                    <span className="inline-flex items-center gap-1 px-3 py-1 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs font-semibold rounded-full shadow-md">
                        🎮 Laptop Gamer
                    </span>
                )}

                {isSmartphone && (
                    <span className="inline-flex items-center gap-1 px-3 py-1 bg-gradient-to-r from-blue-500 to-cyan-500 text-white text-xs font-semibold rounded-full">
                        📱 Smartphone
                    </span>
                )}

                {isElectronica && !isSmartphone && !isGamer && (
                    <span className="inline-flex items-center gap-1 px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                        ⚡ Electrónica
                    </span>
                )}
            </div>

            {/* Botón de selección si está en modo comparación */}
            {onSelect && (
                <div className="mt-3 pt-3 border-t border-gray-200">
                    <button
                        className={`
              w-full py-2 px-4 rounded-lg font-medium transition-colors
              ${isSelected
                                ? 'bg-blue-500 text-white hover:bg-blue-600'
                                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                            }
            `}
                    >
                        {isSelected ? '✓ Seleccionado' : 'Seleccionar'}
                    </button>
                </div>
            )}
        </div>
    );
};

export default ProductCard;

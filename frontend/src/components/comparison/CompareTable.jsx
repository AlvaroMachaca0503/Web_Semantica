const CompareTable = ({ comparison }) => {
    if (!comparison || !comparison.products) {
        return null;
    }

    const { products, comparison_table, winner, winner_score, all_scores, reason, swrl_inference } = comparison;

    return (
        <div className="mt-8 space-y-6">
            {/* Ganador destacado */}
            <div className="bg-gradient-to-r from-green-500 to-emerald-500 text-white p-6 rounded-xl shadow-lg">
                <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
                    <span>🏆</span>
                    <span>Ganador: {winner}</span>
                </h2>
                <p className="text-lg opacity-90">Score: {winner_score}</p>
                <p className="text-sm opacity-80 mt-2">{reason}</p>
            </div>

            {/* Scores de todos los productos */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(all_scores).map(([productId, score]) => (
                    <div
                        key={productId}
                        className={`p-4 rounded-lg border-2 ${productId === winner
                                ? 'border-green-500 bg-green-50'
                                : 'border-gray-200 bg-white'
                            }`}
                    >
                        <h3 className="font-semibold text-gray-800">{productId}</h3>
                        <p className="text-2xl font-bold text-blue-600 mt-1">
                            {score} puntos
                        </p>
                        {productId === winner && (
                            <span className="inline-block mt-2 text-xs bg-green-500 text-white px-2 py-1 rounded">
                                GANADOR
                            </span>
                        )}
                    </div>
                ))}
            </div>

            {/* Tabla comparativa */}
            <div className="bg-white rounded-xl shadow-md overflow-hidden">
                <div className="p-4 bg-gray-50 border-b">
                    <h3 className="text-xl font-bold text-gray-800">Tabla Comparativa Detallada</h3>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-gray-100">
                            <tr>
                                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700 w-1/4">
                                    Propiedad
                                </th>
                                {products.map((product) => (
                                    <th
                                        key={product.id}
                                        className="px-4 py-3 text-left text-sm font-semibold text-gray-700"
                                    >
                                        {product.id}
                                        {product.id === winner && <span className="ml-2 text-xs bg-green-500 text-white px-2 py-0.5 rounded-full">Ganador Global</span>}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {comparison_table && Object.entries(comparison_table).map(([prop, values]) => {
                                // Lógica de colores por fila
                                const getCellStyle = (value, allValues) => {
                                    // 1. Propiedades irrelevantes/neutras -> Gris
                                    const neutralProps = ['vendidoPor', 'tieneMarca', 'tieneNombre', 'esCompatibleCon', 'esSimilarA', 'incompatibleCon', 'id', 'type'];
                                    if (neutralProps.includes(prop)) return 'text-gray-600';

                                    // Limpiar valores para comparación numérica
                                    const cleanValues = allValues.map(v => {
                                        if (v === 'N/A' || v === null) return -1;
                                        return typeof v === 'string' ? parseFloat(v) || v : v;
                                    });

                                    const currentVal = (value === 'N/A' || value === null) ? -1 : (typeof value === 'string' ? parseFloat(value) || value : value);

                                    // 2. Verificar Empate (todos iguales y válidos)
                                    const validValues = cleanValues.filter(v => v !== -1);
                                    if (validValues.length > 1 && validValues.every(v => v === validValues[0])) {
                                        return 'bg-yellow-50 text-yellow-800 font-medium border-l-4 border-yellow-400';
                                    }

                                    // 3. Determinar Ganador
                                    let isWinner = false;

                                    // Precio: Menor es mejor
                                    if (prop === 'tienePrecio') {
                                        const minVal = Math.min(...cleanValues.filter(v => typeof v === 'number' && v > 0));
                                        if (currentVal === minVal) isWinner = true;
                                    }
                                    // Otros numéricos: Mayor es mejor
                                    else if (['tieneRAM_GB', 'tieneAlmacenamiento_GB', 'tieneCalificacion'].includes(prop)) {
                                        const maxVal = Math.max(...cleanValues.filter(v => typeof v === 'number'));
                                        if (currentVal === maxVal) isWinner = true;
                                    }

                                    if (isWinner) return 'bg-green-50 text-green-800 font-bold border-l-4 border-green-500';

                                    return 'text-gray-600';
                                };

                                return (
                                    <tr key={prop} className="hover:bg-gray-50 transition-colors">
                                        <td className="px-4 py-3 text-sm font-medium text-gray-800 bg-gray-50">
                                            {prop}
                                        </td>
                                        {values.map((value, idx) => (
                                            <td
                                                key={idx}
                                                className={`px-4 py-3 text-sm ${getCellStyle(value, values)}`}
                                            >
                                                {value !== null && value !== undefined ? String(value) : 'N/A'}
                                            </td>
                                        ))}
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Inferencias SWRL */}
            {swrl_inference && swrl_inference.esMejorOpcionQue && swrl_inference.esMejorOpcionQue.length > 0 && (
                <div className="bg-purple-50 border border-purple-200 rounded-xl p-6">
                    <h3 className="text-lg font-bold text-purple-900 mb-3 flex items-center gap-2">
                        <span>🧠</span>
                        <span>Inferencias SWRL (Mejor Precio)</span>
                    </h3>
                    <div className="space-y-2">
                        {swrl_inference.esMejorOpcionQue.map((rel, idx) => (
                            <div key={idx} className="flex items-center gap-3 text-sm">
                                <span className="font-semibold text-purple-800">{rel.better}</span>
                                <span className="text-purple-600">es mejor opción que</span>
                                <span className="font-semibold text-purple-800">{rel.worse}</span>
                                <span className="text-xs bg-purple-200 text-purple-800 px-2 py-1 rounded">
                                    {rel.rule}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default CompareTable;

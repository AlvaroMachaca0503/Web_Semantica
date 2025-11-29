import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useComparison } from '../hooks/useComparison';
import ProductSelector from '../components/comparison/ProductSelector';
import CompareTable from '../components/comparison/CompareTable';

const ComparePage = () => {
    const [selectedProducts, setSelectedProducts] = useState([]);
    const { comparison, loading, error, compare } = useComparison();

    const handleCompare = async () => {
        if (selectedProducts.length < 2) {
            alert('Selecciona al menos 2 productos para comparar');
            return;
        }
        await compare(selectedProducts);
    };

    const handleClear = () => {
        setSelectedProducts([]);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-purple-50">
            <div className="container mx-auto px-4 py-8">
                {/* Header */}
                <div className="mb-8">
                    <Link
                        to="/"
                        className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-4"
                    >
                        <span>←</span>
                        <span>Volver al inicio</span>
                    </Link>

                    <h1 className="text-4xl font-bold text-gray-800 mb-2">
                        ⚖️ Comparador Inteligente
                    </h1>
                    <p className="text-gray-600">
                        Compara productos usando Web Semántica y reglas SWRL
                    </p>
                </div>

                {/* Selector de productos */}
                <div className="bg-white rounded-xl shadow-md p-6 mb-6">
                    <ProductSelector
                        selected={selectedProducts}
                        onSelect={setSelectedProducts}
                        maxProducts={5}
                    />

                    {/* Botones de acción */}
                    <div className="flex gap-4 mt-6">
                        <button
                            onClick={handleCompare}
                            disabled={selectedProducts.length < 2 || loading}
                            className={`
                flex-1 py-3 px-6 rounded-lg font-medium transition-colors text-white
                ${selectedProducts.length < 2 || loading
                                    ? 'bg-gray-300 cursor-not-allowed'
                                    : 'bg-green-500 hover:bg-green-600 shadow-md'
                                }
              `}
                        >
                            {loading ? (
                                <span className="flex items-center justify-center gap-2">
                                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                                    <span>Comparando...</span>
                                </span>
                            ) : (
                                `⚖️ Comparar ${selectedProducts.length > 0 ? `(${selectedProducts.length})` : ''}`
                            )}
                        </button>

                        <button
                            onClick={handleClear}
                            className="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium"
                        >
                            Limpiar
                        </button>
                    </div>
                </div>

                {/* Error */}
                {error && (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                        <p className="text-red-600 font-medium">❌ Error: {error}</p>
                    </div>
                )}

                {/* Resultado de comparación */}
                {comparison && <CompareTable comparison={comparison} />}

                {/* Info SWRL */}
                {!comparison && (
                    <div className="bg-blue-50 border border-blue-200 rounded-xl p-6 mt-6">
                        <h3 className="font-bold text-blue-900 mb-2">
                            💡 ¿Cómo funciona la comparación?
                        </h3>
                        <ul className="space-y-2 text-sm text-blue-800">
                            <li>
                                • <strong>Scoring Multi-Factor:</strong> Considera precio, RAM, almacenamiento y calificación
                            </li>
                            <li>
                                • <strong>Regla SWRL "EncontrarMejorPrecio":</strong> Detecta automáticamente productos con mejor relación calidad-precio
                            </li>
                            <li>
                                • <strong>Análisis Semántico:</strong> Compara propiedades y relaciones de la ontología OWL
                            </li>
                            <li>
                                • <strong>Ganador Automático:</strong> El sistema sugiere el mejor producto basado en múltiples criterios
                            </li>
                        </ul>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ComparePage;

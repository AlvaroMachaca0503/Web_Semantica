import { useState, useEffect } from 'react';
import { compareProducts } from '../services/api';

export const useComparison = (productIds = []) => {
    const [comparison, setComparison] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const compare = async (ids = productIds) => {
        if (ids.length < 2) {
            setError('Selecciona al menos 2 productos para comparar');
            return;
        }

        if (ids.length > 5) {
            setError('Máximo 5 productos para comparar');
            return;
        }

        try {
            setLoading(true);
            setError(null);
            const response = await compareProducts(ids);
            setComparison(response.data.comparison);
        } catch (err) {
            setError(err.response?.data?.detail || err.message);
            setComparison(null);
        } finally {
            setLoading(false);
        }
    };

    return { comparison, loading, error, compare };
};

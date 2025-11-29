import { useState, useEffect } from 'react';
import { getProducts } from '../services/api';

export const useProducts = (filters = {}) => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await getProducts(filters);
                setProducts(response.data.data || []);
            } catch (err) {
                setError(err.response?.data?.error || err.message);
                setProducts([]);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, [JSON.stringify(filters)]);

    return { products, loading, error };
};

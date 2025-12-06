import { useState, useEffect, useCallback } from 'react';
import { productService, Product } from '@/services/api';
import { MOCK_PRODUCTS } from '@/lib/constants';

interface UseProductsOptions {
  category?: string;
  minPrice?: number;
  maxPrice?: number;
}

export function useProducts(options: UseProductsOptions = {}) {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProducts = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await productService.getAll({
        category: options.category,
        min_price: options.minPrice,
        max_price: options.maxPrice
      });
      setProducts(response.data);
    } catch (err) {
      console.warn('Backend unavailable, using mock data');
      // Filter mock data based on options
      let filtered = [...MOCK_PRODUCTS];
      
      if (options.category) {
        filtered = filtered.filter(p => p.types.includes(options.category!));
      }
      if (options.minPrice !== undefined) {
        filtered = filtered.filter(p => (p.properties.tienePrecio || 0) >= options.minPrice!);
      }
      if (options.maxPrice !== undefined) {
        filtered = filtered.filter(p => (p.properties.tienePrecio || 0) <= options.maxPrice!);
      }
      
      setProducts(filtered);
    } finally {
      setLoading(false);
    }
  }, [options.category, options.minPrice, options.maxPrice]);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  return { products, loading, error, refetch: fetchProducts };
}

export function useProduct(id: string | undefined) {
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) {
      setLoading(false);
      return;
    }

    const fetchProduct = async () => {
      setLoading(true);
      try {
        const response = await productService.getById(id);
        setProduct(response.data);
      } catch (err) {
        // Use mock data
        const mockProduct = MOCK_PRODUCTS.find(p => p.id === id);
        if (mockProduct) {
          setProduct(mockProduct);
        } else {
          setError('Producto no encontrado');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  return { product, loading, error };
}

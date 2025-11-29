import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api/v1';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// ==================== Productos ====================

export const getProducts = (params = {}) =>
    api.get('/products', { params });

export const getProductById = (id) =>
    api.get(`/products/${id}`);

export const getProductRelationships = (id) =>
    api.get(`/products/${id}/relationships`);

// ==================== Comparación ====================

export const compareProducts = (productIds) =>
    api.post('/compare', { products: productIds });

// ==================== SWRL ====================

export const getBestPrice = () =>
    api.get('/swrl/best-price');

export const getGamingLaptops = () =>
    api.get('/swrl/gaming-laptops');

export const getPositiveReviews = () =>
    api.get('/swrl/positive-reviews');

export const getNegativeReviews = () =>
    api.get('/swrl/negative-reviews');

// ==================== Búsqueda ====================

export const searchProducts = (query, filters = {}) =>
    api.get('/search', {
        params: {
            q: query,
            ...filters
        }
    });

export const searchCompatibleProducts = (productId) =>
    api.get(`/search/compatible/${productId}`);

// ==================== Interceptors ====================

// Response interceptor para manejar errores globalmente
api.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
    }
);

export default api;

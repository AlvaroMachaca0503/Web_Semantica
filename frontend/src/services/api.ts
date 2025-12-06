import axios from 'axios';

const API_BASE = 'http://localhost:5000/api/v1';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000
});

export interface ProductProperties {
  tieneNombre?: string;
  tienePrecio?: number;
  tieneRAM_GB?: number;
  tieneAlmacenamiento_GB?: number;
  tieneCalificacion?: number;
  vendidoPor?: string;
  tieneMarca?: string;
  tieneDescuento?: number;
  procesadorModelo?: string;
  resolucionPantalla?: string;
  pesoGramos?: number;
  bateriaCapacidad_mAh?: number;
  garantiaMeses?: number;
  tienePulgadas?: number;
  tieneSistemaOperativo?: string;
  tarjetaGrafica?: string;
  procesadorVelocidad_GHz?: number;
  numeroNucleosCPU?: number;
  imagenUrl?: string;
}

export interface Product {
  id: string;
  types: string[];
  properties: ProductProperties;
}

export interface ComparisonResult {
  products: Product[];
  comparison_table: Record<string, (string | number)[]>;
  winner: string;
  winner_score: number;
  all_scores: Record<string, number>;
  reason: string;
  swrl_inference: {
    esMejorOpcionQue: { source: string; target: string; rule: string }[];
    tieneMejorRAMQue: { source: string; target: string; rule: string }[];
    tieneMejorAlmacenamientoQue: { source: string; target: string; rule: string }[];
    tieneMejorPantallaQue: { source: string; target: string; rule: string }[];
    esEquivalenteTecnico: { source: string; target: string; rule: string }[];
    rules_applied: string[];
  };
}

export interface Recommendation {
  product_id: string;
  score: number;
  reason: string;
  match_percentage: number;
}

export interface RecommendationPreferences {
  budget?: number;
  min_budget?: number;
  preferred_category?: string;
  min_ram?: number;
  min_storage?: number;
  min_rating?: number;
}

export const productService = {
  getAll: async (params?: { category?: string; min_price?: number; max_price?: number }) => {
    const response = await api.get<{ success: boolean; count: number; data: Product[] }>('/products', { params });
    return response.data;
  },
  getById: async (id: string) => {
    const response = await api.get<{ success: boolean; data: Product }>(`/products/${id}`);
    return response.data;
  },
  getRelationships: async (id: string) => {
    const response = await api.get(`/products/${id}/relationships`);
    return response.data;
  }
};

export const comparisonService = {
  compare: async (productIds: string[]) => {
    const response = await api.post<{ success: boolean; comparison: ComparisonResult }>('/compare', { products: productIds });
    return response.data;
  }
};

export const recommendationService = {
  getRecommendations: async (preferences: RecommendationPreferences, limit = 5) => {
    const response = await api.post<{ success: boolean; total_matches: number; recommendations: Recommendation[]; preferences_used: RecommendationPreferences }>(
      `/recommendations?limit=${limit}`,
      preferences
    );
    return response.data;
  },
  getBestDeals: async (limit = 5) => {
    const response = await api.get(`/recommendations/best-deals?limit=${limit}`);
    return response.data;
  }
};

export const swrlService = {
  getBestPrice: async () => {
    const response = await api.get('/swrl/best-price');
    return response.data;
  },
  getGamingLaptops: async () => {
    const response = await api.get('/swrl/gaming-laptops');
    return response.data;
  }
};

export default api;

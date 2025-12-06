import { useState } from 'react';
import { Sparkles, TrendingUp, AlertCircle } from 'lucide-react';
import { PreferencesPanel } from '@/components/recommendations/PreferencesPanel';
import { RecommendationCard } from '@/components/recommendations/RecommendationCard';
import { recommendationService, Recommendation, RecommendationPreferences } from '@/services/api';
import { MOCK_PRODUCTS } from '@/lib/constants';

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSubmit = async (preferences: RecommendationPreferences) => {
    setLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      const response = await recommendationService.getRecommendations(preferences);
      setRecommendations(response.recommendations);
    } catch (err) {
      console.warn('Backend unavailable, generating mock recommendations');
      
      // Generate mock recommendations
      const filtered = MOCK_PRODUCTS.filter(p => {
        if (preferences.preferred_category && !p.types.includes(preferences.preferred_category)) {
          return false;
        }
        if (preferences.budget && (p.properties.tienePrecio || 0) > preferences.budget) {
          return false;
        }
        if (preferences.min_ram && (p.properties.tieneRAM_GB || 0) < preferences.min_ram) {
          return false;
        }
        if (preferences.min_storage && (p.properties.tieneAlmacenamiento_GB || 0) < preferences.min_storage) {
          return false;
        }
        if (preferences.min_rating && (p.properties.tieneCalificacion || 0) < preferences.min_rating) {
          return false;
        }
        return true;
      });

      const mockRecs: Recommendation[] = filtered.slice(0, 5).map((p, index) => {
        const score = 95 - index * 5;
        const reasons = [];
        if (p.properties.tienePrecio && preferences.budget) {
          reasons.push(`Precio: $${p.properties.tienePrecio} (dentro del presupuesto)`);
        }
        if (p.properties.tieneRAM_GB) {
          reasons.push(`RAM: ${p.properties.tieneRAM_GB}GB`);
        }
        if (p.properties.tieneDescuento) {
          reasons.push(`Descuento del ${p.properties.tieneDescuento}%`);
        }
        if (p.types.includes('LaptopGamer')) {
          reasons.push('Laptop Gamer detectado (SWRL)');
        }
        
        return {
          product_id: p.id,
          score,
          reason: reasons.join(' | ') || 'Excelente relación calidad-precio',
          match_percentage: 100 - index * 5
        };
      });

      setRecommendations(mockRecs);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-8">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-accent to-primary flex items-center justify-center shadow-glow-accent">
              <Sparkles className="w-6 h-6 text-accent-foreground" />
            </div>
            <div>
              <h1 className="font-display text-3xl font-bold text-foreground">
                Recomendaciones Personalizadas
              </h1>
              <p className="text-muted-foreground">
                Encuentra productos perfectos para ti con IA semántica
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Preferences Panel */}
          <div className="lg:col-span-1">
            <PreferencesPanel onSubmit={handleSubmit} loading={loading} />
          </div>

          {/* Results */}
          <div className="lg:col-span-2">
            {error && (
              <div className="bg-destructive/10 border border-destructive/20 rounded-xl p-4 mb-6 flex items-center gap-3">
                <AlertCircle className="w-5 h-5 text-destructive" />
                <p className="text-destructive">{error}</p>
              </div>
            )}

            {!hasSearched ? (
              <div className="bg-card rounded-2xl border border-border/50 p-12 text-center shadow-soft">
                <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-primary/10 to-accent/10 flex items-center justify-center">
                  <TrendingUp className="w-10 h-10 text-primary" />
                </div>
                <h3 className="font-display text-xl font-semibold text-foreground mb-2">
                  Configura tus preferencias
                </h3>
                <p className="text-muted-foreground max-w-md mx-auto">
                  Ajusta el panel de la izquierda con tu presupuesto, categoría preferida y 
                  especificaciones mínimas para obtener recomendaciones personalizadas.
                </p>
              </div>
            ) : recommendations.length === 0 ? (
              <div className="bg-card rounded-2xl border border-border/50 p-12 text-center shadow-soft">
                <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-muted flex items-center justify-center">
                  <Sparkles className="w-10 h-10 text-muted-foreground" />
                </div>
                <h3 className="font-display text-xl font-semibold text-foreground mb-2">
                  Sin resultados
                </h3>
                <p className="text-muted-foreground">
                  No encontramos productos que coincidan con tus preferencias. 
                  Intenta ajustar los filtros.
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="font-display text-xl font-semibold text-foreground">
                    {recommendations.length} recomendaciones encontradas
                  </h2>
                </div>
                {recommendations.map((rec, index) => (
                  <div
                    key={rec.product_id}
                    className="animate-slide-up"
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    <RecommendationCard
                      recommendation={rec}
                      rank={index + 1}
                    />
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

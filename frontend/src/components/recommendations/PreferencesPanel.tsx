import { useState } from 'react';
import { Sparkles, DollarSign, Cpu, HardDrive, Star, Tag } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { CATEGORIES } from '@/lib/constants';
import { RecommendationPreferences } from '@/services/api';

interface PreferencesPanelProps {
  onSubmit: (preferences: RecommendationPreferences) => void;
  loading?: boolean;
}

export function PreferencesPanel({ onSubmit, loading }: PreferencesPanelProps) {
  const [budget, setBudget] = useState<number>(1500);
  const [category, setCategory] = useState<string>('');
  const [minRam, setMinRam] = useState<number>(8);
  const [minStorage, setMinStorage] = useState<number>(256);
  const [minRating, setMinRating] = useState<number>(4.0);

  const handleSubmit = () => {
    onSubmit({
      budget,
      preferred_category: category || undefined,
      min_ram: minRam,
      min_storage: minStorage,
      min_rating: minRating
    });
  };

  return (
    <div className="bg-card rounded-2xl border border-border/50 p-6 shadow-soft space-y-6">
      <div className="flex items-center gap-3">
        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-glow">
          <Sparkles className="w-6 h-6 text-primary-foreground" />
        </div>
        <div>
          <h2 className="font-display text-xl font-bold text-foreground">Tus Preferencias</h2>
          <p className="text-sm text-muted-foreground">Personaliza tu búsqueda de productos</p>
        </div>
      </div>

      <div className="space-y-5">
        {/* Budget */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="flex items-center gap-2 text-sm font-medium text-foreground">
              <DollarSign className="w-4 h-4 text-primary" />
              Presupuesto máximo
            </label>
            <span className="text-lg font-display font-bold text-primary">${budget.toLocaleString()}</span>
          </div>
          <Slider
            value={[budget]}
            onValueChange={([value]) => setBudget(value)}
            min={100}
            max={5000}
            step={50}
            className="py-2"
          />
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>$100</span>
            <span>$5,000</span>
          </div>
        </div>

        {/* Category */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-medium text-foreground">
            <Tag className="w-4 h-4 text-primary" />
            Categoría preferida
          </label>
          <Select value={category} onValueChange={setCategory}>
            <SelectTrigger className="h-11 bg-background">
              <SelectValue placeholder="Cualquier categoría" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Cualquier categoría</SelectItem>
              {CATEGORIES.map((cat) => (
                <SelectItem key={cat.id} value={cat.id}>
                  {cat.icon} {cat.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* RAM */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="flex items-center gap-2 text-sm font-medium text-foreground">
              <Cpu className="w-4 h-4 text-primary" />
              RAM mínima
            </label>
            <span className="font-semibold text-foreground">{minRam} GB</span>
          </div>
          <Slider
            value={[minRam]}
            onValueChange={([value]) => setMinRam(value)}
            min={2}
            max={32}
            step={2}
            className="py-2"
          />
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>2 GB</span>
            <span>32 GB</span>
          </div>
        </div>

        {/* Storage */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="flex items-center gap-2 text-sm font-medium text-foreground">
              <HardDrive className="w-4 h-4 text-primary" />
              Almacenamiento mínimo
            </label>
            <span className="font-semibold text-foreground">{minStorage} GB</span>
          </div>
          <Slider
            value={[minStorage]}
            onValueChange={([value]) => setMinStorage(value)}
            min={64}
            max={2048}
            step={64}
            className="py-2"
          />
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>64 GB</span>
            <span>2 TB</span>
          </div>
        </div>

        {/* Rating */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="flex items-center gap-2 text-sm font-medium text-foreground">
              <Star className="w-4 h-4 text-warning" />
              Calificación mínima
            </label>
            <div className="flex items-center gap-1">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  onClick={() => setMinRating(star)}
                  className="p-0.5 transition-transform hover:scale-110"
                >
                  <Star
                    className={`w-5 h-5 ${
                      star <= minRating
                        ? 'fill-warning text-warning'
                        : 'text-muted'
                    }`}
                  />
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Submit */}
      <Button
        onClick={handleSubmit}
        disabled={loading}
        className="w-full h-12 bg-gradient-to-r from-primary to-accent hover:opacity-90 text-primary-foreground font-semibold shadow-glow"
      >
        {loading ? (
          <span className="flex items-center gap-2">
            <span className="w-4 h-4 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin" />
            Buscando...
          </span>
        ) : (
          <span className="flex items-center gap-2">
            <Sparkles className="w-5 h-5" />
            Obtener Recomendaciones
          </span>
        )}
      </Button>
    </div>
  );
}

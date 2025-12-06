import { useState } from 'react';
import { Search, SlidersHorizontal, X } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { CATEGORIES } from '@/lib/constants';
import { cn } from '@/lib/utils';

interface ProductFiltersProps {
  onCategoryChange: (category: string | undefined) => void;
  onPriceRangeChange: (min: number | undefined, max: number | undefined) => void;
  onSearchChange: (search: string) => void;
  selectedCategory?: string;
}

export function ProductFilters({
  onCategoryChange,
  onPriceRangeChange,
  onSearchChange,
  selectedCategory
}: ProductFiltersProps) {
  const [search, setSearch] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  const handleSearchChange = (value: string) => {
    setSearch(value);
    onSearchChange(value);
  };

  const handlePriceChange = () => {
    onPriceRangeChange(
      minPrice ? parseFloat(minPrice) : undefined,
      maxPrice ? parseFloat(maxPrice) : undefined
    );
  };

  const clearFilters = () => {
    setSearch('');
    setMinPrice('');
    setMaxPrice('');
    onCategoryChange(undefined);
    onPriceRangeChange(undefined, undefined);
    onSearchChange('');
  };

  const hasActiveFilters = search || selectedCategory || minPrice || maxPrice;

  return (
    <div className="space-y-4">
      {/* Search and Toggle */}
      <div className="flex gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
          <Input
            placeholder="Buscar productos..."
            value={search}
            onChange={(e) => handleSearchChange(e.target.value)}
            className="pl-10 h-12 bg-card border-border/50 focus:border-primary"
          />
        </div>
        <Button
          variant="outline"
          className={cn(
            "h-12 px-4 gap-2",
            showFilters && "bg-primary text-primary-foreground hover:bg-primary/90"
          )}
          onClick={() => setShowFilters(!showFilters)}
        >
          <SlidersHorizontal className="w-4 h-4" />
          <span className="hidden sm:inline">Filtros</span>
          {hasActiveFilters && (
            <span className="w-2 h-2 rounded-full bg-success" />
          )}
        </Button>
      </div>

      {/* Expanded Filters */}
      {showFilters && (
        <div className="animate-slide-up bg-card rounded-xl border border-border/50 p-4 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {/* Category Select */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-muted-foreground">Categoría</label>
              <Select
                value={selectedCategory || 'all'}
                onValueChange={(value) => onCategoryChange(value === 'all' ? undefined : value)}
              >
                <SelectTrigger className="h-10 bg-background">
                  <SelectValue placeholder="Todas las categorías" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todas las categorías</SelectItem>
                  {CATEGORIES.map((cat) => (
                    <SelectItem key={cat.id} value={cat.id}>
                      {cat.icon} {cat.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Price Range */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-muted-foreground">Precio mínimo</label>
              <Input
                type="number"
                placeholder="$0"
                value={minPrice}
                onChange={(e) => setMinPrice(e.target.value)}
                onBlur={handlePriceChange}
                className="h-10 bg-background"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-muted-foreground">Precio máximo</label>
              <Input
                type="number"
                placeholder="$∞"
                value={maxPrice}
                onChange={(e) => setMaxPrice(e.target.value)}
                onBlur={handlePriceChange}
                className="h-10 bg-background"
              />
            </div>
          </div>

          {/* Clear Filters */}
          {hasActiveFilters && (
            <Button
              variant="ghost"
              size="sm"
              onClick={clearFilters}
              className="text-muted-foreground hover:text-foreground"
            >
              <X className="w-4 h-4 mr-1" />
              Limpiar filtros
            </Button>
          )}
        </div>
      )}

      {/* Category Quick Filters */}
      <div className="flex flex-wrap gap-2">
        <Button
          variant={!selectedCategory ? "default" : "outline"}
          size="sm"
          onClick={() => onCategoryChange(undefined)}
          className="rounded-full"
        >
          Todos
        </Button>
        {CATEGORIES.slice(0, 5).map((cat) => (
          <Button
            key={cat.id}
            variant={selectedCategory === cat.id ? "default" : "outline"}
            size="sm"
            onClick={() => onCategoryChange(cat.id)}
            className="rounded-full"
          >
            {cat.icon} {cat.label}
          </Button>
        ))}
      </div>
    </div>
  );
}

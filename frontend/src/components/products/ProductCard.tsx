import { Link } from 'react-router-dom';
import { Star, Check, Shield, Cpu, HardDrive, Smartphone, Laptop, Monitor, Gamepad2, Battery, Tag, ShoppingCart, Eye } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Product } from '@/services/api';
import { CATEGORY_ICONS } from '@/lib/constants';
import { Button } from '@/components/ui/button';

interface ProductCardProps {
  product: Product;
  // For comparison page - checkbox mode
  selectable?: boolean;
  isSelected?: boolean;
  onToggleSelect?: (productId: string) => void;
  // For home page - cart mode
  onAddToCart?: (product: Product) => void;
}

export function ProductCard({
  product,
  selectable = false,
  isSelected = false,
  onToggleSelect,
  onAddToCart
}: ProductCardProps) {
  const { id, types, properties } = product;
  const {
    tieneNombre,
    tienePrecio,
    tieneRAM_GB,
    tieneAlmacenamiento_GB,
    tieneCalificacion,
    tieneDescuento,
    procesadorModelo,
    bateriaCapacidad_mAh,
    garantiaMeses,
  } = properties;

  const primaryType = types.find(t => CATEGORY_ICONS[t]) || types[0];
  const categoryIcon = CATEGORY_ICONS[primaryType] || '📦';
  const isGamer = types.includes('LaptopGamer');

  const finalPrice = tieneDescuento && tienePrecio
    ? tienePrecio * (1 - tieneDescuento / 100)
    : tienePrecio;

  const getCategoryIcon = () => {
    if (types.includes('LaptopGamer')) return <Gamepad2 className="w-12 h-12 text-accent" />;
    if (types.includes('Laptop')) return <Laptop className="w-12 h-12 text-primary" />;
    if (types.includes('Smartphone')) return <Smartphone className="w-12 h-12 text-primary" />;
    if (types.includes('Monitor')) return <Monitor className="w-12 h-12 text-primary" />;
    return <span className="text-5xl">{categoryIcon}</span>;
  };

  return (
    <div
      className={cn(
        "group relative bg-card rounded-2xl border transition-all duration-300 hover-lift overflow-hidden",
        isSelected
          ? "border-primary shadow-glow ring-2 ring-primary/20"
          : "border-border/50 hover:border-primary/30 shadow-soft hover:shadow-lg"
      )}
    >
      {/* Selectable Checkbox for Compare Page */}
      {selectable && (
        <div className="absolute top-3 left-3 z-10">
          <button
            onClick={() => onToggleSelect?.(id)}
            className={cn(
              "w-6 h-6 rounded-md border-2 flex items-center justify-center transition-all",
              isSelected
                ? "bg-primary border-primary"
                : "bg-card/80 border-muted-foreground/40 hover:border-primary"
            )}
          >
            {isSelected && <Check className="w-4 h-4 text-primary-foreground" />}
          </button>
        </div>
      )}

      {/* Discount Badge */}
      {tieneDescuento && tieneDescuento > 0 && (
        <div className={cn("absolute top-3 z-10", selectable ? "left-12" : "left-3")}>
          <div className="flex items-center gap-1 px-2 py-1 rounded-full bg-destructive text-destructive-foreground text-xs font-bold">
            <Tag className="w-3 h-3" />
            -{tieneDescuento}%
          </div>
        </div>
      )}

      {/* Gamer Badge */}
      {isGamer && (
        <div className="absolute top-3 right-3 z-10">
          <div className="px-2 py-1 rounded-full bg-accent text-accent-foreground text-xs font-bold">
            🎮 GAMER
          </div>
        </div>
      )}

      {/* Product Image/Icon Area */}
      <Link to={`/product/${id}`} className="block">
        <div className="relative h-40 bg-gradient-to-br from-secondary/50 to-muted/30 flex items-center justify-center overflow-hidden">
          {properties.imagenUrl ? (
            <div className="w-full h-full relative group-hover:scale-110 transition-transform duration-500">
              <img
                src={properties.imagenUrl}
                alt={tieneNombre || id}
                className="w-full h-full object-cover opacity-90 group-hover:opacity-100 transition-opacity"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />
            </div>
          ) : (
            <div className="transform group-hover:scale-110 transition-transform duration-500">
              {getCategoryIcon()}
            </div>
          )}
          <div className="absolute inset-0 bg-gradient-to-t from-card/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
        </div>
      </Link>

      {/* Content */}
      <div className="p-4 space-y-3">
        {/* Category Tags */}
        <div className="flex flex-wrap gap-1">
          {types.slice(0, 2).map(type => (
            <span
              key={type}
              className="px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground text-xs"
            >
              {CATEGORY_ICONS[type]} {type.replace('_', ' ')}
            </span>
          ))}
        </div>

        {/* Name */}
        <Link to={`/product/${id}`}>
          <h3 className="font-display font-semibold text-foreground line-clamp-2 group-hover:text-primary transition-colors">
            {tieneNombre || id}
          </h3>
        </Link>

        {/* Rating */}
        {tieneCalificacion && (
          <div className="flex items-center gap-1">
            {[...Array(5)].map((_, i) => (
              <Star
                key={i}
                className={cn(
                  "w-4 h-4",
                  i < Math.floor(tieneCalificacion)
                    ? "fill-warning text-warning"
                    : "text-muted"
                )}
              />
            ))}
            <span className="ml-1 text-sm font-medium text-muted-foreground">
              {tieneCalificacion.toFixed(1)}
            </span>
          </div>
        )}

        {/* Specs */}
        <div className="grid grid-cols-2 gap-2 text-sm">
          {tieneRAM_GB && (
            <div className="flex items-center gap-1.5 text-muted-foreground">
              <Cpu className="w-3.5 h-3.5" />
              <span>{tieneRAM_GB} GB RAM</span>
            </div>
          )}
          {tieneAlmacenamiento_GB && (
            <div className="flex items-center gap-1.5 text-muted-foreground">
              <HardDrive className="w-3.5 h-3.5" />
              <span>{tieneAlmacenamiento_GB} GB</span>
            </div>
          )}
          {procesadorModelo && (
            <div className="col-span-2 flex items-center gap-1.5 text-muted-foreground">
              <Cpu className="w-3.5 h-3.5" />
              <span className="truncate">{procesadorModelo}</span>
            </div>
          )}
          {bateriaCapacidad_mAh && (
            <div className="flex items-center gap-1.5 text-muted-foreground">
              <Battery className="w-3.5 h-3.5" />
              <span>{bateriaCapacidad_mAh} mAh</span>
            </div>
          )}
        </div>

        {/* Warranty */}
        {garantiaMeses && (
          <div className="flex items-center gap-1.5 text-success text-sm">
            <Shield className="w-3.5 h-3.5" />
            <span>{garantiaMeses} meses garantía</span>
          </div>
        )}

        {/* Price */}
        <div className="pt-2 border-t border-border/50">
          <div className="flex items-end gap-2">
            {tieneDescuento && tienePrecio ? (
              <>
                <span className="text-2xl font-display font-bold text-foreground">
                  ${finalPrice?.toFixed(0)}
                </span>
                <span className="text-sm text-muted-foreground line-through">
                  ${tienePrecio.toFixed(0)}
                </span>
              </>
            ) : (
              <span className="text-2xl font-display font-bold text-foreground">
                ${tienePrecio?.toFixed(0) || 'N/A'}
              </span>
            )}
          </div>
        </div>

        {/* Action Buttons - Only show on Home page (when onAddToCart is provided) */}
        {onAddToCart && !selectable && (
          <div className="flex gap-2 mt-2">
            <Button
              variant="outline"
              className="flex-1"
              asChild
            >
              <Link to={`/product/${id}`}>
                <Eye className="w-4 h-4 mr-2" />
                Ver detalle
              </Link>
            </Button>
            <Button
              variant="default"
              size="icon"
              className="bg-primary hover:bg-primary/90"
              onClick={(e) => {
                e.preventDefault();
                onAddToCart(product);
              }}
            >
              <ShoppingCart className="w-4 h-4" />
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}

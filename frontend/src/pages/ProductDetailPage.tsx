import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Star, Shield, Cpu, HardDrive, Battery, Monitor, Tag, Store, Smartphone, Laptop, Gamepad2 } from 'lucide-react';
import { useProduct } from '@/hooks/useProducts';
import { LoadingPage } from '@/components/common/LoadingSpinner';
import { Button } from '@/components/ui/button';
import { PROPERTY_LABELS, CATEGORY_ICONS } from '@/lib/constants';
import { cn } from '@/lib/utils';

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { product, loading, error } = useProduct(id);

  if (loading) return <LoadingPage />;

  if (error || !product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="font-display text-2xl font-bold text-foreground mb-2">
            Producto no encontrado
          </h2>
          <p className="text-muted-foreground mb-4">{error}</p>
          <Button asChild>
            <Link to="/">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Volver al catálogo
            </Link>
          </Button>
        </div>
      </div>
    );
  }

  const { types, properties } = product;
  const primaryType = types.find(t => CATEGORY_ICONS[t]) || types[0];
  const isGamer = types.includes('LaptopGamer');

  const getCategoryIcon = () => {
    if (types.includes('LaptopGamer')) return <Gamepad2 className="w-24 h-24 text-accent" />;
    if (types.includes('Laptop')) return <Laptop className="w-24 h-24 text-primary" />;
    if (types.includes('Smartphone')) return <Smartphone className="w-24 h-24 text-primary" />;
    if (types.includes('Monitor')) return <Monitor className="w-24 h-24 text-primary" />;
    return <span className="text-8xl">{CATEGORY_ICONS[primaryType] || '📦'}</span>;
  };

  const finalPrice = properties.tieneDescuento && properties.tienePrecio
    ? properties.tienePrecio * (1 - properties.tieneDescuento / 100)
    : properties.tienePrecio;

  // Helper para formatear valores que pueden ser arrays
  const formatValue = (value: unknown): string => {
    if (Array.isArray(value)) {
      return value.map(v => String(v)).join(', ');
    }
    return String(value ?? '');
  };

  // Get all displayable properties
  const displayProps = Object.entries(properties).filter(([key, value]) =>
    value !== undefined &&
    value !== null &&
    !['tieneNombre', 'imagenUrl'].includes(key)
  );

  return (
    <div className="min-h-screen py-8">
      <div className="container mx-auto px-4">
        {/* Back Button */}
        <Button asChild variant="ghost" className="mb-6">
          <Link to="/">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Volver al catálogo
          </Link>
        </Button>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Product Image */}
          <div className="relative">
            <div className="bg-card rounded-3xl border border-border/50 p-12 shadow-soft aspect-square flex items-center justify-center relative overflow-hidden">
              {/* Background decoration */}
              <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5" />
              <div className="absolute top-10 right-10 w-40 h-40 bg-primary/10 rounded-full blur-3xl" />
              <div className="absolute bottom-10 left-10 w-40 h-40 bg-accent/10 rounded-full blur-3xl" />

              <div className="relative transform hover:scale-105 transition-transform duration-500 w-full h-full flex items-center justify-center">
                {properties.imagenUrl ? (
                  <img
                    src={properties.imagenUrl}
                    alt={properties.tieneNombre || id}
                    className="w-full h-full object-contain drop-shadow-2xl"
                  />
                ) : (
                  getCategoryIcon()
                )}
              </div>

              {/* Badges */}
              <div className="absolute top-6 left-6 flex flex-col gap-2">
                {properties.tieneDescuento && properties.tieneDescuento > 0 && (
                  <div className="flex items-center gap-1 px-3 py-1.5 rounded-full bg-destructive text-destructive-foreground text-sm font-bold">
                    <Tag className="w-4 h-4" />
                    -{properties.tieneDescuento}%
                  </div>
                )}
                {isGamer && (
                  <div className="px-3 py-1.5 rounded-full bg-accent text-accent-foreground text-sm font-bold">
                    🎮 GAMER
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Product Info */}
          <div className="space-y-6">
            {/* Category Tags */}
            <div className="flex flex-wrap gap-2">
              {types.slice(0, 4).map(type => (
                <span
                  key={type}
                  className="px-3 py-1 rounded-full bg-secondary text-secondary-foreground text-sm"
                >
                  {CATEGORY_ICONS[type]} {type.replace('_', ' ')}
                </span>
              ))}
            </div>

            {/* Name */}
            <h1 className="font-display text-4xl font-bold text-foreground">
              {properties.tieneNombre || id}
            </h1>

            {/* Rating */}
            {properties.tieneCalificacion && (
              <div className="flex items-center gap-2">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    className={cn(
                      "w-6 h-6",
                      i < Math.floor(properties.tieneCalificacion!)
                        ? "fill-warning text-warning"
                        : "text-muted"
                    )}
                  />
                ))}
                <span className="ml-2 text-lg font-medium text-foreground">
                  {properties.tieneCalificacion.toFixed(1)}
                </span>
              </div>
            )}

            {/* Price */}
            <div className="bg-card rounded-2xl border border-border/50 p-6 shadow-soft">
              <div className="flex items-end gap-3 mb-4">
                {properties.tieneDescuento && properties.tienePrecio ? (
                  <>
                    <span className="text-4xl font-display font-bold text-foreground">
                      ${finalPrice?.toFixed(0)}
                    </span>
                    <span className="text-xl text-muted-foreground line-through">
                      ${properties.tienePrecio.toFixed(0)}
                    </span>
                    <span className="px-2 py-1 rounded bg-success/20 text-success text-sm font-medium">
                      Ahorras ${(properties.tienePrecio - finalPrice!).toFixed(0)}
                    </span>
                  </>
                ) : (
                  <span className="text-4xl font-display font-bold text-foreground">
                    ${properties.tienePrecio?.toFixed(0) || 'N/A'}
                  </span>
                )}
              </div>

              {/* Vendor */}
              {properties.vendidoPor && (
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Store className="w-4 h-4" />
                  <span>Vendido por: {formatValue(properties.vendidoPor).replace(/Vend_/g, '').replace(/_/g, ' ')}</span>
                </div>
              )}
            </div>

            {/* Key Specs */}
            <div className="grid grid-cols-2 gap-4">
              {properties.tieneRAM_GB && (
                <div className="bg-card rounded-xl border border-border/50 p-4 shadow-soft">
                  <div className="flex items-center gap-2 text-primary mb-1">
                    <Cpu className="w-5 h-5" />
                    <span className="text-sm font-medium">RAM</span>
                  </div>
                  <span className="text-2xl font-display font-bold text-foreground">
                    {properties.tieneRAM_GB} GB
                  </span>
                </div>
              )}
              {properties.tieneAlmacenamiento_GB && (
                <div className="bg-card rounded-xl border border-border/50 p-4 shadow-soft">
                  <div className="flex items-center gap-2 text-primary mb-1">
                    <HardDrive className="w-5 h-5" />
                    <span className="text-sm font-medium">Almacenamiento</span>
                  </div>
                  <span className="text-2xl font-display font-bold text-foreground">
                    {properties.tieneAlmacenamiento_GB >= 1024
                      ? `${(properties.tieneAlmacenamiento_GB / 1024).toFixed(0)} TB`
                      : `${properties.tieneAlmacenamiento_GB} GB`}
                  </span>
                </div>
              )}
              {properties.bateriaCapacidad_mAh && (
                <div className="bg-card rounded-xl border border-border/50 p-4 shadow-soft">
                  <div className="flex items-center gap-2 text-primary mb-1">
                    <Battery className="w-5 h-5" />
                    <span className="text-sm font-medium">Batería</span>
                  </div>
                  <span className="text-2xl font-display font-bold text-foreground">
                    {properties.bateriaCapacidad_mAh} mAh
                  </span>
                </div>
              )}
              {properties.garantiaMeses && (
                <div className="bg-card rounded-xl border border-border/50 p-4 shadow-soft">
                  <div className="flex items-center gap-2 text-success mb-1">
                    <Shield className="w-5 h-5" />
                    <span className="text-sm font-medium">Garantía</span>
                  </div>
                  <span className="text-2xl font-display font-bold text-foreground">
                    {properties.garantiaMeses} meses
                  </span>
                </div>
              )}
            </div>

            {/* All Specifications */}
            <div className="bg-card rounded-2xl border border-border/50 shadow-soft overflow-hidden">
              <h3 className="font-display font-semibold text-foreground p-4 border-b border-border/50 bg-muted/30">
                Especificaciones Completas
              </h3>
              <div className="divide-y divide-border/30">
                {displayProps.map(([key, value]) => (
                  <div key={key} className="flex justify-between p-4 hover:bg-muted/20 transition-colors">
                    <span className="text-muted-foreground">{PROPERTY_LABELS[key] || key}</span>
                    <span className="font-medium text-foreground">
                      {key === 'tienePrecio' ? `$${Number(value).toLocaleString()}` :
                        key === 'tieneDescuento' ? `${value}%` :
                          key === 'tieneMarca' ? formatValue(value).replace(/Marca_/g, '') :
                            key === 'vendidoPor' ? formatValue(value).replace(/Vend_/g, '').replace(/_/g, ' ') :
                              key === 'tieneSistemaOperativo' ? formatValue(value).replace(/OS_/g, '').replace(/_/g, ' ') :
                                formatValue(value)}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-4">
              <Button asChild size="lg" className="flex-1 h-14 bg-gradient-to-r from-primary to-accent hover:opacity-90 shadow-glow">
                <Link to={`/compare?add=${id}`}>
                  Añadir a Comparación
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

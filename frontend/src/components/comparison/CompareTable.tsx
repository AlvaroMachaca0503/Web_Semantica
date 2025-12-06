import { Trophy, Brain, ArrowRight, Cpu, HardDrive, Star, DollarSign } from 'lucide-react';
import { ComparisonResult } from '@/services/api';
import { PROPERTY_LABELS, CATEGORY_ICONS } from '@/lib/constants';
import { cn } from '@/lib/utils';

interface CompareTableProps {
  result: ComparisonResult;
}

export function CompareTable({ result }: CompareTableProps) {
  const { products, comparison_table, winner, winner_score, all_scores, reason, swrl_inference } = result;

  const getWinnerProduct = () => products.find(p => p.id === winner);
  const winnerProduct = getWinnerProduct();

  // Determine cell styling based on comparison
  const getCellStyle = (prop: string, value: string | number, index: number) => {
    const neutralProps = ['tieneNombre', 'vendidoPor', 'tieneMarca', 'tieneSistemaOperativo'];
    if (neutralProps.includes(prop)) return '';

    const values = comparison_table[prop];
    if (!values || values.every(v => v === '-')) return '';

    const numericValues = values.map(v => typeof v === 'number' ? v : parseFloat(String(v)) || 0);
    const currentVal = typeof value === 'number' ? value : parseFloat(String(value)) || 0;

    // Check for tie
    if (numericValues.every(v => v === numericValues[0]) && numericValues[0] !== 0) {
      return 'bg-warning/10 text-warning-foreground font-medium';
    }

    // Price: lower is better
    if (prop === 'tienePrecio') {
      const validValues = numericValues.filter(v => v > 0);
      const minVal = Math.min(...validValues);
      if (currentVal === minVal && currentVal > 0) {
        return 'bg-success/15 text-success font-bold';
      }
    }

    // Higher is better for these
    const higherIsBetter = ['tieneRAM_GB', 'tieneAlmacenamiento_GB', 'tieneCalificacion', 'bateriaCapacidad_mAh', 'garantiaMeses', 'tienePulgadas'];
    if (higherIsBetter.includes(prop)) {
      const maxVal = Math.max(...numericValues);
      if (currentVal === maxVal && currentVal > 0) {
        return 'bg-success/15 text-success font-bold';
      }
    }

    return '';
  };

  const formatValue = (prop: string, value: string | number) => {
    if (value === '-' || value === undefined || value === null) return '-';

    if (prop === 'tienePrecio') return `$${Number(value).toLocaleString()}`;
    if (prop === 'tieneRAM_GB') return `${value} GB`;
    if (prop === 'tieneAlmacenamiento_GB') return `${value} GB`;
    if (prop === 'tieneCalificacion') return `⭐ ${Number(value).toFixed(1)}`;
    if (prop === 'tienePulgadas') return `${value}"`;
    if (prop === 'bateriaCapacidad_mAh') return `${value} mAh`;
    if (prop === 'garantiaMeses') return `${value} meses`;
    if (prop === 'tieneDescuento') return `${value}%`;
    if (prop === 'pesoGramos') return `${value}g`;

    return String(value);
  };

  const getPropertyIcon = (prop: string) => {
    if (prop === 'tienePrecio') return <DollarSign className="w-4 h-4" />;
    if (prop === 'tieneRAM_GB') return <Cpu className="w-4 h-4" />;
    if (prop === 'tieneAlmacenamiento_GB') return <HardDrive className="w-4 h-4" />;
    if (prop === 'tieneCalificacion') return <Star className="w-4 h-4" />;
    return null;
  };

  // Collect all SWRL inferences
  const allInferences = [
    ...swrl_inference.esMejorOpcionQue.map(i => ({ ...i, type: 'Mejor Opción' })),
    ...swrl_inference.tieneMejorRAMQue.map(i => ({ ...i, type: 'Mejor RAM' })),
    ...swrl_inference.tieneMejorAlmacenamientoQue.map(i => ({ ...i, type: 'Mejor Almacenamiento' })),
    ...swrl_inference.tieneMejorPantallaQue.map(i => ({ ...i, type: 'Mejor Pantalla' })),
    ...swrl_inference.esEquivalenteTecnico.map(i => ({ ...i, type: 'Equivalente Técnico' })),
  ];

  return (
    <div className="space-y-6">
      {/* Winner Section */}
      <div className="relative overflow-hidden bg-gradient-to-r from-success/10 via-success/5 to-transparent rounded-2xl border border-success/20 p-6">
        <div className="absolute top-0 right-0 w-32 h-32 bg-success/10 rounded-full blur-3xl" />
        <div className="relative flex flex-col sm:flex-row items-start sm:items-center gap-4">
          <div className="flex items-center justify-center w-16 h-16 rounded-2xl bg-success/20 shadow-glow-success">
            <Trophy className="w-8 h-8 text-success" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium text-success uppercase tracking-wide">Ganador</p>
            <h2 className="text-2xl font-display font-bold text-foreground">
              {winnerProduct?.properties.tieneNombre || winner}
            </h2>
            <p className="text-muted-foreground mt-1">{reason}</p>
          </div>
          <div className="text-right">
            <div className="text-4xl font-display font-bold text-success">{winner_score.toFixed(1)}</div>
            <p className="text-sm text-muted-foreground">Score</p>
          </div>
        </div>
      </div>

      {/* Comparison Table */}
      <div className="bg-card rounded-2xl border border-border/50 overflow-hidden shadow-soft">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border/50">
                <th className="text-left p-4 font-medium text-muted-foreground bg-muted/30">
                  Propiedad
                </th>
                {products.map((product, index) => {
                  const isWinner = product.id === winner;
                  const primaryType = product.types.find(t => CATEGORY_ICONS[t]) || product.types[0];
                  
                  return (
                    <th
                      key={product.id}
                      className={cn(
                        "p-4 text-center min-w-[150px]",
                        isWinner ? "bg-success/10" : "bg-muted/30"
                      )}
                    >
                      <div className="flex flex-col items-center gap-2">
                        <span className="text-2xl">{CATEGORY_ICONS[primaryType] || '📦'}</span>
                        <span className={cn(
                          "font-semibold text-sm",
                          isWinner ? "text-success" : "text-foreground"
                        )}>
                          {product.properties.tieneNombre || product.id}
                        </span>
                        <span className="text-xs px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground">
                          Score: {all_scores[product.id]?.toFixed(1)}
                        </span>
                      </div>
                    </th>
                  );
                })}
              </tr>
            </thead>
            <tbody>
              {Object.entries(comparison_table).map(([prop, values]) => (
                <tr key={prop} className="border-b border-border/30 hover:bg-muted/20 transition-colors">
                  <td className="p-4">
                    <div className="flex items-center gap-2 text-muted-foreground">
                      {getPropertyIcon(prop)}
                      <span className="font-medium">{PROPERTY_LABELS[prop] || prop}</span>
                    </div>
                  </td>
                  {values.map((value, index) => (
                    <td
                      key={index}
                      className={cn(
                        "p-4 text-center transition-colors",
                        getCellStyle(prop, value, index)
                      )}
                    >
                      {formatValue(prop, value)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* SWRL Inference Panel */}
      {allInferences.length > 0 && (
        <div className="bg-card rounded-2xl border border-border/50 p-6 shadow-soft">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-xl bg-accent/20 flex items-center justify-center">
              <Brain className="w-5 h-5 text-accent" />
            </div>
            <div>
              <h3 className="font-display font-semibold text-foreground">Inferencias SWRL</h3>
              <p className="text-sm text-muted-foreground">Análisis semántico con reglas OWL</p>
            </div>
          </div>
          
          <div className="space-y-3">
            {allInferences.map((inference, index) => (
              <div
                key={index}
                className="flex items-center gap-3 p-3 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors"
              >
                <span className="px-2 py-0.5 rounded-full bg-accent/20 text-accent text-xs font-medium">
                  {inference.type}
                </span>
                <span className="font-medium text-foreground">{inference.source}</span>
                <ArrowRight className="w-4 h-4 text-muted-foreground" />
                <span className="text-muted-foreground">{inference.target}</span>
                <span className="ml-auto text-xs text-muted-foreground">
                  Regla: {inference.rule}
                </span>
              </div>
            ))}
          </div>

          {swrl_inference.rules_applied.length > 0 && (
            <div className="mt-4 pt-4 border-t border-border/30">
              <p className="text-sm text-muted-foreground">
                <span className="font-medium">Reglas aplicadas:</span>{' '}
                {swrl_inference.rules_applied.join(', ')}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

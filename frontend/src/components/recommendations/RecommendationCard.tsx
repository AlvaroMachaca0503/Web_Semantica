import { Link } from 'react-router-dom';
import { ArrowRight, Percent, TrendingUp } from 'lucide-react';
import { Recommendation } from '@/services/api';
import { cn } from '@/lib/utils';

interface RecommendationCardProps {
  recommendation: Recommendation;
  rank: number;
}

export function RecommendationCard({ recommendation, rank }: RecommendationCardProps) {
  const { product_id, score, reason, match_percentage } = recommendation;

  const getScoreColor = () => {
    if (score >= 90) return 'text-success';
    if (score >= 70) return 'text-primary';
    if (score >= 50) return 'text-warning';
    return 'text-muted-foreground';
  };

  const getGradient = () => {
    if (rank === 1) return 'from-warning/20 via-warning/5 to-transparent border-warning/30';
    if (rank === 2) return 'from-muted/30 via-muted/10 to-transparent border-muted-foreground/20';
    if (rank === 3) return 'from-amber-700/20 via-amber-700/5 to-transparent border-amber-700/20';
    return 'from-secondary/50 to-transparent border-border/50';
  };

  const getMedal = () => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  return (
    <Link
      to={`/product/${product_id}`}
      className={cn(
        "group block relative overflow-hidden bg-gradient-to-r rounded-2xl border p-5 transition-all duration-300 hover-lift",
        getGradient()
      )}
    >
      <div className="flex items-start gap-4">
        {/* Rank Badge */}
        <div className="flex-shrink-0">
          <div className={cn(
            "w-14 h-14 rounded-xl flex items-center justify-center text-2xl font-display font-bold",
            rank <= 3 ? "bg-gradient-to-br from-warning/20 to-warning/5" : "bg-muted"
          )}>
            {getMedal()}
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <h3 className="font-display font-semibold text-lg text-foreground group-hover:text-primary transition-colors truncate">
            {product_id.replace(/_/g, ' ')}
          </h3>
          <p className="mt-1 text-sm text-muted-foreground line-clamp-2">{reason}</p>
          
          {/* Match Percentage */}
          <div className="mt-3 flex items-center gap-4">
            <div className="flex items-center gap-1.5 text-sm">
              <Percent className="w-4 h-4 text-success" />
              <span className="font-medium text-success">{match_percentage.toFixed(0)}% match</span>
            </div>
          </div>
        </div>

        {/* Score Circle */}
        <div className="flex-shrink-0 text-center">
          <div className="relative w-16 h-16">
            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="32"
                cy="32"
                r="28"
                stroke="currentColor"
                strokeWidth="4"
                fill="none"
                className="text-muted"
              />
              <circle
                cx="32"
                cy="32"
                r="28"
                stroke="currentColor"
                strokeWidth="4"
                fill="none"
                strokeDasharray={`${(score / 100) * 175.93} 175.93`}
                strokeLinecap="round"
                className={getScoreColor()}
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className={cn("text-lg font-display font-bold", getScoreColor())}>
                {score.toFixed(0)}
              </span>
            </div>
          </div>
          <span className="text-xs text-muted-foreground">Score</span>
        </div>

        {/* Arrow */}
        <ArrowRight className="w-5 h-5 text-muted-foreground group-hover:text-primary group-hover:translate-x-1 transition-all" />
      </div>

      {/* Hover Glow */}
      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
        <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full blur-3xl" />
      </div>
    </Link>
  );
}

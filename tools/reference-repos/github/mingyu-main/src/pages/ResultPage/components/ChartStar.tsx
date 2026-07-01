import type { PalaceFact } from '@/types/analysis';

export function ChartStar(props: {
  star: PalaceFact['major_stars'][number];
  tone: 'major' | 'minor' | 'scope';
}) {
  const { star, tone } = props;

  return (
    <span
      className={`chart-star chart-star-${tone} ${
        star.birth_mutagen ? 'has-birth-mutagen' : ''
      } ${star.active_scope_mutagen ? 'has-active-mutagen' : ''}`}
    >
      <span className="chart-star-name">{star.name}</span>
      {star.birth_mutagen ? (
        <span className="chart-star-mark chart-star-mark-birth">{star.birth_mutagen}</span>
      ) : null}
      {star.active_scope_mutagen ? (
        <span className="chart-star-mark chart-star-mark-active">{star.active_scope_mutagen}</span>
      ) : null}
    </span>
  );
}

export function ChartStarLine(props: {
  stars: PalaceFact['major_stars'];
  tone: 'major' | 'minor' | 'scope';
  fallback?: string;
  limit?: number;
  layout?: 'wrap' | 'column';
}) {
  const stars = props.limit ? props.stars.slice(0, props.limit) : props.stars;
  const layoutClassName = props.layout === 'column' ? 'is-column' : 'is-wrap';

  if (stars.length === 0) {
    return props.fallback ? (
      <div className={`chart-cell-stars chart-cell-stars-${props.tone} ${layoutClassName}`}>
        <span className="chart-star-empty">{props.fallback}</span>
      </div>
    ) : null;
  }

  return (
    <div className={`chart-cell-stars chart-cell-stars-${props.tone} ${layoutClassName}`}>
      {stars.map((star) => (
        <ChartStar
          key={`${props.tone}-${star.name}-${star.birth_mutagen ?? 'n'}-${star.active_scope_mutagen ?? 'n'}`}
          star={star}
          tone={props.tone}
        />
      ))}
    </div>
  );
}

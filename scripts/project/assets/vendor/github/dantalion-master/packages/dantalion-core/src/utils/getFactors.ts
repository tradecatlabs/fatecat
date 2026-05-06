import type { Source2D } from './create2DAccessor';
import type { BirthdayDetails } from './getBirthdayDetails';
import shiftAndModulo from './shiftAndModulo';

/** Intermediate values that determine the factors of personality. */
export interface Factors {
  /** The factors that determine the sub-personality (cycle). */
  cycle: number;
  /** Gets the coordinates of the table. */
  getXY: (value: number) => Source2D;
  /** The factors that determine the inner personality. */
  inner: number;
  /** The factors that determine the life base. */
  lifeBase: number;
  /** The factors that determine the outer personality. */
  outer: number;
  /** The factors that determine the potentials. */
  potentials: [number, number];
  /** The factors that determine the personality of working. */
  workStyle: number;
}

/** Source for calculating intermediate values. */
export interface FactorSource extends BirthdayDetails {
  monthlyCoefficient: number;
}

/**
 * Calculate the factors that determine the personality.
 * @param source Source for calculation.
 * @returns Intermediate values that determine the factors of personality.
 */
export default (source: FactorSource): Factors => {
  const {
    date,
    month: { early, month, shifted },
    monthlyCoefficient: monthlyCoefficients,
    year: { full, hi, lo },
  } = source;
  const lessThan = date < monthlyCoefficients;
  const outer = shiftAndModulo(month - (lessThan ? 1 : 0), 12) + 1;
  const workStyle = full + 9 - early(lessThan);
  const cycle = new Int32Array([hi * 4.25, (shifted + 1) * 0.6]).reduce(
    (acc, cur) => acc + cur,
    Math.floor((lo - early()) * 5.25) + date + 7
  );
  const potentials = [workStyle - 2, full * 2 + outer + 2].map((v) =>
    shiftAndModulo(v, 10)
  );
  return {
    cycle: shiftAndModulo(cycle, 10),
    getXY: (value: number): Source2D => ({ x: value - 1, y: cycle % 10 }),
    inner: shiftAndModulo(shifted * 6 + hi * 4 + cycle - 6, 12),
    lifeBase: date - monthlyCoefficients,
    outer: shiftAndModulo(outer, 12),
    potentials: [potentials[0], potentials[1]],
    workStyle: shiftAndModulo(workStyle, 12),
  };
};

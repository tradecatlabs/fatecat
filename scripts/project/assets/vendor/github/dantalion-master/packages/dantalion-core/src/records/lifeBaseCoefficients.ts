import { lifeBaseCoefficients } from '../masterData.json';

/**
 * Get the life base factor from the month, day, and coefficient.
 * @param month The month. (1-12)
 * @param dcoef Coefficient of date.
 * @returns The factors of Life base.
 */
export default (month: number, dcoef: number): number =>
  lifeBaseCoefficients[month - 1]?.find(
    (v) => dcoef < (v.t ?? Number.MAX_VALUE)
  )?.v ?? Number.NaN;

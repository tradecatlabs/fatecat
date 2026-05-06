import { monthlyCoefficients } from '../masterData.json';

/**
 * Calculate the monthly coefficient index from the date.
 * @param date The date.
 */
const getIndex = (date: ConstructorParameters<typeof Date>[0]) => {
  const from = new Date(-3058300800000);
  const to = new Date(date);
  return (
    to.getMonth() -
    from.getMonth() +
    12 * (to.getFullYear() - from.getFullYear())
  );
};

/** Get the monthly coefficient corresponding to the specified date. */
export default (date: ConstructorParameters<typeof Date>[0]): number =>
  monthlyCoefficients[getIndex(date)] ?? Number.NaN;

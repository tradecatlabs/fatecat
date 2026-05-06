/**
 * The remainder is calculated so that it is always a positive number.
 * @param a Dividend. This value minus 1 applies.
 * @param n Divisor.
 */
export default (a: number, n: number): number => ((((a - 1) % n) + n) % n) + 1;

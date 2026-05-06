import genius, { Genius } from '../types/genius';

/**
 * Create a record for each genius type from the source.
 * @param source Source.
 * @template T Type of the source.
 */
export default <T>(source: T[]): Record<Genius, T> =>
  <Record<Genius, T>>(
    Object.fromEntries(source.map((value, index) => [genius[index], value]))
  );

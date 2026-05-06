import type { Genius } from '..';
import createGeniusRecord from './createGeniusRecord';

/**
 * Create a record for each genius type from the source.
 * @param table Source.
 * @template T Type of the source.
 */
export default <T>(table: T[][]): Record<Genius, Record<Genius, T>> =>
  createGeniusRecord(table.map((row) => createGeniusRecord(row)));

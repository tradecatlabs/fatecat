/** The params for create2DAccessor function. */
export interface Source<T extends string> {
  /** Labels associated with the table. */
  label: readonly T[];
  /** An table. */
  table: readonly number[][];
}

/** 2D position for a table. */
export interface Source2D {
  /** Column position. */
  x?: number;
  /** Row position. */
  y?: number;
}

/**
 * Get an accessor to the table.
 * @param label List of labels.
 * @param table Table.
 */
export default <T extends string>({
    label,
    table,
  }: Source<T>): (({ x, y }: Source2D) => T) =>
  ({ x = 0, y = 0 }) =>
    label[table[y]?.[x]];

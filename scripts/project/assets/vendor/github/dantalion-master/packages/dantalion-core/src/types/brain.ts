/**
 * The types of thought method.
 *
 * |   Key   | Value                                             |
 * | :-----: | :------------------------------------------------ |
 * | `left`  | Left brain type. Logical thinking is superior.    |
 * | `right` | Right brain type. Intuitive thinking is superior. |
 */
export type Brain = 'left' | 'right';

/** The list that the types of thought methods. */
export default Object.freeze<Brain[]>(['left', 'right']);

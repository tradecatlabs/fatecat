/**
 * The types for role.
 *
 * |   Key    | Value                                                        |
 * | :------: | :----------------------------------------------------------- |
 * | `adjust` | This type of person can solve interpersonal problems.        |
 * | `brain`  | This type of person can create interesting ideas.            |
 * | `direct` | This type of person has all abilities little by little.      |
 * | `quick`  | This type of person has a lot of energy, like a salesperson. |
 */
export type Position = 'adjust' | 'brain' | 'direct' | 'quick';

/** The list of role types. */
export default Object.freeze<Position[]>([
  'adjust',
  'brain',
  'direct',
  'quick',
]);

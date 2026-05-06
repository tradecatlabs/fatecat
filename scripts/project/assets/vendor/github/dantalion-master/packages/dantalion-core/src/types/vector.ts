/**
 * Vector of genius type.
 *
 * | Key            | Value                                                                  |
 * | :------------- | :--------------------------------------------------------------------- |
 * | `authority`    | This type of person would like to do the action for self-authority.    |
 * | `economically` | This type of person would like to do the action to build their wealth. |
 * | `humanely`     | This type of person would like to do the action for self-virtue.       |
 */
export type Vector = 'authority' | 'economically' | 'humanely';

/** The list of personality types. */
export default Object.freeze<Vector[]>([
  'authority',
  'economically',
  'humanely',
]);

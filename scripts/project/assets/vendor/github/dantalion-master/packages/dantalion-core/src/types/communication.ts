/**
 * The types of dialogue policy.
 *
 * |  Key   | Value                                                             |
 * | :----: | :---------------------------------------------------------------- |
 * | `fix`  | This type of person would like to find a way from the conclusion. |
 * | `flex` | This type of person would like to express conclude fluidly.       |
 */
export type Communication = 'fix' | 'flex';

/** The list that the types of dialogue policy. */
export default Object.freeze<Communication[]>(['fix', 'flex']);

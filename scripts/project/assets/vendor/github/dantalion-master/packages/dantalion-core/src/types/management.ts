/**
 * The types that the risk management method.
 *
 * |  Key   | Value                                                                                       |
 * | :----: | :------------------------------------------------------------------------------------------ |
 * | `care` | This type of person has a good intuition for risk but weak for chance perception.           |
 * | `hope` | This type of person has a good intuition for great opportunities, but weak risk perception. |
 */
export type Management = 'care' | 'hope';

/** The list of the types that the risk management method. */
export default Object.freeze<Management[]>(['care', 'hope']);

/**
 * The types of easy to the motivated environment.
 *
 * |      Key      | Value                                                            |
 * | :-----------: | :--------------------------------------------------------------- |
 * | `competition` | The environment that can be compared with other peoples.         |
 * |   `ownMind`   | The environment that they can do on their plan.                  |
 * |    `power`    | The environment that they can do as soon as they think about it. |
 * |   `safety`    | The environment that they can pursue security and peace.         |
 * |   `skillUp`   | The environment that daily improvement can be felt.              |
 * |   `status`    | The environment that they can be different from others.          |
 */
export type Motivation =
  | 'competition'
  | 'ownMind'
  | 'power'
  | 'safety'
  | 'skillUp'
  | 'status';

/** The list of the types that easy to the motivated environment. */
export default Object.freeze<Motivation[]>([
  'competition',
  'ownMind',
  'power',
  'safety',
  'skillUp',
  'status',
]);

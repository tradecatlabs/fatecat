/**
 * The potential type definition that can exert when taking action.
 *
 * | key  | CC  | Value                                                                                        |
 * | :--- | :-- | :------------------------------------------------------------------------------------------- |
 * | `Ci` | _j_ | This type of person is good at sublimating existing works with respect.                      |
 * | `Co` | _i_ | This type of person is skilled at exploring one thing. They also tend to an originator.      |
 * | `Ei` | _d_ | This type of person is good at non-verbal and passive expression.                            |
 * | `Eo` | _c_ | This type of person is skilled at active expression through words.                           |
 * | `Fi` | _f_ | This type of person is relatively cautious and can see the meaning behind the numbers.       |
 * | `Fo` | _e_ | This type of person is good at using numbers and other evidence-based expressions.           |
 * | `Ii` | _b_ | This type of person is a good listener and can draw out the other person's point.            |
 * | `Io` | _a_ | This type of person is good at active and aggressive communication.                          |
 * | `Ni` | _h_ | This type of person has fine self-management skills and is good at maintaining organization. |
 * | `No` | _g_ | This type of person is very caring and good at developing organizations.                     |
 */
export type Potential =
  | 'Ci'
  | 'Co'
  | 'Ei'
  | 'Eo'
  | 'Fi'
  | 'Fo'
  | 'Ii'
  | 'Io'
  | 'Ni'
  | 'No';

/** The list of the types that the potential. */
export default Object.freeze<Potential[]>([
  'Ci',
  'Co',
  'Ei',
  'Eo',
  'Fi',
  'Fo',
  'Ii',
  'Io',
  'Ni',
  'No',
]);

/** A table of Potential to CC. */
export const cc = Object.freeze<Record<Potential, string>>({
  Ci: 'j',
  Co: 'i',
  Ei: 'd',
  Eo: 'c',
  Fi: 'f',
  Fo: 'e',
  Ii: 'b',
  Io: 'a',
  Ni: 'h',
  No: 'g',
});

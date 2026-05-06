/**
 * The types that the base of ego.
 *
 * | Key            | CC  | Value                                                                    |
 * | :------------- | :-- | :----------------------------------------------------------------------- |
 * | `application`  | _G_ | This type of person would like to self-experience seriously.             |
 * | `association`  | _I_ | This type of person would like to do it immediately when they think.     |
 * | `development`  | _D_ | This type of person would like to be perfectionists.                     |
 * | `expression`   | _C_ | This type of person would like to be honest with themselves.             |
 * | `finance`      | _E_ | This type of person would like to put everything within eye reach.       |
 * | `investment`   | _F_ | This type of person would like to be a down-to-earth collector.          |
 * | `organization` | _H_ | This type of person would like to live as a member of a group.           |
 * | `quest`        | _J_ | This type of person would like to learn from the wisdom of our pioneers. |
 * | `selfMind`     | _B_ | This type of person would like to be a leader of the team.               |
 * | `selfReliance` | _A_ | This type of person would like to be a lone wolf.                        |
 */
export type LifeBase =
  | 'application'
  | 'association'
  | 'development'
  | 'expression'
  | 'finance'
  | 'investment'
  | 'organization'
  | 'quest'
  | 'selfMind'
  | 'selfReliance';

/** The list that the base of ego type. */
export default Object.freeze<LifeBase[]>([
  'application',
  'association',
  'development',
  'expression',
  'finance',
  'investment',
  'organization',
  'quest',
  'selfMind',
  'selfReliance',
]);

/** A table of LifeBase to CC. */
export const cc = Object.freeze<Record<LifeBase, string>>({
  application: 'G',
  association: 'I',
  development: 'D',
  expression: 'C',
  finance: 'E',
  investment: 'F',
  organization: 'H',
  quest: 'J',
  selfMind: 'B',
  selfReliance: 'A',
});

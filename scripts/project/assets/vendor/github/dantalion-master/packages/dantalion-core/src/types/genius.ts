/**
 * The types of personality.
 *
 * |  Key  | Value                                                                                   |
 * | :---: | :-------------------------------------------------------------------------------------- |
 * | `000` | This type of person would like to be freedom. And also, They have a good imagination.   |
 * | `001` | This type of person would like to do something different from others with their ideas.  |
 * | `012` | This type of person will like new somethings. They also value discussions, especially.  |
 * | `024` | This type of person is good at turning anxiety into action. They have a strong memory.  |
 * | `025` | This type of person has a strong camaraderie. And also, they have a lot of friends.     |
 * | `100` | This type of person is serious and perfectionist. They expose weak point when praised.  |
 * | `108` | This type of person is shy and honest. And they have a strong sense of responsibility.  |
 * | `125` | This type of person can accept temporary abstinence to fulfill their long-term goals.   |
 * | `555` | This type of person is quick to learn and can do anything. Also, they are dignified.    |
 * | `789` | This type of person value experience and achievement. Also, they prefer to be quiet.    |
 * | `888` | This type of person value the spirit of challenge and are interested in various things. |
 * | `919` | This type of person has the quick situational judgment and also is good at bargaining.  |
 */
export type Genius =
  | '000'
  | '001'
  | '012'
  | '024'
  | '025'
  | '100'
  | '108'
  | '125'
  | '555'
  | '789'
  | '888'
  | '919';

/** The list of personality types. */
export default Object.freeze<Genius[]>([
  '000',
  '001',
  '012',
  '024',
  '025',
  '100',
  '108',
  '125',
  '555',
  '789',
  '888',
  '919',
]);

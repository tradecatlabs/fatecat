import brain, { Brain } from './brain';
import communication, { Communication } from './communication';
import genius, { Genius } from './genius';
import lifeBase, { LifeBase, cc as lifeBaseCC } from './lifeBase';
import management, { Management } from './management';
import motivation, { Motivation } from './motivation';
import position, { Position } from './position';
import potential, { Potential, cc as potentialCC } from './potential';
import response, { Response } from './response';
import vector, { Vector } from './vector';

/** All types list. */
export interface AllTypes {
  /** The list that the types of thought methods. */
  readonly brain: readonly Brain[];
  /** The list that the types of dialogue policy. */
  readonly communication: readonly Communication[];
  /** The list of personality types. */
  readonly genius: readonly Genius[];
  /** The list that the base of ego type. */
  readonly lifeBase: readonly LifeBase[];
  /** The list that the base of ego type. */
  readonly lifeBaseCC: Record<LifeBase, string>;
  /** The list of the types that the risk management method. */
  readonly management: readonly Management[];
  /** The list of the types that easy to the motivated environment. */
  readonly motivation: readonly Motivation[];
  /** The list of role types. */
  readonly position: readonly Position[];
  /** The list of the types that the potential. */
  readonly potential: readonly Potential[];
  /** The list of the types that the potential. */
  readonly potentialCC: Record<Potential, string>;
  /** The list of the types that the role. */
  readonly response: readonly Response[];
  /** The list of personality types. */
  readonly vector: readonly Vector[];
}

/** All types list. */
export default Object.freeze<AllTypes>({
  brain,
  communication,
  genius,
  lifeBase,
  lifeBaseCC,
  management,
  motivation,
  position,
  potential,
  potentialCC,
  response,
  vector,
});

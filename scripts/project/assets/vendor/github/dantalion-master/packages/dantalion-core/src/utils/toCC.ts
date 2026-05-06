import { cc as lifeBaseCC } from '../types/lifeBase';
import { cc as potentialCC } from '../types/potential';
import type { Personality } from './getPersonality';

/**
 * Create a CC string from personality object.
 * @param personality Specify the personality object.
 * @return The CC string.
 */
export default (personality: Personality): string => {
  const { cycle, inner, lifeBase, outer, potentials, workStyle } = personality;
  const c1 = cycle % 10;
  const pcc = potentials.reduceRight(
    (acc, cur) => `${acc}-${potentialCC[cur]}`,
    ''
  );
  return `${inner}-${outer}-${workStyle}-${inner}${c1}-${lifeBaseCC[lifeBase]}${pcc}`;
};

import type { AffinityLevel } from '../types/AffinityLevel';
import createGeniusRecords from '../utils/createGeniusRecords';
import { love } from '../masterData.json';

/** A list of love affinity by genius type. */
export default createGeniusRecords(love as AffinityLevel[][]);

import type { AffinityLevel } from '../types/AffinityLevel';
import createGeniusRecords from '../utils/createGeniusRecords';
import { biz } from '../masterData.json';

/** A list of business affinity by genius type. */
export default createGeniusRecords(biz as AffinityLevel[][]);

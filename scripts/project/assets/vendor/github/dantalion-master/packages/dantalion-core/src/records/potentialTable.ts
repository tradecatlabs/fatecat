import label from '../types/potential';
import create2DAccessor from '../utils/create2DAccessor';
import { potential as table } from '../masterData.json';

/** The table of potential factors. */
export default create2DAccessor({ label, table });

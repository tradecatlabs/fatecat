import label from '../types/genius';
import create2DAccessor from '../utils/create2DAccessor';
import { genius as table } from '../masterData.json';

/** The table of genius factors. */
export default create2DAccessor({ label, table });

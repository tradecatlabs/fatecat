import label from '../types/lifeBase';
import create2DAccessor from '../utils/create2DAccessor';
import { lifeBase as table } from '../masterData.json';

/** A table of the life base factor. */
export default create2DAccessor({ label, table });

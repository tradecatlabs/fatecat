import * as wahr from './wahr.js';
import * as mhb2000a from './mhb2000.js';
import * as mhb2000b from './mhb2000.truncated.js';

export const IAU1980=wahr;
export const IAU2000A = mhb2000a;
export const IAU2000B = mhb2000b;

//default
export * from './mhb2000.truncated.js';

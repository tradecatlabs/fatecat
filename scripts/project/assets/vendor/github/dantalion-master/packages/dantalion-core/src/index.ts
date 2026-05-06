import details, { Detail } from './records/details';
import type { Genius } from './types/genius';

export type { Affinity, Detail } from './records/details';
export { default as types, AllTypes } from './types';
export type { AffinityLevel } from './types/AffinityLevel';
export type { Brain } from './types/brain';
export type { Communication } from './types/communication';
export type { Genius } from './types/genius';
export type { LifeBase } from './types/lifeBase';
export type { Management } from './types/management';
export type { Motivation } from './types/motivation';
export type { Position } from './types/position';
export type { Potential } from './types/potential';
export type { Response } from './types/response';
export type { Vector } from './types/vector';
export { default as getPersonality, Personality } from './utils/getPersonality';
export { default as toCC } from './utils/toCC';

export const getDetail = (genius: Genius): Detail => details[genius];

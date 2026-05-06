import type { AffinityLevel } from '../types/AffinityLevel';
import brain, { Brain } from '../types/brain';
import communication, { Communication } from '../types/communication';
import geniusTable, { Genius } from '../types/genius';
import management, { Management } from '../types/management';
import motivation, { Motivation } from '../types/motivation';
import position, { Position } from '../types/position';
import response, { Response } from '../types/response';
import vector, { Vector } from '../types/vector';
import createGeniusRecord from '../utils/createGeniusRecord';
import { detailsMap } from '../masterData.json';
import bizRecords from './bizRecords';
import loveRecords from './loveRecords';

/** Type of the source. */
type DetailsSourceMap = [
  number,
  number,
  number,
  number,
  number,
  number,
  number
];

/** The lists of affinity by genius type. */
export interface Affinity {
  /** for business. */
  biz: Record<Genius, AffinityLevel>;
  /** for romance. */
  love: Record<Genius, AffinityLevel>;
}

/** The detail for genius type. */
export interface Detail {
  /** The lists of affinity by genius type. */
  affinity: Affinity;
  /** The types of thought method. */
  brain: Brain;
  /** The types of dialogue policy. */
  communication: Communication;
  /** The types that the risk management method. */
  management: Management;
  /** The types of easy to the motivated environment. */
  motivation: Motivation;
  /** The types for role. */
  position: Position;
  /** The types for role. */
  response: Response;
  /** Vector of genius type. */
  vector: Vector;
}

/** The list that the details corresponding to personality type. */
export default createGeniusRecord(
  (detailsMap as DetailsSourceMap[]).map<Detail>((row, index) => ({
    affinity: {
      biz: bizRecords[geniusTable[index]],
      love: loveRecords[geniusTable[index]],
    },
    brain: brain[row[5]],
    communication: communication[row[0]],
    management: management[row[1]],
    motivation: motivation[row[4]],
    position: position[row[3]],
    response: response[row[2]],
    vector: vector[row[6]],
  }))
);

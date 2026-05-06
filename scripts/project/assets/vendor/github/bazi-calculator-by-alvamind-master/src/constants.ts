import type { ElementType } from "./types";

// src/constants.ts
export const STEMS = [
  '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸',
];

export const BRANCHES = [
  '子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥',
];

export const ANIMALS = [
  'Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake',
  'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig',
];

export const ELEMENTS: { [key: string]: string[] } = {
  WOOD: ['甲', '乙'],
  FIRE: ['丙', '丁'],
  EARTH: ['戊', '己'],
  METAL: ['庚', '辛'],
  WATER: ['壬', '癸'],
};

export const BRANCH_ELEMENTS: { [key: string]: string[] } = {
  WATER: ['子', '亥'],
  WOOD: ['寅', '卯'],
  FIRE: ['巳', '午'],
  METAL: ['申', '酉'],
  EARTH: ['丑', '辰', '未', '戌'],
};

export const HIDDEN_STEMS: { [key: string]: string[] } = {
  子: ['癸'],
  丑: ['己', '癸', '辛'],
  寅: ['甲', '丙', '戊'],
  卯: ['乙'],
  辰: ['戊', '乙', '癸'],
  巳: ['丙', '庚', '戊'],
  午: ['丁', '己'],
  未: ['己', '丁', '乙'],
  申: ['庚', '壬', '戊'],
  酉: ['辛'],
  戌: ['戊', '辛', '丁'],
  亥: ['壬', '甲'],
};

export const ELEMENT_RELATIONSHIPS: { [key: string]: { [key: string]: string } } = {
  WOOD: {
    WATER: 'Resource',
    WOOD: 'Companion',
    FIRE: 'Output',
    EARTH: 'Wealth',
    METAL: 'Control'
  },
  FIRE: {
    WOOD: 'Resource',
    FIRE: 'Companion',
    EARTH: 'Output',
    METAL: 'Wealth',
    WATER: 'Control'
  },
  EARTH: {
    FIRE: 'Resource',
    EARTH: 'Companion',
    METAL: 'Output',
    WATER: 'Wealth',
    WOOD: 'Control'
  },
  METAL: {
    EARTH: 'Resource',
    METAL: 'Companion',
    WATER: 'Output',
    WOOD: 'Wealth',
    FIRE: 'Control'
  },
  WATER: {
    METAL: 'Resource',
    WATER: 'Companion',
    WOOD: 'Output',
    FIRE: 'Wealth',
    EARTH: 'Control'
  }
};

export const RELATIONSHIP_WEIGHTS: { [key: string]: number } = {
  'Resource': 3,
  'Companion': 2.5,
  'Output': 2,
  'Wealth': 1.2,
  'Control': 1.2
};

export const HOUR_MAP: [number, number, string][] = [
  [23, 1, '子'], [1, 3, '丑'], [3, 5, '寅'],
  [5, 7, '卯'], [7, 9, '辰'], [9, 11, '巳'],
  [11, 13, '午'], [13, 15, '未'], [15, 17, '申'],
  [17, 19, '酉'], [19, 21, '戌'], [21, 23, '亥'],
];

export const NOBLEMAN_MAP: Record<ElementType, string[]> = {
  WOOD: ['丑', '未'],
  FIRE: ['亥', '巳'],
  EARTH: ['申', '寅'],
  METAL: ['寅', '午'],
  WATER: ['巳', '申']
};

export const INTELLIGENCE_MAP: Record<ElementType, string> = {
  WOOD: '巳',
  FIRE: '申',
  EARTH: '亥',
  METAL: '子',
  WATER: '巳'
};

export const PEACH_BLOSSOM_MAP: Record<ElementType, string> = {
  WOOD: '酉',
  FIRE: '卯',
  EARTH: '午',
  METAL: '午',
  WATER: '申'
};

export const GUA_DIRECTIONS: { [key: number]: { lucky: string[], unlucky: string[] } } = {
  1: { lucky: ['SE', 'E', 'S', 'N'], unlucky: ['NW', 'W', 'SW', 'NE'] },
  2: { lucky: ['NE', 'W', 'NW', 'SW'], unlucky: ['SE', 'E', 'S', 'N'] },
  3: { lucky: ['S', 'E', 'SE', 'N'], unlucky: ['NW', 'W', 'SW', 'NE'] },
  4: { lucky: ['SE', 'E', 'S', 'N'], unlucky: ['NW', 'W', 'SW', 'NE'] },
  6: { lucky: ['W', 'NE', 'SW', 'NW'], unlucky: ['SE', 'E', 'N', 'S'] },
  7: { lucky: ['NW', 'W', 'NE', 'SW'], unlucky: ['SE', 'E', 'S', 'N'] },
  8: { lucky: ['W', 'NE', 'SW', 'NW'], unlucky: ['SE', 'E', 'S', 'N'] },
  9: { lucky: ['S', 'E', 'SE', 'N'], unlucky: ['NW', 'W', 'SW', 'NE'] }
};

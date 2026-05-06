// src/types.ts
export type ElementType = 'WOOD' | 'FIRE' | 'EARTH' | 'METAL' | 'WATER';
export type GenderType = 'male' | 'female';

export interface DateMapping {
  HYear: number;
  EYear: number;
  HMonth: number;
  EMonth: number;
  HDay: number;
  EDay: number;
}

export interface DateMappings {
  [year: string]: {
    [month: string]: {
      [day: string]: DateMapping;
    };
  };
}

export interface ElementRelationships {
  [key: string]: {
    [key: string]: string;
  };
}

export interface Pillar {
  chinese: string;
  element: string;
  animal: string;
  branch: {
    element: string;
  };
}

export interface Pillars {
  year: Pillar;
  month: Pillar;
  day: Pillar;
  time: Pillar;
}

export interface FiveFactors {
  WOOD: number;
  FIRE: number;
  EARTH: number;
  METAL: number;
  WATER: number;
}

export interface EightMansions {
  group: 'West' | 'East';
  lucky: {
    wealth: string;
    health: string;
    romance: string;
    career: string;
  };
  unlucky: {
    obstacles: string;
    quarrels: string;
    setbacks: string;
    totalLoss: string;
  };
}


export interface DayMasterAnalysis {
  stem: string;
  nature: 'Yang' | 'Yin';
  element: ElementType;
}

export interface BasicAnalysis {
  lifeGua: number;
  dayMaster: DayMasterAnalysis;
  nobleman: string[];
  intelligence: string;
  skyHorse: string;
  peachBlossom: string;
  fiveFactors: FiveFactors;
  eightMansions: EightMansions;
}

export interface CompleteAnalysis {
  mainPillars: Pillars;
  basicAnalysis: BasicAnalysis;
}

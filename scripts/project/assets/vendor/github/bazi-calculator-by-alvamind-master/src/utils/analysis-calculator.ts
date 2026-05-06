// src/utils/analysis-calculator.ts
import {
  ELEMENTS,
  ELEMENT_RELATIONSHIPS,
  RELATIONSHIP_WEIGHTS,
  HIDDEN_STEMS,
  NOBLEMAN_MAP,
  INTELLIGENCE_MAP,
  PEACH_BLOSSOM_MAP,
  GUA_DIRECTIONS,
  STEMS,
  BRANCHES
} from '../constants';
import type { ElementType, Pillars, FiveFactors, EightMansions, DayMasterAnalysis } from '../types';
import type { Pillar } from '../types';


export class AnalysisCalculator {
  constructor() { }

  private getElementFromStem(stem: string): ElementType {
    return Object.entries(ELEMENTS)
      .find(([_, stems]) => stems.includes(stem))?.[0] as ElementType || '' as ElementType;
  }

  private getHiddenStems(branch: string): string[] {
    return HIDDEN_STEMS[branch] || [];
  }

  public calculateFiveFactors(pillars: Pillars): FiveFactors {
    const dayMasterElement = this.getElementFromStem(pillars.day.chinese[0]);

    // Collect all elements including hidden stems
    const elements = [
      pillars.year.chinese[0],  // Year stem
      pillars.month.chinese[0], // Month stem
      pillars.day.chinese[0],   // Day stem
      pillars.time.chinese[0],  // Hour stem
      ...this.getHiddenStems(pillars.year.chinese[1]),
      ...this.getHiddenStems(pillars.month.chinese[1]),
      ...this.getHiddenStems(pillars.day.chinese[1]),
      ...this.getHiddenStems(pillars.time.chinese[1])
    ].map(stem => this.getElementFromStem(stem));

    const weights: { [key: string]: number } = {
      WOOD: 0, FIRE: 0, EARTH: 0, METAL: 0, WATER: 0
    };

    elements.forEach(element => {
      const relationship = ELEMENT_RELATIONSHIPS[dayMasterElement][element];
      weights[element] += RELATIONSHIP_WEIGHTS[relationship];
    });

    const total = Object.values(weights).reduce((a, b) => a + b, 0);

    return {
      WOOD: Math.round((weights.WOOD * 100) / total),
      FIRE: Math.round((weights.FIRE * 100) / total),
      EARTH: Math.round((weights.EARTH * 100) / total),
      METAL: Math.round((weights.METAL * 100) / total),
      WATER: Math.round((weights.WATER * 100) / total)
    };
  }

  public calculateLifeGua(year: number, gender: 'male' | 'female'): number {
    const yearSum = year.toString().split('').reduce((acc, d) => acc + parseInt(d), 0);
    let gua = (11 - (yearSum % 9)) || 9;
    if (gender === 'female') {
      gua = (yearSum % 9 || 9) + 4;
      if (gua > 9) gua -= 9;
    }
    return gua;
  }

  private isWestGroup(gua: number): boolean {
    return [2, 6, 7, 8].includes(gua);
  }

  public calculateEightMansions(lifeGua: number): EightMansions {
    const directions = this.getDirectionsForGua(lifeGua);
    return {
      group: this.isWestGroup(lifeGua) ? 'West' : 'East',
      lucky: {
        wealth: directions.lucky[0],
        health: directions.lucky[1],
        romance: directions.lucky[2],
        career: directions.lucky[3]
      },
      unlucky: {
        obstacles: directions.unlucky[0],
        quarrels: directions.unlucky[1],
        setbacks: directions.unlucky[2],
        totalLoss: directions.unlucky[3]
      }
    };
  }

  private getDirectionsForGua(gua: number): { lucky: string[], unlucky: string[] } {
    return GUA_DIRECTIONS[gua] || GUA_DIRECTIONS[1];
  }

  public calculateNobleman(dayMasterElement: ElementType, dayMasterStem: string): string[] {
    const isYang = STEMS.indexOf(dayMasterStem) % 2 === 0;
    const positions = NOBLEMAN_MAP[dayMasterElement];
    return isYang ? positions : positions.reverse();
  }

  public calculateIntelligence(dayMasterElement: ElementType): string {
    return INTELLIGENCE_MAP[dayMasterElement];
  }

  public calculatePeachBlossom(dayMasterElement: ElementType): string {
    return PEACH_BLOSSOM_MAP[dayMasterElement];
  }

  public getStemNature(stem: string): 'Yang' | 'Yin' {
    return STEMS.indexOf(stem) % 2 === 0 ? 'Yang' : 'Yin';
  }

  public getSkyHorse(dayBranch: string): string {
    const oppositeIndex = (BRANCHES.indexOf(dayBranch) + 6) % 12;
    return BRANCHES[oppositeIndex];
  }

  public calculateDayMaster(dayPillar: Pillar): DayMasterAnalysis {
    const dayMasterStem = dayPillar.chinese[0];
    const dayMasterElement = this.getElementFromStem(dayMasterStem);
    return {
      stem: dayMasterStem,
      nature: this.getStemNature(dayMasterStem),
      element: dayMasterElement,
    };
  }
}

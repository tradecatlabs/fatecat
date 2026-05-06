// src/utils/pillar-calculator.ts
import { DateMappingLoader } from './date-mapping';
import {
  STEMS,
  BRANCHES,
  ANIMALS,
  ELEMENTS,
  BRANCH_ELEMENTS,
  HOUR_MAP
} from '../constants';
import type { Pillar } from '../types';

export class PillarCalculator {
  constructor(
    private dateMappingLoader: DateMappingLoader
  ) { }

  private getHourBranch(hour: number): string {
    const branch = HOUR_MAP.find(([start, end]) =>
      (hour >= start && hour < end) ||
      (start === 23 && (hour >= 23 || hour < 1))
    );
    return branch ? branch[2] : '子';
  }

  private calculateHourStem(dayStem: string, branch: string): string {
    const stemOffset = (STEMS.indexOf(dayStem) * 2) % 10;
    const branchIndex = BRANCHES.indexOf(branch);
    return STEMS[(stemOffset + branchIndex) % 10];
  }

  public calculateHourPillar(year: number, month: number, day: number, hour: number): string {
    const hourBranch = this.getHourBranch(hour);
    const dayMapping = this.dateMappingLoader.getMapping(year, month, day);
    const dayStem = STEMS[dayMapping.HDay - 1];
    const hourStem = this.calculateHourStem(dayStem, hourBranch);
    return hourStem + hourBranch;
  }

  public calculatePillars(year: number, month: number, day: number, hour: number): { year: Pillar, month: Pillar, day: Pillar, time: Pillar } {
    const mapping = this.dateMappingLoader.getMapping(year, month, day);

    const yearPillar = STEMS[mapping.HYear - 1] + BRANCHES[mapping.EYear - 1];
    const monthPillar = STEMS[mapping.HMonth - 1] + BRANCHES[mapping.EMonth - 1];
    const dayPillar = STEMS[mapping.HDay - 1] + BRANCHES[mapping.EDay - 1];
    const timePillar = this.calculateHourPillar(year, month, day, hour);

    return {
      year: this.translatePillar(yearPillar),
      month: this.translatePillar(monthPillar),
      day: this.translatePillar(dayPillar),
      time: this.translatePillar(timePillar),
    };
  }

  private translatePillar(pillar: string): Pillar {
    const [stem, branch] = pillar.split('');

    const element = Object.entries(ELEMENTS)
      .find(([_, stems]) => stems.includes(stem))?.[0] || '';

    const animal = ANIMALS[BRANCHES.indexOf(branch)];

    return {
      chinese: pillar,
      element,
      animal,
      branch: {
        element: Object.entries(BRANCH_ELEMENTS)
          .find(([_, branches]) => branches.includes(branch))?.[0] || '',
      },
    };
  }
}

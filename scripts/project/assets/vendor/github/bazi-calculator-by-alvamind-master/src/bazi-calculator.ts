// src/bazi-calculator.ts
import { DateMappingLoader } from './utils/date-mapping';
import { PillarCalculator } from './utils/pillar-calculator';
import { AnalysisCalculator } from './utils/analysis-calculator';
import type { GenderType, CompleteAnalysis, BasicAnalysis, Pillars } from './types';

export class BaziCalculator {
  private pillarCalculator: PillarCalculator;
  private analysisCalculator: AnalysisCalculator;

  constructor(
    private year: number,
    private month: number,
    private day: number,
    private hour: number,
    private gender: GenderType = 'male',
  ) {
    const dateMappingLoader = new DateMappingLoader();
    this.pillarCalculator = new PillarCalculator(dateMappingLoader);
    this.analysisCalculator = new AnalysisCalculator();
  }

  public calculatePillars(): Pillars {
    return this.pillarCalculator.calculatePillars(this.year, this.month, this.day, this.hour);
  }

  public calculateBasicAnalysis(): BasicAnalysis {
    const pillars = this.calculatePillars();
    const lifeGua = this.analysisCalculator.calculateLifeGua(this.year, this.gender);
    const dayMaster = this.analysisCalculator.calculateDayMaster(pillars.day);
    return {
      lifeGua,
      dayMaster,
      nobleman: this.analysisCalculator.calculateNobleman(dayMaster.element, dayMaster.stem),
      intelligence: this.analysisCalculator.calculateIntelligence(dayMaster.element),
      skyHorse: this.analysisCalculator.getSkyHorse(pillars.day.chinese[1]),
      peachBlossom: this.analysisCalculator.calculatePeachBlossom(dayMaster.element),
      fiveFactors: this.analysisCalculator.calculateFiveFactors(pillars),
      eightMansions: this.analysisCalculator.calculateEightMansions(lifeGua),
    };
  }


  public getCompleteAnalysis(): CompleteAnalysis {
    return {
      mainPillars: this.calculatePillars(),
      basicAnalysis: this.calculateBasicAnalysis(),
    };
  }

  public toString(): string {
    const pillars = this.calculatePillars();
    return `${pillars.year.chinese}年${pillars.month.chinese}月${pillars.day.chinese}日${pillars.time.chinese}時`;
  }
}

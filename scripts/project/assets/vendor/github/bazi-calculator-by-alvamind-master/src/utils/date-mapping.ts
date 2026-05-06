// src/utils/date-mapping.ts
import { readFileSync } from 'fs';
import path from 'path';
import type { DateMappings } from '../types';

export class DateMappingLoader {
  private dateMappings: DateMappings;

  constructor(private mappingsPath: string = path.join(__dirname, '../dates_mapping.json')) {
    this.dateMappings = this.loadDateMappings();
  }

  private loadDateMappings(): DateMappings {
    try {
      return JSON.parse(readFileSync(this.mappingsPath, 'utf-8'));
    } catch (error) {
      console.error("Failed to load date mappings:", error);
      throw error;
    }
  }

  public getMapping(year: number, month: number, day: number) {
    if (!this.dateMappings[year] || !this.dateMappings[year][month] || !this.dateMappings[year][month][day]) {
      throw new Error(`No date mapping found for ${year}-${month}-${day}`);
    }
    return this.dateMappings[year][month][day];
  }
}

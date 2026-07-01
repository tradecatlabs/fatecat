export interface Person {
  name: string;
  gender: 'male' | 'female' | '';
  year: string | number;
  month: string | number;
  day: string | number;
  timeIndex: number;
  isLunar?: boolean;
  isLeapMonth?: boolean;
  useTrueSolarTime?: boolean;
  birthHour?: number;
  birthMinute?: number;
  birthPlace?: string;
  birthLongitude?: number;
  age?: number;
}

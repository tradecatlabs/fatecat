export interface ChineseWorkday{
  isWorkday(day: string | Date): boolean;
  isHoliday(day: string | Date): boolean;
  getFestival(day: string | Date): string;
}

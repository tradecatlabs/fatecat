import type { BaziChartResult } from '../baziTypes';

export function branchesContain(
  pillars: BaziChartResult['pillars'],
  requiredBranches: string[],
  requireAll: boolean = true,
): boolean {
  const allBranches = [pillars.year.zhi, pillars.month.zhi, pillars.day.zhi, pillars.hour.zhi];
  if (requireAll) {
    return requiredBranches.every((b) => allBranches.includes(b));
  }
  return requiredBranches.some((b) => allBranches.includes(b));
}

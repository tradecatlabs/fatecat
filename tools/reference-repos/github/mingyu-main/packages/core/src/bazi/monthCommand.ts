
import type { MonthQiElementItem, MonthQiProfile } from '../types/analysis';

export function analyzeMonthQiProfile(
  monthBranch: string,
  commanderStem?: string,
): MonthQiProfile {
  const elemMap: Record<string, string> = { 寅:'木',卯:'木',辰:'土',巳:'火',午:'火',未:'土',申:'金',酉:'金',戌:'土',亥:'水',子:'水',丑:'土' };
  const seasonElements = ['木','火','土','金','水'];
  const monthElement = elemMap[monthBranch] || '土';

  const items: MonthQiElementItem[] = seasonElements.map((elem) => {
    let seasonStatus = '平';
    if (elem === monthElement) seasonStatus = '旺';
    else if ((monthElement === '木' && elem === '火') || (monthElement === '火' && elem === '土') ||
             (monthElement === '土' && elem === '金') || (monthElement === '金' && elem === '水') ||
             (monthElement === '水' && elem === '木')) seasonStatus = '相';
    else if ((elem === '木' && monthElement === '火') || (elem === '火' && monthElement === '土') ||
             (elem === '土' && monthElement === '金') || (elem === '金' && monthElement === '水') ||
             (elem === '水' && monthElement === '木')) seasonStatus = '休';
    else if ((monthElement === '木' && elem === '金') || (monthElement === '火' && elem === '水') ||
             (monthElement === '土' && elem === '木') || (monthElement === '金' && elem === '火') ||
             (monthElement === '水' && elem === '土')) seasonStatus = '囚';
    else seasonStatus = '死';
    return { element: elem, seasonStatus, score: 0, percent: 0, count: 0, summary: elem + '于' + monthBranch + '月' + seasonStatus };
  });

  return { commanderStem: commanderStem || '', leadingElements: [monthElement], items, summary: monthBranch + '月令分析' };
}

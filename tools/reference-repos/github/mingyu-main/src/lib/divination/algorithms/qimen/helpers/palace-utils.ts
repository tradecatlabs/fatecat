export function getDunJiaStem(hourGanZhi: string): string {
  if (!hourGanZhi.startsWith('甲')) {
    return hourGanZhi.charAt(0);
  }

  const dunJiaMap: Record<string, string> = {
    甲子: '戊',
    甲戌: '己',
    甲申: '庚',
    甲午: '辛',
    甲辰: '壬',
    甲寅: '癸',
  };

  return dunJiaMap[hourGanZhi] || '戊';
}

export function getOppositePalace(palace: number): number | null {
  const oppositeMap: Record<number, number> = {
    1: 9,
    2: 8,
    3: 7,
    4: 6,
    6: 4,
    7: 3,
    8: 2,
    9: 1,
  };

  return oppositeMap[palace] || null;
}

export function getDoorElement(door: string): string {
  const doorElementMap: Record<string, string> = {
    休门: '水',
    生门: '土',
    伤门: '木',
    杜门: '木',
    景门: '火',
    死门: '土',
    惊门: '金',
    开门: '金',
  };

  return doorElementMap[door] || '';
}

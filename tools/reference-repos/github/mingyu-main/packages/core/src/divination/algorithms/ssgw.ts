import type { SsgwData } from '../../types/divination';
import { SSGW_SIGNS } from '../../divination/ssgw-data';
import { getDivinationTime } from '../../calendar/timeManager';

const ssgwSigns: Omit<SsgwData, 'ganzhi' | 'timestamp'>[] = SSGW_SIGNS.map((sign) => ({
  number: sign.id,
  title: sign.title,
  poem: sign.qianwen,
  story: sign.story,
  details: sign.details,
}));

/**
 * 随机求签 - 模拟真实的求签过程
 */
export function drawRandomSign(): SsgwData {
  const { ganzhi, timestamp } = getDivinationTime();
  const randomIndex = Math.floor(Math.random() * ssgwSigns.length);
  const sign = ssgwSigns[randomIndex];
  return {
    ...sign,
    timestamp,
    ganzhi,
  };
}

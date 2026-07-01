// 三山国王灵签数据 - 与原项目完全一致

import type { SsgwSign } from './types';
import { SIGNS_01 } from './signs-01';
import { SIGNS_02 } from './signs-02';
import { SIGNS_03 } from './signs-03';

export type { SsgwSign };

// 三山国王灵签数据（共61签）
export const SSGW_SIGNS: SsgwSign[] = [...SIGNS_01, ...SIGNS_02, ...SIGNS_03];

// 获取随机签文
function getRandomSign(): SsgwSign {
  const randomIndex = Math.floor(Math.random() * SSGW_SIGNS.length);
  return SSGW_SIGNS[randomIndex];
}

// 根据ID获取签文
function getSignById(id: number): SsgwSign | undefined {
  return SSGW_SIGNS.find((sign) => sign.id === id);
}

// 模拟投掷圣杯 - 按照原项目逻辑：两个杯子的正反面组合
function throwHolyGrail(): {
  result: '圣杯' | '笑杯' | '阴杯';
  bei1: 'ping' | 'tu';
  bei2: 'ping' | 'tu';
} {
  // 生成两个杯子的正反面 (ping: 正面, tu: 反面)
  const bei1 = Math.random() > 0.5 ? 'ping' : 'tu';
  const bei2 = Math.random() > 0.5 ? 'ping' : 'tu';

  let result: '圣杯' | '笑杯' | '阴杯';

  if (bei1 !== bei2) {
    // 一平一凸 = 圣杯
    result = '圣杯';
  } else if (bei1 === 'ping') {
    // 两平 = 笑杯
    result = '笑杯';
  } else {
    // 两凸 = 阴杯
    result = '阴杯';
  }

  return { result, bei1, bei2 };
}

// 导出到全局作用域
if (typeof window !== 'undefined') {
  const globalWindow = window as unknown as {
    SSGW_SIGNS?: typeof SSGW_SIGNS;
    getRandomSign?: typeof getRandomSign;
    getSignById?: typeof getSignById;
    throwHolyGrail?: typeof throwHolyGrail;
  };
  globalWindow.SSGW_SIGNS = SSGW_SIGNS;
  globalWindow.getRandomSign = getRandomSign;
  globalWindow.getSignById = getSignById;
  globalWindow.throwHolyGrail = throwHolyGrail;
}

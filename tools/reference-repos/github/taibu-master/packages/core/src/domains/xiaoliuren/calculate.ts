/**
 * 小六壬排盘核心引擎
 *
 * 六种状态按固定顺序循环：大安→留连→速喜→赤口→小吉→空亡
 * 1. 月上起大安，顺数到所占农历月
 * 2. 从月上落位起，顺数到所占农历日
 * 3. 从日上落位起，顺数到所占时辰
 */

import type {
  XiaoliurenInput,
  XiaoliurenOutput,
  XiaoliurenStatus,
  XiaoliurenStatusInfo,
} from './types.js';

export type { XiaoliurenInput, XiaoliurenOutput, XiaoliurenStatus, XiaoliurenStatusInfo } from './types.js';

// 六种状态固定顺序
const STATUS_ORDER: XiaoliurenStatus[] = ['大安', '留连', '速喜', '赤口', '小吉', '空亡'];

// 十二时辰名称（子=1, 丑=2, ..., 亥=12）
const SHICHEN_NAMES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];

// 各状态详细信息
const STATUS_INFO: Record<XiaoliurenStatus, Omit<XiaoliurenStatusInfo, 'name'>> = {
  '大安': {
    element: '木',
    direction: '东方',
    nature: '吉',
    description: '身不动时，五行属木，颜色青色，方位东方。临青龙，凡谋事主一、五、七。有静止、心安之意。',
    poem: '大安事事昌，求谋在东方。失物去不远，宅舍保安康。行人身未动，病者主无妨。将军回田野，仔细更推详。',
  },
  '留连': {
    element: '水',
    direction: '北方',
    nature: '凶',
    description: '卒未归时，五行属水，颜色黑色，方位北方。临玄武，凡谋事主二、八、十。有暗昧不明、延迟之意。',
    poem: '留连事难成，求谋日未明。官事凡宜缓，去者未回程。失物南方见，急讨方心称。更须防口舌，人口且平平。',
  },
  '速喜': {
    element: '火',
    direction: '南方',
    nature: '吉',
    description: '人便至时，五行属火，颜色红色，方位南方。临朱雀，凡谋事主三、六、九。有快速、喜庆之意。',
    poem: '速喜喜来临，求财向南行。失物申未午，逢人路上寻。官事有福德，病者无祸侵。田宅六畜吉，行人有信音。',
  },
  '赤口': {
    element: '金',
    direction: '西方',
    nature: '凶',
    description: '官事凶时，五行属金，颜色白色，方位西方。临白虎，凡谋事主四、七、十。有不吉、惊恐之意。',
    poem: '赤口主口舌，官非切宜防。失物速速讨，行人有惊慌。六畜多作怪，病者出西方。更须防咒诅，诚恐染瘟殃。',
  },
  '小吉': {
    element: '水',
    direction: '北方',
    nature: '吉',
    description: '人来喜时，五行属水，颜色黑色，方位北方（一说南方）。临六合，凡谋事主一、五、七。有和合、吉利之意。',
    poem: '小吉最吉昌，路上好商量。阴人来报喜，失物在坤方。行人立便至，交关甚是强。凡事皆和合，病者叩穹苍。',
  },
  '空亡': {
    element: '土',
    direction: '中央',
    nature: '凶',
    description: '音信稀时，五行属土，颜色黄色，方位中央。临勾陈，凡谋事主三、六、九。有无结果、虚耗之意。',
    poem: '空亡事不祥，阴人多乖张。求财无利益，行人有灾殃。失物寻不见，官事有刑伤。病人逢暗鬼，解禳保安康。',
  },
};

/**
 * 将小时数（0-23）转换为时辰序号（1-12）
 */
function hourToShichen(hour: number): number {
  if (hour >= 23 || hour < 1) return 1;  // 子时
  return Math.floor((hour + 1) / 2) + 1;
}

/**
 * 小六壬排盘主函数
 */
export function calculateXiaoliurenData(input: XiaoliurenInput): XiaoliurenOutput {
  const { lunarMonth, lunarDay, question } = input;
  let { hour } = input;

  // 如果传入的是 24 小时制（0 或 13-23），转为时辰序号（1-12）
  // 1-12 视为时辰序号直接使用
  if (hour === 0 || hour > 12) {
    hour = hourToShichen(hour);
  }
  // 确保时辰在 1-12 范围
  if (hour < 1 || hour > 12) {
    hour = ((hour - 1) % 12 + 12) % 12 + 1;
  }

  // 1. 月上起大安：从大安开始数到第 lunarMonth 个位置
  const monthIdx = (lunarMonth - 1) % 6;
  const monthStatus = STATUS_ORDER[monthIdx];

  // 2. 从月上落位起，顺数到农历日
  const dayIdx = (monthIdx + lunarDay - 1) % 6;
  const dayStatus = STATUS_ORDER[dayIdx];

  // 3. 从日上落位起，顺数到时辰
  const hourIdx = (dayIdx + hour - 1) % 6;
  const hourStatus = STATUS_ORDER[hourIdx];

  // 最终结果
  const info = STATUS_INFO[hourStatus];
  const result: XiaoliurenStatusInfo = { name: hourStatus, ...info };

  const shichenIdx = hour - 1;
  const shichen = SHICHEN_NAMES[shichenIdx] || SHICHEN_NAMES[0];

  return {
    monthStatus,
    dayStatus,
    hourStatus,
    result,
    input: {
      lunarMonth,
      lunarDay,
      hour,
      shichen: `${shichen}时`,
    },
    question,
  };
}

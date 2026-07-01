import test from 'node:test';
import assert from 'node:assert/strict';

import {
  toAlmanacText,
  toBaziPillarsResolveText,
  toBaziText,
  toDaliurenText,
  toLiuyaoCanonicalText,
  toQimenText,
  toZiweiFlyingStarText,
  toZiweiHoroscopeText,
  toZiweiText,
  type DaliurenOutput,
} from 'taibu-core';
import { calculateBaziChartBundle, generateBaziChartText } from '@/lib/divination/bazi';
import { calculateZiweiChartBundle, generateZiweiChartText } from '@/lib/divination/ziwei';

const renderToolText = (
  toolName: string,
  result: unknown,
  options?: Record<string, unknown>,
) => {
  switch (toolName) {
    case 'bazi_pillars_resolve':
      return toBaziPillarsResolveText(result as never);
    case 'ziwei_horoscope':
      return toZiweiHoroscopeText(result as never, options as never);
    case 'ziwei_flying_star':
      return toZiweiFlyingStarText(result as never);
    case 'bazi':
      return toBaziText(result as never, options as never);
    case 'ziwei':
      return toZiweiText(result as never, options as never);
    case 'qimen':
      return toQimenText(result as never, options as never);
    case 'daliuren':
      return toDaliurenText(result as never, options as never);
    case 'almanac':
      return toAlmanacText(result as never, options as never);
    default:
      throw new Error(`Unsupported tool in test renderer: ${toolName}`);
  }
};

const renderToolDebugText = (toolName: string, result: unknown) =>
  toolName === 'liuyao'
    ? toLiuyaoCanonicalText(result as never)
    : '';

test('specialized core canonical text renderers should cover non-mainline tools', () => {
  const pillarsText = renderToolText('bazi_pillars_resolve', {
    pillars: {
      yearPillar: '甲子',
      monthPillar: '乙丑',
      dayPillar: '丙寅',
      hourPillar: '丁卯',
    },
    count: 1,
    candidates: [{
      candidateId: 'cand-1',
      lunarText: '农历1990年正月初一',
      solarText: '1990-01-27',
      birthYear: 1990,
      birthMonth: 1,
      birthDay: 1,
      birthHour: 5,
      birthMinute: 30,
      isLeapMonth: false,
      nextCall: {
        tool: 'bazi',
        arguments: {
          birthYear: 1990,
          birthMonth: 1,
          birthDay: 1,
          birthHour: 5,
          birthMinute: 30,
          calendarType: 'lunar',
          isLeapMonth: false,
        },
        missing: ['gender'],
      },
    }],
  });
  assert.match(pillarsText, /四柱反推候选时间/u);
  assert.match(pillarsText, /候选 1/u);

  const horoscopeText = renderToolText('ziwei_horoscope', {
    solarDate: '1990-01-01',
    lunarDate: '1989-12-05',
    soul: '廉贞',
    body: '天相',
    fiveElement: '金四局',
    targetDate: '2026-03-22',
    hasExplicitTargetTime: false,
    decadal: { index: 0, name: '命宫', heavenlyStem: '甲', earthlyBranch: '子', mutagen: ['廉贞', '破军', '武曲', '太阳'], palaceNames: ['命宫'], startAge: 31, endAge: 40 },
    age: { index: 1, name: '兄弟', heavenlyStem: '乙', earthlyBranch: '丑', mutagen: [], palaceNames: ['兄弟'], nominalAge: 37 },
    yearly: { index: 2, name: '夫妻', heavenlyStem: '丙', earthlyBranch: '寅', mutagen: ['权'], palaceNames: ['夫妻'] },
    monthly: { index: 3, name: '子女', heavenlyStem: '丁', earthlyBranch: '卯', mutagen: [], palaceNames: ['子女'] },
    daily: { index: 4, name: '财帛', heavenlyStem: '戊', earthlyBranch: '辰', mutagen: [], palaceNames: ['财帛'] },
    hourly: { index: 5, name: '疾厄', heavenlyStem: '己', earthlyBranch: '巳', mutagen: [], palaceNames: ['疾厄'] },
    transitStars: [{ starName: '流昌', palaceName: '命宫' }, { starName: '流禄', palaceName: '财帛' }],
    yearlyDecStar: { suiqian12: ['岁建'], jiangqian12: ['将星'] },
  });
  const horoscopeFullText = renderToolText('ziwei_horoscope', {
    solarDate: '1990-01-01',
    lunarDate: '1989-12-05',
    soul: '廉贞',
    body: '天相',
    fiveElement: '金四局',
    targetDate: '2026-03-22',
    hasExplicitTargetTime: true,
    decadal: { index: 0, name: '命宫', heavenlyStem: '甲', earthlyBranch: '子', mutagen: ['廉贞', '破军', '武曲', '太阳'], palaceNames: ['命宫'], startAge: 31, endAge: 40 },
    age: { index: 1, name: '兄弟', heavenlyStem: '乙', earthlyBranch: '丑', mutagen: [], palaceNames: ['兄弟'], nominalAge: 37 },
    yearly: { index: 2, name: '夫妻', heavenlyStem: '丙', earthlyBranch: '寅', mutagen: ['权'], palaceNames: ['夫妻'] },
    monthly: { index: 3, name: '子女', heavenlyStem: '丁', earthlyBranch: '卯', mutagen: [], palaceNames: ['子女'] },
    daily: { index: 4, name: '财帛', heavenlyStem: '戊', earthlyBranch: '辰', mutagen: [], palaceNames: ['财帛'] },
    hourly: { index: 5, name: '疾厄', heavenlyStem: '己', earthlyBranch: '巳', mutagen: [], palaceNames: ['疾厄'] },
    transitStars: [{ starName: '流昌', palaceName: '命宫' }, { starName: '流禄', palaceName: '财帛' }],
    yearlyDecStar: { suiqian12: ['岁建'], jiangqian12: ['将星'] },
  }, { detailLevel: 'full' });
  assert.match(horoscopeText, /紫微运限/u);
  assert.match(horoscopeText, /## 运限叠宫与四化/u);
  assert.match(horoscopeText, /目标日期/u);
  assert.match(horoscopeText, /流年星曜/u);
  assert.doesNotMatch(horoscopeText, /岁前十二星/u);
  assert.doesNotMatch(horoscopeText, /流时/u);
  assert.match(horoscopeFullText, /流时/u);
  assert.match(horoscopeFullText, /岁前十二星|将前十二星/u);

  const flyingStarText = renderToolText('ziwei_flying_star', {
    results: [
      {
        queryIndex: 0,
        type: 'fliesTo',
        result: true,
        queryTarget: { fromPalace: '命宫', toPalace: '财帛宫', mutagens: ['禄'] },
        actualFlights: [{ mutagen: '禄', targetPalace: '夫妻宫', starName: '天同' }],
      },
      {
        queryIndex: 1,
        type: 'mutagedPlaces',
        result: [{ mutagen: '禄', targetPalace: '财帛' }],
        queryTarget: { palace: '命宫' },
        sourcePalaceGanZhi: '丙辰',
        actualFlights: [{ mutagen: '禄', targetPalace: '财帛宫', starName: '天同' }],
      },
    ],
  });
  assert.match(flyingStarText, /紫微飞星/u);
  assert.match(flyingStarText, /实际落点|本宫干支|化禄|结果|查询类型/u);
});

test('core and web bazi text should surface full true-solar metadata details', () => {
  const trueSolarTimeInfo = {
    clockTime: '23:40',
    trueSolarTime: '23:29',
    longitude: 73,
    correctionMinutes: -11,
    trueTimeIndex: 12,
    dayOffset: -1,
  };

  const markdown = renderToolText('bazi', {
    gender: 'male',
    birthPlace: '新疆',
    dayMaster: '甲',
    kongWang: { xun: '甲子', kongZhi: ['戌', '亥'] },
    fourPillars: {
      year: { stem: '甲', branch: '子', tenGod: '比肩', hiddenStems: [], naYin: '海中金', diShi: '沐浴', shenSha: [], kongWang: { isKong: false } },
      month: { stem: '乙', branch: '丑', tenGod: '劫财', hiddenStems: [], naYin: '海中金', diShi: '冠带', shenSha: [], kongWang: { isKong: false } },
      day: { stem: '甲', branch: '寅', hiddenStems: [], naYin: '大溪水', diShi: '临官', shenSha: [], kongWang: { isKong: false } },
      hour: { stem: '丙', branch: '子', tenGod: '食神', hiddenStems: [], naYin: '涧下水', diShi: '沐浴', shenSha: [], kongWang: { isKong: false } },
    },
    relations: [],
    tianGanWuHe: [],
    tianGanChongKe: [],
    diZhiBanHe: [],
    diZhiSanHui: [],
    trueSolarTimeInfo,
  });

  assert.match(markdown, /时辰索引|真太阳时索引/u, 'mcp bazi markdown should expose trueTimeIndex');
  assert.match(markdown, /跨日/u, 'mcp bazi markdown should expose dayOffset');

  const { output: chart } = calculateBaziChartBundle({
    name: '测试',
    gender: 'male',
    birthYear: 1990,
    birthMonth: 1,
    birthDay: 1,
    birthHour: 12,
    birthMinute: 0,
    calendarType: 'solar',
  });
  chart.trueSolarTimeInfo = trueSolarTimeInfo;

  const text = generateBaziChartText(chart);
  assert.match(text, /时辰索引|真太阳时索引/u, 'web bazi copy text should expose trueTimeIndex');
  assert.match(text, /跨日/u, 'web bazi copy text should expose dayOffset');
});

test('ziwei full text should keep full age arrays instead of truncating them while default stays compact', () => {
  const markdown = renderToolText('ziwei', {
    solarDate: '1990-1-1',
    lunarDate: '1989-12-5',
    fourPillars: {
      year: { gan: '己', zhi: '巳' },
      month: { gan: '丙', zhi: '子' },
      day: { gan: '甲', zhi: '子' },
      hour: { gan: '甲', zhi: '子' },
    },
    soul: '廉贞',
    body: '天相',
    fiveElement: '金四局',
    zodiac: '蛇',
    sign: '摩羯座',
    palaces: [{
      name: '命宫',
      heavenlyStem: '甲',
      earthlyBranch: '子',
      isBodyPalace: false,
      majorStars: [],
      minorStars: [],
      ages: [101, 102, 103, 104, 105, 106],
      liuNianAges: [201, 202, 203, 204, 205, 206],
      sanFangSiZheng: ['财帛', '官禄', '迁移'],
    }],
    decadalList: [],
    time: '子时',
    timeRange: '23:00-00:59',
    trueSolarTimeInfo: {
      clockTime: '23:40',
      trueSolarTime: '23:29',
      longitude: 73,
      correctionMinutes: -11,
      trueTimeIndex: 12,
      dayOffset: -1,
    },
    smallLimit: [{ palaceName: '命宫', ages: [301, 302, 303, 304, 305, 306] }],
  }, { detailLevel: 'full' });

  assert.match(markdown, /206/u, 'mcp ziwei markdown should keep full liuNian ages');
  assert.match(markdown, /106/u, 'mcp ziwei markdown should keep full smallLimit ages in dedicated column');
  assert.doesNotMatch(markdown, /\.\.\./u, 'mcp ziwei markdown should not use truncation markers');
  assert.match(markdown, /时辰索引|真太阳时索引/u, 'mcp ziwei markdown should expose trueTimeIndex');
  assert.match(markdown, /跨日/u, 'mcp ziwei markdown should expose dayOffset');

  const chart = calculateZiweiChartBundle({
    name: '测试',
    gender: 'male',
    birthYear: 1990,
    birthMonth: 1,
    birthDay: 1,
    birthHour: 12,
    birthMinute: 0,
    calendarType: 'solar',
  }).output;

  chart.trueSolarTimeInfo = {
    clockTime: '23:40',
    trueSolarTime: '23:29',
    longitude: 73,
    correctionMinutes: -11,
    trueTimeIndex: 12,
    dayOffset: -1,
  };
  chart.palaces[0].ages = [101, 102, 103, 104, 105, 106];
  chart.palaces[0].liuNianAges = [201, 202, 203, 204, 205, 206];
  chart.smallLimit = [{ palaceName: '命宫', ages: [301, 302, 303, 304, 305, 306] }];

  const defaultText = generateZiweiChartText(chart);
  assert.doesNotMatch(defaultText, /206/u, 'default web ziwei copy text should omit full liuNian age arrays');
  assert.doesNotMatch(defaultText, /106/u, 'default web ziwei copy text should omit full smallLimit age arrays');
  assert.doesNotMatch(defaultText, /时辰索引|真太阳时索引/u, 'default web ziwei copy text should keep true-solar detail compact');
  assert.doesNotMatch(defaultText, /跨日/u, 'default web ziwei copy text should keep true-solar detail compact');

  const text = generateZiweiChartText(chart, { detailLevel: 'full' });
  assert.match(text, /206/u, 'full web ziwei copy text should keep full liuNian ages');
  assert.match(text, /106/u, 'full web ziwei copy text should keep full smallLimit ages in dedicated column');
  assert.match(text, /时辰索引|真太阳时索引/u, 'full web ziwei copy text should expose trueTimeIndex');
  assert.match(text, /跨日/u, 'full web ziwei copy text should expose dayOffset');
});

test('qimen canonical text should keep default compact while full appends supplements', () => {
  const chart = {
    dateInfo: {
      solarDate: '2003-09-02',
      lunarDate: '二〇〇三年八月初六',
      solarTerm: '处暑',
      solarTermRange: '2003-08-23 21:09 ~ 2003-09-08 09:21',
    },
    siZhu: {
      year: '癸未',
      month: '庚申',
      day: '戊寅',
      hour: '丁巳',
    },
    dunType: 'yin' as const,
    juNumber: 7,
    yuan: '下元',
    xunShou: '甲寅',
    zhiFu: { star: '天芮星', palace: 1 },
    zhiShi: { gate: '死门', palace: 8 },
    palaces: [
      { palaceIndex: 1, palaceName: '坎', direction: '正北', element: '水', earthStem: '丁', heavenStem: '癸', star: '天芮星', starElement: '土', gate: '景门', gateElement: '火', deity: '值符', formations: ['腾蛇夭矫'], elementState: '相' },
      { palaceIndex: 2, palaceName: '坤', direction: '西南', element: '土', earthStem: '癸', heavenStem: '壬', star: '天冲星', starElement: '木', gate: '生门', gateElement: '土', deity: '六合', formations: [], elementState: '休', isYiMa: true },
      { palaceIndex: 3, palaceName: '震', direction: '正东', element: '木', earthStem: '壬', heavenStem: '己', star: '天心星', starElement: '金', gate: '惊门', gateElement: '金', deity: '九地', formations: [], elementState: '死' },
      { palaceIndex: 4, palaceName: '巽', direction: '东南', element: '木', earthStem: '辛', heavenStem: '丁', star: '天蓬星', starElement: '水', gate: '开门', gateElement: '金', deity: '玄武', formations: [], elementState: '死' },
      { palaceIndex: 5, palaceName: '中', direction: '中央', element: '土', earthStem: '庚', heavenStem: '', star: '', starElement: '', gate: '', gateElement: '', deity: '', formations: [], elementState: '休' },
      { palaceIndex: 6, palaceName: '乾', direction: '西北', element: '金', earthStem: '己', heavenStem: '丙', star: '天英星', starElement: '火', gate: '杜门', gateElement: '木', deity: '螣蛇', formations: [], elementState: '旺', isRuMu: true },
      { palaceIndex: 7, palaceName: '兑', direction: '正西', element: '金', earthStem: '戊', heavenStem: '辛', star: '天辅星', starElement: '木', gate: '伤门', gateElement: '木', deity: '太阴', formations: [], elementState: '旺' },
      { palaceIndex: 8, palaceName: '艮', direction: '东北', element: '土', earthStem: '乙', heavenStem: '戊', star: '天柱星', starElement: '金', gate: '死门', gateElement: '土', deity: '九天', formations: ['日出扶桑'], elementState: '休' },
      { palaceIndex: 9, palaceName: '离', direction: '正南', element: '火', earthStem: '丙', heavenStem: '乙', star: '天任星', starElement: '土', gate: '休门', gateElement: '水', deity: '白虎', formations: ['奇仪相佐'], elementState: '囚' },
    ],
    kongWang: {
      dayKong: { branches: ['戌', '亥'], palaces: [2, 7] },
      hourKong: { branches: ['子', '丑'], palaces: [1, 8] },
    },
    yiMa: { branch: '申', palace: 2 },
    globalFormations: ['坎宫: 腾蛇夭矫', '艮宫: 日出扶桑', '离宫: 奇仪相佐'],
    panType: '转盘',
    juMethod: '拆补法',
    monthPhase: { 甲: '死', 乙: '死', 丙: '囚', 丁: '囚', 戊: '休', 己: '休', 庚: '旺', 辛: '旺', 壬: '相', 癸: '相' },
  };

  const defaultText = renderToolText('qimen', chart);
  const fullText = renderToolText('qimen', chart, { detailLevel: 'full' });

  assert.match(defaultText, /值符 \(大局趋势\): 天芮星/u);
  assert.match(defaultText, /\| 宫位\(五行\) \| 八神 \| 九星\(五行\) \| 八门\(五行\) \| 天盘天干 \| 地盘天干 \| 宫位状态 \|/u);
  assert.doesNotMatch(defaultText, /## 补充信息/u);
  assert.match(fullText, /## 补充信息/u);
  assert.match(fullText, /## 全局格局/u);
  assert.match(fullText, /方位/u);
});

test('daliuren canonical text should keep default focused while full only appends deterministic details', () => {
  const chart: DaliurenOutput = {
    dateInfo: {
      solarDate: '2003年9月2日 10时20分',
      lunarDate: '二〇〇三年八月初六',
      bazi: '癸未 庚申 戊寅 丁巳',
      ganZhi: { year: '癸未', month: '庚申', day: '戊寅', hour: '丁巳' },
      yueJiang: '巳',
      yueJiangName: '太乙',
      xun: '甲子旬',
      kongWang: ['申', '酉'] as [string, string],
      yiMa: '申',
      dingMa: '丑',
      tianMa: '午',
      diurnal: true,
    },
    tianDiPan: { diPan: {}, tianPan: {}, tianJiang: {} },
    siKe: {
      yiKe: ['巳戊', '勾陈'],
      erKe: ['巳巳', '勾陈'],
      sanKe: ['寅寅', '腾蛇'],
      siKe: ['寅寅', '腾蛇'],
    },
    sanChuan: {
      chu: ['巳', '勾陈', '父母', '辛'],
      zhong: ['申', '白虎', '子孙', ''],
      mo: ['寅', '腾蛇', '官鬼', '戊'],
      method: '伏吟',
    },
    keTi: {
      method: '伏吟',
      subTypes: ['伏吟'],
      extraTypes: ['自任'],
    },
    keName: '戊寅日第七局',
    shenSha: [],
    gongInfos: [
      { diZhi: '子', tianZhi: '子', tianJiang: '天后', tianJiangShort: '后', dunGan: '丙', changSheng: '胎', wuXing: '水', wangShuai: '相', jianChu: '定' },
      { diZhi: '丑', tianZhi: '丑', tianJiang: '贵人', tianJiangShort: '贵', dunGan: '丁', changSheng: '养', wuXing: '土', wangShuai: '休', jianChu: '执' },
      { diZhi: '寅', tianZhi: '寅', tianJiang: '腾蛇', tianJiangShort: '蛇', dunGan: '戊', changSheng: '长生', wuXing: '木', wangShuai: '死', jianChu: '破' },
      { diZhi: '卯', tianZhi: '卯', tianJiang: '朱雀', tianJiangShort: '雀', dunGan: '己', changSheng: '沐浴', wuXing: '木', wangShuai: '死', jianChu: '危' },
      { diZhi: '辰', tianZhi: '辰', tianJiang: '六合', tianJiangShort: '合', dunGan: '庚', changSheng: '冠带', wuXing: '土', wangShuai: '休', jianChu: '成' },
      { diZhi: '巳', tianZhi: '巳', tianJiang: '勾陈', tianJiangShort: '勾', dunGan: '辛', changSheng: '临官', wuXing: '火', wangShuai: '囚', jianChu: '收' },
      { diZhi: '午', tianZhi: '午', tianJiang: '青龙', tianJiangShort: '龙', dunGan: '壬', changSheng: '帝旺', wuXing: '火', wangShuai: '囚', jianChu: '开' },
      { diZhi: '未', tianZhi: '未', tianJiang: '天空', tianJiangShort: '空', dunGan: '癸', changSheng: '衰', wuXing: '土', wangShuai: '休', jianChu: '闭' },
      { diZhi: '申', tianZhi: '申', tianJiang: '白虎', tianJiangShort: '虎', dunGan: '', changSheng: '病', wuXing: '金', wangShuai: '旺', jianChu: '建' },
      { diZhi: '酉', tianZhi: '酉', tianJiang: '太常', tianJiangShort: '常', dunGan: '', changSheng: '死', wuXing: '金', wangShuai: '旺', jianChu: '除' },
      { diZhi: '戌', tianZhi: '戌', tianJiang: '玄武', tianJiangShort: '玄', dunGan: '甲', changSheng: '墓', wuXing: '土', wangShuai: '休', jianChu: '满' },
      { diZhi: '亥', tianZhi: '亥', tianJiang: '太阴', tianJiangShort: '阴', dunGan: '乙', changSheng: '绝', wuXing: '水', wangShuai: '相', jianChu: '平' },
    ],
    dunGan: {},
    jianChu: {},
    benMing: '癸未',
    xingNian: '乙酉',
    question: '事业如何',
  };

  const defaultText = renderToolText('daliuren', chart);
  const fullText = renderToolText('daliuren', chart, { detailLevel: 'full' });

  assert.match(defaultText, /# 大六壬排盘/u);
  assert.match(defaultText, /## 基本信息/u);
  assert.match(defaultText, /关键状态: 空亡\(申, 酉\)/u);
  assert.match(defaultText, /## 天地盘全图 \(十二宫\)/u);
  assert.doesNotMatch(defaultText, /神煞/u);
  assert.doesNotMatch(defaultText, /建除/u);
  assert.match(fullText, /本命: 癸未/u);
  assert.match(fullText, /附加课体: 自任/u);
  assert.match(fullText, /\| 地盘 \(五行·状态\) \| 天盘 \(月将\) \| 天将 \| 遁干 \| 长生十二神 \| 建除 \|/u);
});

test('almanac canonical text should keep default compact while full appends calendrical details', () => {
  const text = renderToolText('almanac', {
    date: '2026-04-01',
    dayInfo: { stem: '乙', branch: '巳', ganZhi: '乙巳' },
    tenGod: '正官',
    almanac: {
      lunarDate: '二〇二六年二月十四',
      lunarMonth: '二月',
      lunarDay: '十四',
      zodiac: '马',
      solarTerm: '',
      suitable: ['纳财', '开市'],
      avoid: ['移徙', '入宅'],
      chongSha: '冲(己亥)猪 煞东',
      pengZuBaiJi: '乙不栽植千株不长 巳不远行财物伏藏',
      jishen: ['相日', '驿马'],
      xiongsha: ['五虚', '大煞'],
      directions: {
        caiShen: '东北',
        xiShen: '西北',
        fuShen: '西南',
        yangGui: '正北',
        yinGui: '西南',
      },
      dayOfficer: '定',
      tianShen: '司命',
      tianShenType: '黄道',
      tianShenLuck: '吉',
      lunarMansion: '毕月乌',
      lunarMansionLuck: '吉',
      lunarMansionSong: '毕星造作主光前',
      nayin: '佛灯火',
      dayNineStar: {
        number: 3,
        description: '三碧木 震(正东) 天玑',
        color: '碧',
        wuXing: '木',
        position: '正东',
      },
      taiShen: '碓磨床 房内东',
      hourlyFortune: [
        { ganZhi: '丙子', tianShen: '青龙', tianShenType: '黄道', tianShenLuck: '吉', chong: '冲马', sha: '煞南', suitable: ['祭祀'], avoid: ['出行'] },
      ],
    },
  });
  const fullText = renderToolText('almanac', {
    date: '2026-04-01',
    dayInfo: { stem: '乙', branch: '巳', ganZhi: '乙巳' },
    tenGod: '正官',
    almanac: {
      lunarDate: '二〇二六年二月十四',
      lunarMonth: '二月',
      lunarDay: '十四',
      zodiac: '马',
      solarTerm: '',
      suitable: ['纳财', '开市'],
      avoid: ['移徙', '入宅'],
      chongSha: '冲(己亥)猪 煞东',
      pengZuBaiJi: '乙不栽植千株不长 巳不远行财物伏藏',
      jishen: ['相日', '驿马'],
      xiongsha: ['五虚', '大煞'],
      directions: {
        caiShen: '东北',
        xiShen: '西北',
        fuShen: '西南',
        yangGui: '正北',
        yinGui: '西南',
      },
      dayOfficer: '定',
      tianShen: '司命',
      tianShenType: '黄道',
      tianShenLuck: '吉',
      lunarMansion: '毕月乌',
      lunarMansionLuck: '吉',
      lunarMansionSong: '毕星造作主光前',
      nayin: '佛灯火',
      dayNineStar: {
        number: 3,
        description: '三碧木 震(正东) 天玑',
        color: '碧',
        wuXing: '木',
        position: '正东',
      },
      taiShen: '碓磨床 房内东',
      hourlyFortune: [
        { ganZhi: '丙子', tianShen: '青龙', tianShenType: '黄道', tianShenLuck: '吉', chong: '冲马', sha: '煞南', suitable: ['祭祀'], avoid: ['出行'] },
      ],
    },
  }, { detailLevel: 'full' });

  assert.match(text, /# 每日黄历/u);
  assert.match(text, /## 择日宜忌/u);
  assert.match(text, /宜: 纳财, 开市/u);
  assert.doesNotMatch(text, /## 方位信息/u);
  assert.match(fullText, /## 方位信息/u);
  assert.match(fullText, /## 值日信息/u);
  assert.match(fullText, /## 时辰吉凶/u);
});

test('web ziwei text should include horoscope block when caller explicitly requests it', () => {
  const bundle = calculateZiweiChartBundle({
    name: '测试',
    gender: 'male',
    birthYear: 1990,
    birthMonth: 1,
    birthDay: 1,
    birthHour: 12,
    birthMinute: 0,
    calendarType: 'solar',
  });

  const text = generateZiweiChartText(bundle.output, { includeHoroscope: true, astrolabe: bundle.astrolabe });

  assert.match(text, /## 当前运限/u, 'web ziwei text should preserve the explicit horoscope block');
  assert.match(text, /当前大限|流年宫位|流月宫位|流日宫位/u, 'web ziwei text should surface current horoscope details');
});

test('core liuyao markdown should surface changedNaJia and huaType in yongshen analysis text', () => {
  const markdown = renderToolDebugText('liuyao', {
    question: '测试问题',
    hexagramName: '乾为天',
    hexagramGong: '乾',
    hexagramElement: '金',
    ganZhiTime: {
      year: { gan: '甲', zhi: '子' },
      month: { gan: '乙', zhi: '丑' },
      day: { gan: '丙', zhi: '寅' },
      hour: { gan: '丁', zhi: '卯' },
      xun: '甲子',
    },
    kongWang: { xun: '甲子', kongDizhi: ['戌', '亥'] },
    kongWangByPillar: {
      year: { xun: '甲子', kongDizhi: ['戌', '亥'] },
      month: { xun: '甲子', kongDizhi: ['戌', '亥'] },
      day: { xun: '甲子', kongDizhi: ['戌', '亥'] },
      hour: { xun: '甲子', kongDizhi: ['戌', '亥'] },
    },
    fullYaos: [],
    yongShen: [{
      targetLiuQin: '官鬼',
      selectionStatus: 'from_changed',
      selectionNote: '变出取用',
      selected: {
        liuQin: '官鬼',
        naJia: '子',
        changedNaJia: '酉',
        huaType: '回头生',
        element: '水',
        position: 3,
        source: 'changed',
        strength: 'strong',
        strengthLabel: '旺相',
        movementState: 'changing',
        movementLabel: '明动',
        isShiYao: false,
        isYingYao: false,
        evidence: ['测试证据'],
      },
      candidates: [{
        liuQin: '官鬼',
        naJia: '子',
        changedNaJia: '酉',
        huaType: '回头生',
        element: '水',
        position: 3,
        source: 'changed',
        strength: 'strong',
        strengthLabel: '旺相',
        movementState: 'changing',
        movementLabel: '明动',
        isShiYao: false,
        isYingYao: false,
        evidence: ['测试证据'],
      }],
    }],
    shenSystemByYongShen: [],
    globalShenSha: [],
  });

  assert.match(markdown, /酉/u, 'mcp liuyao markdown should expose changedNaJia');
  assert.match(markdown, /回头生/u, 'mcp liuyao markdown should expose huaType');
});

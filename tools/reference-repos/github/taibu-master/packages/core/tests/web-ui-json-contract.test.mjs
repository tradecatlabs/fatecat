import test from 'node:test';
import assert from 'node:assert/strict';

import {
  calculateDailyAlmanac,
  calculateDaliuren,
  calculateQimen,
  calculateTarot,
  calculateZiwei,
  calculateZiweiFlyingStar,
  calculateZiweiHoroscope,
  resolveBaziPillars,
  toAlmanacJson,
  toBaziJson,
  toBaziPillarsResolveJson,
  toDaliurenJson,
  toQimenJson,
  toTarotJson,
  toZiweiFlyingStarJson,
  toZiweiHoroscopeJson,
  toZiweiJson,
} from 'taibu-core';

function createBaziResult(overrides = {}) {
  return {
    gender: 'male',
    dayMaster: '甲',
    kongWang: { xun: '甲子', kongZhi: ['戌', '亥'] },
    fourPillars: {
      year: {
        stem: '甲',
        branch: '戌',
        tenGod: '比肩',
        hiddenStems: [],
        naYin: '山头火',
        diShi: '养',
        shenSha: ['空亡', '天乙贵人'],
        kongWang: { isKong: true },
      },
      month: {
        stem: '乙',
        branch: '亥',
        tenGod: '劫财',
        hiddenStems: [],
        naYin: '山头火',
        diShi: '长生',
        shenSha: ['文昌贵人'],
        kongWang: { isKong: true },
      },
      day: {
        stem: '甲',
        branch: '子',
        hiddenStems: [],
        naYin: '海中金',
        diShi: '沐浴',
        shenSha: [],
        kongWang: { isKong: false },
      },
      hour: {
        stem: '丙',
        branch: '辰',
        tenGod: '食神',
        hiddenStems: [],
        naYin: '沙中土',
        diShi: '衰',
        shenSha: [],
        kongWang: { isKong: false },
      },
    },
    relations: [
      { type: '合', description: '子辰半合水', pillars: ['日支', '时支'] },
      { type: '会', description: '寅卯辰三会木', pillars: ['年支', '月支', '时支'] },
    ],
    tianGanWuHe: [],
    tianGanChongKe: [],
    diZhiBanHe: [{ branches: ['子', '辰'], resultElement: '水', missingBranch: '申' }],
    diZhiSanHui: [{ branches: ['寅', '卯', '辰'], resultElement: '木' }],
    ...overrides,
  };
}

test('qimen canonical json should preserve machine-readable fields needed by web ui', async () => {
  const result = await calculateQimen({
    year: 2026,
    month: 3,
    day: 22,
    hour: 10,
    minute: 0,
    timezone: 'Asia/Shanghai',
    question: '项目推进',
  });

  const json = toQimenJson(result);
  const fullJson = toQimenJson(result, { detailLevel: 'full' });

  assert.equal(json.九宫盘.length, 9);
  assert.equal(typeof json.九宫盘[0]?.宫位序号, 'number');
  assert.equal(typeof json.九宫盘[0]?.宫名, 'string');
  assert.equal(typeof json.九宫盘[0]?.宫位五行, 'string');
  assert.equal('公历' in json.基本信息, false);
  assert.equal('农历' in json.基本信息, false);
  assert.equal('盘式' in json.基本信息, false);
  assert.equal('定局法' in json.基本信息, false);
  assert.equal('空亡信息' in json, false);
  assert.equal(typeof fullJson.空亡信息?.日空?.地支?.[0], 'string');
  assert.equal(typeof fullJson.十干月令旺衰?.甲, 'string');
});

test('daliuren canonical json should not expose fields omitted by canonical text spec', async () => {
  const result = await calculateDaliuren({
    date: '2026-03-22',
    hour: 10,
    minute: 0,
    timezone: 'Asia/Shanghai',
    question: '项目推进',
  });

  const json = toDaliurenJson(result);
  const fullJson = toDaliurenJson(result, { detailLevel: 'full' });

  assert.equal('yinYangGuiRen' in result, false);
  assert.equal(json.四课.length, 4);
  assert.equal(json.三传.length, 3);
  assert.equal(Array.isArray(json.天地盘), true);
  assert.equal('农历' in json.基本信息, false);
  assert.equal('本命' in json.基本信息, false);
  assert.equal('附加课体' in json.基本信息, false);
  assert.equal('建除' in json.天地盘[0], false);
  assert.equal('神煞' in json, false);
  assert.equal(typeof fullJson.天地盘[0]?.建除, 'string');
});

test('almanac canonical json should expose Chinese grouped keys and keep full-only calendrical extensions opt-in', async () => {
  const result = await calculateDailyAlmanac({
    date: '2026-04-01',
    dayMaster: '戊',
  });

  const json = toAlmanacJson(result);
  const fullJson = toAlmanacJson(result, { detailLevel: 'full' });

  assert.equal(typeof json.基础与个性化坐标.日期, 'string');
  assert.equal(typeof json.基础与个性化坐标.日干支, 'string');
  assert.equal(typeof json.基础与个性化坐标.流日十神, 'string');
  assert.equal(Array.isArray(json.择日宜忌.宜), true);
  assert.equal(Array.isArray(json.择日宜忌.忌), true);
  assert.equal(typeof json.神煞参考.吉神宜趋?.[0], 'string');
  assert.equal(json.方位信息, undefined);
  assert.equal(json.值日信息, undefined);
  assert.equal(json.时辰吉凶, undefined);

  assert.equal(typeof fullJson.方位信息?.财神, 'string');
  assert.equal(typeof fullJson.值日信息?.建除十二值星, 'string');
  assert.ok(Array.isArray(fullJson.时辰吉凶));
  assert.equal('basicInfo' in json, false);
  assert.equal('almanac' in json, false);
});

test('bazi canonical json should de-duplicate branch relation summaries without showing missing banhe branches', () => {
  const json = toBaziJson(createBaziResult());

  assert.deepEqual(json.干支关系, ['子辰半合水', '寅卯辰三会木']);
});

test('bazi_pillars_resolve canonical json should expose Chinese keys and next-call guidance', async () => {
  const result = await resolveBaziPillars({
    yearPillar: '癸未',
    monthPillar: '庚申',
    dayPillar: '戊寅',
    hourPillar: '丁巳',
  });

  const json = toBaziPillarsResolveJson(result);

  assert.equal(typeof json.原始四柱.年柱, 'string');
  assert.equal(typeof json.候选数量, 'number');
  if (json.候选列表.length > 0) {
    assert.equal(typeof json.候选列表[0].候选序号, 'number');
    assert.equal(typeof json.候选列表[0].农历, 'string');
    assert.equal(typeof json.候选列表[0].公历, 'string');
    assert.equal(typeof json.候选列表[0].下一步排盘建议.工具, 'string');
    assert.equal(typeof json.候选列表[0].下一步排盘建议.参数.出生年, 'number');
    assert.equal(Array.isArray(json.候选列表[0].下一步排盘建议.缺少信息), true);
  }
  assert.equal('originalPillars' in json, false);
  assert.equal('count' in json, false);
  assert.equal('candidates' in json, false);
});

test('daliuren canonical json keeps full tianjiang names for palace grid color mapping', async () => {
  const result = await calculateDaliuren({
    date: '2026-03-22',
    hour: 10,
    minute: 0,
    timezone: 'Asia/Shanghai',
    question: '项目推进',
  });

  const json = toDaliurenJson(result);

  assert.deepEqual(
    json.天地盘.map((item) => item.天将),
    result.gongInfos.map((item) => item.tianJiang),
  );
});

test('ziwei canonical json should expose compact default output while keeping full detail opt-in', async () => {
  const result = await calculateZiwei({
    gender: 'male',
    birthYear: 1990,
    birthMonth: 1,
    birthDay: 1,
    birthHour: 12,
    birthMinute: 0,
    calendarType: 'solar',
  });

  const json = toZiweiJson(result);
  const fullJson = toZiweiJson(result, { detailLevel: 'full' });

  assert.equal(Array.isArray(json.十二宫位), true);
  assert.equal('decadalList' in json, false);
  assert.equal(Array.isArray(json.小限), false);
  assert.equal(typeof json.基本信息.生年四化?.天干, 'string');
  assert.equal(Array.isArray(json.基本信息.生年四化?.四化星曜), true);
  assert.equal(Array.isArray(json.十二宫位[0]?.杂曜), false);
  assert.equal(Array.isArray(json.十二宫位[0]?.神煞), false);
  assert.equal(Array.isArray(json.十二宫位[0]?.小限虚岁), false);
  assert.equal(Array.isArray(json.十二宫位[0]?.流年虚岁), false);
  assert.equal('currentTransit' in json, false);

  assert.equal(Array.isArray(fullJson.小限), true);
  assert.deepEqual(
    fullJson.小限?.slice(0, 4).map((item) => item.宫位),
    ['命宫', '父母', '福德', '田宅'],
  );
  assert.ok(Array.isArray(fullJson.十二宫位[0]?.杂曜));
  assert.ok(Array.isArray(fullJson.十二宫位[0]?.神煞));
  assert.ok(Array.isArray(fullJson.十二宫位[0]?.小限虚岁));
  assert.ok(Array.isArray(fullJson.十二宫位[0]?.流年虚岁));
  assert.equal('currentTransit' in fullJson, false);
});

test('ziwei_horoscope canonical json should expose Chinese keys for horoscope periods', async () => {
  const result = await calculateZiweiHoroscope({
    gender: 'male',
    birthYear: 2003,
    birthMonth: 9,
    birthDay: 2,
    birthHour: 10,
    birthMinute: 20,
    calendarType: 'solar',
    targetDate: '2026-03-22',
  });

  const json = toZiweiHoroscopeJson(result);
  const fullJson = toZiweiHoroscopeJson(result, { detailLevel: 'full' });

  assert.equal(typeof json.基本信息.目标日期, 'string');
  assert.equal(typeof json.基本信息.五行局, 'string');
  assert.equal(json.基本信息.阳历, undefined);
  assert.equal(Array.isArray(json.运限叠宫), true);
  assert.equal(typeof json.运限叠宫[0]?.层次, 'string');
  assert.equal(typeof json.运限叠宫[0]?.宫位索引, 'number');
  assert.equal(typeof json.运限叠宫[0]?.落入本命宫位, 'string');
  assert.equal(Array.isArray(json.运限叠宫[0]?.运限四化), true);
  assert.equal(typeof json.流年星曜?.吉星分布?.[0], 'string');
  assert.equal(fullJson.基本信息.阳历?.length > 0, true);
  assert.equal(Array.isArray(fullJson.岁前十二星), true);
  assert.equal(Array.isArray(fullJson.将前十二星), true);
  assert.equal('basicInfo' in json, false);
  assert.equal('periods' in json, false);
});

test('ziwei_flying_star canonical json should expose Chinese keys and readable query labels', async () => {
  const result = await calculateZiweiFlyingStar({
    gender: 'male',
    birthYear: 2003,
    birthMonth: 9,
    birthDay: 2,
    birthHour: 10,
    birthMinute: 20,
    calendarType: 'solar',
    queries: [
      { type: 'fliesTo', from: '命宫', to: '财帛宫', mutagens: ['禄'] },
      { type: 'mutagedPlaces', palace: '命宫' },
      { type: 'surroundedPalaces', palace: '命宫' },
    ],
  });

  const json = toZiweiFlyingStarJson(result);

  assert.equal(Array.isArray(json.查询结果), true);
  assert.equal(typeof json.查询结果[0]?.查询序号, 'number');
  assert.equal(typeof json.查询结果[0]?.查询类型, 'string');
  assert.equal(typeof json.查询结果[0]?.判断目标, 'string');
  assert.equal(['是', '否'].includes(json.查询结果[0]?.结果), true);
  assert.equal(Array.isArray(json.查询结果[0]?.实际飞化), true);
  assert.equal(Array.isArray(json.查询结果[1]?.四化落宫), true);
  assert.equal(typeof json.查询结果[1]?.发射宫干支, 'string');
  assert.equal(typeof json.查询结果[1]?.四化落宫?.[0]?.星曜, 'string');
  assert.equal(typeof json.查询结果[2]?.本宫, 'string');
  assert.equal(typeof json.查询结果[2]?.矩阵宫位?.三合1, 'string');
  assert.equal('results' in json, false);
});

test('tarot canonical json should expose slim default output and full numerology detail on demand', async () => {
  const result = await calculateTarot({
    spreadType: 'three-card',
    question: '接下来会怎样',
    birthYear: 2003,
    birthMonth: 9,
    birthDay: 2,
    seed: 'tarot-contract',
  });

  const json = toTarotJson(result);
  const fullJson = toTarotJson(result, { detailLevel: 'full' });

  assert.equal(typeof json.问卜设定.牌阵, 'string');
  assert.equal(typeof json.问卜设定.问题, 'string');
  assert.equal(json.问卜设定.出生日期, undefined);
  assert.equal(json.问卜设定.随机种子, undefined);
  assert.equal(Array.isArray(json.牌阵展开), true);
  assert.equal(typeof json.牌阵展开[0]?.位置, 'string');
  assert.equal(typeof json.牌阵展开[0]?.塔罗牌, 'string');
  assert.equal(typeof json.牌阵展开[0]?.状态, 'string');
  assert.equal(Array.isArray(json.牌阵展开[0]?.核心基调), true);
  assert.equal(typeof json.牌阵展开[0]?.元素, 'string');
  assert.equal(json.求问者生命数字, undefined);

  assert.equal(typeof fullJson.问卜设定.出生日期, 'string');
  assert.equal(typeof fullJson.问卜设定.随机种子, 'string');
  assert.equal(typeof fullJson.牌阵展开[0]?.元素, 'string');
  assert.equal(typeof fullJson.求问者生命数字?.人格牌?.对应塔罗, 'string');
  assert.equal('basicInfo' in json, false);
  assert.equal('cards' in json, false);
});

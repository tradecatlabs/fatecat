import type {
  AlmanacCanonicalJSON
} from './json-types.js';
import {
  normalizeDetailLevelBinary
} from '../../shared/render-utils.js';
import type {
  AlmanacOutput
} from './types.js';
import type {
  AlmanacCanonicalTextOptions
} from '../shared/text-options.js';

export function renderAlmanacCanonicalJSON(result: AlmanacOutput, options: { detailLevel?: AlmanacCanonicalTextOptions['detailLevel']; } = {}): AlmanacCanonicalJSON {
  const detailLevel = normalizeDetailLevelBinary(options.detailLevel);
  const { date, dayInfo, tenGod, almanac } = result;

  const json: AlmanacCanonicalJSON = {
    基础与个性化坐标: {
      日期: date,
      日干支: dayInfo.ganZhi,
    },
    传统黄历基调: {
      农历: almanac.lunarDate || `${almanac.lunarMonth}${almanac.lunarDay}`,
      生肖: almanac.zodiac,
    },
    择日宜忌: {
      宜: almanac.suitable,
      忌: almanac.avoid,
    },
    神煞参考: {},
  };
  if (tenGod) json.基础与个性化坐标.流日十神 = tenGod;

  if (almanac.solarTerm) json.传统黄历基调.节气 = almanac.solarTerm;
  if (almanac.chongSha) json.传统黄历基调.冲煞 = almanac.chongSha;
  if (almanac.pengZuBaiJi) json.传统黄历基调.彭祖百忌 = almanac.pengZuBaiJi;
  if (almanac.taiShen) json.传统黄历基调.胎神占方 = almanac.taiShen;
  if (almanac.dayNineStar) {
    json.传统黄历基调.日九星 = {
      描述: almanac.dayNineStar.description,
      方位: almanac.dayNineStar.position,
    };
  }
  if (almanac.jishen?.length) json.神煞参考.吉神宜趋 = almanac.jishen;
  if (almanac.xiongsha?.length) json.神煞参考.凶煞宜忌 = almanac.xiongsha;

  if (detailLevel === 'full') {
    json.方位信息 = {
      财神: almanac.directions.caiShen,
      喜神: almanac.directions.xiShen,
      福神: almanac.directions.fuShen,
      阳贵人: almanac.directions.yangGui,
      阴贵人: almanac.directions.yinGui,
    };
    json.值日信息 = {
      ...(almanac.dayOfficer ? { 建除十二值星: almanac.dayOfficer } : {}),
      ...(almanac.tianShen ? { 天神: almanac.tianShen } : {}),
      ...(almanac.tianShenType ? { 天神类型: almanac.tianShenType } : {}),
      ...(almanac.tianShenLuck ? { 天神吉凶: almanac.tianShenLuck } : {}),
      ...(almanac.lunarMansion ? { 二十八星宿: almanac.lunarMansion } : {}),
      ...(almanac.lunarMansionLuck ? { 星宿吉凶: almanac.lunarMansionLuck } : {}),
      ...(almanac.lunarMansionSong ? { 星宿歌诀: almanac.lunarMansionSong } : {}),
      ...(almanac.nayin ? { 日柱纳音: almanac.nayin } : {}),
    };
    if (almanac.hourlyFortune.length > 0) {
      json.时辰吉凶 = almanac.hourlyFortune.map((hour) => ({
        时辰: hour.ganZhi,
        ...(hour.tianShen ? { 天神: hour.tianShen } : {}),
        ...(hour.tianShenType ? { 天神类型: hour.tianShenType } : {}),
        ...(hour.tianShenLuck ? { 天神吉凶: hour.tianShenLuck } : {}),
        ...([hour.chong, hour.sha].filter(Boolean).length ? { 冲煞: [hour.chong, hour.sha].filter(Boolean).join(' / ') } : {}),
        ...(hour.suitable.length ? { 宜: hour.suitable } : {}),
        ...(hour.avoid.length ? { 忌: hour.avoid } : {}),
      }));
    }
  }

  return json;
}

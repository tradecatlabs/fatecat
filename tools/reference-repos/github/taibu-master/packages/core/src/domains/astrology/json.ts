import type { AstrologyCanonicalTextOptions } from '../shared/text-options.js';
import type {
  AstrologyCanonicalJSON,
  AstrologyCompactAspectJSON,
  AstrologyFactorSnapshotJSON,
  AstrologyHouseJSON,
} from './json-types.js';
import type { AstrologyAspect, AstrologyFactor, AstrologyHouse, AstrologyOutput } from './types.js';
import { buildAstrologyRenderModel } from './render-model.js';

function factorToSnapshotJson(item: AstrologyFactor, isApproximate: boolean): AstrologyFactorSnapshotJSON {
  return {
    星座: item.sign.label,
    黄经: `${item.position.absolute} / ${item.position.withinSign}`,
    ...(!isApproximate && typeof item.house === 'number' ? { 宫位: `第${item.house}宫` } : {}),
    ...(item.retrograde ? { 逆行: '是' as const } : {}),
  };
}

function aspectToCompactJson(item: AstrologyAspect, currentFactorKey: string): AstrologyCompactAspectJSON {
  return {
    对象: item.from.key === currentFactorKey ? item.to.label : item.from.label,
    相位: item.label,
    容许度: Number(item.orb.toFixed(4)),
  };
}

function aspectToJson(item: AstrologyAspect) {
  return {
    相位: item.label,
    起点: item.from.label,
    终点: item.to.label,
    容许度: Number(item.orb.toFixed(4)),
    实际夹角: Number(item.actualAngle.toFixed(4)),
  };
}

function houseToJson(item: AstrologyHouse): AstrologyHouseJSON {
  return {
    宫位: item.label,
    宫头星座: item.sign.label,
    宫头黄经: `${item.start.absolute} / ${item.start.withinSign}`,
  };
}

export function renderAstrologyCanonicalJSON(
  result: AstrologyOutput,
  options: { detailLevel?: AstrologyCanonicalTextOptions['detailLevel']; } = {},
): AstrologyCanonicalJSON {
  const model = buildAstrologyRenderModel(result, options);
  const { detailLevel, isApproximate } = model;

  const json: AstrologyCanonicalJSON = {
    基础坐标: {
      计算模式: model.basicInfo.calculationModeLabel,
      ...(model.basicInfo.calculationNote ? { 说明: model.basicInfo.calculationNote } : {}),
      ...(model.basicInfo.birthPlace ? { 出生地: model.basicInfo.birthPlace } : {}),
      坐标: model.basicInfo.coordinatesLabel,
      本命时区: model.basicInfo.natalTimeZoneLabel,
      本命时刻: model.basicInfo.natalDateTime,
      流运时刻: model.basicInfo.transitDateTime,
      黄道体系: model.basicInfo.zodiacLabel,
      宫制: model.basicInfo.houseSystemLabel,
    },
    命盘锚点: {
      太阳: factorToSnapshotJson(model.anchors.sun, isApproximate),
      月亮: factorToSnapshotJson(model.anchors.moon, isApproximate),
      ...(model.anchors.ascendant
        ? { 上升: factorToSnapshotJson(model.anchors.ascendant, isApproximate) }
        : { 上升说明: '未计算（需经纬度）' }),
      ...(model.anchors.midheaven
        ? { 天顶: factorToSnapshotJson(model.anchors.midheaven, isApproximate) }
        : { 天顶说明: '未计算（需经纬度）' }),
    },
    本命主星: model.natalBodies.map((entry) => ({
      因素: entry.factor.label,
      ...factorToSnapshotJson(entry.factor, isApproximate),
      关键相位: entry.aspects.map((aspect) => aspectToCompactJson(aspect, entry.factor.key)),
    })),
    当前流运触发: model.transitTriggers.map((entry) => ({
      流运星体: entry.factor.label,
      ...factorToSnapshotJson(entry.factor, isApproximate),
      触发相位: entry.aspects.map((aspect) => aspectToCompactJson(aspect, entry.factor.key)),
    })),
  };

  if (detailLevel === 'more' || detailLevel === 'full') {
    json.扩展信息 = {};
    if (model.pointPairs.length > 0) {
      json.扩展信息.附加点与交点 = model.pointPairs.map((pair) => ({
        因素: pair.label,
        本命: factorToSnapshotJson(pair.natal, isApproximate),
        ...(pair.transit ? { 流运: factorToSnapshotJson(pair.transit, isApproximate) } : {}),
      }));
    }
    if (model.houses.length > 0) {
      json.扩展信息.宫位宫头 = model.houses.map(houseToJson);
    }
  }

  if (detailLevel === 'full') {
    json.扩展信息 = {
      ...(json.扩展信息 ?? {}),
      完整相位矩阵: {
        本命: model.fullNatalAspects.map(aspectToJson),
        流运: model.fullTransitAspects.map(aspectToJson),
      },
      黄道分界: model.zodiacCusps.map((item) => ({
        星座: item.sign.label,
        起点黄经: `${item.start.absolute} / ${item.start.withinSign}`,
      })),
    };
  }

  return json;
}

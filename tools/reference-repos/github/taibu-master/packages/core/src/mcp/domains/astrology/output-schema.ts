import { arr, num, obj, str, type OutputSchema } from '../../schema-builders.js';

const factorSnapshotSchema = obj({
  星座: str('星座'),
  黄经: str('黄经'),
  宫位: str('宫位'),
  逆行: str('逆行'),
});

const compactAspectSchema = obj({
  对象: str('相位对象'),
  相位: str('相位'),
  容许度: num('容许度'),
});

const factorWithAspectsSchema = obj({
  因素: str('因素'),
  星座: str('星座'),
  黄经: str('黄经'),
  宫位: str('宫位'),
  逆行: str('逆行'),
  关键相位: arr(compactAspectSchema, '关键相位'),
});

const transitTriggerSchema = obj({
  流运星体: str('流运星体'),
  星座: str('星座'),
  黄经: str('黄经'),
  宫位: str('宫位'),
  逆行: str('逆行'),
  触发相位: arr(compactAspectSchema, '触发相位'),
});

const pointPairSchema = obj({
  因素: str('因素'),
  本命: factorSnapshotSchema,
  流运: factorSnapshotSchema,
});

const aspectSchema = obj({
  相位: str('相位'),
  起点: str('起点'),
  终点: str('终点'),
  容许度: num('容许度'),
  实际夹角: num('实际夹角'),
});

const houseSchema = obj({
  宫位: str('宫位'),
  宫头星座: str('宫头星座'),
  宫头黄经: str('宫头黄经'),
});

export const astrologyOutputSchema: OutputSchema = obj({
  基础坐标: obj({
    计算模式: str('计算模式'),
    说明: str('补充说明'),
    出生地: str('出生地'),
    坐标: str('坐标'),
    本命时区: str('本命时区'),
    本命时刻: str('本命时刻'),
    流运时刻: str('流运时刻'),
    黄道体系: str('黄道体系'),
    宫制: str('宫制'),
  }),
  命盘锚点: obj({
    太阳: factorSnapshotSchema,
    月亮: factorSnapshotSchema,
    上升: factorSnapshotSchema,
    天顶: factorSnapshotSchema,
    上升说明: str('上升未计算说明'),
    天顶说明: str('天顶未计算说明'),
  }),
  本命主星: arr(factorWithAspectsSchema, '本命主星'),
  当前流运触发: arr(transitTriggerSchema, '当前流运触发'),
  扩展信息: obj({
    附加点与交点: arr(pointPairSchema, '附加点与交点'),
    宫位宫头: arr(houseSchema, '宫位宫头'),
    完整相位矩阵: obj({
      本命: arr(aspectSchema, '本命完整相位'),
      流运: arr(aspectSchema, '流运完整相位'),
    }),
    黄道分界: arr(obj({
      星座: str('星座'),
      起点黄经: str('起点黄经'),
    }), '黄道分界'),
  }),
});

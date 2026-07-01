export interface AstrologyFactorSnapshotJSON {
  星座: string;
  黄经: string;
  宫位?: string;
  逆行?: '是';
}

export type AstrologyFactorJSON = AstrologyFactorSnapshotJSON;

export interface AstrologyCompactAspectJSON {
  对象: string;
  相位: string;
  容许度: number;
}

export interface AstrologyFactorWithAspectsJSON extends AstrologyFactorSnapshotJSON {
  因素: string;
  关键相位: AstrologyCompactAspectJSON[];
}

export interface AstrologyTransitTriggerJSON extends AstrologyFactorSnapshotJSON {
  流运星体: string;
  触发相位: AstrologyCompactAspectJSON[];
}

export interface AstrologyPointPairJSON {
  因素: string;
  本命: AstrologyFactorSnapshotJSON;
  流运?: AstrologyFactorSnapshotJSON;
}

export interface AstrologyAspectJSON {
  相位: string;
  起点: string;
  终点: string;
  容许度: number;
  实际夹角: number;
}

export interface AstrologyHouseJSON {
  宫位: string;
  宫头星座: string;
  宫头黄经: string;
}

export interface AstrologyCanonicalJSON {
  基础坐标: {
    计算模式: string;
    说明?: string;
    出生地?: string;
    坐标: string;
    本命时区: string;
    本命时刻: string;
    流运时刻: string;
    黄道体系: string;
    宫制: string;
  };
  命盘锚点: {
    太阳: AstrologyFactorSnapshotJSON;
    月亮: AstrologyFactorSnapshotJSON;
    上升?: AstrologyFactorSnapshotJSON;
    天顶?: AstrologyFactorSnapshotJSON;
    上升说明?: string;
    天顶说明?: string;
  };
  本命主星: AstrologyFactorWithAspectsJSON[];
  当前流运触发: AstrologyTransitTriggerJSON[];
  扩展信息?: {
    附加点与交点?: AstrologyPointPairJSON[];
    宫位宫头?: AstrologyHouseJSON[];
    完整相位矩阵?: {
      本命: AstrologyAspectJSON[];
      流运: AstrologyAspectJSON[];
    };
    黄道分界?: Array<{
      星座: string;
      起点黄经: string;
    }>;
  };
}

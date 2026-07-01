export interface TaiyiCanonicalJSON {
  问卜与时空底盘: {
    占问?: string;
    时间: string;
    农历: string;
    节气?: string;
    四柱: string;
    分钟段?: string;
  };
  外部时空环境: {
    星宿: string;
    值星: string;
    天神: string;
  };
  核心物理关系: {
    能量交互: string;
  };
  九星阵列: Array<{
    观测层级: string;
    太乙名: string;
    神性: string;
    北斗名: string;
    映射参考: string;
    五行: string;
    方位: string;
    宫位: string;
  }>;
  古典参考: {
    主诀原文: string;
    使用提示: string;
  };
}


// ===== 每日黄历 =====

export interface AlmanacCanonicalJSON {
  基础与个性化坐标: {
    日期: string;
    日干支: string;
    流日十神?: string;
  };
  传统黄历基调: {
    农历: string;
    生肖: string;
    节气?: string;
    冲煞?: string;
    彭祖百忌?: string;
    胎神占方?: string;
    日九星?: { 描述: string; 方位: string; };
  };
  择日宜忌: {
    宜: string[];
    忌: string[];
  };
  神煞参考: {
    吉神宜趋?: string[];
    凶煞宜忌?: string[];
  };
  方位信息?: {
    财神: string;
    喜神: string;
    福神: string;
    阳贵人: string;
    阴贵人: string;
  };
  值日信息?: {
    建除十二值星?: string;
    天神?: string;
    天神类型?: string;
    天神吉凶?: string;
    二十八星宿?: string;
    星宿吉凶?: string;
    星宿歌诀?: string;
    日柱纳音?: string;
  };
  时辰吉凶?: Array<{
    时辰: string;
    天神?: string;
    天神类型?: string;
    天神吉凶?: string;
    冲煞?: string;
    宜?: string[];
    忌?: string[];
  }>;
}

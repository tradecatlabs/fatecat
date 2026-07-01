
// ===== 紫微运限 =====

export interface ZiweiHoroscopeCanonicalJSON {
  基本信息: {
    目标日期: string;
    五行局: string;
    阳历?: string;
    农历?: string;
    命主?: string;
    身主?: string;
  };
  运限叠宫: Array<{
    层次: string;
    时间段备注: string;
    宫位索引: number;
    干支: string;
    落入本命宫位: string;
    运限四化: string[];
    十二宫重排?: string[];
  }>;
  流年星曜?: {
    吉星分布: string[];
    煞星分布: string[];
    '桃花/文星': string[];
  };
  岁前十二星?: string[];
  将前十二星?: string[];
}

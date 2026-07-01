export interface DaliurenCanonicalJSON {
  基本信息: {
    占事?: string;
    占测时间: string;
    昼夜: string;
    四柱: string;
    课式: string;
    月将: string;
    关键状态: {
      空亡: string[];
      驿马: string;
      丁马: string;
      天马: string;
    };
    农历?: string;
    月将名称?: string;
    本命?: string;
    行年?: string;
    附加课体?: string[];
  };
  四课: Array<{
    课别: string;
    乘将: string;
    上神: string;
    下神: string;
  }>;
  三传: Array<{
    传序: string;
    地支: string;
    天将: string;
    六亲: string;
    遁干: string;
  }>;
  天地盘: Array<{
    地盘: string;
    五行?: string;
    旺衰?: string;
    天盘: string;
    天将: string;
    遁干: string;
    长生十二神: string;
    建除?: string;
  }>;
}

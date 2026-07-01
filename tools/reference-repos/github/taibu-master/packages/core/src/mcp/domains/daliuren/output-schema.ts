import {
  arr,
  obj,
  type OutputSchema,
  str
} from '../../schema-builders.js';

export const daliurenOutputSchema: OutputSchema = obj({
  基本信息: obj({
    占事: str('占事'),
    占测时间: str('占测时间'),
    昼夜: str('昼夜'),
    四柱: str('四柱'),
    课式: str('课式'),
    月将: str('月将'),
    关键状态: obj({
      空亡: arr(str(), '空亡'),
      驿马: str('驿马'),
      丁马: str('丁马'),
      天马: str('天马'),
    }),
    农历: str('农历'),
    月将名称: str('月将名称'),
    本命: str('本命'),
    行年: str('行年'),
    附加课体: arr(str(), '附加课体'),
  }),
  四课: arr(obj({
    课别: str('课别'),
    乘将: str('乘将'),
    上神: str('上神'),
    下神: str('下神'),
  })),
  三传: arr(obj({
    传序: str('传序'),
    地支: str('地支'),
    天将: str('天将'),
    六亲: str('六亲'),
    遁干: str('遁干'),
  })),
  天地盘: arr(obj({
    地盘: str('地盘'),
    五行: str('五行'),
    旺衰: str('旺衰'),
    天盘: str('天盘'),
    天将: str('天将'),
    遁干: str('遁干'),
    长生十二神: str('长生十二神'),
    建除: str('建除'),
  })),
});

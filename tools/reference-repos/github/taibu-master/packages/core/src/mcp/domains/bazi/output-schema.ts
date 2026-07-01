import {
  arr,
  num,
  obj,
  type OutputSchema,
  str
} from '../../schema-builders.js';

export const baziCalculateOutputSchema: OutputSchema = obj({
  基本信息: obj({
    性别: str('性别'),
    日主: str('日主'),
    命主五行: str('命主五行'),
    空亡: arr(str(), '空亡'),
    出生地: str('出生地'),
    真太阳时: obj({
      钟表时间: str('钟表时间'),
      真太阳时: str('真太阳时'),
      经度: num('经度'),
      校正分钟: num('校正分钟'),
    }),
    胎元: str('胎元'),
    命宫: str('命宫'),
  }),
  四柱: arr(obj({
    柱: str('柱名'),
    干支: str('干支'),
    天干十神: str('十神'),
    藏干: arr(obj({
      天干: str('藏干天干'),
      十神: str('藏干十神'),
      气性: str('气性'),
    })),
    地势: str('地势'),
    纳音: str('纳音'),
    神煞: arr(str()),
    空亡: str('是否空亡'),
  }), '四柱'),
  干支关系: arr(str(), '干支关系'),
  大运: obj({
    起运信息: str('起运信息'),
    大运列表: arr(obj({
      起运年份: num('起始年份'),
      起运年龄: num('起运年龄'),
      干支: str('干支'),
      天干: str('天干'),
      地支: str('地支'),
      十神: str('十神'),
      地支主气十神: str('地支主气十神'),
      藏干: arr(obj({
        天干: str('藏干天干'),
        十神: str('藏干十神'),
        气性: str('气性'),
      })),
      地势: str('地势'),
      纳音: str('纳音'),
      神煞: arr(str(), '神煞'),
      原局关系: arr(obj({
        类型: str('关系类型'),
        地支: arr(str(), '涉及地支'),
        描述: str('关系描述'),
      }), '原局关系'),
      流年列表: arr(obj({
        流年: num('流年年份'),
        年龄: num('年龄'),
        干支: str('干支'),
        天干: str('天干'),
        地支: str('地支'),
        十神: str('十神'),
        纳音: str('纳音'),
        藏干: arr(obj({
          天干: str('藏干天干'),
          十神: str('藏干十神'),
          气性: str('气性'),
        })),
        地势: str('地势'),
        神煞: arr(str(), '神煞'),
        原局关系: arr(obj({
          类型: str('关系类型'),
          地支: arr(str(), '涉及地支'),
          描述: str('关系描述'),
        }), '原局关系'),
        太岁关系: arr(str(), '太岁关系'),
      }), '流年列表'),
    }), '大运列表'),
  }),
});

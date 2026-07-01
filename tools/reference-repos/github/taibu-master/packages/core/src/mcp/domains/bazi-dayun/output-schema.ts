import {
  arr,
  num,
  obj,
  type OutputSchema,
  str
} from '../../schema-builders.js';

export const baziDayunOutputSchema: OutputSchema = obj({
  起运信息: obj({
    起运年龄: num('起运年龄'),
    起运详情: str('起运详情'),
  }),
  小运: arr(obj({
    年龄: num('年龄'),
    干支: str('干支'),
    十神: str('天干十神'),
  }), '小运列表'),
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
});

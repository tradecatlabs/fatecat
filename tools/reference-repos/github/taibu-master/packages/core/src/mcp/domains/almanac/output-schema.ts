import {
  arr,
  obj,
  type OutputSchema,
  str
} from '../../schema-builders.js';

export const almanacOutputSchema: OutputSchema = obj({
  基础与个性化坐标: obj({
    日期: str('日期'),
    日干支: str('日干支'),
    流日十神: str('流日十神'),
  }),
  传统黄历基调: obj({
    农历: str('农历'),
    生肖: str('生肖'),
    节气: str('节气'),
    冲煞: str('冲煞'),
    彭祖百忌: str('彭祖百忌'),
    胎神占方: str('胎神'),
    日九星: obj({
      描述: str('描述'),
      方位: str('方位'),
    }),
  }),
  择日宜忌: obj({
    宜: arr(str(), '宜'),
    忌: arr(str(), '忌'),
  }),
  神煞参考: obj({
    吉神宜趋: arr(str(), '吉神'),
    凶煞宜忌: arr(str(), '凶煞'),
  }),
  方位信息: obj({
    财神: str('财神'),
    喜神: str('喜神'),
    福神: str('福神'),
    阳贵人: str('阳贵人'),
    阴贵人: str('阴贵人'),
  }),
  值日信息: obj({
    建除十二值星: str('建除十二值星'),
    天神: str('天神'),
    天神类型: str('天神类型'),
    天神吉凶: str('天神吉凶'),
    二十八星宿: str('二十八星宿'),
    星宿吉凶: str('星宿吉凶'),
    星宿歌诀: str('星宿歌诀'),
    日柱纳音: str('日柱纳音'),
  }),
  时辰吉凶: arr(obj({
    时辰: str('时辰'),
    天神: str('天神'),
    天神类型: str('天神类型'),
    天神吉凶: str('天神吉凶'),
    冲煞: str('冲煞'),
    宜: arr(str(), '宜'),
    忌: arr(str(), '忌'),
  })),
});

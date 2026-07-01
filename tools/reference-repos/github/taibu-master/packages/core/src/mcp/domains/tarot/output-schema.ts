import {
  arr,
  num,
  obj,
  type OutputSchema,
  str
} from '../../schema-builders.js';

export const tarotOutputSchema: OutputSchema = obj({
  问卜设定: obj({
    牌阵: str('牌阵'),
    问题: str('问题'),
    出生日期: str('出生日期'),
    随机种子: str('随机种子'),
  }),
  牌阵展开: arr(obj({
    位置: str('位置'),
    塔罗牌: str('塔罗牌'),
    状态: str('状态'),
    核心基调: arr(str(), '核心基调'),
    元素: str('元素'),
    星象: str('星象对应'),
  })),
  求问者生命数字: obj({
    人格牌: obj({
      对应塔罗: str('人格牌'),
      背景基调: arr(str(), '背景基调'),
      元素: str('元素'),
      星象: str('星象对应'),
    }),
    灵魂牌: obj({
      对应塔罗: str('灵魂牌'),
      背景基调: arr(str(), '背景基调'),
      元素: str('元素'),
      星象: str('星象对应'),
    }),
    年度牌: obj({
      对应塔罗: str('年度牌'),
      年份: num('年份'),
      背景基调: arr(str(), '背景基调'),
      元素: str('元素'),
      星象: str('星象对应'),
    }),
  }),
});

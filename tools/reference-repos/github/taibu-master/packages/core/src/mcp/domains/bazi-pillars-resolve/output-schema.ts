import {
  arr,
  num,
  obj,
  type OutputSchema,
  str
} from '../../schema-builders.js';

export const baziPillarsResolveOutputSchema: OutputSchema = obj({
  原始四柱: obj({
    年柱: str('年柱'),
    月柱: str('月柱'),
    日柱: str('日柱'),
    时柱: str('时柱'),
  }),
  候选数量: num('候选总数'),
  候选列表: arr(obj({
    候选序号: num('候选序号'),
    农历: str('农历文本'),
    公历: str('公历文本'),
    出生时间: str('出生时间'),
    是否闰月: str('是否闰月'),
    下一步排盘建议: obj({
      工具: str('工具名'),
      参数: obj({
        出生年: num('农历出生年'),
        出生月: num('农历出生月'),
        出生日: num('农历出生日'),
        出生时: num('出生时'),
        出生分: num('出生分'),
        历法: str('历法'),
        是否闰月: str('是否闰月'),
      }),
      缺少信息: arr(str(), '缺少信息'),
    }),
  })),
});

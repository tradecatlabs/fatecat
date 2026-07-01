import{
  obj,
  str,
  num,
  type OutputSchema,
} from '../../schema-builders.js';

export const xiaoliurenOutputSchema: OutputSchema = obj({
  起课信息: obj({
    占问: str('占问事项'),
    农历月: num('农历月'),
    农历日: num('农历日'),
    时辰: str('时辰名称'),
    时辰序号: num('时辰序号'),
  }),
  推演链: obj({
    月上起: str('月上起落点'),
    日上落: str('日上落点'),
    时上落: str('时上最终落点'),
  }),
  结果: obj({
    落宫: str('最终落宫'),
    五行: str('五行'),
    方位: str('方位'),
    性质: str('性质'),
    释义: str('释义'),
    诗诀: str('诗诀'),
  }),
});

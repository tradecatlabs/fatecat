import {
  arr,
  num,
  obj,
  type OutputSchema,
  str
} from '../../schema-builders.js';

export const ziweiHoroscopeOutputSchema: OutputSchema = obj({
  基本信息: obj({
    目标日期: str('目标日期'),
    五行局: str('五行局'),
    阳历: str('阳历'),
    农历: str('农历'),
    命主: str('命主'),
    身主: str('身主'),
  }),
  运限叠宫: arr(obj({
    层次: str('层次'),
    时间段备注: str('时间段或备注'),
    宫位索引: num('宫位索引'),
    干支: str('干支'),
    落入本命宫位: str('落入本命宫位'),
    运限四化: arr(str(), '运限四化'),
    十二宫重排: arr(str(), '十二宫重排'),
  })),
  流年星曜: obj({
    吉星分布: arr(str(), '吉星分布'),
    煞星分布: arr(str(), '煞星分布'),
    '桃花/文星': arr(str(), '桃花/文星'),
  }),
  岁前十二星: arr(str(), '岁前十二星'),
  将前十二星: arr(str(), '将前十二星'),
});

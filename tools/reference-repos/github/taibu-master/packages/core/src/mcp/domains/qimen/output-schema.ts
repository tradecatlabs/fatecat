import {
  arr,
  num,
  obj,
  type OutputSchema,
  str
} from '../../schema-builders.js';

export const qimenCalculateOutputSchema: OutputSchema = obj({
  基本信息: obj({
    占问: str('占问'),
    四柱: str('四柱'),
    节气: str('节气'),
    局式: str('局式'),
    三元: str('三元'),
    旬首: str('旬首'),
    值符: str('值符'),
    值使: str('值使'),
    公历: str('公历'),
    农历: str('农历'),
    节气范围: str('节气范围'),
    盘式: str('盘式'),
    定局法: str('定局法'),
  }),
  九宫盘: arr(obj({
    宫名: str('宫名'),
    宫位序号: num('宫位序号'),
    宫位: str('宫位'),
    宫位五行: str('宫位五行'),
    八神: str('八神'),
    九星: str('九星'),
    九星五行: str('九星五行'),
    八门: str('八门'),
    八门五行: str('八门五行'),
    天盘天干: str('天盘天干'),
    地盘天干: str('地盘天干'),
    宫位状态: arr(str(), '宫位状态'),
    方位: str('方位'),
    格局: arr(str(), '格局'),
    宫旺衰: str('宫旺衰'),
    天盘天干五行: str('天盘天干五行'),
    地盘天干五行: str('地盘天干五行'),
  })),
  空亡信息: obj({
    日空: obj({
      地支: arr(str(), '地支'),
      宫位: arr(str(), '宫位'),
    }),
    时空: obj({
      地支: arr(str(), '地支'),
      宫位: arr(str(), '宫位'),
    }),
  }),
  驿马: obj({
    地支: str('驿马地支'),
    宫位: str('驿马宫位'),
  }),
  十干月令旺衰: {
    type: 'object',
    description: '十天干在月令中的旺衰',
    additionalProperties: { type: 'string' },
  },
  全局格局: arr(str(), '全局格局'),
});

import {
  arr,
  num,
  obj,
  type OutputSchema,
  str
} from '../../schema-builders.js';

export const ziweiFlyingStarOutputSchema: OutputSchema = obj({
  查询结果: arr(obj({
    查询序号: num('查询序号'),
    查询类型: str('查询类型'),
    判断目标: str('判断目标'),
    结果: str('结果'),
    发射宫位: str('发射宫位'),
    发射宫干支: str('发射宫干支'),
    实际飞化: arr(obj({
      四化: str('四化'),
      宫位: str('目标宫位'),
      星曜: str('星曜'),
    })),
    四化落宫: arr(obj({
      四化: str('四化'),
      宫位: str('目标宫位'),
      星曜: str('星曜'),
    })),
    本宫: str('本宫'),
    矩阵宫位: obj({
      对宫: str('对宫'),
      三合1: str('三合宫1'),
      三合2: str('三合宫2'),
    }),
  })),
});

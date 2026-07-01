import { arr, obj, str, type OutputSchema } from '../../schema-builders.js';

export const taiyiOutputSchema: OutputSchema = obj({
  问卜与时空底盘: obj({
    占问: str('占问事项'),
    时间: str('时间'),
    农历: str('农历时间'),
    节气: str('节气'),
    四柱: str('四柱'),
    分钟段: str('分钟段'),
  }),
  外部时空环境: obj({
    星宿: str('星宿'),
    值星: str('值星'),
    天神: str('天神'),
  }),
  核心物理关系: obj({
    能量交互: str('能量交互'),
  }),
  九星阵列: arr(obj({
    观测层级: str('观测层级'),
    太乙名: str('太乙名'),
    神性: str('神性'),
    北斗名: str('北斗名'),
    映射参考: str('映射参考'),
    五行: str('五行'),
    方位: str('方位'),
    宫位: str('宫位'),
  }), '九星阵列'),
  古典参考: obj({
    主诀原文: str('主诀原文'),
    使用提示: str('使用提示'),
  }),
});

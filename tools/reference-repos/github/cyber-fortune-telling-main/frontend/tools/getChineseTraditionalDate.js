// tools/getChineseTraditionalDate.js
import { Solar } from 'lunar-javascript';

function getChineseTraditionalDate(dateString) {
  // dateString: 'YYYY-MM-DD'
  const [year, month, day] = dateString.split('-').map(Number);
  const solar = Solar.fromYmd(year, month, day);
  const lunar = solar.getLunar();

  // 干支年、月、日
  const ganzhiYear = lunar.getYearInGanZhi();
  const ganzhiMonth = lunar.getMonthInGanZhi();
  const ganzhiDay = lunar.getDayInGanZhi();

  // 农历月日
  const lunarMonth = lunar.getMonthInChinese();
  const lunarDay = lunar.getDayInChinese();

  // 生肖
  const zodiac = lunar.getYearShengXiao();

  // 传统叫法
  return `干支：${ganzhiYear}年${ganzhiMonth}月${ganzhiDay}日\n农历：${lunarMonth}月${lunarDay}日\n生肖：${zodiac}年`;
}

export default getChineseTraditionalDate;
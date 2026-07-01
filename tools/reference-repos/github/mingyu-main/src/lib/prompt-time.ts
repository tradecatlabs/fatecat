import { SolarTime } from 'tyme4ts';

const promptTimeCache = new Map<string, string>();

function formatSolarPromptTime(date: Date) {
  return `公历：${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日 ${date.getHours()}时${date.getMinutes()}分`;
}

function getPromptTimeCacheKey(date: Date) {
  return [
    date.getFullYear(),
    date.getMonth() + 1,
    date.getDate(),
    date.getHours(),
    date.getMinutes(),
  ].join('-');
}

function formatPromptGanzhiCalendar(date: Date) {
  const solarTime = SolarTime.fromYmdHms(
    date.getFullYear(),
    date.getMonth() + 1,
    date.getDate(),
    date.getHours(),
    date.getMinutes(),
    date.getSeconds(),
  );
  const lunarHour = solarTime.getLunarHour();
  const lunarDay = lunarHour.getLunarDay();
  const lunarText = lunarDay.toString().replace(/^农历/, '');
  const lunarHourText = lunarHour.toString().replace(/^农历/, '');
  const hourLabel = lunarHourText.slice(-2);

  return [
    `农历：${lunarText} ${hourLabel}`,
    `干支历：${lunarHour.getYearSixtyCycle()}年 ${lunarHour.getMonthSixtyCycle()}月 ${lunarDay.getSixtyCycle()}日 ${lunarHour.getSixtyCycle()}时`,
    `当前节气：${solarTime.getTerm().getName()}`,
  ].join('\n');
}

export function formatPromptCurrentTime(date: Date = new Date()) {
  const cacheKey = getPromptTimeCacheKey(date);
  const cachedText = promptTimeCache.get(cacheKey);
  if (cachedText) {
    return cachedText;
  }

  const solarText = formatSolarPromptTime(date);

  try {
    const text = [solarText, formatPromptGanzhiCalendar(date)].join('\n');
    promptTimeCache.clear();
    promptTimeCache.set(cacheKey, text);
    return text;
  } catch {
    const text = [solarText, '干支历：暂无法计算'].join('\n');
    promptTimeCache.clear();
    promptTimeCache.set(cacheKey, text);
    return text;
  }
}

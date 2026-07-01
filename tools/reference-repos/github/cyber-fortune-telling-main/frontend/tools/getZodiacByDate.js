function getZodiacByDate(dateString) {
  // 生肖顺序
  const zodiacs = [
    "🐭", "🐮", "🐯", "🐰", "🐲", "🐍", "🐴", "🐑", "🐵", "🐔", "🐶", "🐷"
  ];
  // 以2020年为鼠年为基准
  const baseYear = 2020;
  const date = new Date(dateString);
  if (isNaN(date)) return null;
  const year = date.getFullYear();
  const index = (year - baseYear) % 12;
  // 处理负数年份
  return zodiacs[(index + 12) % 12];
}

export default getZodiacByDate; 
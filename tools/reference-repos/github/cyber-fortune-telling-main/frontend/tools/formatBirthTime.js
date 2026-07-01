// 格式化时间为 HH:mm:ss.SSS
function formatBirthTime(time) {
  if (!time) return "";
  if (/^\d{2}:\d{2}:\d{2}\.\d{3}$/.test(time)) return time;
  if (/^\d{2}:\d{2}:\d{2}$/.test(time)) return time + ".000";
  return time + ":00.000";
}

export default formatBirthTime; 
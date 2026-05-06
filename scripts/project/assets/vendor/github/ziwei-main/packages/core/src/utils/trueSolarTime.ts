/**
 * 依据 NOAA 推荐公式计算指定地点的真太阳时对应的 Date。
 *
 * @param date - 基准时间（JavaScript Date，包含绝对 UTC 时间）
 * @param longitude - 经度（东经为正，西经为负），单位：度
 * @param timezoneOffsetHours - 时区偏移（小时，默认取运行环境对 date 的解释）
 *
 * @returns 调整为真太阳时的 `Date`
 */
export function calculateTrueSolarTime(
  date: Date,
  longitude: number,
  timezoneOffsetHours: number = -date.getTimezoneOffset() / 60,
) {
  const timezoneOffsetMinutes = timezoneOffsetHours * 60;
  const localTime = new Date(date.getTime() + timezoneOffsetMinutes * 60_000);
  const startOfYear = Date.UTC(localTime.getUTCFullYear(), 0, 0);
  const dayOfYear = Math.floor((localTime.getTime() - startOfYear) / 86_400_000);
  const minutesPastMidnight =
    localTime.getUTCHours() * 60 +
    localTime.getUTCMinutes() +
    localTime.getUTCSeconds() / 60 +
    localTime.getUTCMilliseconds() / 60000;

  // NOAA 建议的分数年角（弧度）
  const gamma = (2 * Math.PI * (dayOfYear - 1 + minutesPastMidnight / 1440)) / 365;

  // 时间方程（单位：分钟）
  const equationOfTime =
    229.18 *
    (0.000075 +
      0.001868 * Math.cos(gamma) -
      0.032077 * Math.sin(gamma) -
      0.014615 * Math.cos(2 * gamma) -
      0.040849 * Math.sin(2 * gamma));

  // 经度与时区修正（分钟），4min 对应 1° 经度
  const longitudeCorrection = 4 * longitude;
  const correctionMinutes = equationOfTime + longitudeCorrection - timezoneOffsetMinutes;

  return new Date(date.getTime() + correctionMinutes * 60_000);
}

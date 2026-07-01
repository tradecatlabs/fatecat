function getChineseTraditionalTime(timeString) {
    const [hourStr, minuteStr] = timeString.split(":");
    const hour = parseInt(hourStr, 10);
    const minute = parseInt(minuteStr, 10);
  
    // 时辰定义
    const chineseHours = [
      { name: "子时", start: 23, end: 0 },
      { name: "丑时", start: 1, end: 2 },
      { name: "寅时", start: 3, end: 4 },
      { name: "卯时", start: 5, end: 6 },
      { name: "辰时", start: 7, end: 8 },
      { name: "巳时", start: 9, end: 10 },
      { name: "午时", start: 11, end: 12 },
      { name: "未时", start: 13, end: 14 },
      { name: "申时", start: 15, end: 16 },
      { name: "酉时", start: 17, end: 18 },
      { name: "戌时", start: 19, end: 20 },
      { name: "亥时", start: 21, end: 22 }
    ];
  
    const chineseNumbers = ["一", "二", "三", "四", "五", "六", "七", "八"];
  
    let shichen = "";
    if (hour === 23 || hour === 0) {
      shichen = "子时";
    } else {
      for (const item of chineseHours) {
        if (hour >= item.start && hour <= item.end) {
          shichen = item.name;
          break;
        }
      }
    }
  
    // 计算在本时辰内的分钟数
    let shichenStartHour;
    if (shichen === "子时") {
      shichenStartHour = hour === 23 ? 23 : 0;
    } else {
      shichenStartHour = chineseHours.find(item => item.name === shichen).start;
    }
    let minutesInShichen = (hour - shichenStartHour) * 60 + minute;
    if (minutesInShichen < 0) minutesInShichen += 120; // 跨天修正
  
    // 计算第几刻
    const ke = Math.floor(minutesInShichen / 15); // 0~7
    const keChinese = chineseNumbers[ke];
  
    return `${shichen}${keChinese}刻`;
  }
  
  export default getChineseTraditionalTime;
  
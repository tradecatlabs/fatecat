function getGenderEmoji(gender) {
  // 精选特别有男性特征且有趣的emoji
  const maleEmojis = [
    "🤠", "🎣", "👨‍💻"
  ];
  // 精选特别有女性特征且有趣的emoji
  const femaleEmojis = [
    "💃", "🧜‍♀️", "🦄"
  ];
  if (gender === "male") {
    return maleEmojis[Math.floor(Math.random() * maleEmojis.length)];
  } else {
    return femaleEmojis[Math.floor(Math.random() * femaleEmojis.length)];
  }
}

export default getGenderEmoji;
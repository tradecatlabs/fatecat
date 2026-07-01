/**
 * 占卜栏目配置
 */
const FORTUNE_SECTIONS = {
  prophecy: {
    key: "prophecy",
    label: "谶语",
    description: "神秘的预言诗句",
    icon: "📜",
    required: false,
    prompt: "请给我一个100字左右的谶语小诗, 小诗对仗工整，需要包含以下内容: 架空的世界，玄妙的情节，不可说破的寓意；如果需要解谶语小故事，语气像街头算命的道长，不要完全说破，给用户留有想象空间",
    template: `
    ## 📜今天给{username}的谶语

    <div class="fortune-story">
      <div class="fortune-story-item">{谶语小诗语句}</div>
      <div class="fortune-story-item">{谶语小诗语句}</div>
      <div class="fortune-story-item">{谶语小诗语句}</div>
      <div class="fortune-story-item">{谶语小诗语句}</div>
      <div class="fortune-story-item">{谶语小诗语句}</div>
      <div class="fortune-story-item">{谶语小诗语句}</div>
      <div class="fortune-story-item">{谶语小诗语句}</div>
      <div class="fortune-story-item">{谶语小诗语句}</div>
    </div>
    `
  },
  health_advice: {
    key: "health_advice",
    label: "中医养生建议",
    description: "基于中医理论的健康建议",
    icon: "🌿",
    required: false,
    prompt: "请用资深中医的语气，结合中医理论（如阴阳五行、脏腑经络、辨证论治等），用温和、专业、富有文化底蕴的语言，引用一些道德经名言，给出健康建议，并总结健康建议到 health-summary 部分",
    template: `
    ## 🌿今日中医养生健康建议:

    <div class="health-advice">
      <div class="health-advice-item">{健康建议}</div>
      <div class="health-advice-item">{健康建议}</div>
      <div class="health-advice-item">{健康建议}</div>
      <div class="health-advice-item">{健康建议}</div>
      <div class="health-advice-item">{健康建议}</div>
      <div class="health-advice-item">{健康建议}</div>
      <div class="health-advice-item">{健康建议}</div>
      <div class="health-advice-item">{健康建议}</div>
    </div>

    <div class="health-summary">
      {健康建议总结}
    </div>
    `
  },
  fortune_analysis: {
    key: "fortune_analysis",
    label: "八字与流年分析",
    description: "根据八字分析运势",
    icon: "🍀",
    required: false,
    prompt: "请根据用户的八字信息和当前流年，分析今日在事业工作、财运、感情人际、健康等方面的运势情况",
    template: `
    ## 🍀八字与流年分析 {username}今日{currentDate}具体运势分析：
    - 事业与工作：
    - 财运：
    - 感情与人际：
    - 健康：
    `
  },
  lucky_color: {
    key: "lucky_color",
    label: "幸运色",
    description: "今日幸运色彩",
    icon: "🍭",
    required: false,
    prompt: "请根据用户的八字信息和今日运势，推荐一个幸运颜色，并说明其寓意和建议如何使用",
    template: `
    ## 🍭幸运色分析

    <div class="lucky-color" style="color: {颜色值}">{颜色描述信息}</div>
    `
  },
  lucky_number: {
    key: "lucky_number",
    label: "幸运数字",
    description: "今日幸运数字",
    icon: "🔢",
    required: false,
    prompt: "请根据用户的运势分析，推荐一个今日的幸运数字，并说明其含义和运用建议",
    template: `
    ## 🔢今日幸运数字

    <div class="lucky-number">{数字描述信息}</div>
    `
  },
  social_contacts: {
    key: "social_contacts",
    label: "适合交流的人物",
    description: "今日适合交流的人物类型",
    icon: "💬",
    required: false,
    prompt: "基于以上分析，请推荐今日适合交流的人物类型，包括年龄、性格、职业等特征，说明为什么适合交流",
    template: `
    ## 💬基于以上分析,今日适合交流的人物:

    1.
    2.
    3.
    `
  },
  dating_places: {
    key: "dating_places",
    label: "脱单适合去哪里",
    description: "今日脱单的好去处",
    icon: "💏",
    required: false,
    prompt: "请推荐今日脱单的好去处，包括具体的地点类型、环境特色，说明为什么适合脱单",
    template: `
    ## 💏今天脱单适合去哪里

    <div class="dating-place">{地点描述信息}</div>
    <div class="dating-place">{地点描述信息}</div>
    <div class="dating-place">{地点描述信息}</div>
    `
  },
  entertainment_places: {
    key: "entertainment_places",
    label: "适合去哪里玩",
    description: "今日适合的娱乐场所",
    icon: "🤠",
    required: false,
    prompt: "请推荐今日适合的娱乐场所和活动，包括具体地点、活动类型，说明为什么适合今天去",
    template: `
    ## 🤠今天适合去哪里玩

    <div class="play-place">{地点描述信息}</div>
    <div class="play-place">{地点描述信息}</div>
    <div class="play-place">{地点描述信息}</div>
    `
  },
  healthy_food: {
    key: "healthy_food",
    label: "适合吃什么",
    description: "今日养生食物推荐",
    icon: "🍽️",
    required: false,
    prompt: "请根据用户的健康状况和今日运势，推荐适合的养生食物，包括具体的食物、制作方法、养生功效",
    template: `
    ## 🍽️为了长寿,今天适合吃什么

    <div class="food">{食物描述信息}</div>
    <div class="food">{食物描述信息}</div>
    <div class="food">{食物描述信息}</div>
    `
  },
  traditional_calendar: {
    key: "traditional_calendar",
    label: "传统黄历",
    description: "中国传统黄历信息",
    icon: "🗓️",
    required: false,
    prompt: "请根据今日的传统黄历信息，包括五行属性、值神、冲煞、财神喜神方位、重要时辰运势、今日宜忌等内容",
    template: `

    ## 📅 {currentDate} 黄历精要

    | 项目 | 内容 |
    |:----:|:-----|
    | 🌟 **五行** | {当日五行属性} |
    | 🙏 **值神** | {当日值神} |
    | ⚡ **冲煞** | {冲煞信息} |
    | 💰 **财神** | {财神方位} |
    | 😊 **喜神** | {喜神方位} |
    | 🍀 **福神** | {福神方位} |

    ## ⏰ 重要时辰

    | 时辰 | 时间 | 运势 |
    |:----:|:----:|:-----|
    | 🌅 **卯时** | 05-07时 | {卯时运势简述} |
    | ☀️ **巳时** | 09-11时 | {巳时运势简述} |
    | 🌞 **午时** | 11-13时 | {午时运势简述} |
    | 🌆 **酉时** | 17-19时 | {酉时运势简述} |


    ## 📝 今日宜忌

    <div class="fortune-yi">宜：{今日宜做的事情}</div>
    <div class="fortune-ji">忌：{今日忌做的事情}</div>
    `
  },

  prophecy_explanation: {
    key: "prophecy_explanation",
    label: "解谶语小故事",
    description: "谶语的详细解释",
    icon: "💡",
    required: false,
    prompt: "请对前面的谶语小诗进行解释，用街头算命道长的语气，讲一个小故事来解释谶语的含义，但不要完全说破，给用户留有想象空间",
    template: `
    ## 💡解谶语小故事

    <div class="fortune-story-explanation">{谶语小故事解释}</div>
    `
  },

  feng_shui_decoration: {
    key: "feng_shui_decoration",
    label: "风水摆件",
    description: "今日适合的风水摆件",
    icon: "🪆",
    required: true,
    prompt: "请从目前可用的摆件列表中选择一个最适合今日运势的摆件，并说明其风水寓意和摆放建议",
    template: `
    ## 🪆基于以上分析, 今天适合在桌面摆放的一个摆件为{摆件名}:
     <img class="desk-decor" src="/api/random-desk-decor?keyword={摆件名}" />
    `
  },
  daily_tips: {
    key: "daily_tips",
    label: "每日贴士",
    description: "基于分析的实用建议",
    icon: "💡",
    required: true,
    prompt: "请根据已输出的所有内容，总结12到20条实用的tips，这些tips用于长时间轮播提示给用户，请尽可能涵盖已输出内容的重点信息",
    template: `
    ## 🎯总结

    ## 基于以上内容, 总结今日tips信息:

    <div class="fortune-tip">{tip信息}</div>
    `
  },
};

/**
 * 获取所有可用的栏目
 */
const getAllFortuneSections = () => {
  return Object.values(FORTUNE_SECTIONS);
};

/**
 * 根据key获取栏目配置
 */
const getFortuneSectionByKey = (key) => {
  return FORTUNE_SECTIONS[key];
};

/**
 * 获取必填栏目
 */
const getRequiredFortuneSections = () => {
  return Object.values(FORTUNE_SECTIONS).filter(section => section.required).map(section => section.key);
};

/**
 * 获取默认选中的栏目
 */
const getDefaultFortuneSections = () => {
  const allSections = Object.keys(FORTUNE_SECTIONS);
  // 确保必填栏目始终包含在默认配置中
  const requiredSections = getRequiredFortuneSections();
  const sectionsWithRequired = [...new Set([...allSections, ...requiredSections])];
  return sectionsWithRequired;
};

/**
 * 根据用户选择的栏目构建提示词部分
 */
const buildSectionsPrompt = (selectedSections) => {
  if (!selectedSections || selectedSections.length === 0) {
    return { promptInstructions: "", outputFormat: "" };
  }

  // 收集选中栏目的提示词
  const promptInstructions = selectedSections.map(sectionKey => {
    const section = FORTUNE_SECTIONS[sectionKey];
    if (!section?.prompt) return "";
    return section.prompt;
  }).filter(prompt => prompt !== "").join('\n\n');

  // 收集选中栏目的输出格式
  const outputFormat = selectedSections.map(sectionKey => {
    const section = FORTUNE_SECTIONS[sectionKey];
    if (!section?.template) return "";
    return section.template;
  }).filter(template => template !== "").join('\n\n');

  return {
    promptInstructions,
    outputFormat
  };
};

/**
 * 构建完整的prompt（兼容旧版本）
 */
const buildSectionsPromptLegacy = (selectedSections) => {
  const { promptInstructions, outputFormat } = buildSectionsPrompt(selectedSections);
  
  if (!promptInstructions && !outputFormat) {
    return "";
  }

  return `

请根据以下要求输出对应的栏目内容：

${promptInstructions}

请按照以下格式输出相应的栏目：

${outputFormat}

`;
};

module.exports = {
  FORTUNE_SECTIONS,
  getAllFortuneSections,
  getFortuneSectionByKey,
  getRequiredFortuneSections,
  getDefaultFortuneSections,
  buildSectionsPrompt,
  buildSectionsPromptLegacy
}; 
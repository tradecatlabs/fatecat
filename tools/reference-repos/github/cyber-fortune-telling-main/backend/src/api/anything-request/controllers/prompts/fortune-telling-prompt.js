const moment = require("moment");
const { getEnumLabel } = require("../../../../config/enum-mappings");
const { buildSectionsPrompt } = require("../../../../config/fortune-sections");

// 默认选中的算命栏目配置
const DEFAULT_FORTUNE_SECTIONS = [
  "prophecy",
  "health_advice", 
  "fortune_analysis",
  // "entertainment_places",
  // "healthy_food",
  "traditional_calendar",
  "prophecy_explanation",
  // 这两个是默认的
  "feng_shui_decoration",
  "daily_tips",
];

/**
 * Builds the fortune telling prompt based on user information
 * @param {Object} user - User information including birth details
 * @returns {string} Formatted prompt for the LLM
 */
const buildFortuneTellingPrompt = (user) => {
  // 基于 "水晶洞","金蟾","貔貅","文昌塔", "关公像","龙龟","葫芦","福禄寿三星","五帝钱", "大象" 随机抽取3个摆件
  const availableDecor = ["水晶洞","金蟾","貔貅","文昌塔", "关公像","龙龟","葫芦","福禄寿三星","五帝钱", "大象"];
  const randomDecor = availableDecor.sort(() => Math.random() - 0.5).slice(0, 3);
  const decorString = randomDecor.join(",");

  const currentDate = moment().format("YYYY-MM-DD");

  // 获取用户详细信息变量
  // 基本身体信息
  const userHeight = user.height || null; // 身高（米）
  const userWeight = user.weight || null; // 体重（公斤）
  const userProfession = user.profession || null; // 职业

  // 健康状况信息
  const userConstitutionType = user.constitution_type || null; // 体质类型（原始值）
  const userConstitutionTypeLabel = userConstitutionType ? getEnumLabel('constitution_type', userConstitutionType) : null; // 体质类型（显示文本）
  
  const userSleepQuality = user.sleep_quality || null; // 睡眠质量（原始值）
  const userSleepQualityLabel = userSleepQuality ? getEnumLabel('sleep_quality', userSleepQuality) : null; // 睡眠质量（显示文本）
  
  const userExerciseFrequency = user.exercise_frequency || null; // 运动频率（原始值）
  const userExerciseFrequencyLabel = userExerciseFrequency ? getEnumLabel('exercise_frequency', userExerciseFrequency) : null; // 运动频率（显示文本）

  // 症状和偏好信息（数组类型）
  const userCommonSymptoms = user.common_symptoms || []; // 常见症状列表
  const userDietaryPreferences = user.dietary_preferences || []; // 饮食偏好列表
  const userBodyDiscomfort = user.body_discomfort || []; // 身体不适部位列表

  // 补充说明
  const userHealthInfo = user.health_info || null; // 健康信息补充说明

  // 获取用户选择的栏目配置，如果没有则使用默认配置
  let selectedSections = user.fortune_sections || DEFAULT_FORTUNE_SECTIONS;
  
  // 确保必填栏目始终包含在选择中
  const { getRequiredFortuneSections } = require("../../../../config/fortune-sections");
  const requiredSections = getRequiredFortuneSections();
  const sectionsWithRequired = [...new Set([...selectedSections, ...requiredSections])];
  
  // 使用包含必填项的栏目列表
  selectedSections = sectionsWithRequired;

  // 使用新的插件化结构构建prompt
  const { promptInstructions, outputFormat } = buildSectionsPrompt(selectedSections);

  // 构建基础信息部分
  const baseInfo = `
    我是${user.username}，出生信息如下：
    - 出生日期：${user.birth_date} (阳历)
    - 出生时间：${user.birth_time}
    - 性别：${user.gender === "male" ? "男性" : "女性"}

    我的身高是：${userHeight}米，体重是：${userWeight}公斤，职业是：${userProfession}

    我的健康状况是：${userConstitutionTypeLabel}，睡眠质量是：${userSleepQualityLabel}，运动频率是：${userExerciseFrequencyLabel}

    我的常见症状是：${userCommonSymptoms.length > 0 ? userCommonSymptoms.join('、') : '无'}，饮食偏好是：${userDietaryPreferences.length > 0 ? userDietaryPreferences.join('、') : '无'}，身体不适部位是：${userBodyDiscomfort.length > 0 ? userBodyDiscomfort.join('、') : '无'}

    我的健康信息补充说明是：${userHealthInfo}
  
    今天的日期是：${currentDate}

    目前可用的摆件列表: ${decorString}

    输出文本时可以使用一些Emoji来增加趣味性，但不要过多，可以参考100个字一个Emoji

    ## 请根据以下要求输出对应的栏目内容：

    ${promptInstructions}

    ## 请按照以下格式输出相应的栏目：

    ${outputFormat}
  `;

  return baseInfo;
};

module.exports = {
  buildFortuneTellingPrompt
}; 
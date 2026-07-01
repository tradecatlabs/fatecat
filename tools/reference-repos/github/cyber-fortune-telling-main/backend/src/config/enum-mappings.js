'use strict';

/**
 * 枚举值映射配置
 * 这个文件集中管理所有的枚举值和它们对应的显示文本
 */

const ENUM_MAPPINGS = {
  // 体质类型映射
  constitution_type: {
    "pinghe": "平和质 (身体健康，精力充沛)",
    "qixu": "气虚质 (容易疲劳，说话声音小)",
    "yangxu": "阳虚质 (怕冷，手脚冰凉)",
    "yinxu": "阴虚质 (容易上火，口干舌燥)",
    "tanshi": "痰湿质 (身体沉重，容易发胖)",
    "shire": "湿热质 (面部油腻，口苦口臭)",
    "xueyu": "血瘀质 (面色暗沉，容易淤青)",
    "qiyu": "气郁质 (情绪低落，容易焦虑)",
    "tebing": "特禀质 (过敏体质，容易过敏)"
  },
  
  // 睡眠质量映射
  sleep_quality: {
    "excellent": "很好 (深度睡眠，精力充沛)",
    "good": "良好 (入睡容易，偶尔失眠)",
    "average": "一般 (浅睡多梦，时有疲劳)",
    "poor": "较差 (难以入睡，经常醒来)",
    "very_poor": "很差 (严重失眠，白天困乏)"
  },
  
  // 运动频率映射
  exercise_frequency: {
    "daily": "每天 (坚持日常锻炼)",
    "frequent": "经常运动 (每周3-5次)",
    "occasional": "偶尔运动 (每周1-2次)",
    "rarely": "很少运动 (每月几次)",
    "never": "不运动 (基本不锻炼)"
  },

  // 性别映射
  gender: {
    "male": "男",
    "female": "女"
  },

  // 常见症状列表（用于前端多选）
  common_symptoms_options: [
    "失眠多梦", "头痛头晕", "胃痛胃胀", "便秘", "腹泻", 
    "疲劳乏力", "心悸气短", "咳嗽痰多", "腰痛", "关节痛",
    "口干舌燥", "手脚冰凉", "易出汗", "食欲不振", "记忆力减退"
  ],

  // 饮食偏好列表（用于前端多选）
  dietary_preferences_options: [
    "偏爱辛辣", "偏爱甜食", "偏爱油腻", "偏爱生冷", 
    "偏爱热食", "清淡饮食", "素食主义", "不规律饮食",
    "爱喝冷饮", "爱吃烧烤", "宵夜习惯", "暴饮暴食"
  ],

  // 身体不适部位列表（用于前端多选）
  body_discomfort_options: [
    "头部", "颈部", "肩部", "背部", "腰部", 
    "腹部", "腿部", "脚部", "手部", "胸部",
    "眼部", "咽喉", "膝盖", "脚踝"
  ]
};

/**
 * 获取指定字段的枚举映射
 * @param {string} fieldName - 字段名
 * @returns {Object|null} 对应的枚举映射
 */
function getEnumMapping(fieldName) {
  return ENUM_MAPPINGS[fieldName] || null;
}

/**
 * 获取所有枚举映射
 * @returns {Object} 所有枚举映射
 */
function getAllEnumMappings() {
  return ENUM_MAPPINGS;
}

/**
 * 获取枚举值对应的显示文本
 * @param {string} fieldName - 字段名
 * @param {string} value - 枚举值
 * @returns {string} 显示文本，如果没有找到则返回原值
 */
function getEnumLabel(fieldName, value) {
  const mapping = getEnumMapping(fieldName);
  return mapping ? (mapping[value] || value) : value;
}

/**
 * 映射用户数据的枚举值，添加对应的标签字段
 * @param {Object} userData - 用户数据
 * @returns {Object} 包含标签字段的用户数据
 */
function mapUserEnumValues(userData) {
  if (!userData) return userData;
  
  const mappedData = { ...userData };
  
  // 映射体质类型
  if (mappedData.constitution_type) {
    mappedData.constitution_type_label = getEnumLabel('constitution_type', mappedData.constitution_type);
  }
  
  // 映射睡眠质量
  if (mappedData.sleep_quality) {
    mappedData.sleep_quality_label = getEnumLabel('sleep_quality', mappedData.sleep_quality);
  }
  
  // 映射运动频率
  if (mappedData.exercise_frequency) {
    mappedData.exercise_frequency_label = getEnumLabel('exercise_frequency', mappedData.exercise_frequency);
  }

  // 映射性别
  if (mappedData.gender) {
    mappedData.gender_label = getEnumLabel('gender', mappedData.gender);
  }
  
  return mappedData;
}

/**
 * 生成用户完整描述文本（用于大模型推理）
 * @param {Object} userData - 用户数据
 * @returns {string} 完整的用户描述文本
 */
function getUserDescriptionText(userData) {
  if (!userData) return '';
  
  let description = '';
  
  // 基本信息
  if (userData.username) description += `姓名：${userData.username}；`;
  if (userData.gender) description += `性别：${getEnumLabel('gender', userData.gender)}；`;
  if (userData.birth_date) description += `出生日期：${userData.birth_date}；`;
  if (userData.birth_time) description += `出生时间：${userData.birth_time}；`;
  
  // 身体信息
  if (userData.height) description += `身高：${userData.height}米；`;
  if (userData.weight) description += `体重：${userData.weight}公斤；`;
  if (userData.profession) description += `职业：${userData.profession}；`;
  
  // 健康信息
  if (userData.constitution_type) {
    const label = getEnumLabel('constitution_type', userData.constitution_type);
    description += `体质类型：${label}；`;
  }
  
  if (userData.sleep_quality) {
    const label = getEnumLabel('sleep_quality', userData.sleep_quality);
    description += `睡眠质量：${label}；`;
  }
  
  if (userData.exercise_frequency) {
    const label = getEnumLabel('exercise_frequency', userData.exercise_frequency);
    description += `运动频率：${label}；`;
  }
  
  if (userData.common_symptoms && userData.common_symptoms.length > 0) {
    description += `常见症状：${userData.common_symptoms.join('、')}；`;
  }
  
  if (userData.dietary_preferences && userData.dietary_preferences.length > 0) {
    description += `饮食偏好：${userData.dietary_preferences.join('、')}；`;
  }
  
  if (userData.body_discomfort && userData.body_discomfort.length > 0) {
    description += `身体不适部位：${userData.body_discomfort.join('、')}；`;
  }
  
  if (userData.health_info) {
    description += `补充说明：${userData.health_info}；`;
  }
  
  return description;
}

module.exports = {
  ENUM_MAPPINGS,
  getEnumMapping,
  getAllEnumMappings,
  getEnumLabel,
  mapUserEnumValues,
  getUserDescriptionText
}; 
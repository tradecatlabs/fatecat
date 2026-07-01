'use strict';

/**
 * fortune-telling-user service
 */

const { createCoreService } = require('@strapi/strapi').factories;
const { 
  getAllEnumMappings, 
  mapUserEnumValues, 
  getUserDescriptionText 
} = require('../../../config/enum-mappings');

module.exports = createCoreService('api::fortune-telling-user.fortune-telling-user', ({ strapi }) => ({
  // 重写 find 方法
  async find(params) {
    const { results, pagination } = await super.find(params);
    
    // 为每个结果添加映射字段
    const mappedResults = results.map(result => {
      const mappedData = mapUserEnumValues(result);
      // 添加完整描述文本
      mappedData.description_text = getUserDescriptionText(result);
      return mappedData;
    });
    
    return { results: mappedResults, pagination };
  },
  
  // 重写 findOne 方法
  async findOne(entityId, params) {
    const result = await super.findOne(entityId, params);
    
    if (result) {
      const mappedData = mapUserEnumValues(result);
      // 添加完整描述文本
      mappedData.description_text = getUserDescriptionText(result);
      return mappedData;
    }
    
    return result;
  },
  
  // 导出映射配置供其他地方使用
  getEnumMappings() {
    return getAllEnumMappings();
  },
  
  // 导出用户描述文本生成函数
  getUserDescriptionText
}));

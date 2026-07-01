'use strict';

/**
 * fortune-telling-user controller
 */

const { createCoreController } = require('@strapi/strapi').factories;

module.exports = createCoreController('api::fortune-telling-user.fortune-telling-user', ({ strapi }) => ({
  // 获取枚举映射配置
  async getEnumMappings(ctx) {
    try {
      const service = strapi.service('api::fortune-telling-user.fortune-telling-user');
      const mappings = service.getEnumMappings();
      
      ctx.body = {
        data: mappings
      };
    } catch (error) {
      ctx.throw(500, '获取枚举映射失败');
    }
  },

  // 获取占卜栏目配置
  async getFortuneSections(ctx) {
    try {
      const { getAllFortuneSections } = require('../../../config/fortune-sections');
      const sections = getAllFortuneSections();
      
      ctx.body = {
        data: sections
      };
    } catch (error) {
      ctx.throw(500, '获取占卜栏目配置失败');
    }
  }
}));

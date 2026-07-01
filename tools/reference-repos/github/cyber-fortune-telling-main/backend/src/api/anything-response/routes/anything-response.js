'use strict';

/**
 * anything-response router
 */

const { createCoreRouter } = require('@strapi/strapi').factories;

module.exports = createCoreRouter('api::anything-response.anything-response', {
  config: {
    find: {
      auth: false,  // 允许公开访问，无需认证
    },
    findOne: {
      auth: false,  // 允许公开访问，无需认证
    },
    create: {
      auth: false,  // 允许公开访问，无需认证
    },
    update: {
      auth: false,  // 允许公开访问，无需认证
    },
    delete: {
      auth: false,  // 允许公开访问，无需认证
    },
  },
});

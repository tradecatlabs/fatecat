'use strict';

/**
 * Custom routes for fortune-telling-user
 */

module.exports = {
  routes: [
    {
      method: 'GET',
      path: '/fortune-telling-users/enum-mappings',
      handler: 'api::fortune-telling-user.fortune-telling-user.getEnumMappings',
      config: {
        auth: false,
        policies: [],
        middlewares: [],
      },
    },
    {
      method: 'GET',
      path: '/fortune-telling-users/fortune-sections',
      handler: 'api::fortune-telling-user.fortune-telling-user.getFortuneSections',
      config: {
        auth: false,
        policies: [],
        middlewares: [],
      },
    },
  ],
}; 
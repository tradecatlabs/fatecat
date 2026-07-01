'use strict';

/**
 * sign-in router
 */

module.exports = {
  routes: [
    {
      method: 'POST',
      path: '/sign-in',
      handler: 'sign-in.signIn',
      config: {
        policies: [],
        middlewares: [],
        auth: false,  // 允许公开访问，无需认证
      },
    },
    {
      method: 'GET',
      path: '/sign-in/dates',
      handler: 'sign-in.getSignInDates',
      config: {
        policies: [],
        middlewares: [],
        auth: false,  // 允许公开访问，无需认证
      },
    },
  ],
};

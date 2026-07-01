module.exports = {
  routes: [
    {
     method: 'GET',
     path: '/get-tips',
     handler: 'get-tips.getTips',
     config: {
       policies: [],
       middlewares: [],
       auth: false,  // 允许公开访问，无需认证
     },
    },
  ],
};

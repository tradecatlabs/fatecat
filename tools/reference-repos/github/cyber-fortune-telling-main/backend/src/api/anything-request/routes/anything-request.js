module.exports = {
  routes: [
    {
     method: 'GET',
     path: '/anything-request',
     handler: 'anything-request.generateFortuneTelling',
     config: {
       policies: [],
       middlewares: [],
       auth: false,  // 允许公开访问，无需认证
     },
    },
    {
      method: 'GET',
      path: '/anything-request/getConversationIdAndHistory',
      handler: 'anything-request.getConversationIdAndHistory',
      config: {
        policies: [],
        middlewares: [],
        auth: false,  // 允许公开访问，无需认证
      },  
    },
    {
      method: 'POST',
      path: '/anything-request/getAnswerFromLLM',
      handler: 'anything-request.getAnswerFromLLM',
      config: {
        policies: [],
        middlewares: [],
        auth: false,  // 允许公开访问，无需认证
      },
    },
    // getInfoForDeskDecor
    {
      method: 'GET',
      path: '/anything-request/getInfoForDeskDecor',
      handler: 'anything-request.getInfoForDeskDecor',
      config: {
        policies: [],
        middlewares: [],
        auth: false,  // 允许公开访问，无需认证
      },
    }
  ],
};

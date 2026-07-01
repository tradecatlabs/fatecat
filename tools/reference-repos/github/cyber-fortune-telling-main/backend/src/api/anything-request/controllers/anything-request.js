'use strict';

/**
 * Controller for handling fortune telling requests
 * This module provides functionality to generate fortune telling predictions
 * using various LLM providers (NVIDIA/DeepSeek, OpenAI)
 */

const { Chatbot, ChatGPTInput, SupportedChatModels } = require("intellinode");
const moment = require("moment");
const OpenAI = require("openai");
const { buildFortuneTellingPrompt } = require("./prompts/fortune-telling-prompt");
const { v4: uuid } = require('uuid');
/**
 * Delays execution for a specified number of milliseconds
 * @param {number} ms - Number of milliseconds to delay
 * @returns {Promise} Promise that resolves after the delay
 */
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * LLM Provider Configurations
 * Contains API keys, model specifications and client configurations for different LLM providers
 */
const LLM_CONFIG = {
  // DeepSeek Configuration
  DEEPSEEK: {
    key: process.env.OPENAI_API_KEY,
    model: 'deepseek-chat',
    provider: 'deepseek',
    // @ts-ignore
    client: new OpenAI({
      baseURL: process.env.OPENAI_BASE_URL,
      apiKey: process.env.OPENAI_API_KEY
    })
  },
};

/**
 * Creates an LLM client based on the specified provider
 * @param {string} provider - The LLM provider to use (default: 'DEEPSEEK')
 * @returns {Object} The configured LLM client
 * @throws {Error} If provider is unsupported or API key is missing
 */
const createLLMClient = (provider = 'DEEPSEEK') => {
  const config = LLM_CONFIG[provider];
  
  // Validate provider and API key
  if (!config) {
    throw new Error(`Unsupported LLM provider: ${provider}`);
  }
  if (!config.key) {
    throw new Error(`API key not found for provider: ${provider}`);
  }
  
  // Return appropriate client configuration based on provider
  return config.provider === 'deepseek' 
    ? { client: config.client, model: config.model }
    : { chatbot: new Chatbot(config.key, config.provider), input: config.createInput("You are an insightful fortune teller.") };
};

/**
 * Sets up SSE (Server-Sent Events) headers for streaming response
 * @param {Object} res - HTTP response object
 */
const setupSSEHeaders = (res) => {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'X-Accel-Buffering': 'no'
  });
};

module.exports = {
  /**
   * Main action handler for fortune telling requests
   * Supports streaming responses using SSE
   */
  generateFortuneTelling: async (ctx, next) => {
    try {
      // Extract query parameters
      const { query } = ctx.request;
      const fortune_telling_uid = query.fortune_telling_uid;
      const provider = query.provider?.toUpperCase() || 'DEEPSEEK';
      
      // Fetch user data from database first to get updated timestamp
      const results = await strapi.entityService.findMany('api::fortune-telling-user.fortune-telling-user', {
        filters: { fortune_telling_uid },
      });
      const fortune_telling_user = results && results.length > 0 ? results[0] : null;
      
      if (!fortune_telling_user) {
        ctx.throw(404, '用户不存在');
      }
      
      console.log("User data retrieved:", fortune_telling_user);

      // Check cache with both URL and user updated timestamp
      const requestUrl = ctx.request.url;
      const userUpdatedAt = fortune_telling_user.updatedAt;

      // 日志：打印缓存命中条件的实际值
      console.log("[Cache Check] requestUrl:", requestUrl);
      console.log("[Cache Check] userUpdatedAt:", userUpdatedAt);
      
      const cachedResults = await strapi.entityService.findMany('api::anything-response.anything-response', {
        filters: { 
          request_url: requestUrl,
          user_updated_at: userUpdatedAt,
        },
        populate: ['*'],
        publicationState: 'preview'
      });
      const cachedResponse = cachedResults && cachedResults.length > 0 ? cachedResults[0] : null;

      // 详细日志：分析每个条件是否命中
      if (cachedResults && cachedResults.length > 0) {
        // 命中缓存，打印所有缓存项的命中条件
        cachedResults.forEach((item, idx) => {
          console.log(`[Cache Candidate ${idx}] request_url:`, item.request_url, '| user_updated_at:', item.user_updated_at);
          if (item.request_url === requestUrl) {
            console.log(`[Cache Candidate ${idx}] request_url 匹配`);
          } else {
            console.log(`[Cache Candidate ${idx}] request_url 不匹配`);
          }
          if (item.user_updated_at === userUpdatedAt) {
            console.log(`[Cache Candidate ${idx}] user_updated_at 匹配`);
          } else {
            console.log(`[Cache Candidate ${idx}] user_updated_at 不匹配`);
          }
        });
      } else {
        // 没有任何缓存项
        console.log("[Cache Check] 没有找到任何缓存项");
      }

      if (cachedResponse) {
        console.log("Cache hit for URL:", requestUrl, "with user updated at:", userUpdatedAt);
        ctx.respond = false;
        setupSSEHeaders(ctx.res);
        // Send cached response in chunks to simulate streaming
        const responseData = cachedResponse.response_data;
        const content = responseData.content || '';
        const chunkSize = 100; // 每段100字符
        for (let i = 0; i < content.length; i += chunkSize) {
          const chunk = content.slice(i, i + chunkSize);
          ctx.res.write(`data: ${JSON.stringify({ content: chunk })}\n\n`);
          await delay(100); // 添加0.1秒延迟
        }
        ctx.res.write('data: [DONE]\n\n');
        ctx.res.end();
        return;
      }

      console.log("Cache miss - proceeding with LLM request");
      
      // Setup streaming response
      ctx.respond = false;
      setupSSEHeaders(ctx.res);

      // Initialize LLM client and generate response
      const client = createLLMClient(provider);
      const systemPrompt = "You are an insightful fortune teller.";
      const prompt = buildFortuneTellingPrompt(fortune_telling_user);
      
      let fullResponse = ''; // Store complete response for caching

      if (client.client) {
        // Handle DeepSeek API streaming
        const stream = await client.client.chat.completions.create({
          model: client.model,
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: prompt }
          ],
          stream: true
        });

        for await (const chunk of stream) {
          const content = chunk.choices[0]?.delta?.content || '';
          if (content) {
            fullResponse += content;
            // console.log('Streaming chunk:', content);
            ctx.res.write(`data: ${JSON.stringify({ content })}\n\n`);
            await delay(100); // 添加0.1秒延迟
          }
        }
      } else {
        // Handle other providers (OpenAI, etc)
        client.input.addUserMessage(prompt);
        for await (const chunk of client.chatbot.stream(client.input)) {
          fullResponse += chunk;
          ctx.res.write(`data: ${JSON.stringify({ content: chunk })}\n\n`);
          await delay(100); // 添加0.1秒延迟
        }
      }
      
      // Create and publish response to cache, 写入成功后，打印日志
      const cacheData = {
        request_url: requestUrl,
        user_updated_at: userUpdatedAt, // 添加用户信息更新时间
        conversation_id: uuid() + "_" + moment().format('YYYYMMDDHHmmss'), // 会话id
        conversation_history: [
          {
            role: 'system',
            content: systemPrompt
          },
          {
            role: 'user',
            content: prompt
          },
          {
            role: 'assistant',
            content: fullResponse
          }
        ],
        response_data: {
          content: fullResponse,
          timestamp: new Date().toISOString(),
          provider: provider
        },
        publishedAt: new Date(),
      }

      // 使用 entityService.create 语法
      await strapi.entityService.create('api::anything-response.anything-response', {
        data: cacheData,
      });
      console.log("缓存数据写入成功:", cacheData);

      // Send completion signal
      ctx.res.write('data: [DONE]\n\n');
      ctx.res.end();
    } catch (err) {
      console.error('Error:', err);
      if (!ctx.respond) {
        // Send error event if streaming has started
        ctx.res.write(`event: error\ndata: ${JSON.stringify({ error: err.message })}\n\n`);
        ctx.res.end();
      } else {
        ctx.throw(500, err);
      }
    }
  },


  // 获取会话id和历史记录
  getConversationIdAndHistory: async (ctx, next) => {
    try {
      let tmpRequestUrl = ctx.request.url;
      let requestUrl = tmpRequestUrl.replace("/anything-request/getConversationIdAndHistory", "/anything-request");
      
      // 从 URL 中提取 fortune_telling_uid 参数
      const urlParams = new URL(requestUrl, 'http://localhost').searchParams;
      const fortune_telling_uid = urlParams.get('fortune_telling_uid');
      
      if (!fortune_telling_uid) {
        ctx.throw(400, '缺少 fortune_telling_uid 参数');
      }
      
      // 获取用户信息和更新时间
      const userResults = await strapi.entityService.findMany('api::fortune-telling-user.fortune-telling-user', {
        filters: { fortune_telling_uid },
      });
      const fortune_telling_user = userResults && userResults.length > 0 ? userResults[0] : null;
      
      if (!fortune_telling_user) {
        ctx.throw(404, '用户不存在');
      }
      
      const userUpdatedAt = fortune_telling_user.updatedAt;
      
      // 通过 requestUrl 和用户更新时间获取会话id和历史记录
      const results = await strapi.entityService.findMany('api::anything-response.anything-response', {
        filters: { 
          request_url: requestUrl,
          user_updated_at: userUpdatedAt 
        },
        populate: ['*']
      });
      const anythingResponse = results && results.length > 0 ? results[0] : null;

      // 查询到的缓存信息
      console.log("查询到的缓存信息:", anythingResponse);

      if (!anythingResponse) {
        ctx.body = {
          conversation_id: null,
          conversation_history: []
        };
        return;
      }

      // console.log("anythingResponse", anythingResponse);
      let conversation_history = anythingResponse.conversation_history
      console.log("查询到的缓存conversation_history:", conversation_history);
      // 前两条是固定的提示词格式，不返回给前端
      // 如果会话历史记录小于3条，或conversation_history为null，则返回空数组
      if (!Array.isArray(conversation_history) || conversation_history.length < 3) {
        conversation_history = [];
      } else {
        conversation_history = conversation_history.slice(3);
      }
      // 将会话id和历史记录返回给前端
      const responseData = {
        conversation_id: anythingResponse.conversation_id,
        conversation_history: conversation_history
      }
      // 用户查询的历史记录
      console.log("history:", responseData);
      ctx.body = responseData;
    } catch (err) {
      console.error('getConversationIdAndHistory Error:', err);
      ctx.throw(500, err.message);
    }
  },

  // 用户传入会话id, 和提问prompt, 在数据库查询对应的会话和历史记录, 构建上下文，向LLM请求回答, 流式输出给前端
  getAnswerFromLLM: async (ctx, next) => {
    try {
      const { body } = ctx.request;
      const newBody = JSON.parse(body);
      const conversation_id = newBody.conversationId;
      const prompt = newBody.prompt;

      // 打印
      console.log("对应的 conversation_id:", conversation_id);
      console.log("新的prompt:", prompt);
      
      // 通过 conversationId 获取会话和历史记录
      const results = await strapi.entityService.findMany('api::anything-response.anything-response', {
        filters: { conversation_id: conversation_id },
        populate: ['*']
      });
      const anythingResponse = results && results.length > 0 ? results[0] : null;

      if (!anythingResponse) {
        ctx.respond = false;
        ctx.res.writeHead(200, {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
          'X-Accel-Buffering': 'no'
        });
        ctx.res.write(`event: error\ndata: ${JSON.stringify({ error: '会话不存在' })}\n\n`);
        ctx.res.write('data: [DONE]\n\n');
        ctx.res.end();
        return;
      }

      // 构建上下文
      const provider = newBody.provider?.toUpperCase() || 'DEEPSEEK';
      // 向LLM请求回答
      const client = createLLMClient(provider);

      ctx.respond = false;
      ctx.res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Accel-Buffering': 'no'
      });

      // 如果历史的长度小于30条，则触发请求，如果大于30条，则返回"明天再来"

      if (anythingResponse.conversation_history.length < 30) {
        if (client.client) {
          let messages = Array.isArray(anythingResponse.conversation_history) ? [...anythingResponse.conversation_history] : [];
          messages.push({ role: "user", content: prompt });
  
          // 打印
          console.log("发起新请求的messages:", messages);
          const stream = await client.client.chat.completions.create({
            model: client.model,
            messages: messages,
            stream: true
          });
  
          // 记录流式输出的内容
          let fullResponse = '';
  
          // 流式输出给前端
          for await (const chunk of stream) {
            const content = chunk.choices[0]?.delta?.content || '';
            if (content) {
              ctx.res.write(`data: ${JSON.stringify({ content })}\n\n`);
              fullResponse += content;
              // console.log("fullResponse", fullResponse);
              await delay(100); // 添加0.1秒延迟
            }
          }
  
          let conversation_history = anythingResponse.conversation_history || [];
          conversation_history.push({ role: "user", content: prompt });
          conversation_history.push({ role: "assistant", content: fullResponse });
          // 更新到数据库的conversation_history
          console.log("更新到数据库的conversation_history:", conversation_history, "对应的id", conversation_id);
          // 然后 update
          if (anythingResponse && anythingResponse.id) {
            await strapi.entityService.update('api::anything-response.anything-response', anythingResponse.id, {
              data: {
                conversation_history: conversation_history,
              }
            });
          }
  
          ctx.res.write('data: [DONE]\n\n');
          ctx.res.end();
        }
      } else {
        // 返回"明天再来"
        ctx.res.write(`data: ${JSON.stringify({ content: "明天再来" })}\n\n`);
        ctx.res.write('data: [DONE]\n\n');
        ctx.res.end();
        return;
      }
    } catch (err) {
      console.error('getAnswerFromLLM Error:', err);
      try {
        ctx.respond = false;
        ctx.res.writeHead(200, {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
          'X-Accel-Buffering': 'no'
        });
        ctx.res.write(`event: error\ndata: ${JSON.stringify({ error: err.message })}\n\n`);
        ctx.res.write('data: [DONE]\n\n');
        ctx.res.end();
      } catch (e) {
        // 如果流已关闭或响应已发送，忽略
      }
    }
  },


  getInfoForDeskDecor: async (ctx, next) => {
    try {
      console.log("getInfoForDeskDecor");

      let tmpRequestUrl = ctx.request.url;
      let requestUrl = tmpRequestUrl.replace("/anything-request/getInfoForDeskDecor", "/anything-request");

      // 从 URL 中提取 fortune_telling_uid 参数
      const urlParams = new URL(requestUrl, 'http://localhost').searchParams;
      const fortune_telling_uid = urlParams.get('fortune_telling_uid');
      
      if (!fortune_telling_uid) {
        ctx.throw(400, '缺少 fortune_telling_uid 参数');
      }
      
      // 获取用户信息和更新时间
      const userResults = await strapi.entityService.findMany('api::fortune-telling-user.fortune-telling-user', {
        filters: { fortune_telling_uid },
      });
      const fortune_telling_user = userResults && userResults.length > 0 ? userResults[0] : null;
      
      if (!fortune_telling_user) {
        ctx.throw(404, '用户不存在');
      }
      
      const userUpdatedAt = fortune_telling_user.updatedAt;

      // 通过 requestUrl 和用户更新时间获取会话id和历史记录
      const results = await strapi.entityService.findMany('api::anything-response.anything-response', {
        filters: { 
          request_url: requestUrl,
          user_updated_at: userUpdatedAt 
        },
        populate: ['*']
      });
      const anythingResponse = results && results.length > 0 ? results[0] : null;

      // 查询到的缓存信息
      console.log("查询到的缓存信息:", anythingResponse);

      let conversation_history = [];

      if(anythingResponse){
        let conversation_history = anythingResponse.conversation_history;
        console.log("查询到的缓存conversation_history:", conversation_history);
        // 前两条是固定的提示词格式，不返回给前端
        // 如果会话历史记录小于3条，或conversation_history为null，则返回空数组
        if (!Array.isArray(conversation_history) || conversation_history.length < 3) {
          conversation_history = [];
        }
    
        // 取第三条（原始的第三条，index 2）
        let tips = [];
        let deskDecor = null;
        if (conversation_history[2] && conversation_history[2].content) {
          // 提取 fortune-tip 内容
          const tipMatches = conversation_history[2].content.match(/<div class="fortune-tip">([^<]+)<\/div>/g) || [];
          tips = tipMatches.map(tip => {
            const match = tip.match(/<div class="fortune-tip">([^<]+)<\/div>/);
            return match ? match[1] : '';
          });
    
          // 提取 desk-decor keyword
          const deskDecorMatch = conversation_history[2].content.match(/<img class="desk-decor" src="([^"]+)" \/>/);
          if (deskDecorMatch && deskDecorMatch[1]) {
            const keywordMatch = deskDecorMatch[1].match(/keyword=([^&"]+)/);
            deskDecor = keywordMatch ? keywordMatch[1] : null;
          }
        }
    
        const responseData = {
          tips,
          deskDecor
        };
        ctx.body = responseData;
      } else {
        conversation_history = [];
        const responseData = {
          tips: ["今天是个好日子"],
          deskDecor: "貔貅"
        };
        ctx.body = responseData;
      }
    } catch (err) {
      console.error('getInfoForDeskDecor Error:', err);
      ctx.throw(500, err.message);
    }
  }
};

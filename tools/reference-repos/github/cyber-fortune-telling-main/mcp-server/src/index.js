#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import axios from 'axios';

/**
 * MCP Server for Cyber Fortune Telling API
 * Wraps the existing Strapi API endpoints as MCP tools
 */

// Default API base URL - can be overridden via environment variable
const API_BASE_URL = process.env.CYBER_FORTUNE_API_BASE_URL || 'http://localhost:11337/api';

/**
 * Makes HTTP requests to the fortune telling API
 */
async function makeApiRequest(endpoint, options = {}) {
  try {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await axios({
      url,
      timeout: 30000, // 30 second timeout
      ...options
    });
    
    return {
      success: true,
      data: response.data,
      status: response.status,
      headers: response.headers
    };
  } catch (error) {
    console.error(`API Request failed for ${endpoint}:`, error.message);
    return {
      success: false,
      error: error.message,
      status: error.response?.status || 500,
      data: error.response?.data || null
    };
  }
}

/**
 * Handles streaming responses from fortune telling endpoints
 */
async function handleStreamingRequest(endpoint, options = {}) {
  try {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await axios({
      url,
      method: 'GET',
      responseType: 'stream',
      timeout: 60000, // 60 second timeout for streaming
      ...options
    });

    return new Promise((resolve, reject) => {
      let fullContent = '';
      let chunks = [];

      response.data.on('data', (chunk) => {
        const chunkStr = chunk.toString();
        chunks.push(chunkStr);
        
        // Parse SSE data
        const lines = chunkStr.split('\n');
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') {
              resolve({
                success: true,
                content: fullContent,
                chunks: chunks,
                status: response.status
              });
              return;
            }
            try {
              const parsed = JSON.parse(data);
              if (parsed.content) {
                fullContent += parsed.content;
              }
            } catch (e) {
              // Ignore JSON parse errors
            }
          }
        }
      });

      response.data.on('end', () => {
        resolve({
          success: true,
          content: fullContent,
          chunks: chunks,
          status: response.status
        });
      });

      response.data.on('error', (error) => {
        reject({
          success: false,
          error: error.message,
          status: 500
        });
      });
    });

  } catch (error) {
    console.error(`Streaming request failed for ${endpoint}:`, error.message);
    return {
      success: false,
      error: error.message,
      status: error.response?.status || 500
    };
  }
}

// Create the MCP server
const server = new Server(
  {
    name: "cyber-fortune-telling-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool definitions for all 4 API endpoints
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "generate_fortune_telling",
        description: "Generate fortune telling prediction for a user with streaming response",
        inputSchema: {
          type: "object",
          properties: {
            fortune_telling_uid: {
              type: "string",
              description: "Unique identifier for the fortune telling user"
            },
            date: {
              type: "string",
              description: "Date for the fortune telling prediction (YYYY-MM-DD format)",
              pattern: "^\\d{4}-\\d{2}-\\d{2}$"
            }
          },
          required: ["fortune_telling_uid", "date"]
        }
      },
      {
        name: "get_conversation_history",
        description: "Get conversation ID and chat history for a user's fortune telling session",
        inputSchema: {
          type: "object",
          properties: {
            fortune_telling_uid: {
              type: "string",
              description: "Unique identifier for the fortune telling user"
            },
            date: {
              type: "string",
              description: "Date for the fortune telling session (YYYY-MM-DD format)",
              pattern: "^\\d{4}-\\d{2}-\\d{2}$"
            }
          },
          required: ["fortune_telling_uid", "date"]
        }
      },
      {
        name: "ask_llm_question",
        description: "Ask a follow-up question to the LLM in an existing conversation with streaming response",
        inputSchema: {
          type: "object",
          properties: {
            conversationId: {
              type: "string",
              description: "ID of the existing conversation"
            },
            prompt: {
              type: "string",
              description: "The question or prompt to ask the LLM"
            }
          },
          required: ["conversationId", "prompt"]
        }
      },
      {
        name: "get_desk_decoration_info",
        description: "Get fortune tips and desk decoration recommendations for a user",
        inputSchema: {
          type: "object",
          properties: {
            fortune_telling_uid: {
              type: "string",
              description: "Unique identifier for the fortune telling user"
            },
            date: {
              type: "string",
              description: "Date for the fortune telling session (YYYY-MM-DD format)",
              pattern: "^\\d{4}-\\d{2}-\\d{2}$"
            }
          },
          required: ["fortune_telling_uid", "date"]
        }
      }
    ],
  };
});

// Tool execution handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "generate_fortune_telling": {
        const { fortune_telling_uid, date } = args;
        
        if (!fortune_telling_uid || !date) {
          throw new Error("Missing required parameters: fortune_telling_uid and date");
        }

        const endpoint = `/anything-request?fortune_telling_uid=${encodeURIComponent(fortune_telling_uid)}&date=${encodeURIComponent(date)}`;
        const result = await handleStreamingRequest(endpoint);
        
        if (!result.success) {
          throw new Error(`Failed to generate fortune telling: ${result.error}`);
        }

        return {
          content: [
            {
              type: "text",
              text: `Fortune telling generated successfully!\n\nContent:\n${result.content}`
            }
          ]
        };
      }

      case "get_conversation_history": {
        const { fortune_telling_uid, date } = args;
        
        if (!fortune_telling_uid || !date) {
          throw new Error("Missing required parameters: fortune_telling_uid and date");
        }

        const endpoint = `/anything-request/getConversationIdAndHistory?fortune_telling_uid=${encodeURIComponent(fortune_telling_uid)}&date=${encodeURIComponent(date)}`;
        const result = await makeApiRequest(endpoint, { method: 'GET' });
        
        if (!result.success) {
          throw new Error(`Failed to get conversation history: ${result.error}`);
        }

        return {
          content: [
            {
              type: "text",
              text: `Conversation History Retrieved:\n\nConversation ID: ${result.data.conversation_id || 'None'}\n\nHistory Length: ${result.data.conversation_history?.length || 0} messages\n\nHistory:\n${JSON.stringify(result.data.conversation_history, null, 2)}`
            }
          ]
        };
      }

      case "ask_llm_question": {
        const { conversationId, prompt } = args;
        
        if (!conversationId || !prompt) {
          throw new Error("Missing required parameters: conversationId and prompt");
        }

        const endpoint = `/anything-request/getAnswerFromLLM`;
        const requestBody = {
          conversationId,
          prompt
        };

        // This endpoint expects a POST with streaming response
        const result = await axios({
          url: `${API_BASE_URL}${endpoint}`,
          method: 'POST',
          data: JSON.stringify(requestBody),
          headers: {
            'Content-Type': 'application/json'
          },
          responseType: 'stream',
          timeout: 60000
        }).then(response => {
          return new Promise((resolve, reject) => {
            let fullContent = '';
            let chunks = [];

            response.data.on('data', (chunk) => {
              const chunkStr = chunk.toString();
              chunks.push(chunkStr);
              
              const lines = chunkStr.split('\n');
              for (const line of lines) {
                if (line.startsWith('data: ')) {
                  const data = line.slice(6);
                  if (data === '[DONE]') {
                    resolve({
                      success: true,
                      content: fullContent,
                      chunks: chunks
                    });
                    return;
                  }
                  try {
                    const parsed = JSON.parse(data);
                    if (parsed.content) {
                      fullContent += parsed.content;
                    }
                  } catch (e) {
                    // Ignore JSON parse errors
                  }
                }
              }
            });

            response.data.on('end', () => {
              resolve({
                success: true,
                content: fullContent,
                chunks: chunks
              });
            });

            response.data.on('error', reject);
          });
        }).catch(error => {
          return {
            success: false,
            error: error.message
          };
        });
        
        if (!result.success) {
          throw new Error(`Failed to get LLM answer: ${result.error}`);
        }

        return {
          content: [
            {
              type: "text",
              text: `LLM Response:\n\n${result.content}`
            }
          ]
        };
      }

      case "get_desk_decoration_info": {
        const { fortune_telling_uid, date } = args;
        
        if (!fortune_telling_uid || !date) {
          throw new Error("Missing required parameters: fortune_telling_uid and date");
        }

        const endpoint = `/anything-request/getInfoForDeskDecor?fortune_telling_uid=${encodeURIComponent(fortune_telling_uid)}&date=${encodeURIComponent(date)}`;
        const result = await makeApiRequest(endpoint, { method: 'GET' });
        
        if (!result.success) {
          throw new Error(`Failed to get desk decoration info: ${result.error}`);
        }

        const { tips, deskDecor } = result.data;
        
        return {
          content: [
            {
              type: "text",
              text: `Desk Decoration Info:\n\nDaily Tips:\n${tips?.join('\n') || 'No tips available'}\n\nRecommended Desk Decoration: ${deskDecor || 'No decoration recommended'}`
            }
          ]
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    console.error(`Error executing tool ${name}:`, error);
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`
        }
      ],
      isError: true
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Cyber Fortune Telling MCP Server started");
}

main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
}); 
#!/usr/bin/env node
/**
 * TaiBu MCP Server - Local (stdio)
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

import {
  executeTool,
  buildListToolsPayload,
  buildToolSuccessPayload,
  normalizeTransportDetailLevel,
} from 'taibu-core/mcp';

import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { version } = require('../package.json') as { version: string };

// 创建服务器
const server = new McpServer(
  { name: 'taibu-mcp', version },
  { capabilities: { tools: {} } }
);

// 列出工具
server.server.setRequestHandler(ListToolsRequestSchema, async () => buildListToolsPayload());

// 调用工具
server.server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  try {
    const toolArgs = args === undefined ? {} : args;
    const result = await executeTool(name, toolArgs);
    const detailLevel = normalizeTransportDetailLevel(args?.detailLevel);
    return buildToolSuccessPayload(name, result, { detailLevel });
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return {
      content: [{ type: 'text', text: `Error: ${message}` }],
      isError: true,
    };
  }
});

// 启动服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);

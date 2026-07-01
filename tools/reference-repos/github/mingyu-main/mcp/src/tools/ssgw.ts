import { z } from 'zod';
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { drawRandomSign } from '../../../src/lib/divination/algorithms/ssgw.js';
import { resultOutputSchema } from '../schemas.js';
import {
  createErrorToolResult,
  createStructuredToolResult,
  getErrorMessage,
} from '../tool-results.js';
import { buildCommonDivinationPrompt, extendPromptSchema } from './divination-common.js';

const ssgwSchema = z.object({});

const ssgwPromptSchema = extendPromptSchema(ssgwSchema, '用户希望围绕灵签解读的问题');

export function registerSsgwTool(server: McpServer) {
  server.registerTool(
    'divine_ssgw',
    {
      description:
        '三山国王灵签求签：模拟传统摇签、掷筊流程。随机取签后掷筊确认（一阴一阳为圣杯，两平为笑杯，两凸为阴杯），圣杯确认后方为有效签文；三连阴杯则神明未应、拒绝起卦。返回签题、签诗、典故故事、解签详情及完整掷筊记录（ritual）',
      inputSchema: ssgwSchema.shape,
      outputSchema: resultOutputSchema,
    },
    async (_args) => {
      try {
        const result = drawRandomSign();
        return createStructuredToolResult({ result });
      } catch (error) {
        return createErrorToolResult(getErrorMessage(error, '求签失败'));
      }
    },
  );

  server.registerTool(
    'ssgw_prompt',
    {
      description:
        '三山国王灵签求签并生成结构化 AI 解读提示词：一次调用返回灵签结果（含传统掷筊流程）和可直接复制给 AI 的提示词',
      inputSchema: ssgwPromptSchema.shape,
      outputSchema: {
        result: z.unknown().describe('灵签结果'),
        prompt: z.string().describe('可直接用于 AI 解读的结构化提示词'),
      },
    },
    async (args) => {
      try {
        const result = drawRandomSign();
        return createStructuredToolResult({
          result,
          prompt: buildCommonDivinationPrompt('ssgw', args.question, result, args.promptMode),
        });
      } catch (error) {
        return createErrorToolResult(getErrorMessage(error, '生成灵签提示词失败'));
      }
    },
  );
}

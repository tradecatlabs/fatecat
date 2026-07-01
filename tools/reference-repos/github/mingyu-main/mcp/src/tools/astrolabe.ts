import { z } from 'zod';
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { ASTROLABE_PROMPT_TOPICS } from '../../../src/lib/astrolabe-prompts.js';
import { generateAstrolabe } from '../../../src/lib/divination/algorithms/astrolabe.js';
import type { AstrolabeBirthInput } from '../../../src/types/divination.js';
import { resultOutputSchema } from '../schemas.js';
import {
  createErrorToolResult,
  createStructuredToolResult,
  getErrorMessage,
} from '../tool-results.js';
import { buildCommonDivinationPrompt, extendPromptSchema } from './divination-common.js';
import {
  assertMcpSolarBirthDate,
  readMcpIntegerLikeInRange,
  readMcpNumberLikeInRange,
} from './input-helpers.js';

const astrolabeSchema = z.object({
  name: z.string().optional().describe('姓名（可选）'),
  gender: z.enum(['男', '女', '']).optional().describe('性别'),
  year: z.number().describe('出生年'),
  month: z.number().describe('出生月'),
  day: z.number().describe('出生日'),
  hour: z.number().describe('出生小时'),
  minute: z.number().describe('出生分钟'),
  latitude: z.number().describe('出生地纬度'),
  longitude: z.number().describe('出生地经度'),
  timezone: z.number().describe('时区偏移，例如中国大陆为 8'),
  locationName: z.string().optional().describe('出生地点名称'),
  useTrueSolarTime: z.boolean().optional().describe('是否启用真太阳时校正'),
});

const astrolabePromptSchema = extendPromptSchema(
  astrolabeSchema.extend({
    astrolabeTopic: z.enum(ASTROLABE_PROMPT_TOPICS).optional().describe('星盘提示词主题'),
    astrolabeScopeText: z
      .string()
      .optional()
      .describe('星盘分析对象文本，例如本命、流年、流月或流日范围与行运证据'),
  }),
  '用户希望围绕星盘解读的问题',
);

function buildAstrolabeInput(args: z.infer<typeof astrolabeSchema>): AstrolabeBirthInput {
  assertMcpSolarBirthDate({
    year: args.year,
    month: args.month,
    day: args.day,
  });

  const hour = readMcpIntegerLikeInRange(args.hour, 'hour', 0, 23);
  const minute = readMcpIntegerLikeInRange(args.minute, 'minute', 0, 59);
  const latitude = readMcpNumberLikeInRange(args.latitude, 'latitude', -90, 90);
  const longitude = readMcpNumberLikeInRange(args.longitude, 'longitude', -180, 180);
  const timezone = readMcpNumberLikeInRange(args.timezone, 'timezone', -12, 14);

  return {
    name: args.name ?? '',
    gender: args.gender ?? '',
    year: String(args.year),
    month: String(args.month),
    day: String(args.day),
    hour: String(hour),
    minute: String(minute),
    latitude: String(latitude),
    longitude: String(longitude),
    timezone: String(timezone),
    locationName: args.locationName ?? '',
    useTrueSolarTime: args.useTrueSolarTime ?? false,
  };
}

function buildAstrolabeResult(args: z.infer<typeof astrolabeSchema>) {
  return generateAstrolabe(buildAstrolabeInput(args));
}

export function registerAstrolabeTool(server: McpServer) {
  server.registerTool(
    'divine_astrolabe',
    {
      description: '星盘生成：根据出生时间、经纬度和时区生成星体、宫位、相位与元素模式数据',
      inputSchema: astrolabeSchema.shape,
      outputSchema: resultOutputSchema,
    },
    async (args) => {
      try {
        const result = buildAstrolabeResult(args);
        return createStructuredToolResult({ result });
      } catch (error) {
        return createErrorToolResult(getErrorMessage(error, '星盘生成失败'));
      }
    },
  );

  server.registerTool(
    'astrolabe_prompt',
    {
      description:
        '星盘生成并生成结构化 AI 解读提示词：一次调用返回星盘结果和可直接复制给 AI 的提示词',
      inputSchema: astrolabePromptSchema.shape,
      outputSchema: {
        result: z.unknown().describe('星盘结果'),
        prompt: z.string().describe('可直接用于 AI 解读的结构化提示词'),
      },
    },
    async (args) => {
      try {
        const result = buildAstrolabeResult(args);
        return createStructuredToolResult({
          result,
          prompt: buildCommonDivinationPrompt('astrolabe', args.question, result, args.promptMode, {
            astrolabeTopic: args.astrolabeTopic,
            astrolabeScopeText: args.astrolabeScopeText,
          }),
        });
      } catch (error) {
        return createErrorToolResult(getErrorMessage(error, '生成星盘提示词失败'));
      }
    },
  );
}

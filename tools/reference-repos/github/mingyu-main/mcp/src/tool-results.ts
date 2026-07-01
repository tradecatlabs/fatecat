import type { CallToolResult } from '@modelcontextprotocol/sdk/types.js';

type StructuredContent = Record<string, unknown>;

export function createStructuredToolResult(structuredContent: StructuredContent): CallToolResult {
  return {
    structuredContent,
    content: [
      {
        type: 'text',
        text: JSON.stringify(structuredContent, null, 2),
      },
    ],
  };
}

export function createErrorToolResult(message: string): CallToolResult {
  return {
    structuredContent: { error: message },
    content: [
      {
        type: 'text',
        text: JSON.stringify({ error: message }),
      },
    ],
    isError: true,
  };
}

export function getErrorMessage(error: unknown, fallback: string) {
  return error instanceof Error ? error.message : fallback;
}

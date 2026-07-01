import type { ListedToolDefinition, RenderOptions } from './contract.js';
import { getToolContract, listToolDefinitions } from './execute.js';

export type ToolContentItem = {
  type: 'text';
  text: string;
};

export type RenderedToolResult = {
  content: ToolContentItem[];
  structuredContent?: unknown;
};

export type ToolListPayload = {
  tools: ListedToolDefinition[];
};

function stringifyResult(result: unknown): string {
  return typeof result === 'object' && result !== null
    ? JSON.stringify(result, null, 2)
    : String(result);
}

export function renderToolResult(
  toolName: string,
  result: unknown,
  options?: RenderOptions,
): RenderedToolResult {
  const tool = getToolContract(toolName);
  if (!tool) {
    return {
      content: [{ type: 'text', text: stringifyResult(result) }],
    };
  }

  const canonicalJSON = tool.renderJSON(result, options);
  const textContent = tool.renderText(result, options);

  const structuredContent = canonicalJSON !== undefined
    ? (tool.mergeRuntimeExtras
      ? tool.mergeRuntimeExtras(canonicalJSON, result)
      : canonicalJSON)
    : undefined;

  return {
    content: [{ type: 'text', text: textContent || stringifyResult(result) }],
    ...(structuredContent !== undefined ? { structuredContent } : {}),
  };
}

export function buildListToolsPayload(): ToolListPayload {
  return {
    tools: listToolDefinitions(),
  };
}

export function buildToolSuccessPayload(
  toolName: string,
  result: unknown,
  options?: RenderOptions,
) {
  const rendered = renderToolResult(toolName, result, options);

  if (rendered.structuredContent !== undefined) {
    return {
      structuredContent: rendered.structuredContent,
      content: rendered.content,
    };
  }

  return rendered;
}

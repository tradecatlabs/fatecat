import type { ListedToolDefinition } from './contract.js';
import { toolByName, tools } from './tools.js';
import { validateInput } from './input-validator.js';

export function listToolDefinitions(): ListedToolDefinition[] {
  return tools.map((tool) => ({
    ...tool.definition,
    outputSchema: tool.outputSchema,
  }));
}

export function getToolContract(name: string) {
  return toolByName.get(name);
}

export async function executeTool(name: string, args: unknown): Promise<unknown> {
  const tool = getToolContract(name);
  if (!tool) {
    const availableTools = listToolDefinitions().map((item) => item.name).join(', ');
    throw new Error(`未知工具: ${name}。可用的工具: ${availableTools}`);
  }

  validateInput(args, tool.definition.inputSchema);
  return tool.execute(args);
}

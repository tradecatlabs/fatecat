/**
 * 用户 MCP Key 管理 API
 *
 * GET  — 获取当前用户的 MCP Key
 * POST — 首次生成 MCP Key
 * PUT  — 重置 MCP Key
 */

import { type NextRequest } from 'next/server';
import { requireUserContext, jsonOk, jsonError } from '@/lib/api-utils';
import { getMcpKey, createMcpKey, resetMcpKey } from '@/lib/mcp-keys';

export async function GET(request: NextRequest) {
  const auth = await requireUserContext(request);
  if ('error' in auth) return jsonError(auth.error.message, auth.error.status);

  const key = await getMcpKey(auth.db, auth.user.id);
  return jsonOk({ key });
}

export async function POST(request: NextRequest) {
  const auth = await requireUserContext(request);
  if ('error' in auth) return jsonError(auth.error.message, auth.error.status);

  const result = await createMcpKey(auth.db, auth.user.id);
  if (!result.success) {
    return jsonError(result.error || '创建失败', result.status || 400);
  }
  return jsonOk({ key: result.key }, 201);
}

export async function PUT(request: NextRequest) {
  const auth = await requireUserContext(request);
  if ('error' in auth) return jsonError(auth.error.message, auth.error.status);

  const result = await resetMcpKey(auth.db, auth.user.id);
  if (!result.success) {
    return jsonError(result.error || '重置失败', result.status || 400);
  }
  return jsonOk({ key: result.key });
}

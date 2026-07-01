/**
 * MCP API Key 管理库
 *
 * 设计目标：
 * 1) 用户态操作基于 RLS（不依赖 service role）
 * 2) 管理员跨用户操作走受控 RPC
 */

import crypto from 'crypto';
import type { SupabaseClient } from '@supabase/supabase-js';

type UserMcpClient = Pick<SupabaseClient, 'from' | 'rpc'>;
type AdminMcpClient = Pick<SupabaseClient, 'rpc'>;

export interface McpApiKey {
  id: string;
  user_id: string;
  key_code: string;
  is_active: boolean;
  is_banned: boolean;
  created_at: string;
  last_used_at: string | null;
}

export interface McpApiKeyWithUser extends Omit<McpApiKey, 'key_code'> {
  key_preview: string;
  user_email: string | null;
  user_nickname: string | null;
}

interface AdminListRow {
  id: string;
  user_id: string;
  key_code: string;
  is_active: boolean;
  is_banned: boolean;
  created_at: string;
  last_used_at: string | null;
  user_email: string | null;
  user_nickname: string | null;
}

function buildKeyPreview(keyCode: string): string {
  if (keyCode.length <= 8) return keyCode;
  return `${keyCode.slice(0, 4)}••••${keyCode.slice(-4)}`;
}

/**
 * 生成 MCP Key 代码（格式: sk-mcp-taibu- + 24 位随机字符）
 */
export function generateMcpKeyCode(): string {
  const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
  const randomBytes = crypto.randomBytes(24);
  let code = 'sk-mcp-taibu-';
  for (let i = 0; i < 24; i++) {
    code += chars[randomBytes[i] % chars.length];
  }
  return code;
}

/**
 * 获取用户的 MCP Key（用户态 RLS 查询）
 */
export async function getMcpKey(
  supabase: UserMcpClient,
  userId: string
): Promise<McpApiKey | null> {
  try {
    const { data, error } = await supabase
      .from('mcp_api_keys')
      .select('*')
      .eq('user_id', userId)
      .maybeSingle();

    if (error) {
      console.error('[mcp-keys] Failed to get key:', error);
      return null;
    }
    return (data as McpApiKey | null) ?? null;
  } catch (error) {
    console.error('[mcp-keys] Error getting key:', error);
    return null;
  }
}

/**
 * 首次生成 MCP Key（用户态 RLS）
 */
export async function createMcpKey(
  supabase: UserMcpClient,
  userId: string
): Promise<{ success: boolean; key?: McpApiKey; error?: string; status?: number }> {
  try {
    const existing = await getMcpKey(supabase, userId);
    if (existing) {
      if (existing.is_banned) {
        return {
          success: false,
          error: '当前账号的 MCP Key 已被管理员永久封禁，请联系管理员',
          status: 403,
        };
      }
      return { success: false, error: '已存在 MCP Key，请使用重置功能' };
    }

    const keyCode = generateMcpKeyCode();
    const { data, error } = await supabase
      .from('mcp_api_keys')
      .insert({ user_id: userId, key_code: keyCode, is_active: true, is_banned: false })
      .select()
      .single();

    if (error) {
      if (error.code === '23505') {
        return { success: false, error: '已存在 MCP Key' };
      }
      if (error.code === '42501') {
        return {
          success: false,
          error: '当前账号的 MCP Key 已被管理员永久封禁，请联系管理员',
          status: 403,
        };
      }
      console.error('[mcp-keys] Failed to create key:', error);
      return { success: false, error: '创建 MCP Key 失败' };
    }

    return { success: true, key: data as McpApiKey };
  } catch (error) {
    console.error('[mcp-keys] Error creating key:', error);
    return { success: false, error: '服务器错误' };
  }
}

/**
 * 重置 MCP Key（用户态 RLS）
 */
export async function resetMcpKey(
  supabase: UserMcpClient,
  userId: string
): Promise<{ success: boolean; key?: McpApiKey; error?: string; status?: number }> {
  try {
    const existing = await getMcpKey(supabase, userId);
    if (!existing) {
      return { success: false, error: '未找到 MCP Key，请先生成' };
    }
    if (existing.is_banned) {
      return {
        success: false,
        error: '当前账号的 MCP Key 已被管理员永久封禁，请联系管理员',
        status: 403,
      };
    }

    const newKeyCode = generateMcpKeyCode();
    const { data, error } = await supabase.rpc('mcp_reset_key', {
      p_user_id: userId,
      p_new_key_code: newKeyCode,
    });

    if (error) {
      if (error.code === '42501') {
        return {
          success: false,
          error: '当前账号的 MCP Key 已被管理员永久封禁，请联系管理员',
          status: 403,
        };
      }
      console.error('[mcp-keys] Failed to reset key:', error);
      return { success: false, error: '重置 MCP Key 失败' };
    }

    if (!data || (Array.isArray(data) && data.length === 0)) {
      return { success: false, error: '重置 MCP Key 失败' };
    }

    const row = Array.isArray(data) ? data[0] : data;
    return { success: true, key: row as McpApiKey };
  } catch (error) {
    console.error('[mcp-keys] Error resetting key:', error);
    return { success: false, error: '服务器错误' };
  }
}

/**
 * 管理员永久封禁 MCP Key（RPC）
 */
export async function revokeMcpKey(
  supabase: AdminMcpClient,
  userId: string
): Promise<{ success: boolean; error?: string }> {
  try {
    const { data, error } = await supabase.rpc('admin_revoke_mcp_key', {
      p_user_id: userId,
    });

    if (error) {
      console.error('[mcp-keys] Failed to revoke key:', error);
      return { success: false, error: '吊销 MCP Key 失败' };
    }

    if (!data) {
      return { success: false, error: '未找到可吊销的 MCP Key' };
    }

    return { success: true };
  } catch (error) {
    console.error('[mcp-keys] Error revoking key:', error);
    return { success: false, error: '服务器错误' };
  }
}

/**
 * 管理员解除 MCP Key 封禁（RPC）
 */
export async function unbanMcpKey(
  supabase: AdminMcpClient,
  userId: string
): Promise<{ success: boolean; error?: string }> {
  try {
    const { data, error } = await supabase.rpc('admin_unban_mcp_key', {
      p_user_id: userId,
    });

    if (error) {
      console.error('[mcp-keys] Failed to unban key:', error);
      return { success: false, error: '解除封禁失败' };
    }

    if (!data) {
      return { success: false, error: '未找到已封禁的 MCP Key' };
    }

    return { success: true };
  } catch (error) {
    console.error('[mcp-keys] Error unbanning key:', error);
    return { success: false, error: '服务器错误' };
  }
}

/**
 * 管理员列出所有 MCP Key（RPC）
 */
export async function getAllMcpKeys(
  supabase: AdminMcpClient,
  filters?: { isActive?: boolean }
): Promise<McpApiKeyWithUser[]> {
  try {
    const { data, error } = await supabase.rpc('admin_list_mcp_keys', {
      p_is_active: filters?.isActive ?? null,
    });

    if (error) {
      console.error('[mcp-keys] Failed to fetch all keys:', error);
      return [];
    }

    const rows = (data as AdminListRow[] | null) ?? [];
    return rows.map((row) => ({
      id: row.id,
      user_id: row.user_id,
      key_preview: buildKeyPreview(row.key_code),
      is_active: row.is_active,
      is_banned: row.is_banned,
      created_at: row.created_at,
      last_used_at: row.last_used_at,
      user_email: row.user_email,
      user_nickname: row.user_nickname,
    }));
  } catch (error) {
    console.error('[mcp-keys] Error fetching all keys:', error);
    return [];
  }
}

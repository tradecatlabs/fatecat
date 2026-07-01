import 'server-only';

import type { SupabaseClient, User } from '@supabase/supabase-js';
import { buildMembershipInfo } from '@/lib/user/membership';
import type { MembershipInfoSource } from '@/lib/user/membership';
import type { ChatBootstrapData, ChatBootstrapKnowledgeBase } from '@/lib/chat/bootstrap';
import { isFeatureModuleEnabled } from '@/lib/app-settings';
import { ensureUserRecordRow } from '@/lib/user/profile-record';

function resolveChatBootstrapError(message: string, error?: unknown): Error {
  if (error) {
    console.error('[chat/bootstrap] failed:', message, error);
  }
  return new Error('加载对话上下文失败');
}

export type ChatBootstrapSupabase = Pick<SupabaseClient, 'from'>;

type PromptSettingsRow = {
  prompt_kb_ids?: unknown;
};

function toPromptKnowledgeBaseIds(value: unknown): string[] {
  if (!Array.isArray(value)) return [];
  return value.filter((item): item is string => typeof item === 'string' && item.length > 0);
}

async function loadMembershipRow(
  supabase: ChatBootstrapSupabase,
  userId: string,
) {
  return await supabase
    .from('users')
    .select('id, membership, membership_expires_at, ai_chat_count')
    .eq('id', userId)
    .maybeSingle();
}

async function loadMembershipRowWithRecovery(
  supabase: ChatBootstrapSupabase,
  userId: string,
) {
  let membershipResult = await loadMembershipRow(supabase, userId);
  if (membershipResult.error || membershipResult.data) {
    return membershipResult;
  }

  const recoveryProbe = supabase.from('users');
  if (typeof recoveryProbe.upsert !== 'function') {
    return membershipResult;
  }

  const ensured = await ensureUserRecordRow(
    supabase as unknown as Parameters<typeof ensureUserRecordRow>[0],
    { id: userId, user_metadata: {} } as Pick<User, 'id' | 'user_metadata'>,
  );
  if (!ensured.ok) {
    return {
      data: null,
      error: ensured.error,
    };
  }

  membershipResult = await loadMembershipRow(supabase, userId);
  return membershipResult;
}

export async function buildChatBootstrap(
  supabase: ChatBootstrapSupabase,
  userId: string,
): Promise<ChatBootstrapData> {
  const knowledgeBaseFeatureEnabled = await isFeatureModuleEnabled('knowledge-base');
  const { data: membershipRow, error: membershipError } = await loadMembershipRowWithRecovery(supabase, userId);

  if (membershipError) {
    throw resolveChatBootstrapError('load users row', membershipError);
  }
  if (!membershipRow || typeof (membershipRow as { ai_chat_count?: unknown }).ai_chat_count !== 'number') {
    throw resolveChatBootstrapError('missing or invalid users row', membershipRow);
  }

  const membership = buildMembershipInfo((membershipRow ?? null) as MembershipInfoSource | null);

  const promptKbIds = membership?.type === 'free' || !knowledgeBaseFeatureEnabled
    ? []
    : await (async () => {
      const { data: settingsRow, error: settingsError } = await supabase
        .from('user_settings')
        .select('prompt_kb_ids')
        .eq('user_id', userId)
        .maybeSingle();
      if (settingsError) {
        throw resolveChatBootstrapError('load user settings', settingsError);
      }
      return toPromptKnowledgeBaseIds((settingsRow as PromptSettingsRow | null)?.prompt_kb_ids);
    })();

  if (membership?.type === 'free' || !knowledgeBaseFeatureEnabled || promptKbIds.length === 0) {
    return {
      userId,
      promptKnowledgeBaseIds: [],
      promptKnowledgeBases: [],
    };
  }

  const { data: kbRows, error: kbError } = await supabase
    .from('knowledge_bases')
    .select('id, name, description')
    .eq('user_id', userId)
    .in('id', promptKbIds);

  if (kbError) {
    throw resolveChatBootstrapError('load knowledge bases', kbError);
  }

  const kbMap = new Map(
    ((kbRows ?? []) as ChatBootstrapKnowledgeBase[]).map((kb) => [kb.id, kb] as const)
  );

  return {
    userId,
    promptKnowledgeBaseIds: promptKbIds,
    promptKnowledgeBases: promptKbIds
      .map((kbId) => kbMap.get(kbId))
      .filter((kb): kb is ChatBootstrapKnowledgeBase => !!kb),
  };
}

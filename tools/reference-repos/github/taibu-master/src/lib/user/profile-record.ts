import type { User } from '@supabase/supabase-js';

type UserRecordSeedInput = Pick<User, 'id' | 'user_metadata'>;

type UserRecordEnsureClient = {
  from: (table: 'users') => {
    upsert: (
      payload: ReturnType<typeof buildUserRecordSeed>,
      options: { onConflict: string; ignoreDuplicates: boolean },
    ) => PromiseLike<{ error: unknown }>;
  };
};

export function buildUserRecordSeed(user: UserRecordSeedInput) {
  return {
    id: user.id,
    nickname: typeof user.user_metadata?.nickname === 'string' && user.user_metadata.nickname.trim().length > 0
      ? user.user_metadata.nickname.trim()
      : '命理爱好者',
    avatar_url: typeof user.user_metadata?.avatar_url === 'string'
      ? user.user_metadata.avatar_url
      : null,
    membership: 'free' as const,
    ai_chat_count: 1,
  };
}

export async function ensureUserRecordRow(
  supabase: UserRecordEnsureClient,
  user: UserRecordSeedInput,
): Promise<{ ok: true } | { ok: false; error: unknown }> {
  const { error } = await supabase
    .from('users')
    .upsert(buildUserRecordSeed(user), {
      onConflict: 'id',
      ignoreDuplicates: true,
    });

  if (error) {
    return { ok: false, error };
  }

  return { ok: true };
}

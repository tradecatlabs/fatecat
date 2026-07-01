import 'server-only';

import { createAnonClient, createAuthedClient, createRequestSupabaseClient } from '@/lib/api-utils';

/**
 * 服务端知识库客户端入口。
 *
 * 浏览器侧请求统一走 `browser-client.ts`；
 * 这里仅保留给服务端库逻辑复用的 Supabase client 构造。
 */
export async function createKbClient(accessToken?: string) {
  if (accessToken) {
    return createAuthedClient(accessToken);
  }

  try {
    return await createRequestSupabaseClient();
  } catch {
    return createAnonClient();
  }
}

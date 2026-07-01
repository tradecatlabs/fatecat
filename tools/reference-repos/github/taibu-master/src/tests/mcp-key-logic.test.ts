import { test } from 'node:test';
import assert from 'node:assert/strict';

process.env.NEXT_PUBLIC_SUPABASE_URL = 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test-anon';

type FakeFromQuery = {
  select: () => {
    eq: (column: string, value: string) => {
      maybeSingle: () => Promise<{ data: unknown; error: unknown }>;
    };
  };
  update: (payload: Record<string, unknown>) => {
    eq: (column: string, value: string) => {
      select: () => {
        single: () => Promise<{ data: unknown; error: unknown }>;
      };
    };
  };
};

test('generateMcpKeyCode uses sk-mcp-taibu- prefix', async () => {
  const { generateMcpKeyCode } = await import('../lib/mcp-keys');
  const key = generateMcpKeyCode();

  assert.ok(key.startsWith('sk-mcp-taibu-'));
  assert.equal(key.length, 'sk-mcp-taibu-'.length + 24);
});

test('resetMcpKey should call mcp_reset_key RPC and return updated key', async () => {
  let rpcName = '';
  let rpcArgs: Record<string, unknown> | undefined;

  const keyRow = {
    id: 'key-1',
    user_id: 'user-1',
    key_code: 'old-key',
    is_active: true,
    is_banned: false,
    created_at: new Date().toISOString(),
    last_used_at: null,
    reset_count: 5,
  };

  const authedClient = {
    from: (table: string): FakeFromQuery => {
      if (table !== 'mcp_api_keys') {
        throw new Error(`Unexpected table: ${table}`);
      }

      return {
        select: () => ({
          eq: () => ({
            maybeSingle: async () => ({ data: keyRow, error: null }),
          }),
        }),
        update: () => {
          throw new Error('Should not call update directly');
        },
      };
    },
    rpc: async (name: string, args?: Record<string, unknown>) => {
      rpcName = name;
      rpcArgs = args;
      return {
        data: [{ ...keyRow, key_code: args?.p_new_key_code, reset_count: 6, last_used_at: null }],
        error: null,
      };
    },
  };

  const { resetMcpKey } = await import('../lib/mcp-keys');
  const result = await resetMcpKey(authedClient as never, 'user-1');

  assert.equal(result.success, true);
  assert.equal(rpcName, 'mcp_reset_key');
  assert.equal(rpcArgs?.p_user_id, 'user-1');
  assert.ok(typeof rpcArgs?.p_new_key_code === 'string', 'should pass new key code');
});

test('resetMcpKey should reject permanently banned keys', async () => {
  let updateCalled = false;

  const keyRow = {
    id: 'key-1',
    user_id: 'user-1',
    key_code: 'old-key',
    is_active: false,
    is_banned: true,
    created_at: new Date().toISOString(),
    last_used_at: null,
  };

  const authedClient = {
    from: (table: string): FakeFromQuery => {
      if (table !== 'mcp_api_keys') {
        throw new Error(`Unexpected table: ${table}`);
      }

      return {
        select: () => ({
          eq: () => ({
            maybeSingle: async () => ({ data: keyRow, error: null }),
          }),
        }),
        update: () => {
          updateCalled = true;
          return {
            eq: () => ({
              select: () => ({
                single: async () => ({ data: keyRow, error: null }),
              }),
            }),
          };
        },
      };
    },
  };

  const { resetMcpKey } = await import('../lib/mcp-keys');
  const result = await resetMcpKey(authedClient as never, 'user-1');

  assert.equal(result.success, false);
  assert.match(result.error || '', /封禁/);
  assert.equal(updateCalled, false, 'banned key must not be reset');
});

test('resetMcpKey should allow inactive but unbanned key to regenerate', async () => {
  let rpcName = '';

  const keyRow = {
    id: 'key-2',
    user_id: 'user-2',
    key_code: 'old-key-2',
    is_active: false,
    is_banned: false,
    created_at: new Date().toISOString(),
    last_used_at: null,
    reset_count: 1,
  };

  const authedClient = {
    from: (table: string): FakeFromQuery => {
      if (table !== 'mcp_api_keys') {
        throw new Error(`Unexpected table: ${table}`);
      }

      return {
        select: () => ({
          eq: () => ({
            maybeSingle: async () => ({ data: keyRow, error: null }),
          }),
        }),
        update: () => {
          throw new Error('Should not call update directly');
        },
      };
    },
    rpc: async (name: string, args?: Record<string, unknown>) => {
      rpcName = name;
      return {
        data: [{
          ...keyRow,
          key_code: args?.p_new_key_code,
          is_active: true,
          reset_count: 2,
          last_used_at: null,
        }],
        error: null,
      };
    },
  };

  const { resetMcpKey } = await import('../lib/mcp-keys');
  const result = await resetMcpKey(authedClient as never, 'user-2');

  assert.equal(result.success, true);
  assert.equal(rpcName, 'mcp_reset_key');
  assert.equal(result.key?.is_active, true);
});

test('getAllMcpKeys should use admin_list_mcp_keys rpc', async () => {
  let rpcName = '';
  let rpcArgs: Record<string, unknown> | undefined;

  const adminClient = {
    rpc: async (name: string, args?: Record<string, unknown>) => {
      rpcName = name;
      rpcArgs = args;
      return {
        data: [
          {
            id: 'key-1',
            user_id: 'user-1',
            key_code: 'sk-mcp-taibu-abcdef1234567890abcdef12',
            is_active: true,
            is_banned: false,
            created_at: '2026-02-11T00:00:00.000Z',
            last_used_at: null,
            user_email: 'user1@example.com',
            user_nickname: '测试用户',
          },
        ],
        error: null,
      };
    },
  };

  const { getAllMcpKeys } = await import('../lib/mcp-keys');
  const result = await getAllMcpKeys(adminClient as never, { isActive: true });

  assert.equal(rpcName, 'admin_list_mcp_keys');
  assert.deepEqual(rpcArgs, { p_is_active: true });
  assert.equal(result.length, 1);
  assert.equal(result[0].user_nickname, '测试用户');
  assert.equal(result[0].user_email, 'user1@example.com');
  assert.equal(result[0].key_preview, 'sk-m••••ef12');
});

test('unbanMcpKey should call admin_unban_mcp_key rpc', async () => {
  let rpcName = '';
  let rpcArgs: Record<string, unknown> | undefined;

  const adminClient = {
    rpc: async (name: string, args?: Record<string, unknown>) => {
      rpcName = name;
      rpcArgs = args;
      return { data: true, error: null };
    },
  };

  const { unbanMcpKey } = await import('../lib/mcp-keys');
  const result = await unbanMcpKey(adminClient as never, 'user-9');

  assert.equal(result.success, true);
  assert.equal(rpcName, 'admin_unban_mcp_key');
  assert.deepEqual(rpcArgs, { p_user_id: 'user-9' });
});

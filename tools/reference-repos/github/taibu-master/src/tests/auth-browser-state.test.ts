import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { NextRequest } from 'next/server';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';

process.env.NEXT_PUBLIC_SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'test-anon';

test('checkLoginAttempts should return an explicit guard error instead of failing open', async () => {
  const browserApiModule = require('../lib/browser-api') as typeof import('../lib/browser-api');
  const authPath = require.resolve('../lib/auth');
  const originalRequestBrowserJson = browserApiModule.requestBrowserJson;

  browserApiModule.requestBrowserJson = async () => ({
    data: null,
    error: { message: 'guard backend down', code: 'guard_backend_down' },
  });

  try {
    delete require.cache[authPath];
    const { checkLoginAttempts, authSessionCacheConstants } = require('../lib/auth') as typeof import('../lib/auth');
    const result = await checkLoginAttempts('user@example.com');

    assert.deepEqual(result, {
      blocked: false,
      remainingAttempts: 5,
      error: {
        message: authSessionCacheConstants.LOGIN_GUARD_UNAVAILABLE_MESSAGE,
        code: 'guard_backend_down',
      },
    });
  } finally {
    browserApiModule.requestBrowserJson = originalRequestBrowserJson;
    delete require.cache[authPath];
  }
});

test('signInWithEmailProtected should fail closed when the login guard is unavailable', async () => {
  const browserApiModule = require('../lib/browser-api') as typeof import('../lib/browser-api');
  const authPath = require.resolve('../lib/auth');
  const originalRequestBrowserJson = browserApiModule.requestBrowserJson;
  const calls: Array<{ url: string; method?: string }> = [];

  browserApiModule.requestBrowserJson = async (url: string, init?: RequestInit) => {
    calls.push({ url, method: init?.method });
    return {
      data: null,
      error: { message: 'guard backend down', code: 'guard_backend_down' },
    };
  };

  try {
    delete require.cache[authPath];
    const { signInWithEmailProtected, authSessionCacheConstants } = require('../lib/auth') as typeof import('../lib/auth');
    const result = await signInWithEmailProtected('user@example.com', 'password');

    assert.deepEqual(result, {
      success: false,
      error: {
        message: authSessionCacheConstants.LOGIN_GUARD_UNAVAILABLE_MESSAGE,
        code: 'guard_backend_down',
      },
    });
    assert.equal(calls.length, 1);
    assert.equal(calls[0]?.url, '/api/auth');
  } finally {
    browserApiModule.requestBrowserJson = originalRequestBrowserJson;
    delete require.cache[authPath];
  }
});

test('browser auth session cache should support explicit invalidate and revalidate flows', async () => {
  const authPath = require.resolve('../lib/auth');
  const originalFetch = global.fetch;
  let callCount = 0;

  global.fetch = async () => {
    callCount += 1;
    const userId = `user-${callCount}`;
    return Response.json({
      data: {
        session: {
          access_token: `access-token-${callCount}`,
          refresh_token: `refresh-token-${callCount}`,
          token_type: 'bearer',
          expires_in: 3600,
          expires_at: Math.floor(Date.now() / 1000) + 3600,
          user: { id: userId },
        },
        user: { id: userId },
      },
      error: null,
    });
  };

  try {
    delete require.cache[authPath];
    const { supabase } = require('../lib/auth') as typeof import('../lib/auth');

    const first = await supabase.auth.getSession();
    const second = await supabase.auth.getSession();
    supabase.auth.invalidateSessionCache();
    const third = await supabase.auth.getSession();
    const events: Array<{ event: string; userId: string | null }> = [];
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      events.push({ event, userId: session?.user?.id ?? null });
    });
    await new Promise((resolve) => setImmediate(resolve));
    const fourth = await supabase.auth.revalidateSession();

    subscription.unsubscribe();
    assert.equal(first.data.session?.user?.id, 'user-1');
    assert.equal(second.data.session?.user?.id, 'user-1');
    assert.equal(third.data.session?.user?.id, 'user-2');
    assert.equal(fourth.data.session?.user?.id, 'user-3');
    assert.equal(callCount, 3);
    assert.deepEqual(events, [
      { event: 'INITIAL_SESSION', userId: 'user-2' },
      { event: 'TOKEN_REFRESHED', userId: 'user-3' },
    ]);
  } finally {
    global.fetch = originalFetch;
    delete require.cache[authPath];
  }
});

test('useSessionMembership should align resolved and loading semantics with viewerStateResolved', () => {
  const source = readFileSync(resolve(process.cwd(), 'src/lib/hooks/useSessionMembership.ts'), 'utf8');

  assert.match(source, /const membershipResolved = !user \|\| bootstrap\.viewerStateResolved;/u);
  assert.match(
    source,
    /membershipLoading:\s*sessionLoading\s*\|\|\s*\(!!user\s*&&\s*!bootstrap\.viewerStateResolved\)/u,
  );
});

test('useAppBootstrap should defer viewer failures briefly before surfacing them', () => {
  const source = readFileSync(resolve(process.cwd(), 'src/lib/hooks/useAppBootstrap.ts'), 'utf8');

  assert.match(source, /const VIEWER_STATE_ERROR_GRACE_MS = 3_000;/u);
  assert.match(source, /const VIEWER_STATE_RETRY_INTERVAL_MS = 800;/u);
  assert.match(source, /if \(viewerPendingKey && !viewerFailureTimedOut\)/u);
});

test('useSessionMembership should keep viewer failures in loading state until bootstrap resolves', () => {
  const clientProvidersModule = require('../components/providers/ClientProviders') as typeof import('../components/providers/ClientProviders');
  const appBootstrapModule = require('../lib/hooks/useAppBootstrap') as typeof import('../lib/hooks/useAppBootstrap');
  const hookPath = require.resolve('../lib/hooks/useSessionMembership');

  const originalUseSessionSafe = clientProvidersModule.useSessionSafe;
  const originalUseAppBootstrap = appBootstrapModule.useAppBootstrap;

  (clientProvidersModule as { useSessionSafe: typeof import('../components/providers/ClientProviders').useSessionSafe }).useSessionSafe = () => ({
    session: { user: { id: 'user-1' } } as never,
    user: { id: 'user-1' } as never,
    loading: false,
  });
  (appBootstrapModule as { useAppBootstrap: typeof import('../lib/hooks/useAppBootstrap').useAppBootstrap }).useAppBootstrap = () => ({
    data: {
      viewerLoaded: false,
      viewerSummary: null,
      viewerErrorMessage: '加载账户状态失败',
      membership: null,
      featureToggles: {},
      featureTogglesLoaded: true,
      featureTogglesErrorMessage: null,
      unreadCount: 0,
      unreadCountLoaded: true,
    },
    isLoading: false,
    hasBootstrapData: true,
    viewerStateLoaded: false,
    viewerStateResolved: false,
    viewerStateError: null,
    refresh: async () => ({
      viewerLoaded: false,
      viewerSummary: null,
      viewerErrorMessage: '加载账户状态失败',
      membership: null,
      featureToggles: {},
      featureTogglesLoaded: true,
      featureTogglesErrorMessage: null,
      unreadCount: 0,
      unreadCountLoaded: true,
    }),
    markCreditsExhausted() {},
  } as ReturnType<typeof import('../lib/hooks/useAppBootstrap').useAppBootstrap>);

  try {
    delete require.cache[hookPath];
    const { useSessionMembership } = require('../lib/hooks/useSessionMembership') as typeof import('../lib/hooks/useSessionMembership');

    function Probe() {
      const membership = useSessionMembership();
      return React.createElement('div', {
        'data-membership-resolved': String(membership.membershipResolved),
        'data-membership-loading': String(membership.membershipLoading),
        'data-membership-info-null': String(membership.membershipInfo === null),
      });
    }

    const html = renderToStaticMarkup(React.createElement(Probe));
    assert.match(html, /data-membership-resolved="false"/u);
    assert.match(html, /data-membership-loading="true"/u);
    assert.match(html, /data-membership-info-null="true"/u);
  } finally {
    (clientProvidersModule as { useSessionSafe: typeof import('../components/providers/ClientProviders').useSessionSafe }).useSessionSafe = originalUseSessionSafe;
    (appBootstrapModule as { useAppBootstrap: typeof import('../lib/hooks/useAppBootstrap').useAppBootstrap }).useAppBootstrap = originalUseAppBootstrap;
    delete require.cache[hookPath];
  }
});

test('useFeatureToggles should keep the app in loading state while bootstrap is still pending', () => {
  const appBootstrapModule = require('../lib/hooks/useAppBootstrap') as typeof import('../lib/hooks/useAppBootstrap');
  const hookPath = require.resolve('../lib/hooks/useFeatureToggles');

  const originalUseAppBootstrap = appBootstrapModule.useAppBootstrap;

  (appBootstrapModule as { useAppBootstrap: typeof import('../lib/hooks/useAppBootstrap').useAppBootstrap }).useAppBootstrap = () => ({
    data: {
      viewerLoaded: false,
      viewerSummary: null,
      viewerErrorMessage: null,
      membership: null,
      featureToggles: {},
      featureTogglesLoaded: false,
      featureTogglesErrorMessage: null,
      unreadCount: 0,
      unreadCountLoaded: false,
    },
    error: null,
    isLoading: false,
    hasBootstrapData: false,
    refresh: async () => ({
      viewerLoaded: true,
      viewerSummary: null,
      viewerErrorMessage: null,
      membership: null,
      featureToggles: {},
      featureTogglesLoaded: true,
      featureTogglesErrorMessage: null,
      unreadCount: 0,
      unreadCountLoaded: true,
    }),
    markCreditsExhausted() {},
  } as ReturnType<typeof import('../lib/hooks/useAppBootstrap').useAppBootstrap>);

  try {
    delete require.cache[hookPath];
    const { useFeatureToggles } = require('../lib/hooks/useFeatureToggles') as typeof import('../lib/hooks/useFeatureToggles');

    function Probe() {
      const featureToggles = useFeatureToggles();
      return React.createElement('div', {
        'data-loading': String(featureToggles.isLoading),
        'data-loaded': String(featureToggles.loaded),
        'data-has-error': String(featureToggles.error instanceof Error),
      });
    }

    const html = renderToStaticMarkup(React.createElement(Probe));
    assert.match(html, /data-loading="true"/u);
    assert.match(html, /data-loaded="false"/u);
    assert.match(html, /data-has-error="false"/u);
  } finally {
    (appBootstrapModule as { useAppBootstrap: typeof import('../lib/hooks/useAppBootstrap').useAppBootstrap }).useAppBootstrap = originalUseAppBootstrap;
    delete require.cache[hookPath];
  }
});

test('ClientProviders should revalidate auth state and invalidate auth-bound queries after auth changes', () => {
  const source = readFileSync(resolve(process.cwd(), 'src/components/providers/ClientProviders.tsx'), 'utf8');

  assert.match(source, /supabase\.auth\.revalidateSession\(\)/u);
  assert.match(source, /invalidateQueriesForPath\('\/api\/auth'\)/u);
});

test('/api/reminders GET should return 500 when reminder subscriptions cannot be loaded', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const remindersModule = require('../lib/reminders') as any;
  const routePath = require.resolve('../app/api/reminders/route');

  const originalRequireUserContext = apiUtilsModule.requireUserContext;
  const originalGetReminderSubscriptions = remindersModule.getReminderSubscriptions;

  apiUtilsModule.requireUserContext = async () => ({
    user: { id: 'user-1' },
    supabase: null,
  });
  remindersModule.getReminderSubscriptions = async () => {
    throw new remindersModule.ReminderReadError('获取提醒订阅失败');
  };

  t.after(() => {
    apiUtilsModule.requireUserContext = originalRequireUserContext;
    remindersModule.getReminderSubscriptions = originalGetReminderSubscriptions;
    delete require.cache[routePath];
  });

  delete require.cache[routePath];
  const { GET } = require('../app/api/reminders/route') as typeof import('../app/api/reminders/route');
  const response = await GET(new NextRequest('http://localhost/api/reminders'));
  const payload = await response.json();

  assert.equal(response.status, 500);
  assert.equal(payload.error, '获取提醒订阅失败');
});

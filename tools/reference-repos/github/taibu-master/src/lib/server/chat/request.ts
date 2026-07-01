import 'server-only';

import type { NextRequest } from 'next/server';
import { DEFAULT_MODEL_ID } from '@/lib/ai/ai-config';
import { getDefaultModelConfigAsync, getModelConfigAsync } from '@/lib/server/ai-config';
import { isModelAllowedForMembership, isReasoningAllowedForMembership } from '@/lib/ai/ai-access';
import { getAuthContext, jsonError, requireUserContext, resolveRequestDbClient, type AuthContextResult } from '@/lib/api-utils';
import { buildChatPromptContext } from '@/lib/server/chat/prompt-context';
import {
  attemptCreditUse,
  getUserAuthInfo,
  refundCreditsOrLog,
  UserStateResolutionError,
} from '@/lib/user/credits';
import type { MembershipType } from '@/lib/user/membership';
import { normalizeIdentityUserProfile, type UserIdentityProfile } from '@/lib/user/settings';
import type { ChatMessage, DifyContext } from '@/types';
import type { Mention } from '@/types/mentions';
import { checkRateLimit } from '@/lib/rate-limit';
import { normalizeVisualizationSettings, type VisualizationSettings } from '@/lib/visualization/settings';

const INTERNAL_SECRET = process.env.INTERNAL_API_SECRET;
const BROWSER_DIRECT_CHAT_RATE_LIMIT_CONFIG = {
  maxRequests: 20,
  windowMs: 60_000,
};
const BROWSER_DIRECT_CHAT_RATE_LIMIT_KEY = '/api/chat/direct/prepare';

type ChatAuthUser = NonNullable<AuthContextResult['user']>;

export interface ChatRequestBody {
  messages: ChatMessage[];
  skipCreditCheck?: boolean;
  internalSecret?: string;
  stream?: boolean;
  mangpaiMode?: boolean;
  model?: string;
  reasoning?: boolean;
  difyContext?: DifyContext;
  mentions?: Mention[];
  dreamMode?: boolean;
  expressionStyle?: 'direct' | 'gentle';
  customInstructions?: string | null;
  userProfile?: UserIdentityProfile | null;
  visualizationSettings?: VisualizationSettings;
}

export interface ResolvedChatRequest {
  body: ChatRequestBody;
  userId: string | null;
  canSkipCredit: boolean;
  accessTokenForKB: string | null;
  requestedModelId: string;
  membershipType: MembershipType;
  reasoningEnabled: boolean;
  creditDeducted: boolean;
}

export type PreparedChatRequest =
  ResolvedChatRequest &
  Awaited<ReturnType<typeof buildChatPromptContext>>;

export async function parseChatRequestBody(request: NextRequest): Promise<ChatRequestBody | Response> {
  let body: ChatRequestBody;
  try {
    body = await request.json() as ChatRequestBody;
  } catch {
    return jsonError('请求体不是合法 JSON', 400);
  }
  if (!body.messages || !Array.isArray(body.messages)) {
    return jsonError('无效的消息格式', 400);
  }
  console.log(`[chat-parse] mentions=${JSON.stringify(body.mentions)} msgCount=${body.messages.length}`);
  body.userProfile = normalizeIdentityUserProfile(body.userProfile);
  body.visualizationSettings = normalizeVisualizationSettings(body.visualizationSettings);
  return body;
}

export function getChatAccessTokenForKnowledgeBase(request: NextRequest): string | null {
  const authHeader = request.headers.get('authorization');
  if (authHeader) {
    return authHeader.replace(/Bearer\s+/i, '');
  }

  return request.cookies.get('sb-access-token')?.value ?? null;
}

export async function resolveChatRequest(
  request: NextRequest,
  body: ChatRequestBody,
): Promise<ResolvedChatRequest | Response> {
  const canSkipCredit = !!(INTERNAL_SECRET && body.skipCreditCheck && body.internalSecret === INTERNAL_SECRET);

  let accessTokenForKB: string | null = getChatAccessTokenForKnowledgeBase(request);
  let authUser: ChatAuthUser | null = null;
  let authDb: ReturnType<typeof resolveRequestDbClient> = null;

  let userId: string | null = null;
  if (canSkipCredit) {
    const auth = await getAuthContext(request);
    if (auth.authError) {
      return jsonError(auth.authError.message, auth.authError.status);
    }
    authUser = auth.user;
    authDb = resolveRequestDbClient(auth);
    userId = auth.user?.id || null;
  } else {
    const auth = await requireUserContext(request);
    if ('error' in auth) {
      return jsonError(auth.error.message, auth.error.status);
    }
    authUser = auth.user;
    authDb = resolveRequestDbClient(auth);
    userId = auth.user.id;
    accessTokenForKB = accessTokenForKB || auth.accessToken || null;
  }

  const requestedModelId = body.model?.trim() || DEFAULT_MODEL_ID;
  const modelConfig = requestedModelId
    ? await getModelConfigAsync(requestedModelId)
    : await getDefaultModelConfigAsync('chat');
  if (!modelConfig) {
    return jsonError('无效的模型', 400);
  }

  let authInfo = null;
  if (userId) {
    try {
      authInfo = await getUserAuthInfo(userId, {
        client: authDb ?? undefined,
        user: authUser ?? undefined,
      });
    } catch (error) {
      if (error instanceof UserStateResolutionError) {
        return jsonError(error.message, 500, { code: error.code });
      }
      throw error;
    }
  }
  const membershipType = authInfo?.effectiveMembership ?? 'free';
  if (!isModelAllowedForMembership(modelConfig, membershipType)) {
    return jsonError('当前会员等级无法使用该模型', 403);
  }

  const reasoningAllowed = isReasoningAllowedForMembership(modelConfig, membershipType);
  const reasoningEnabled = reasoningAllowed ? !!body.reasoning : false;

  let creditDeducted = false;
  if (userId && !canSkipCredit) {
    const hasEnough = authInfo?.hasCredits ?? false;
    if (!hasEnough) {
      return jsonError('积分不足，请先通过签到、激活码或会员权益获取积分', 402, {
        code: 'INSUFFICIENT_CREDITS',
        needRecharge: true,
      });
    }

    // 流式与非流式统一预扣费，避免并发流式请求在完成后扣费时漏计。
    const creditUse = await attemptCreditUse(userId, {
      client: authDb ?? undefined,
      user: authUser ?? undefined,
    });
    if (!creditUse.ok) {
      if (creditUse.reason === 'insufficient_credits') {
        return jsonError('积分不足，请先通过签到、激活码或会员权益获取积分', 402, {
          code: 'INSUFFICIENT_CREDITS',
          needRecharge: true,
        });
      }
      return jsonError('积分扣减失败，请重试', 500, {
        code: 'CREDIT_DEDUCTION_FAILED',
      });
    }
    creditDeducted = true;
  }

  return {
    body,
    userId,
    canSkipCredit,
    accessTokenForKB,
    requestedModelId: modelConfig.id,
    membershipType,
    reasoningEnabled,
    creditDeducted,
  };
}

export async function prepareBrowserDirectChatRequest(
  request: NextRequest,
  body: ChatRequestBody,
): Promise<PreparedChatRequest | Response> {
  const auth = await requireUserContext(request);
  if ('error' in auth) {
    return jsonError(auth.error.message, auth.error.status);
  }

  const rateLimit = await checkRateLimit(
    auth.user.id,
    BROWSER_DIRECT_CHAT_RATE_LIMIT_KEY,
    BROWSER_DIRECT_CHAT_RATE_LIMIT_CONFIG,
  );
  if (!rateLimit.allowed) {
    return jsonError('请求过于频繁，请稍后再试', 429);
  }

  let accessTokenForKB = getChatAccessTokenForKnowledgeBase(request);
  accessTokenForKB = accessTokenForKB || auth.accessToken || null;

  let authInfo;
  try {
    authInfo = await getUserAuthInfo(auth.user.id, {
      client: resolveRequestDbClient(auth) ?? undefined,
      user: auth.user,
    });
  } catch (error) {
    if (error instanceof UserStateResolutionError) {
      return jsonError(error.message, 500, { code: error.code });
    }
    throw error;
  }
  const requestedModelId = body.model?.trim() || DEFAULT_MODEL_ID;
  const reasoningEnabled = body.reasoning === true;
  const resolvedRequest: ResolvedChatRequest = {
    body,
    userId: auth.user.id,
    canSkipCredit: true,
    accessTokenForKB,
    requestedModelId,
    membershipType: authInfo.effectiveMembership,
    reasoningEnabled,
    creditDeducted: false,
  };

  return {
    ...resolvedRequest,
    ...(await buildChatPromptContext(resolvedRequest)),
  };
}

export async function prepareChatRequest(
  request: NextRequest,
  body: ChatRequestBody,
): Promise<PreparedChatRequest | Response> {
  const resolvedRequest = await resolveChatRequest(request, body);
  if (resolvedRequest instanceof Response) {
    return resolvedRequest;
  }

  try {
    const promptContext = await buildChatPromptContext(resolvedRequest);
    return {
      ...resolvedRequest,
      ...promptContext,
    };
  } catch (error) {
    if (resolvedRequest.creditDeducted && resolvedRequest.userId && !resolvedRequest.canSkipCredit) {
      await refundCreditsOrLog(resolvedRequest.userId, 1, 'chat prompt-context');
    }
    throw error;
  }
}

import { runDirectAnalysisFlow } from '@/lib/ai/direct-analysis-client';
import { getCustomProvider } from '@/lib/chat/custom-provider';
import type { DirectStreamingRequest } from '@/lib/hooks/useStreamingResponse';

type AnalysisStreaming = {
  startStream: (
    url: string,
    options: RequestInit,
  ) => Promise<{ content: string; reasoning: string | null; error?: string } | null>;
  startDirectStream: (
    request: DirectStreamingRequest,
  ) => Promise<{ content: string; reasoning: string | null; error?: string } | null>;
};

export type SharedAnalysisFlowOptions = {
  endpoint: string;
  streaming: AnalysisStreaming;
  isCreditsError: (error: string | null) => boolean;
  headers?: Record<string, string>;
  direct?: {
    prepareBody: Record<string, unknown>;
    persistBody: Record<string, unknown>;
  };
  streamBody: Record<string, unknown>;
};

export type SharedAnalysisFlowResult = {
  content: string | null;
  reasoning: string | null;
  conversationId: string | null;
  error: string | null;
  requiresCredits: boolean;
};

export async function runSharedAnalysisFlow(
  options: SharedAnalysisFlowOptions,
): Promise<SharedAnalysisFlowResult> {
  const headers = options.headers ?? { 'Content-Type': 'application/json' };
  const customProvider = getCustomProvider();

  if (customProvider && options.direct) {
    const directResult = await runDirectAnalysisFlow({
      endpoint: options.endpoint,
      headers,
      provider: customProvider,
      streaming: options.streaming,
      prepareBody: options.direct.prepareBody,
      persistBody: options.direct.persistBody,
    });
    const error = directResult.error ?? null;
    const requiresCredits = options.isCreditsError(error);

    return {
      content: directResult.content || null,
      reasoning: directResult.reasoning,
      conversationId: directResult.conversationId,
      error: requiresCredits ? null : error,
      requiresCredits,
    };
  }

  const streamResult = await options.streaming.startStream(options.endpoint, {
    method: 'POST',
    headers,
    body: JSON.stringify(options.streamBody),
  });
  const error = streamResult?.error ?? null;
  const requiresCredits = options.isCreditsError(error);

  return {
    content: streamResult?.content || null,
    reasoning: streamResult?.reasoning || null,
    conversationId: null,
    error: requiresCredits ? null : error,
    requiresCredits,
  };
}

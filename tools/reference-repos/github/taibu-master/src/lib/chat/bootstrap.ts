import { requestBrowserJson } from '@/lib/browser-api';

export interface ChatBootstrapKnowledgeBase {
  id: string;
  name: string;
  description: string | null;
}

export interface ChatBootstrapData {
  userId: string | null;
  promptKnowledgeBaseIds: string[];
  promptKnowledgeBases: ChatBootstrapKnowledgeBase[];
}

export const EMPTY_CHAT_BOOTSTRAP: ChatBootstrapData = {
  userId: null,
  promptKnowledgeBaseIds: [],
  promptKnowledgeBases: [],
};

const DEFAULT_CHAT_BOOTSTRAP_ERROR = '加载对话上下文失败';

export async function loadChatBootstrap(): Promise<ChatBootstrapData> {
  const result = await requestBrowserJson<ChatBootstrapData>('/api/chat/bootstrap');
  if (result.error) {
    throw new Error(result.error.message || DEFAULT_CHAT_BOOTSTRAP_ERROR);
  }
  if (!result.data) {
    throw new Error(DEFAULT_CHAT_BOOTSTRAP_ERROR);
  }
  return result.data;
}

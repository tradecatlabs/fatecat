/**
 * 知识库功能开关共享 Hook
 *
 * 'use client' 标记说明：
 * - 依赖 useFeatureToggles 读取浏览器侧功能开关状态
 */
'use client';

import { useFeatureToggles } from '@/lib/hooks/useFeatureToggles';

export function useKnowledgeBaseFeatureEnabled() {
    const { isFeatureEnabled, isLoading } = useFeatureToggles();
    return {
        knowledgeBaseEnabled: !isLoading && isFeatureEnabled('knowledge-base'),
        knowledgeBaseFeatureLoading: isLoading,
    };
}

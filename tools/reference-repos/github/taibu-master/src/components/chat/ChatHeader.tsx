/**
 * Chat 页面头部：桌面端右上角个性化与知识库入口
 *
 * 'use client' 标记说明：
 * - 渲染条件依赖 props
 */
'use client';

import { BookOpenText } from 'lucide-react';
import { SettingsCenterLink } from '@/components/settings/SettingsCenterLink';
import { SETTINGS_CENTER_TAB_ICONS } from '@/components/settings/settings-center-icons';

interface ChatHeaderProps {
    membershipType: string;
    knowledgeBaseEnabled: boolean;
    aiPersonalizationEnabled: boolean;
}

const PersonalizationIcon = SETTINGS_CENTER_TAB_ICONS.personalization;

export function ChatHeader({
    membershipType,
    knowledgeBaseEnabled,
    aiPersonalizationEnabled,
}: ChatHeaderProps) {
    return (
        <div className="hidden lg:flex absolute top-4 right-4 z-10 flex-wrap justify-end gap-2">
            {aiPersonalizationEnabled && (
                <SettingsCenterLink
                    tab="personalization"
                    className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-background/80 backdrop-blur-md border border-border shadow-sm hover:bg-accent/10 hover:text-accent hover:border-accent/30 transition-all duration-300 group"
                    title="个性化"
                >
                    <PersonalizationIcon size={20} className="text-foreground-secondary group-hover:text-accent transition-colors" />
                    <span className="text-sm font-medium text-foreground-secondary group-hover:text-accent transition-colors">
                        个性化
                    </span>
                </SettingsCenterLink>
            )}

            {membershipType !== 'free' && knowledgeBaseEnabled && (
                <SettingsCenterLink
                    tab="knowledge-base"
                    className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-background/80 backdrop-blur-md border border-border shadow-sm hover:bg-accent/10 hover:text-accent hover:border-accent/30 transition-all duration-300 group"
                    title="知识库"
                >
                    <BookOpenText className="w-5 h-5 text-foreground-secondary group-hover:text-accent transition-colors" />
                    <span className="text-sm font-medium text-foreground-secondary group-hover:text-accent transition-colors">
                        知识库
                    </span>
                </SettingsCenterLink>
            )}
        </div>
    );
}

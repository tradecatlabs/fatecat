/**
 * 大六壬历史记录页面 - 使用 HistoryPageTemplate
 */
'use client';

import { BookOpen } from 'lucide-react';
import { HistoryPageTemplate } from '@/components/history/HistoryPageTemplate';

export default function DaliurenHistoryPage() {
    const defaultTimeZone = typeof Intl !== 'undefined'
        ? Intl.DateTimeFormat().resolvedOptions().timeZone || 'Asia/Shanghai'
        : 'Asia/Shanghai';

    return (
        <HistoryPageTemplate
            sourceType="daliuren"
            title="六壬历史"
            subtitle="查看您的历史六壬记录"
            icon={BookOpen}
            iconColor="text-cyan-500"
            searchPlaceholder="搜索..."
            emptyActionLabel="开始起课"
            emptyActionHref="/daliuren"
            deleteMessage="确定要删除这条六壬记录吗？此操作无法撤销。"
            kbSourceType="daliuren_divination"
            themeColor="cyan-500"
            restoreTimezone={defaultTimeZone}
        />
    );
}

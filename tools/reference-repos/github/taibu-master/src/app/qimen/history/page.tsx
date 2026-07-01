/**
 * 奇门遁甲历史记录页面 - 使用 HistoryPageTemplate
 */
'use client';

import { Compass } from 'lucide-react';
import { HistoryPageTemplate } from '@/components/history/HistoryPageTemplate';

export default function QimenHistoryPage() {
    return (
        <HistoryPageTemplate
            sourceType="qimen"
            title="奇门遁甲历史"
            subtitle="三式之首，洞察天时地利"
            icon={Compass}
            iconColor="text-indigo-500"
            searchPlaceholder="搜索占事..."
            emptyActionLabel="开始起课"
            emptyActionHref="/qimen"
            deleteMessage="确定要删除这条排盘记录吗？此操作无法撤销。"
            kbSourceType="qimen_chart"
            themeColor="indigo-500"
            invalidateTypes={['qimen_chart']}
            kbTitleFn={item => item.question || '奇门遁甲排盘'}
        />
    );
}

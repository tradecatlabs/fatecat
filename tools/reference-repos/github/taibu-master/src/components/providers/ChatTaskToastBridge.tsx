'use client';

import { useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useToast } from '@/components/ui/Toast';
import { chatStreamManager, type ChatStreamEvent } from '@/lib/chat/chat-stream-manager';

export function ChatTaskToastBridge() {
    const router = useRouter();
    const { showToast } = useToast();

    const routerRef = useRef(router);
    const showToastRef = useRef(showToast);

    useEffect(() => {
        routerRef.current = router;
        showToastRef.current = showToast;
    }, [router, showToast]);

    useEffect(() => {
        const unsubscribe = chatStreamManager.subscribe((event: ChatStreamEvent) => {
            const shouldNotify = event.type === 'task_completed'
                || ((event.type === 'task_failed' || event.type === 'task_stopped') && event.task.content.trim().length > 0);
            if (!shouldNotify) return;

            const completedConversationId = event.task.conversationId;
            const currentPathname = window.location.pathname;
            const currentSearch = window.location.search;
            const currentActiveConversationId = currentPathname === '/chat'
                ? new URLSearchParams(currentSearch).get('id')
                : null;
            const isViewingTargetConversation = currentPathname === '/chat' && currentActiveConversationId === completedConversationId;
            const completionMessage = event.type === 'task_completed'
                ? '该对话已回复完成'
                : '该对话回复已结束';
            if (isViewingTargetConversation) {
                showToastRef.current('chat', completionMessage);
                return;
            }

            showToastRef.current('chat', completionMessage, {
                duration: 6000,
                action: {
                    label: '查看',
                    onClick: () => routerRef.current.push(`/chat?id=${completedConversationId}`),
                },
            });
        });

        return unsubscribe;
    }, []);

    return null;
}

/**
 * 虚拟化聊天消息列表
 *
 * 'use client' 标记说明：
 * - 使用 React hooks (useRef, useEffect, useCallback)
 * - 使用 @tanstack/react-virtual 进行虚拟滚动
 */
'use client';

import { useRef, useEffect, useCallback } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';
import type { ChatMessage, Mention } from '@/types';
import { ChatMessageItem } from '@/components/chat/ChatMessageItem';
import { isNearBottom } from '@/lib/chat/chat-scroll';

interface VirtualizedChatMessageListProps {
    messages: ChatMessage[];
    isLoading: boolean;
    onEditMessage?: (messageId: string, newContent: string, mentions?: Mention[]) => void;
    onRegenerateResponse?: (messageId: string) => void;
    onSwitchVersion?: (messageId: string, versionIndex: number) => void;
    onArchiveMessage?: (message: ChatMessage) => void;
    disabled?: boolean;
}

// 估算消息高度（用于虚拟化初始计算）
function estimateMessageHeight(message: ChatMessage): number {
    const baseHeight = 80; // 基础高度（padding + 操作按钮）
    const contentLength = message.content.length;
    const reasoningLength = message.reasoning?.length || 0;

    // 根据内容长度估算行数（假设每行约 60 个字符）
    const contentLines = Math.ceil(contentLength / 60);
    const reasoningLines = Math.ceil(reasoningLength / 60);

    // 每行约 24px
    const contentHeight = contentLines * 24;
    const reasoningHeight = reasoningLines * 20;

    // 附件额外高度
    const attachmentHeight = message.attachments?.fileName ? 60 : 0;

    return baseHeight + contentHeight + reasoningHeight + attachmentHeight;
}

export function VirtualizedChatMessageList({
    messages,
    isLoading,
    onEditMessage,
    onRegenerateResponse,
    onSwitchVersion,
    onArchiveMessage,
    disabled = false,
}: VirtualizedChatMessageListProps) {
    const parentRef = useRef<HTMLDivElement>(null);
    const lastMessageCountRef = useRef(0);
    const hasInitialScrollRef = useRef(false);
    const conversationIdRef = useRef<string | null>(null); // 通过首条消息 ID 追踪当前对话
    const shouldAutoFollowRef = useRef(true);

    // 找到最后一条正在流式输出的AI消息
    const lastMessage = messages[messages.length - 1];
    const isStreamingAI = isLoading && lastMessage?.role === 'assistant';

    // eslint-disable-next-line react-hooks/incompatible-library -- TanStack Virtual 库特性，不影响功能
    const virtualizer = useVirtualizer({
        count: messages.length,
        getScrollElement: () => parentRef.current,
        estimateSize: (index) => estimateMessageHeight(messages[index]),
        overscan: 5, // 预渲染上下各 5 条消息
        getItemKey: (index) => messages[index]?.id || `msg-${index}`,
    });

    // 滚动到底部
    const scrollToBottom = useCallback((behavior: 'auto' | 'smooth' = 'smooth') => {
        if (messages.length > 0) {
            virtualizer.scrollToIndex(messages.length - 1, {
                align: 'end',
                behavior,
            });
        }
    }, [messages.length, virtualizer]);

    const handleScroll = useCallback(() => {
        const container = parentRef.current;
        if (!container) return;
        shouldAutoFollowRef.current = isNearBottom({
            scrollHeight: container.scrollHeight,
            scrollTop: container.scrollTop,
            clientHeight: container.clientHeight,
        });
    }, []);

    // 新消息时自动滚动到底部
    useEffect(() => {
        // 通过首条消息 ID 检测对话切换
        const currentConversationId = messages[0]?.id || null;
        const isConversationChanged = currentConversationId !== conversationIdRef.current;

        if (isConversationChanged) {
            // 对话切换，重置状态
            conversationIdRef.current = currentConversationId;
            hasInitialScrollRef.current = false;
            lastMessageCountRef.current = 0;
            shouldAutoFollowRef.current = true;
        }

        // 首次渲染或切换对话时，立即滚动到底部
        if (!hasInitialScrollRef.current && messages.length > 0) {
            hasInitialScrollRef.current = true;
            scrollToBottom('auto');
            lastMessageCountRef.current = messages.length;
            return;
        }

        if (messages.length > lastMessageCountRef.current && shouldAutoFollowRef.current) {
            // 新消息添加，滚动到底部
            scrollToBottom('smooth');
        }
        lastMessageCountRef.current = messages.length;
    }, [messages, scrollToBottom]);

    // 流式输出时，监听最后一条消息内容变化来滚动（包括 reasoning 和 content）
    const lastMessageContent = lastMessage?.content;
    const lastMessageReasoning = lastMessage?.reasoning;
    const lastMessageTotalLengthRef = useRef(0);

    useEffect(() => {
        if (isStreamingAI && shouldAutoFollowRef.current) {
            // 计算 content + reasoning 的总长度
            const totalLength = (lastMessageContent?.length || 0) + (lastMessageReasoning?.length || 0);
            // 只在内容实际增加时滚动
            if (totalLength > lastMessageTotalLengthRef.current) {
                lastMessageTotalLengthRef.current = totalLength;
                scrollToBottom('auto');
            }
        } else {
            // 流式结束，重置长度记录
            lastMessageTotalLengthRef.current = 0;
        }
    }, [isStreamingAI, lastMessageContent, lastMessageReasoning, scrollToBottom]);

    const virtualItems = virtualizer.getVirtualItems();

    return (
        <div
            ref={parentRef}
            onScroll={handleScroll}
            className="h-full overflow-auto"
            style={{ contain: 'strict' }}
        >
            <div
                className="max-w-3xl mx-auto relative"
                style={{
                    height: `${virtualizer.getTotalSize()}px`,
                }}
            >
                <div
                    className="absolute top-0 left-0 w-full"
                    style={{
                        transform: `translateY(${virtualItems[0]?.start ?? 0}px)`,
                    }}
                >
                    {virtualItems.map((virtualRow) => {
                        const message = messages[virtualRow.index];
                        if (!message) return null;

                        return (
                            <div
                                key={virtualRow.key}
                                data-index={virtualRow.index}
                                ref={virtualizer.measureElement}
                                className="py-3"
                            >
                                <ChatMessageItem
                                    message={message}
                                    isStreamingAI={isStreamingAI}
                                    isLastMessage={virtualRow.index === messages.length - 1}
                                    disabled={disabled}
                                    onEditMessage={onEditMessage}
                                    onRegenerateResponse={onRegenerateResponse}
                                    onSwitchVersion={onSwitchVersion}
                                    onArchiveMessage={onArchiveMessage}
                                />
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}

/**
 * 流式文本平滑渲染 Hook
 *
 * 'use client' 标记说明：
 * - 使用 React hooks (useState, useCallback, useRef, useEffect)
 * - 需要在客户端处理动画渲染
 */
'use client';

import { useState, useCallback, useRef, useEffect } from 'react';

export interface StreamingTextOptions {
    /** 字符消费间隔（毫秒），默认 25ms */
    updateInterval?: number;
    /** 是否使用 requestAnimationFrame 优化，默认 true */
    useRAF?: boolean;
    /** 每次消费的字符数，默认 1 */
    batchSize?: number;
    /** 是否启用动态批量大小（根据队列长度自动调整），默认 true */
    dynamicBatchSize?: boolean;
    /** 动态批量大小的阈值配置 */
    dynamicThresholds?: {
        /** 队列长度超过此值时使用中等批量，默认 50 */
        medium?: number;
        /** 队列长度超过此值时使用大批量，默认 200 */
        large?: number;
    };
    /** 是否立即显示首字符（不等待队列），默认 true */
    immediateFirstChar?: boolean;
}

interface StreamingTextState {
    /** 当前可见的内容 */
    visibleContent: string;
    /** 是否正在渲染 */
    isRendering: boolean;
    /** 队列中剩余的字符数 */
    pendingCount: number;
}

interface StreamingTextActions {
    /** 添加字符到队列 */
    addCharacters: (chars: string) => void;
    /** 重置状态 */
    reset: () => void;
    /** 立即完成渲染（跳过动画） */
    flush: () => void;
    /** 停止渲染 */
    stop: () => void;
}

type UseStreamingTextReturn = StreamingTextState & StreamingTextActions;

/**
 * 流式文本平滑渲染 Hook
 *
 * 将流式接收的文本通过队列机制平滑渲染，避免一次性更新导致的卡顿
 */
export function useStreamingText(
    options: StreamingTextOptions = {}
): UseStreamingTextReturn {
    const {
        updateInterval = 25,
        useRAF = true,
        batchSize = 1,
        dynamicBatchSize = true,
        dynamicThresholds = {},
        immediateFirstChar = true,
    } = options;

    const { medium: mediumThreshold = 50, large: largeThreshold = 200 } = dynamicThresholds;

    const [visibleContent, setVisibleContent] = useState('');
    const [isRendering, setIsRendering] = useState(false);
    const [pendingCount, setPendingCount] = useState(0);

    const charQueueRef = useRef<string[]>([]);
    const queueHeadRef = useRef(0); // 队列头部索引，避免 shift() 的 O(n) 操作
    const drainTimerRef = useRef<number | null>(null);
    const rafIdRef = useRef<number | null>(null);
    const isActiveRef = useRef(false);
    const accumulatedRef = useRef('');
    const rafLoopRef = useRef<() => void>(() => {});

    // 清理定时器和 RAF
    const cleanup = useCallback(() => {
        if (drainTimerRef.current !== null) {
            clearInterval(drainTimerRef.current);
            drainTimerRef.current = null;
        }
        if (rafIdRef.current !== null) {
            cancelAnimationFrame(rafIdRef.current);
            rafIdRef.current = null;
        }
    }, []);

    // 消费队列中的字符
    const drainQueue = useCallback(() => {
        const queue = charQueueRef.current;
        const head = queueHeadRef.current;
        const remaining = queue.length - head;

        if (remaining === 0) {
            // 队列已空，重置
            charQueueRef.current = [];
            queueHeadRef.current = 0;
            cleanup();
            setIsRendering(false);
            isActiveRef.current = false;
            return;
        }

        // 动态计算批量大小
        let effectiveBatchSize = batchSize;
        if (dynamicBatchSize) {
            if (remaining > largeThreshold) {
                effectiveBatchSize = Math.max(batchSize * 4, 8);
            } else if (remaining > mediumThreshold) {
                effectiveBatchSize = Math.max(batchSize * 2, 4);
            }
        }

        // 批量消费字符（使用索引，O(1) 操作）
        const consumeCount = Math.min(effectiveBatchSize, remaining);
        const consumed = queue.slice(head, head + consumeCount).join('');
        queueHeadRef.current = head + consumeCount;

        if (consumed) {
            accumulatedRef.current += consumed;
            setVisibleContent(accumulatedRef.current);
            setPendingCount(queue.length - queueHeadRef.current);
        }

        // 定期压缩队列，避免内存泄漏
        if (queueHeadRef.current > 1000) {
            charQueueRef.current = queue.slice(queueHeadRef.current);
            queueHeadRef.current = 0;
        }
    }, [batchSize, cleanup, dynamicBatchSize, mediumThreshold, largeThreshold]);

    // 使用 RAF 的渲染循环 - 在 useEffect 中更新 ref
    useEffect(() => {
        rafLoopRef.current = () => {
            drainQueue();
            if (charQueueRef.current.length > 0 && isActiveRef.current) {
                rafIdRef.current = requestAnimationFrame(rafLoopRef.current);
            }
        };
    }, [drainQueue]);

    // 启动渲染
    const startDrain = useCallback(() => {
        if (isActiveRef.current) return;
        isActiveRef.current = true;
        setIsRendering(true);

        if (useRAF) {
            rafIdRef.current = requestAnimationFrame(rafLoopRef.current);
        } else {
            drainTimerRef.current = window.setInterval(drainQueue, updateInterval);
        }
    }, [useRAF, drainQueue, updateInterval]);

    // 添加字符到队列
    const addCharacters = useCallback((chars: string) => {
        if (!chars) return;

        // 立即显示首字符，提升用户感知的响应速度
        if (immediateFirstChar && !isActiveRef.current && accumulatedRef.current === '') {
            // 立即显示第一个字符
            accumulatedRef.current = chars[0];
            setVisibleContent(accumulatedRef.current);

            // 剩余字符加入队列
            for (let i = 1; i < chars.length; i++) {
                charQueueRef.current.push(chars[i]);
            }
            setPendingCount(charQueueRef.current.length - queueHeadRef.current);

            // 复用 startDrain 启动队列消费
            startDrain();
            return;
        }

        // 正常流程：追加字符到队列
        for (const ch of chars) {
            charQueueRef.current.push(ch);
        }
        setPendingCount(charQueueRef.current.length - queueHeadRef.current);

        if (!isActiveRef.current) {
            startDrain();
        }
    }, [startDrain, immediateFirstChar]);

    // 重置状态
    const reset = useCallback(() => {
        cleanup();
        charQueueRef.current = [];
        queueHeadRef.current = 0;
        accumulatedRef.current = '';
        isActiveRef.current = false;
        setVisibleContent('');
        setIsRendering(false);
        setPendingCount(0);
    }, [cleanup]);

    // 立即完成渲染
    const flush = useCallback(() => {
        cleanup();
        const queue = charQueueRef.current;
        const head = queueHeadRef.current;
        if (queue.length > head) {
            accumulatedRef.current += queue.slice(head).join('');
            charQueueRef.current = [];
            queueHeadRef.current = 0;
            setVisibleContent(accumulatedRef.current);
        }
        isActiveRef.current = false;
        setIsRendering(false);
        setPendingCount(0);
    }, [cleanup]);

    // 停止渲染
    const stop = useCallback(() => {
        cleanup();
        isActiveRef.current = false;
        setIsRendering(false);
    }, [cleanup]);

    // 组件卸载时清理
    useEffect(() => {
        return () => {
            cleanup();
        };
    }, [cleanup]);

    return {
        visibleContent,
        isRendering,
        pendingCount,
        addCharacters,
        reset,
        flush,
        stop,
    };
}

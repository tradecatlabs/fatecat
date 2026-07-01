/**
 * MBTI 进度条组件
 * 
 * 使用 BottomBar 组件，支持点击展开查看题号
 */
'use client';

import { useState, useMemo } from 'react';
import { ChevronUp, ChevronDown } from 'lucide-react';
import { BottomBar } from '@/components/layout/BottomBar';

interface MBTIProgressBarProps {
    totalQuestions: number;
    answeredIndexes: number[];
    currentQuestionIndex: number;  // 当前正在做的题目索引
    onJumpToQuestion: (index: number) => void;
}

export function MBTIProgressBar({
    totalQuestions,
    answeredIndexes,
    currentQuestionIndex,
    onJumpToQuestion,
}: MBTIProgressBarProps) {
    const [expanded, setExpanded] = useState(false);

    const answeredCount = answeredIndexes.length;
    const progress = totalQuestions > 0 ? (answeredCount / totalQuestions) * 100 : 0;

    // 生成题号数据
    const questionNumbers = useMemo(() => {
        const numbers = [];
        for (let i = 0; i < totalQuestions; i++) {
            numbers.push({
                index: i,
                number: i + 1,
                answered: answeredIndexes.includes(i),
                isCurrent: i === currentQuestionIndex,  // 只高亮当前题目
            });
        }
        return numbers;
    }, [totalQuestions, answeredIndexes, currentQuestionIndex]);

    // 题号网格（可展开内容）
    const questionGrid = (
        <div className="grid grid-cols-10 gap-2 max-h-56 overflow-y-auto p-1">
            {questionNumbers.map(({ index, number, answered, isCurrent }) => (
                <button
                    key={index}
                    onClick={() => onJumpToQuestion(index)}
                    className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium
                        transition-all hover:scale-110 ${answered
                            ? 'bg-green-500 text-white'
                            : 'bg-background-secondary dark:bg-gray-700 text-gray-500 dark:text-gray-400'
                        } ${isCurrent ? 'ring-2 ring-accent ring-offset-2 ring-offset-background' : ''}`}
                >
                    {number}
                </button>
            ))}
        </div>
    );

    return (
        <BottomBar
            show={true}
            expandableContent={questionGrid}
            expanded={expanded}
            expandedMaxHeight="260px"
        >
            {/* 左侧：展开按钮 */}
            <button
                onClick={() => setExpanded(!expanded)}
                className="flex items-center gap-2 text-foreground-secondary hover:text-foreground transition-colors"
            >
                {expanded ? (
                    <ChevronDown className="w-4 h-4" />
                ) : (
                    <ChevronUp className="w-4 h-4" />
                )}
                <span className="text-sm">
                    {expanded ? '收起' : '查看题号'}
                </span>
            </button>

            {/* 右侧：进度信息 */}
            <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 text-sm">
                    <span className="text-green-600 dark:text-green-400 font-medium">
                        ✓ {answeredCount}
                    </span>
                    <span className="text-foreground-secondary">/</span>
                    <span className="text-gray-500">
                        {totalQuestions}
                    </span>
                </div>

                <div className="w-24 h-2 bg-background-secondary dark:bg-gray-700 rounded-full overflow-hidden">
                    <div
                        className="h-full bg-accent transition-all duration-300"
                        style={{ width: `${progress}%` }}
                    />
                </div>
            </div>
        </BottomBar>
    );
}

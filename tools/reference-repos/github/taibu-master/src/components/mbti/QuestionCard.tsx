/**
 * MBTI 测试题目卡片组件 (7级 Likert 量表)
 */
'use client';

import { type MBTIQuestion, type LikertValue } from '@/lib/divination/mbti';

interface QuestionCardProps {
    question: MBTIQuestion;
    questionNumber: number;
    totalQuestions: number;
    onAnswer: (likertValue: LikertValue) => void;
    selectedValue?: LikertValue;
    showProgress?: boolean;  // 是否显示顶部进度条
}

// Likert 量表配置
const LIKERT_OPTIONS: { value: LikertValue; size: number }[] = [
    { value: 1, size: 40 },   // 强烈同意 A
    { value: 2, size: 32 },   // 同意 A
    { value: 3, size: 26 },   // 略同意 A
    { value: 4, size: 20 },   // 中立
    { value: 5, size: 26 },   // 略同意 B
    { value: 6, size: 32 },   // 同意 B
    { value: 7, size: 40 },   // 强烈同意 B
];

export function QuestionCard({
    question,
    questionNumber,
    totalQuestions,
    onAnswer,
    selectedValue,
    showProgress = false
}: QuestionCardProps) {
    // 获取选项颜色 - 使用 Notion 风格的辅助色
    const getOptionStyle = (value: LikertValue, isSelected: boolean) => {
        if (!isSelected) {
            // 未选中状态：淡灰色边框
            return {
                borderColor: '#e2e8f0',
                backgroundColor: 'transparent',
            };
        }

        // 选中状态：Notion 强调色
        if (value <= 3) {
            return {
                borderColor: '#0f7b6c', // green
                backgroundColor: '#0f7b6c',
            };
        } else if (value === 4) {
            return {
                borderColor: '#37352f', // dark gray
                backgroundColor: '#37352f',
            };
        } else {
            return {
                borderColor: '#a083ff', // purple/violet
                backgroundColor: '#a083ff',
            };
        }
    };

    return (
        <div className="w-full text-foreground">
            {/* 进度条（可选） */}
            {showProgress && (
                <div className="mb-6">
                    <div className="flex justify-between text-[11px] font-bold uppercase tracking-wider text-foreground/40 mb-2">
                        <span>问题 {questionNumber}/{totalQuestions}</span>
                        <span>{Math.round((questionNumber / totalQuestions) * 100)}%</span>
                    </div>
                    <div className="h-1 bg-background-secondary rounded-full overflow-hidden">
                        <div
                            className="h-full bg-[#2383e2] transition-all duration-300"
                            style={{ width: `${(questionNumber / totalQuestions) * 100}%` }}
                        />
                    </div>
                </div>
            )}

            {/* 题号 */}
            <div className="text-[11px] font-bold uppercase tracking-widest text-[#2383e2] mb-3">QUESTION {questionNumber}</div>

            {/* 问题 */}
            <div className="bg-background rounded-md p-5 mb-8 border border-border/60">
                <p className="text-base font-bold text-center leading-relaxed">
                    {question.question}
                </p>
            </div>

            {/* Likert 量表 */}
            <div className="space-y-4">
                {/* 圆圈选项 */}
                <div className="flex items-center justify-between px-2">
                    {LIKERT_OPTIONS.map(({ value, size }) => {
                        const isSelected = selectedValue === value;
                        const style = getOptionStyle(value, isSelected);

                        return (
                            <button
                                key={value}
                                onClick={() => onAnswer(value)}
                                className={`transition-all duration-150 rounded-full border-2 ${isSelected ? '' : 'hover:border-[#37352f]/30'}`}
                                style={{
                                    width: size,
                                    height: size,
                                    borderColor: style.borderColor,
                                    backgroundColor: style.backgroundColor,
                                }}
                                aria-label={`选择 ${value}`}
                            />
                        );
                    })}
                </div>

                {/* 选项文字说明 - 使用实际选项文字 */}
                <div className="flex justify-between gap-4">
                    <div className="flex-1 text-left">
                        <p className="text-xs font-bold text-[#0f7b6c] px-1 line-clamp-2 uppercase tracking-tight">
                            {question.choice_a.text}
                        </p>
                    </div>
                    <div className="flex-1 text-right">
                        <p className="text-xs font-bold text-[#a083ff] px-1 line-clamp-2 uppercase tracking-tight">
                            {question.choice_b.text}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}

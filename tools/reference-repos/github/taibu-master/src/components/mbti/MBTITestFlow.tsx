/**
 * MBTI 测试流程组件
 *
 * 负责题目作答、分页与结果计算
 */
'use client'; // Uses client-side state, scrolling, and navigation.

import { useState, useEffect, useCallback, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, ArrowRight, Brain, Check } from 'lucide-react';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { saveDivinationAction } from '@/lib/divination/save-client';
import { QuestionCard } from '@/components/mbti/QuestionCard';
import { MBTIProgressBar } from '@/components/mbti/MBTIProgressBar';
import { useToast } from '@/components/ui/Toast';
import {
    loadQuestions,
    calculateResult,
    type MBTIQuestion,
    type TestAnswer,
    type LikertValue,
} from '@/lib/divination/mbti';
import { supabase } from '@/lib/auth';

const QUESTIONS_PER_PAGE = 10;

export function MBTITestFlow() {
    const router = useRouter();
    const { showToast } = useToast();
    // Tracks test progress and answers on the client.
    const [questions, setQuestions] = useState<MBTIQuestion[]>([]);
    const [currentPage, setCurrentPage] = useState(0);
    const [answers, setAnswers] = useState<TestAnswer[]>([]);
    const [highlightedQuestion, setHighlightedQuestion] = useState<number | null>(null);
    const [isCalculating, setIsCalculating] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    // Controls the intro modal before answering.
    const [showIntroModal, setShowIntroModal] = useState(true);

    // 加载全部题目
    useEffect(() => {
        let active = true;
        loadQuestions()
            .then((allQuestions) => {
                if (!active) return;
                setQuestions(allQuestions);
                setIsLoading(false);
            })
            .catch(() => {
                if (!active) return;
                setQuestions([]);
                setIsLoading(false);
            });

        return () => {
            active = false;
        };
    }, []);

    // 当前页的题目
    const currentPageQuestions = useMemo(() => {
        const start = currentPage * QUESTIONS_PER_PAGE;
        const end = Math.min(start + QUESTIONS_PER_PAGE, questions.length);
        return questions.slice(start, end);
    }, [questions, currentPage]);

    // 总页数
    const totalPages = Math.ceil(questions.length / QUESTIONS_PER_PAGE);

    // 已回答的题目索引
    const answeredIndexes = useMemo(() => {
        return answers.map(a => a.questionIndex);
    }, [answers]);

    // 当前页所有题目是否已答完
    const currentPageAllAnswered = useMemo(() => {
        const start = currentPage * QUESTIONS_PER_PAGE;
        const end = Math.min(start + QUESTIONS_PER_PAGE, questions.length);
        for (let i = start; i < end; i++) {
            if (!answeredIndexes.includes(i)) {
                return false;
            }
        }
        return true;
    }, [currentPage, questions.length, answeredIndexes]);

    // 当前正在做的题目索引（当前页第一道未答题，如果都答完则为该页最后一题）
    const currentQuestionIndex = useMemo(() => {
        const start = currentPage * QUESTIONS_PER_PAGE;
        const end = Math.min(start + QUESTIONS_PER_PAGE, questions.length);
        for (let i = start; i < end; i++) {
            if (!answeredIndexes.includes(i)) {
                return i;
            }
        }
        return end - 1; // 都答完了就高亮最后一题
    }, [currentPage, questions.length, answeredIndexes]);

    const handleAnswer = useCallback((questionIndex: number, likertValue: LikertValue | null) => {
        // 如果点击相同选项，取消选择
        const existingAnswer = answers.find(a => a.questionIndex === questionIndex);
        if (existingAnswer && existingAnswer.likertValue === likertValue) {
            setAnswers(answers.filter(a => a.questionIndex !== questionIndex));
            return;
        }

        if (likertValue === null) return;

        const newAnswer: TestAnswer = {
            questionIndex,
            likertValue,
        };

        // 更新或添加答案
        const existingIndex = answers.findIndex(a => a.questionIndex === questionIndex);
        const newAnswers = existingIndex >= 0
            ? answers.map((a, i) => i === existingIndex ? newAnswer : a)
            : [...answers, newAnswer];

        setAnswers(newAnswers);

        // 清除高亮（因为用户已经开始答题）
        if (highlightedQuestion === questionIndex) {
            setHighlightedQuestion(null);
        }
    }, [answers, highlightedQuestion]);

    const goToPreviousPage = useCallback(() => {
        if (currentPage > 0) {
            setCurrentPage(currentPage - 1);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }, [currentPage]);

    const handleJumpToQuestion = useCallback((index: number) => {
        const targetPage = Math.floor(index / QUESTIONS_PER_PAGE);
        const needsPageChange = targetPage !== currentPage;

        setCurrentPage(targetPage);
        setHighlightedQuestion(index);

        // 滚动到指定题目
        const scrollToQuestion = () => {
            const questionElement = document.getElementById(`question-${index}`);
            if (questionElement) {
                questionElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        };

        if (needsPageChange) {
            // 如果需要切换页面，等待渲染完成
            setTimeout(scrollToQuestion, 150);
        } else {
            scrollToQuestion();
        }
    }, [currentPage]);

    const goToNextPage = useCallback(() => {
        if (!currentPageAllAnswered) {
            showToast('warning', '请完成当前页的所有题目后再翻页');
            return;
        }
        if (currentPage < totalPages - 1) {
            const nextIndex = (currentPage + 1) * QUESTIONS_PER_PAGE;
            handleJumpToQuestion(nextIndex);
        }
    }, [currentPageAllAnswered, currentPage, totalPages, handleJumpToQuestion, showToast]);

    const finishTest = useCallback(async () => {
        if (answers.length < questions.length) {
            const unanswered = questions.length - answers.length;
            showToast('warning', `还有 ${unanswered} 道题未完成，请完成所有题目后再提交`);
            return;
        }

        setIsCalculating(true);

        // 计算结果
        const result = calculateResult(questions, answers);

        // 保存测试记录到数据库
        let readingId: string | null = null;
        try {
            const { data: { session } } = await supabase.auth.getSession();
            if (session?.user) {
                const saveResult = await saveDivinationAction({
                    endpoint: '/api/mbti',
                    body: {
                        type: result.type,
                        scores: result.scores,
                        percentages: result.percentages,
                    },
                    idKey: 'readingId',
                    fallbackMessage: '保存测试记录失败',
                });
                if (!saveResult.ok) {
                    throw new Error(saveResult.error.message || '保存测试记录失败');
                }
                if (saveResult.id) {
                    readingId = saveResult.id;
                }
            }
        } catch (error) {
            console.error('保存测试记录失败:', error);
        }

        // 存储结果到 sessionStorage（包含 readingId）
        sessionStorage.setItem('mbti_result', JSON.stringify({ ...result, readingId }));

        // 延迟跳转
        setTimeout(() => {
            router.push('/mbti/result');
        }, 1500);
    }, [answers, questions, showToast, router]);

    if (isCalculating) {
        return (
            <div className="min-h-screen bg-background flex items-center justify-center">
                <div className="text-center">
                    <Brain className="w-16 h-16 text-[#2383e2] mx-auto mb-4" />
                    <h2 className="text-xl font-bold text-foreground mb-2">正在分析你的性格类型...</h2>
                    <p className="text-foreground/60 font-medium tracking-wide">请稍候</p>
                </div>
            </div>
        );
    }

    if (!showIntroModal && isLoading) {
        return (
            <div className="min-h-screen bg-background flex items-center justify-center">
                <div className="text-center">
                    <SoundWaveLoader variant="inline" />
                    <p className="text-foreground/60 mt-4 font-medium">正在加载题目...</p>
                </div>
            </div>
        );
    }

    if (!showIntroModal && !isLoading && questions.length === 0) {
        return (
            <div className="min-h-screen bg-background flex items-center justify-center px-4">
                <div className="text-center">
                    <p className="text-foreground/60 font-medium">题库加载失败，请稍后再试</p>
                    <button
                        onClick={() => router.push('/mbti')}
                        className="mt-4 px-6 py-2 rounded-md bg-[#2383e2] text-white font-bold hover:bg-[#2383e2]/90 transition-all duration-150"
                    >
                        返回首页
                    </button>
                </div>
            </div>
        );
    }

    const isLastPage = currentPage === totalPages - 1;
    const allAnswered = answers.length === questions.length;

    return (
        <div className="min-h-screen bg-background pb-32 text-foreground">
            {!showIntroModal && !isLoading && questions.length > 0 && (
                <>
                    <div className="max-w-2xl mx-auto px-4 py-6">
                        <Link
                            href="/mbti"
                            className="inline-flex items-center gap-2 text-sm font-bold text-foreground/50
                                hover:text-foreground transition-colors mb-4"
                        >
                            <ArrowLeft className="w-4 h-4" />
                            返回首页
                        </Link>
                        {/* 页面头部 */}
                        <div className="flex items-center justify-between mb-6">
                            <div className="text-xs font-bold uppercase tracking-wider text-foreground/40">
                                第 {currentPage + 1} / {totalPages} 页
                            </div>
                            <div className="text-xs font-bold uppercase tracking-wider text-foreground/40">
                                已完成 {answers.length} / {questions.length}
                            </div>
                        </div>

                        {/* 题目列表 */}
                        <div className="space-y-8">
                            {currentPageQuestions.map((question, idx) => {
                                const globalIndex = currentPage * QUESTIONS_PER_PAGE + idx;
                                const currentAnswer = answers.find(a => a.questionIndex === globalIndex);
                                const isHighlighted = highlightedQuestion === globalIndex;

                                return (
                                    <div
                                        key={globalIndex}
                                        id={`question-${globalIndex}`}
                                        className={`bg-background rounded-lg border border-border p-6 shadow-sm transition-all duration-150 ${isHighlighted ? 'ring-2 ring-[#2383e2] ring-offset-4 ring-offset-[#f7f6f3]' : ''}`}
                                    >
                                        <QuestionCard
                                            question={question}
                                            questionNumber={globalIndex + 1}
                                            totalQuestions={questions.length}
                                            onAnswer={(value) => handleAnswer(globalIndex, value)}
                                            selectedValue={currentAnswer?.likertValue}
                                        />
                                    </div>
                                );
                            })}
                        </div>

                        {/* 分页导航 */}
                        <div className="flex justify-between mt-12">
                            <button
                                onClick={goToPreviousPage}
                                disabled={currentPage === 0}
                                className="flex items-center gap-2 px-4 py-2 text-sm font-bold text-foreground/60
                                    disabled:opacity-20 hover:bg-background-secondary rounded-md transition-all duration-150"
                            >
                                <ArrowLeft className="w-4 h-4" />
                                上一页
                            </button>

                            {isLastPage ? (
                                <button
                                    onClick={finishTest}
                                    disabled={!allAnswered}
                                    className="flex items-center gap-2 px-8 py-2 bg-[#2383e2] text-white rounded-md font-bold
                                        disabled:opacity-50 disabled:cursor-not-allowed hover:bg-[#2383e2]/90 active:bg-[#1a65b0] transition-all duration-150"
                                >
                                    <Check className="w-4 h-4" />
                                    完成测试
                                </button>
                            ) : (
                                <button
                                    onClick={goToNextPage}
                                    disabled={!currentPageAllAnswered}
                                    className="flex items-center gap-2 px-4 py-2 text-sm font-bold text-foreground/60
                                        disabled:opacity-20 hover:bg-background-secondary rounded-md transition-all duration-150"
                                >
                                    下一页
                                    <ArrowRight className="w-4 h-4" />
                                </button>
                            )}
                        </div>
                    </div>

                    {/* 底部进度条 */}
                    <MBTIProgressBar
                        totalQuestions={questions.length}
                        answeredIndexes={answeredIndexes}
                        currentQuestionIndex={highlightedQuestion ?? currentQuestionIndex}
                        onJumpToQuestion={handleJumpToQuestion}
                    />
                </>
            )}

            {showIntroModal && (
                <div
                    className="fixed inset-0 z-50 flex items-center justify-center p-4"
                    data-role="mbti-intro-modal"
                >
                    <div className="absolute inset-0 bg-[#37352f]/20 backdrop-blur-[2px]" />
                    <div className="relative w-full max-w-lg rounded-lg bg-background border border-border p-8 shadow-xl text-foreground">
                        <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
                            <Brain className="w-5 h-5 text-[#2383e2]" />
                            测试说明
                        </h3>
                        <ul className="space-y-4 text-sm font-medium text-foreground/70">
                            <li className="flex items-start gap-3">
                                <span className="w-1.5 h-1.5 rounded-full bg-[#2383e2] mt-1.5 flex-shrink-0" />
                                <span>本测试共 {questions.length || '93'} 道题，每页 {QUESTIONS_PER_PAGE} 题</span>
                            </li>
                            <li className="flex items-start gap-3">
                                <span className="w-1.5 h-1.5 rounded-full bg-[#2383e2] mt-1.5 flex-shrink-0" />
                                <span>请根据你的第一反应作答，不要过度思考</span>
                            </li>
                            <li className="flex items-start gap-3">
                                <span className="w-1.5 h-1.5 rounded-full bg-[#2383e2] mt-1.5 flex-shrink-0" />
                                <span>用量表选择你的倾向程度（左侧或右侧代表不同选项）</span>
                            </li>
                            <li className="flex items-start gap-3">
                                <span className="w-1.5 h-1.5 rounded-full bg-[#2383e2] mt-1.5 flex-shrink-0" />
                                <span>必须完成当前页所有题目才能翻到下一页</span>
                            </li>
                        </ul>
                        {isLoading && (
                            <div className="mt-6 flex items-center gap-2 text-xs font-bold text-foreground/40 uppercase tracking-wider">
                                <SoundWaveLoader variant="inline" />
                                正在加载题目...
                            </div>
                        )}
                        <div className="mt-10 flex items-center justify-end gap-3">
                            <button
                                onClick={() => router.push('/mbti')}
                                className="px-6 py-2 rounded-md bg-transparent border border-border text-sm font-bold
                                    hover:bg-background-secondary active:bg-background-tertiary transition-all duration-150"
                            >
                                返回首页
                            </button>
                            <button
                                onClick={() => setShowIntroModal(false)}
                                disabled={isLoading || questions.length === 0}
                                className="px-8 py-2 rounded-md bg-[#2383e2] text-white text-sm font-bold hover:bg-[#2383e2]/90
                                    active:bg-[#1a65b0] disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-150 shadow-sm"
                            >
                                开始测试
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

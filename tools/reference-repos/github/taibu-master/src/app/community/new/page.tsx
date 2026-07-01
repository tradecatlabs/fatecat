/**
 * 发布新帖子页面
 *
 * 'use client' 标记说明：
 * - 使用 React hooks (useState, useEffect)
 * - 使用 useRouter 进行客户端导航
 */
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft } from 'lucide-react';
import { useSessionSafe } from '@/components/providers/ClientProviders';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { PostCategory, POST_CATEGORIES, createPost } from '@/lib/community';

export default function NewPostPage() {
    const router = useRouter();
    const { user, loading: sessionLoading } = useSessionSafe();
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [category, setCategory] = useState<PostCategory>('general');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        if (!sessionLoading && !user) {
            router.push('/community');
        }
    }, [router, sessionLoading, user]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!title.trim() || !content.trim()) {
            setError('标题和内容不能为空');
            return;
        }

        setLoading(true);
        setError('');

        try {
            const post = await createPost({
                title,
                content,
                category,
            });
            router.push(`/community/${post.id}`);
        } catch (submitError) {
            setError(submitError instanceof Error ? submitError.message : '发帖失败，请重试');
        } finally {
            setLoading(false);
        }
    };

    if (sessionLoading) {
        return (
            <div className="min-h-screen bg-background flex items-center justify-center">
                <SoundWaveLoader variant="block" />
            </div>
        );
    }

    if (!user) {
        return (
            <div className="min-h-screen bg-background flex items-center justify-center px-4">
                <div className="rounded-xl border border-[#ead9bf] bg-[#fcf8ee] px-5 py-4 text-sm text-[#946c21]">
                    {error || '认证失败，请返回社区后重试。'}
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background text-foreground relative overflow-hidden">
            {/* Background Decorations */}
            <div className="absolute top-0 right-0 w-96 h-96 bg-purple-500/10 rounded-full blur-[100px] pointer-events-none -translate-y-1/2 translate-x-1/2" />
            <div className="absolute bottom-0 left-0 w-64 h-64 bg-indigo-500/10 rounded-full blur-[80px] pointer-events-none translate-y-1/2 -translate-x-1/4" />

            <div className="max-w-3xl mx-auto px-4 py-8 relative z-10">
                {/* Header */}
                <div className="mb-8">
                    <button
                        onClick={() => router.back()}
                        className="flex items-center gap-2 text-foreground-secondary hover:text-purple-600 transition-colors mb-6 group"
                    >
                        <div className="p-2 rounded-full bg-background-secondary group-hover:bg-purple-100 dark:group-hover:bg-purple-900/30 transition-colors">
                            <ArrowLeft className="w-4 h-4 group-hover:-translate-x-0.5 transition-transform" />
                        </div>
                        <span className="font-medium">返回社区</span>
                    </button>

                    <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-indigo-600 dark:from-purple-400 dark:to-indigo-400 mb-2">
                        发起新的讨论
                    </h1>
                    <p className="text-foreground-secondary/80 text-lg">
                        分享你的命理见解，或提出困扰你的问题
                    </p>
                </div>

                {/* Main Form Card */}
                <div className="bg-background-secondary/40 backdrop-blur-xl border border-border/50 rounded-2xl shadow-xl overflow-hidden">
                    <div className="h-1 bg-gradient-to-r from-purple-500 via-indigo-500 to-purple-500" />

                    <form onSubmit={handleSubmit} className="p-6 md:p-8 space-y-8">
                        {error && (
                            <div className="bg-red-500/10 border border-red-500/20 text-red-600 dark:text-red-400 p-4 rounded-xl flex items-center gap-3 animate-in fade-in slide-in-from-top-2">
                                <span className="text-lg">⚠️</span>
                                <p>{error}</p>
                            </div>
                        )}

                        <div className="grid md:grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="block text-sm font-medium text-foreground-secondary ml-1">
                                    话题分类
                                </label>
                                <div className="relative">
                                    <select
                                        value={category}
                                        onChange={(e) => setCategory(e.target.value as PostCategory)}
                                        className="w-full bg-background/50 border border-border/50 hover:border-purple-500/30 rounded-xl px-4 py-3 pl-10 text-foreground focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500/20 transition-all appearance-none cursor-pointer font-medium"
                                    >
                                        {POST_CATEGORIES.map(cat => (
                                            <option key={cat.value} value={cat.value}>
                                                {cat.label}
                                            </option>
                                        ))}
                                    </select>
                                    <div className="absolute left-3 top-1/2 -translate-y-1/2 text-foreground-secondary/50">
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>
                                    </div>
                                    <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-foreground-secondary">
                                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
                                    </div>
                                </div>
                            </div>

                            <div className="space-y-2">
                                <label className="block text-sm font-medium text-foreground-secondary ml-1">
                                    发布身份
                                </label>
                                <div className="w-full bg-background/50 border border-border/50 rounded-xl px-4 py-3 text-foreground-secondary">
                                    社区将显示你的公开昵称
                                </div>
                                <p className="text-xs text-foreground-secondary/60 ml-1">
                                    如需修改显示名称，请前往账户页调整昵称
                                </p>
                            </div>
                        </div>

                        {/* Title */}
                        <div className="space-y-2">
                            <label className="block text-sm font-medium text-foreground-secondary ml-1">
                                标题 <span className="text-red-400">*</span>
                            </label>
                            <input
                                type="text"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                className="w-full bg-background/50 border border-border/50 hover:border-purple-500/30 rounded-xl px-4 py-3 text-foreground text-lg font-medium placeholder:font-normal focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500/20 transition-all"
                                placeholder="请用一两句话概括你的主题"
                                maxLength={100}
                            />
                        </div>

                        {/* Content */}
                        <div className="space-y-2">
                            <label className="block text-sm font-medium text-foreground-secondary ml-1">
                                内容详情 <span className="text-red-400">*</span>
                            </label>
                            <div className="relative">
                                <textarea
                                    value={content}
                                    onChange={(e) => setContent(e.target.value)}
                                    rows={12}
                                    className="w-full bg-background/50 border border-border/50 hover:border-purple-500/30 rounded-xl p-4 text-foreground leading-relaxed focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500/20 transition-all resize-none"
                                    placeholder="请详细描述你的问题或观点，支持 Markdown 格式..."
                                />
                                <div className="absolute bottom-3 right-3 text-xs text-foreground-secondary/50 font-mono pointer-events-none">
                                    {content.length} 字
                                </div>
                            </div>
                        </div>

                        {/* Actions */}
                        <div className="flex items-center gap-4 pt-4 border-t border-border/30">
                            <button
                                type="button"
                                onClick={() => router.back()}
                                className="px-6 py-3 rounded-xl border border-border/50 hover:bg-background-secondary text-foreground-secondary hover:text-foreground transition-all font-medium"
                            >
                                取消
                            </button>
                            <button
                                type="submit"
                                disabled={loading || !title.trim() || !content.trim()}
                                className="flex-1 px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-medium rounded-xl shadow-lg shadow-purple-500/20 transition-all hover:scale-[1.01] active:scale-[0.99] disabled:opacity-70 disabled:hover:scale-100 disabled:shadow-none flex items-center justify-center gap-2"
                            >
                                {loading ? (
                                    <>
                                        <SoundWaveLoader variant="inline" />
                                        发布中...
                                    </>
                                ) : (
                                    <>
                                        <span className="text-lg">✨</span> 发布帖子
                                    </>
                                )}
                            </button>
                        </div>
                    </form>
                </div>

                {/* Guidelines Tip */}
                <div className="mt-8 text-center text-sm text-foreground-secondary/60">
                    <p>发布即代表同意社区友好准则，请理性讨论</p>
                </div>
            </div>
        </div>
    );
}

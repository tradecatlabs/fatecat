/**
 * 帖子操作组件：投票按钮、举报模态框、编辑帖子模态框
 *
 * 'use client' 标记说明：
 * - 使用 React hooks (useState)
 * - 有表单交互
 */
'use client';

import { useState } from 'react';
import {
    ThumbsUp,
    ThumbsDown,
    Flag,
    Edit2,
    Trash2,
    Pin,
    Star,
} from 'lucide-react';
import { CommunityPost, VoteType, REPORT_REASONS, createReport, updatePost } from '@/lib/community';
import { useToast } from '@/components/ui/Toast';

// =====================================================
// 投票按钮组件
// =====================================================
export function VoteButtons({
    upvotes,
    downvotes,
    userVote,
    onVote
}: {
    upvotes: number;
    downvotes: number;
    userVote: VoteType | null;
    onVote: (type: VoteType) => void;
}) {
    return (
        <div className="flex items-center gap-2">
            <button
                onClick={() => onVote('up')}
                className={`flex items-center gap-1 px-2 py-1 rounded transition-colors ${userVote === 'up'
                    ? 'bg-green-500/20 text-green-400'
                    : 'text-foreground-secondary hover:text-green-400'
                    }`}
            >
                <ThumbsUp className="w-4 h-4" />
                <span className="text-sm">{upvotes}</span>
            </button>
            <button
                onClick={() => onVote('down')}
                className={`flex items-center gap-1 px-2 py-1 rounded transition-colors ${userVote === 'down'
                    ? 'bg-red-500/20 text-red-400'
                    : 'text-foreground-secondary hover:text-red-400'
                    }`}
            >
                <ThumbsDown className="w-4 h-4" />
                <span className="text-sm">{downvotes}</span>
            </button>
        </div>
    );
}

// =====================================================
// 举报模态框
// =====================================================
export function ReportModal({
    targetType,
    targetId,
    onClose
}: {
    targetType: 'post' | 'comment';
    targetId: string;
    onClose: () => void;
}) {
    const { showToast } = useToast();
    const [reason, setReason] = useState('');
    const [description, setDescription] = useState('');
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!reason) return;

        setLoading(true);
        try {
            await createReport(targetType, targetId, reason as typeof REPORT_REASONS[number]['value'], description);
            setSuccess(true);
            setTimeout(onClose, 1500);
        } catch (error) {
            showToast('error', error instanceof Error ? error.message : '提交举报失败');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-background rounded-xl w-full max-w-md border border-border">
                <div className="p-4 border-b border-border">
                    <h2 className="text-lg font-medium text-foreground">举报{targetType === 'post' ? '帖子' : '评论'}</h2>
                </div>
                <form onSubmit={handleSubmit} className="p-4 space-y-4">
                    {success ? (
                        <div className="text-green-400 text-center py-4">
                            举报已提交，感谢您的反馈
                        </div>
                    ) : (
                        <>
                            <div>
                                <label className="block text-sm text-foreground-secondary mb-2">举报原因 *</label>
                                <div className="space-y-2">
                                    {REPORT_REASONS.map(r => (
                                        <label key={r.value} className="flex items-center gap-2 cursor-pointer">
                                            <input
                                                type="radio"
                                                name="reason"
                                                value={r.value}
                                                checked={reason === r.value}
                                                onChange={(e) => setReason(e.target.value)}
                                                className="text-purple-600"
                                            />
                                            <span className="text-foreground">{r.label}</span>
                                        </label>
                                    ))}
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm text-foreground-secondary mb-1">补充说明</label>
                                <textarea
                                    value={description}
                                    onChange={(e) => setDescription(e.target.value)}
                                    rows={3}
                                    className="w-full bg-background-secondary border border-border rounded-lg px-3 py-2 text-foreground focus:outline-none focus:border-accent resize-none"
                                    placeholder="可选"
                                />
                            </div>

                            <div className="flex gap-2 pt-2">
                                <button
                                    type="button"
                                    onClick={onClose}
                                    className="flex-1 px-4 py-2 text-foreground-secondary hover:text-foreground transition-colors"
                                >
                                    取消
                                </button>
                                <button
                                    type="submit"
                                    disabled={loading || !reason}
                                    className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50"
                                >
                                    {loading ? '提交中...' : '提交举报'}
                                </button>
                            </div>
                        </>
                    )}
                </form>
            </div>
        </div>
    );
}

// =====================================================
// 编辑帖子弹窗
// =====================================================
export function EditPostModal({
    post,
    onClose,
    onSave
}: {
    post: CommunityPost;
    onClose: () => void;
    onSave: (updatedPost: CommunityPost) => void;
}) {
    const [title, setTitle] = useState(post.title);
    const [content, setContent] = useState(post.content);
    const { showToast } = useToast();
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!title.trim() || !content.trim()) return;

        setLoading(true);
        try {
            const updatedPost = await updatePost(post.id, { title, content });
            onSave({ ...post, ...updatedPost, title, content });
            onClose();
        } catch (error) {
            showToast('error', error instanceof Error ? error.message : '更新失败，请重试');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-in fade-in duration-200">
            <div className="bg-background/95 backdrop-blur-xl rounded-2xl w-full max-w-2xl border border-white/10 max-h-[90vh] overflow-hidden flex flex-col shadow-2xl animate-in zoom-in-95 duration-200">
                <div className="p-5 border-b border-border/50 flex-shrink-0 bg-gradient-to-r from-purple-500/10 to-indigo-500/10 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-purple-500/10 flex items-center justify-center text-purple-500 shadow-inner">
                        <Edit2 className="w-5 h-5" />
                    </div>
                    <div>
                        <h2 className="text-lg font-bold text-foreground">编辑讨论</h2>
                        <p className="text-xs text-foreground-secondary">完善你的观点，让讨论更精彩</p>
                    </div>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-5 overflow-y-auto flex-1">
                    <div>
                        <label className="block text-sm font-medium text-foreground-secondary mb-1.5 ml-1">标题</label>
                        <input
                            type="text"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            className="w-full bg-background-secondary/50 border border-border/50 hover:border-purple-500/50 rounded-xl px-4 py-3 text-foreground font-medium focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500/20 transition-all"
                            placeholder="请输入精炼的标题"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-foreground-secondary mb-1.5 ml-1">内容</label>
                        <textarea
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            rows={10}
                            className="w-full bg-background-secondary/50 border border-border/50 hover:border-purple-500/50 rounded-xl px-4 py-3 text-foreground focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500/20 transition-all resize-none leading-relaxed"
                            placeholder="请输入详细内容"
                        />
                    </div>

                    <div className="flex gap-3 pt-2">
                        <button
                            type="button"
                            onClick={onClose}
                            className="flex-1 px-4 py-2.5 rounded-xl border border-border hover:bg-background-secondary/80 text-foreground-secondary hover:text-foreground transition-all"
                        >
                            取消
                        </button>
                        <button
                            type="submit"
                            disabled={loading || !title.trim() || !content.trim()}
                            className="flex-1 px-4 py-2.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-medium rounded-xl shadow-lg shadow-purple-500/20 transition-all hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:hover:scale-100"
                        >
                            {loading ? '保存中...' : '保存修改'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

// =====================================================
// 帖子顶部导航栏（含编辑/删除/管理员操作）
// =====================================================
export interface PostNavBarProps {
    isAuthor: boolean;
    isAdmin: boolean;
    post: CommunityPost;
    onBack: () => void;
    onEdit: () => void;
    onDelete: () => void;
    onAdminAction: (action: 'pin' | 'feature' | 'delete', value?: boolean) => void;
}

export function PostNavBar({
    isAuthor,
    isAdmin,
    post,
    onBack,
    onEdit,
    onDelete,
    onAdminAction,
}: PostNavBarProps) {
    return (
        <div className="sticky top-0 z-30 bg-background/80 backdrop-blur-md border-b border-border/50">
            <div className="max-w-3xl mx-auto px-4 h-14 flex items-center justify-between">
                <button
                    onClick={onBack}
                    className="flex items-center gap-2 text-foreground-secondary hover:text-foreground transition-colors p-2 -ml-2 rounded-lg hover:bg-background-secondary/50"
                >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
                    <span className="font-medium">返回</span>
                </button>

                {(isAuthor || isAdmin) && (
                    <div className="flex items-center gap-1">
                        <button
                            onClick={onEdit}
                            className="p-2 text-foreground-secondary hover:text-purple-500 hover:bg-purple-500/10 rounded-lg transition-colors"
                            title="编辑"
                        >
                            <Edit2 className="w-4 h-4" />
                        </button>
                        <button
                            onClick={onDelete}
                            className="p-2 text-foreground-secondary hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-colors"
                            title="删除"
                        >
                            <Trash2 className="w-4 h-4" />
                        </button>
                    </div>
                )}
                {isAdmin && (
                    <div className="flex items-center gap-1 ml-1 border-l border-border pl-1">
                        <button
                            onClick={() => onAdminAction('pin', !post.is_pinned)}
                            className={`p-2 rounded-lg transition-colors ${post.is_pinned ? 'text-yellow-500 bg-yellow-500/10' : 'text-foreground-secondary hover:text-yellow-500 hover:bg-yellow-500/10'}`}
                            title={post.is_pinned ? '取消置顶' : '置顶'}
                        >
                            <Pin className="w-4 h-4" />
                        </button>
                        <button
                            onClick={() => onAdminAction('feature', !post.is_featured)}
                            className={`p-2 rounded-lg transition-colors ${post.is_featured ? 'text-purple-500 bg-purple-500/10' : 'text-foreground-secondary hover:text-purple-500 hover:bg-purple-500/10'}`}
                            title={post.is_featured ? '取消精华' : '设为精华'}
                        >
                            <Star className="w-4 h-4" />
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}

// =====================================================
// 帖子底部操作栏（投票 + 举报）
// =====================================================
export interface PostFooterActionsProps {
    post: CommunityPost;
    postVote: VoteType | null;
    onVote: (type: VoteType) => void;
    onReport: () => void;
}

export function PostFooterActions({
    post,
    postVote,
    onVote,
    onReport,
}: PostFooterActionsProps) {
    return (
        <div className="flex items-center gap-6 mt-12 pt-6 border-t border-border/50">
            <VoteButtons
                upvotes={post.upvote_count}
                downvotes={post.downvote_count}
                userVote={postVote}
                onVote={onVote}
            />
            <button
                onClick={onReport}
                className="text-foreground-secondary hover:text-foreground text-sm flex items-center gap-1.5 transition-colors ml-auto"
            >
                <Flag className="w-4 h-4" /> 举报
            </button>
        </div>
    );
}

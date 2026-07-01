/**
 * 记录详情相关组件：表单模态框、小记、导入导出
 *
 * 'use client' 标记说明：
 * - 使用 React hooks (useState)
 * - 有表单交互和文件上传
 */
'use client';

import { useState } from 'react';
import {
    Plus,
    Edit2,
    Trash2,
    Download,
    Upload,
    BookOpen,
    ChevronRight,
} from 'lucide-react';
import {
    createNote,
    createRecord,
    deleteNote,
    downloadExportData,
    exportData,
    importData,
    MingRecord,
    MingNote,
    RecordCategory,
    RECORD_CATEGORIES,
    readImportFile,
    NOTE_MOODS,
    NoteMood,
    updateRecord,
} from '@/lib/records';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { ConfirmDialog } from '@/components/ui/ConfirmDialog';
import { useToast } from '@/components/ui/Toast';

function getErrorMessage(error: unknown, fallback: string) {
    return error instanceof Error && error.message ? error.message : fallback;
}

// =====================================================
// 记录表单模态框
// =====================================================
export function RecordFormModal({
    userId,
    record,
    onClose,
    onSave
}: {
    userId: string | null;
    record?: MingRecord | null;
    onClose: () => void;
    onSave: () => void | Promise<void>;
}) {
    const [title, setTitle] = useState(record?.title || '');
    const [content, setContent] = useState(record?.content || '');
    const [category, setCategory] = useState<RecordCategory>(record?.category || 'general');
    const [eventDate, setEventDate] = useState(record?.event_date || new Date().toISOString().split('T')[0]);
    const [tagsInput, setTagsInput] = useState(record?.tags.join(', ') || '');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const { showToast } = useToast();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!userId) {
            setError('请先登录后再保存记录');
            return;
        }
        if (!title.trim()) {
            setError('标题不能为空');
            return;
        }

        setLoading(true);
        setError('');

        try {
            const tags = tagsInput.split(/[,，]/).map(t => t.trim()).filter(Boolean);
            const data = {
                title: title.trim(),
                content: content.trim() || undefined,
                category,
                event_date: eventDate || undefined,
                tags,
            };

            if (record) {
                await updateRecord(record.id, data);
            } else {
                await createRecord(data);
            }

            await Promise.resolve(onSave());
        } catch (saveError) {
            const message = getErrorMessage(saveError, '保存失败，请重试');
            setError(message);
            showToast('error', message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-in fade-in duration-200">
            <div className="bg-background/95 backdrop-blur-xl rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto border border-white/10 shadow-2xl animate-in zoom-in-95 duration-200">
                <div className="p-4 sm:p-6 border-b border-border/50 flex flex-col items-center justify-center bg-gradient-to-r from-emerald-500/5 to-teal-500/5">
                    <div className="w-12 h-12 rounded-full bg-emerald-500/10 flex items-center justify-center text-emerald-500 mb-3 shadow-inner">
                        {record ? <Edit2 className="w-5 h-5" /> : <Plus className="w-5 h-5" />}
                    </div>
                    <h2 className="text-xl font-bold text-foreground">{record ? '编辑命理记录' : '新增命理感悟'}</h2>
                    <p className="text-sm text-foreground-secondary mt-1">记录当下的所思所想，积累智慧</p>
                </div>

                <form onSubmit={handleSubmit} className="p-4 sm:p-6 space-y-5">
                    {error && (
                        <div className="text-red-400 text-sm bg-red-500/10 border border-red-500/20 p-3 rounded-xl flex items-center gap-2">
                            <div className="w-1.5 h-1.5 rounded-full bg-red-500" />
                            {error}
                        </div>
                    )}

                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-foreground-secondary mb-1.5 ml-1">标题</label>
                            <input
                                type="text"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                className="w-full bg-background-secondary/50 border border-border/50 hover:border-emerald-500/50 rounded-xl px-4 py-3 text-foreground placeholder:text-foreground-secondary/30 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500/20 transition-all"
                                placeholder="例如：今日八字排盘感悟..."
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-foreground-secondary mb-1.5 ml-1">分类</label>
                                <div className="relative">
                                    <select
                                        value={category}
                                        onChange={(e) => setCategory(e.target.value as RecordCategory)}
                                        className="w-full bg-background-secondary/50 border border-border/50 hover:border-emerald-500/50 rounded-xl px-4 py-2.5 text-foreground focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500/20 transition-all appearance-none cursor-pointer"
                                    >
                                        {RECORD_CATEGORIES.map(cat => (
                                            <option key={cat.value} value={cat.value}>
                                                {cat.label}
                                            </option>
                                        ))}
                                    </select>
                                    <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-foreground-secondary">
                                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-foreground-secondary mb-1.5 ml-1">事件日期</label>
                                <input
                                    type="date"
                                    value={eventDate}
                                    onChange={(e) => setEventDate(e.target.value)}
                                    className="w-full bg-background-secondary/50 border border-border/50 hover:border-emerald-500/50 rounded-xl px-4 py-2.5 text-foreground focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500/20 transition-all font-sans"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-foreground-secondary mb-1.5 ml-1">标签</label>
                            <input
                                type="text"
                                value={tagsInput}
                                onChange={(e) => setTagsInput(e.target.value)}
                                className="w-full bg-background-secondary/50 border border-border/50 hover:border-emerald-500/50 rounded-xl px-4 py-2.5 text-foreground placeholder:text-foreground-secondary/30 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500/20 transition-all"
                                placeholder="使用逗号分隔，例如：事业, 运势"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-foreground-secondary mb-1.5 ml-1">详情内容</label>
                            <textarea
                                value={content}
                                onChange={(e) => setContent(e.target.value)}
                                rows={6}
                                className="w-full bg-background-secondary/50 border border-border/50 hover:border-emerald-500/50 rounded-xl px-4 py-3 text-foreground placeholder:text-foreground-secondary/30 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500/20 transition-all resize-none leading-relaxed"
                                placeholder="记录详细的断语、排盘结果或心得体会..."
                            />
                        </div>
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
                            disabled={loading}
                            className="flex-1 px-4 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-500 text-white font-medium rounded-xl hover:shadow-lg hover:shadow-emerald-500/25 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 disabled:hover:scale-100"
                        >
                            {loading ? '保存中...' : '保存记录'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

// =====================================================
// 小记组件
// =====================================================
export function DailyNotes({
    userId,
    notes,
    onRefresh
}: {
    userId: string | null;
    notes: MingNote[];
    onRefresh: () => void | Promise<void>;
}) {
    const [content, setContent] = useState('');
    const [mood, setMood] = useState<NoteMood>('neutral');
    const [loading, setLoading] = useState(false);
    const [deleteNoteId, setDeleteNoteId] = useState<string | null>(null);
    const [error, setError] = useState('');
    const { showToast } = useToast();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!content.trim()) return;
        if (!userId) {
            const message = '请先登录后再记录小记';
            setError(message);
            showToast('error', message);
            return;
        }

        setLoading(true);
        setError('');
        try {
            await createNote({ content: content.trim(), mood });
            setContent('');
            await Promise.resolve(onRefresh());
        } catch (submitError) {
            const message = getErrorMessage(submitError, '创建小记失败');
            setError(message);
            showToast('error', message);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id: string) => {
        try {
            setError('');
            await deleteNote(id);
            await Promise.resolve(onRefresh());
        } catch (deleteError) {
            const message = getErrorMessage(deleteError, '删除小记失败');
            setError(message);
            showToast('error', message);
        } finally {
            setDeleteNoteId(null);
        }
    };

    return (
        <div className="bg-background/50 dark:bg-zinc-900/50 rounded-2xl p-6 border border-border/50 shadow-sm relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 group-hover:bg-emerald-500/10 transition-colors duration-700" />

            <div className="flex items-center gap-3 mb-6 relative z-10">
                <div className="p-2 bg-emerald-100 dark:bg-emerald-900/30 rounded-xl text-emerald-600 dark:text-emerald-400">
                    <BookOpen className="w-5 h-5" />
                </div>
                <div>
                    <h3 className="font-bold text-foreground">今日小记</h3>
                    <p className="text-xs text-foreground-secondary">记录当下的心情与感悟</p>
                </div>
            </div>

            {error && (
                <div className="mb-4 rounded-xl border border-red-500/20 bg-red-500/5 px-3 py-2 text-sm text-red-500 relative z-10">
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit} className="mb-6 relative z-10">
                <div className="flex flex-col gap-3">
                    <div className="flex gap-2 mb-1 p-1 bg-background-secondary/50 rounded-xl w-fit">
                        {NOTE_MOODS.map(m => (
                            <button
                                key={m.value}
                                type="button"
                                onClick={() => setMood(m.value)}
                                className={`
                                    relative w-9 h-9 rounded-lg flex items-center justify-center text-lg transition-all
                                    ${mood === m.value
                                        ? 'bg-background dark:bg-zinc-800 shadow-sm scale-110 z-10 ring-1 ring-border/50'
                                        : 'hover:bg-background/50 dark:hover:bg-zinc-800/50 hover:scale-105 opacity-60 hover:opacity-100'
                                    }
                                `}
                                title={m.label}
                            >
                                <span className={`transition-transform duration-300 ${mood === m.value ? 'scale-110' : ''}`}>
                                    {m.icon}
                                </span>
                                {mood === m.value && (
                                    <span className="absolute -bottom-1 w-1 h-1 rounded-full bg-emerald-500" />
                                )}
                            </button>
                        ))}
                    </div>

                    <div className="relative group/input">
                        <textarea
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            placeholder="写下此刻的想法..."
                            rows={2}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter' && !e.shiftKey) {
                                    e.preventDefault();
                                    handleSubmit(e);
                                }
                            }}
                            className="w-full bg-background border border-border rounded-xl pl-4 pr-12 py-3 text-foreground text-sm resize-none focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500/30 transition-all placeholder:text-foreground-secondary/40"
                        />
                        <button
                            type="submit"
                            disabled={loading || !content.trim()}
                            className="absolute right-3 bottom-3 p-1.5 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg shadow-md hover:shadow-lg disabled:opacity-50 disabled:shadow-none transition-all flex items-center justify-center transform active:scale-95"
                            title="发送 (Enter)"
                        >
                            {loading ? (
                                <SoundWaveLoader variant="inline" />
                            ) : (
                                <ChevronRight className="w-4 h-4" />
                            )}
                        </button>
                    </div>
                </div>
            </form>

            <div className="space-y-4 max-h-[18rem] overflow-y-auto pr-1">
                {notes.length === 0 ? (
                    <div className="text-center py-6 border-2 border-dashed border-border/50 rounded-xl bg-background-secondary/20">
                        <p className="text-foreground-secondary/60 text-sm">今天还没有记录，写点什么吧...</p>
                    </div>
                ) : (
                    <div className="relative pl-4 space-y-6 before:absolute before:left-[5px] before:top-2 before:bottom-0 before:w-px before:bg-gradient-to-b before:from-border before:to-transparent">
                        {notes.map((note, index) => {
                            const moodInfo = NOTE_MOODS.find(m => m.value === note.mood);
                            return (
                                <div key={note.id} className="relative group/item animate-fade-in-up" style={{ animationDelay: `${index * 50}ms` }}>
                                    <div className="absolute -left-[1.35rem] top-0 w-3 h-3 rounded-full bg-background border-2 border-emerald-500 z-10 shadow-[0_0_0_4px_rgba(var(--background-start-rgb),1)]" />

                                    <div className="bg-background hover:bg-background-secondary/40 border border-border/50 hover:border-emerald-500/20 rounded-xl p-3.5 transition-all duration-300 hover:shadow-sm">
                                        <div className="flex items-start justify-between gap-3">
                                            <div className="flex-1 min-w-0">
                                                <div className="flex items-center gap-2 mb-1.5">
                                                    <span className="text-lg leading-none filter drop-shadow-sm transform group-hover/item:scale-110 transition-transform duration-300" title={moodInfo?.label}>
                                                        {moodInfo?.icon}
                                                    </span>
                                                    <span className="text-[10px] items-center px-1.5 py-0.5 rounded-full bg-background-secondary text-foreground-secondary border border-border/50 hidden group-hover/item:inline-flex">
                                                        {moodInfo?.label}
                                                    </span>
                                                </div>
                                                <p className="text-sm text-foreground/90 leading-relaxed font-light break-words">
                                                    {note.content}
                                                </p>
                                            </div>
                                            <button
                                                onClick={() => setDeleteNoteId(note.id)}
                                                className="opacity-0 group-hover/item:opacity-100 p-1.5 text-foreground-secondary hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-all scale-90 hover:scale-100"
                                                title="删除"
                                            >
                                                <Trash2 className="w-3.5 h-3.5" />
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>
            <ConfirmDialog
                isOpen={!!deleteNoteId}
                onClose={() => setDeleteNoteId(null)}
                onConfirm={() => deleteNoteId ? handleDelete(deleteNoteId) : undefined}
                title="确认删除"
                description="确定要删除这条小记吗？此操作无法撤销。"
                confirmText="确认删除"
                variant="danger"
            />
        </div>
    );
}

// =====================================================
// 导入导出模态框
// =====================================================
export function ImportExportModal({
    userId,
    onClose,
    onImport
}: {
    userId: string | null;
    onClose: () => void;
    onImport: () => void | Promise<void>;
}) {
    const [importing, setImporting] = useState(false);
    const [exporting, setExporting] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleExport = async () => {
        if (!userId) {
            setError('请先登录后再导出数据');
            return;
        }
        setExporting(true);
        setError('');
        setSuccess('');
        try {
            const data = await exportData();
            downloadExportData(data);
            setSuccess('导出成功！');
        } catch (exportError) {
            setError(getErrorMessage(exportError, '导出失败'));
        } finally {
            setExporting(false);
        }
    };

    const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;
        if (!userId) {
            setError('请先登录后再导入数据');
            e.target.value = '';
            return;
        }

        setImporting(true);
        setError('');
        setSuccess('');

        try {
            const data = await readImportFile(file);
            const result = await importData(data);
            setSuccess(`成功导入 ${result.recordsImported} 条记录和 ${result.notesImported} 条小记`);
            await Promise.resolve(onImport());
        } catch (importError) {
            setError(getErrorMessage(importError, '导入失败'));
        } finally {
            setImporting(false);
            e.target.value = '';
        }
    };

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-background rounded-xl w-full max-w-md border border-border">
                <div className="p-4 border-b border-border">
                    <h2 className="text-lg font-medium text-foreground">数据管理</h2>
                </div>
                <div className="p-4 space-y-4">
                    {error && (
                        <div className="text-red-400 text-sm bg-red-900/20 p-2 rounded">{error}</div>
                    )}
                    {success && (
                        <div className="text-green-400 text-sm bg-green-900/20 p-2 rounded">{success}</div>
                    )}

                    <div className="space-y-2">
                        <h3 className="font-medium text-foreground flex items-center gap-2">
                            <Download className="w-4 h-4" /> 导出数据
                        </h3>
                        <p className="text-sm text-foreground-secondary">将所有记录和小记导出为 JSON 文件</p>
                        <button
                            onClick={handleExport}
                            disabled={exporting}
                            className="w-full px-4 py-2 bg-accent text-white rounded-lg hover:bg-accent/90 transition-colors disabled:opacity-50"
                        >
                            {exporting ? '导出中...' : '导出数据'}
                        </button>
                    </div>

                    <div className="border-t border-border pt-4 space-y-2">
                        <h3 className="font-medium text-foreground flex items-center gap-2">
                            <Upload className="w-4 h-4" /> 导入数据
                        </h3>
                        <div className="bg-yellow-900/20 text-yellow-400 text-sm p-2 rounded">
                            注意：导入将覆盖所有现有数据！
                        </div>
                        <label className="block w-full px-4 py-2 bg-background-secondary text-foreground rounded-lg hover:bg-background-tertiary transition-colors cursor-pointer text-center border border-border">
                            {importing ? '导入中...' : '选择 JSON 文件'}
                            <input
                                type="file"
                                accept=".json"
                                onChange={handleImport}
                                disabled={importing}
                                className="hidden"
                            />
                        </label>
                    </div>

                    <button
                        onClick={onClose}
                        className="w-full px-4 py-2 text-foreground-secondary hover:text-foreground transition-colors"
                    >
                        关闭
                    </button>
                </div>
            </div>
        </div>
    );
}

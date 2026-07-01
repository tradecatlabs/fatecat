/**
 * 添加到知识库弹窗组件
 *
 * 'use client' 标记说明：
 * - 使用 React hooks (useState, useEffect, useCallback)
 * - 有弹窗交互和表单提交功能
 */
'use client';

import { useCallback, useEffect, useState } from 'react';
import { X } from 'lucide-react';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { useToast } from '@/components/ui/Toast';
import { useKnowledgeBaseFeatureEnabled } from '@/components/knowledge-base/useKnowledgeBaseFeatureEnabled';
import {
    createKnowledgeBase,
    ingestKnowledgeBaseSource,
    listKnowledgeBases,
    type KnowledgeBaseSummary,
} from '@/lib/knowledge-base/browser-client';

export function AddToKnowledgeBaseModal({
    open,
    onClose,
    onSuccess,
    sourceTitle,
    sourceType,
    sourceId,
    sourceMeta,
}: {
    open: boolean;
    onClose: () => void;
    onSuccess?: (payload: { sourceType: string; sourceId: string; kbId: string }) => void;
    sourceTitle: string;
    sourceType: string;
    sourceId: string;
    sourceMeta?: Record<string, unknown>;
}) {
    const [kbLoading, setKbLoading] = useState(false);
    const [kbSaving, setKbSaving] = useState(false);
    const [kbError, setKbError] = useState<string | null>(null);
    const [kbList, setKbList] = useState<KnowledgeBaseSummary[]>([]);
    const [kbSelectedId, setKbSelectedId] = useState<string>('');
    const [kbNewName, setKbNewName] = useState('');
    const { showToast } = useToast();
    const { knowledgeBaseEnabled } = useKnowledgeBaseFeatureEnabled();

    const loadKnowledgeBases = useCallback(async () => {
        setKbLoading(true);
        setKbError(null);
        try {
            const list = await listKnowledgeBases();
            setKbList(list);
            if (!kbSelectedId && list.length) {
                setKbSelectedId(list[0].id);
            }
        } catch (loadError) {
            setKbError(loadError instanceof Error ? loadError.message : '获取知识库失败');
            setKbList([]);
        } finally {
            setKbLoading(false);
        }
    }, [kbSelectedId]);

    useEffect(() => {
        if (!open || !knowledgeBaseEnabled) return;
        void loadKnowledgeBases();
    }, [knowledgeBaseEnabled, loadKnowledgeBases, open]);

    const handleCreateKnowledgeBase = useCallback(async () => {
        const name = kbNewName.trim();
        if (!name) {
            setKbError('请输入知识库名称');
            return;
        }
        setKbSaving(true);
        setKbError(null);
        try {
            const created = await createKnowledgeBase({ name });
            setKbNewName('');
            setKbSelectedId(created.id);
            await loadKnowledgeBases();
        } catch (createError) {
            setKbError(createError instanceof Error ? createError.message : '创建知识库失败');
        } finally {
            setKbSaving(false);
        }
    }, [kbNewName, loadKnowledgeBases]);

    const handleIngest = useCallback(async () => {
        if (!kbSelectedId) {
            setKbError('请选择知识库');
            return;
        }
        setKbSaving(true);
        setKbError(null);
        try {
            await ingestKnowledgeBaseSource({
                kbId: kbSelectedId,
                sourceType,
                sourceId,
                sourceMeta,
            });
            onSuccess?.({ sourceType, sourceId, kbId: kbSelectedId });
            showToast('success', '已加入知识库');
            onClose();
        } catch (ingestError) {
            const message = ingestError instanceof Error ? ingestError.message : '加入知识库失败';
            setKbError(message);
            showToast('error', message);
        } finally {
            setKbSaving(false);
        }
    }, [kbSelectedId, onClose, onSuccess, showToast, sourceId, sourceMeta, sourceType]);

    if (!open || !knowledgeBaseEnabled) return null;

    return (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-in fade-in duration-200">
            <div className="bg-background/95 backdrop-blur-xl rounded-2xl w-full max-w-lg border border-white/10 shadow-2xl animate-in zoom-in-95 duration-200">
                <div className="p-4 sm:p-6 border-b border-border/50 flex items-center justify-between">
                    <div className="min-w-0">
                        <div className="text-base font-semibold truncate">加入知识库</div>
                        <div className="text-xs text-foreground-secondary truncate">{sourceTitle}</div>
                    </div>
                    <button
                        type="button"
                        onClick={onClose}
                        className="p-2 rounded-lg hover:bg-background-secondary transition-colors"
                        aria-label="关闭"
                    >
                        <X className="w-4 h-4" />
                    </button>
                </div>

                <div className="p-4 sm:p-6 space-y-4">
                    {kbLoading ? (
                        <div className="flex items-center justify-center py-8">
                            <SoundWaveLoader variant="inline" />
                        </div>
                    ) : (
                        <div className="space-y-2">
                            {kbList.length === 0 ? (
                                <div className="text-sm text-foreground-secondary">你还没有知识库，先创建一个。</div>
                            ) : (
                                <div className="space-y-2 max-h-56 overflow-auto pr-1">
                                    {kbList.map(kb => (
                                        <label
                                            key={kb.id}
                                            className={`flex items-start gap-3 p-3 rounded-xl border cursor-pointer transition-colors ${kbSelectedId === kb.id ? 'border-emerald-500/40 bg-emerald-500/5' : 'border-border hover:bg-background-secondary'}`}
                                        >
                                            <input
                                                type="radio"
                                                name="kb"
                                                className="mt-1"
                                                checked={kbSelectedId === kb.id}
                                                onChange={() => setKbSelectedId(kb.id)}
                                            />
                                            <div className="min-w-0">
                                                <div className="text-sm font-medium truncate">{kb.name}</div>
                                                <div className="text-xs text-foreground-secondary truncate">{kb.description || '知识库'}</div>
                                            </div>
                                        </label>
                                    ))}
                                </div>
                            )}
                        </div>
                    )}

                    {!kbLoading && kbList.length === 0 && (
                        <div className="border-t border-border/50 pt-4 space-y-2">
                            <div className="text-sm font-medium">创建新知识库</div>
                            <div className="flex items-center gap-2">
                                <input
                                    value={kbNewName}
                                    onChange={(e) => setKbNewName(e.target.value)}
                                    className="flex-1 bg-background border border-border rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500/30"
                                    placeholder="例如：我的命理笔记"
                                />
                                <button
                                    type="button"
                                    onClick={handleCreateKnowledgeBase}
                                    disabled={kbSaving || !kbNewName.trim()}
                                    className="px-3 py-2 text-sm rounded-xl bg-background border border-border hover:border-emerald-500/40 hover:text-emerald-500 disabled:opacity-50 transition-colors"
                                >
                                    创建
                                </button>
                            </div>
                        </div>
                    )}

                    {kbError && (
                        <div className="text-sm text-red-500">{kbError}</div>
                    )}
                </div>

                <div className="p-4 sm:p-6 border-t border-border/50 flex items-center justify-end gap-2">
                    <button
                        type="button"
                        onClick={onClose}
                        className="px-4 py-2 text-sm rounded-xl bg-background border border-border hover:bg-background-secondary transition-colors"
                    >
                        取消
                    </button>
                    <button
                        type="button"
                        onClick={handleIngest}
                        disabled={kbSaving || kbLoading || !kbSelectedId}
                        className="px-4 py-2 text-sm rounded-xl bg-emerald-500 text-white hover:bg-emerald-600 disabled:opacity-50 transition-colors"
                    >
                        {kbSaving ? (
                            <span className="inline-flex items-center gap-2">
                                <SoundWaveLoader variant="inline" />
                                加入中
                            </span>
                        ) : (
                            '加入'
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}

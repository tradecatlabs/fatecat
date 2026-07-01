/**
 * 命理记录页面
 *
 * 对齐 Notion 风格：极简布局、柔和边框、列表化展示
 */
'use client';

import { useState, useEffect, useCallback } from 'react';
import { Plus, Download } from 'lucide-react';
import { MING_RECORD_SOURCE_TYPE } from '@/lib/data-sources/types';
import {
    deleteRecord,
    getNotesByDate,
    getRecords,
    MingRecord,
    MingNote,
    RecordCategory,
    toggleRecordPin,
} from '@/lib/records';
import { ConfirmDialog } from '@/components/ui/ConfirmDialog';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { useToast } from '@/components/ui/Toast';
import { useSessionSafe } from '@/components/providers/ClientProviders';
import { RecordFilters } from '@/components/records/RecordFilters';
import { RecordsList } from '@/components/records/RecordsList';
import {
    RecordFormModal,
    DailyNotes,
    ImportExportModal,
} from '@/components/records/RecordDetail';
import { AddToKnowledgeBaseModal } from '@/components/knowledge-base/AddToKnowledgeBaseModal';
import {
    KNOWLEDGE_BASE_SYNC_EVENT,
} from '@/lib/browser-api';

const PAGE_SIZE = 10;

function SectionError({
    message,
    onRetry,
}: {
    message: string;
    onRetry: () => void | Promise<void>;
}) {
    return (
        <div className="p-6">
            <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-500 space-y-3">
                <p>{message}</p>
                <button
                    type="button"
                    onClick={() => { void onRetry(); }}
                    className="inline-flex rounded-lg border border-red-500/20 px-3 py-1.5 text-xs font-medium text-red-500 transition-colors hover:bg-red-500/10"
                >
                    重试
                </button>
            </div>
        </div>
    );
}

export default function RecordsPage() {
    const [loading, setLoading] = useState(true);
    const [notesLoading, setNotesLoading] = useState(true);
    const [records, setRecords] = useState<MingRecord[]>([]);
    const [notes, setNotes] = useState<MingNote[]>([]);
    const [total, setTotal] = useState(0);
    const [recordsError, setRecordsError] = useState<string | null>(null);
    const [notesError, setNotesError] = useState<string | null>(null);
    const [page, setPage] = useState(1);
    const [search, setSearch] = useState('');
    const [category, setCategory] = useState<RecordCategory | ''>('');
    const [showRecordForm, setShowRecordForm] = useState(false);
    const [editingRecord, setEditingRecord] = useState<MingRecord | null>(null);
    const [showImportExport, setShowImportExport] = useState(false);
    const [kbTargetRecord, setKbTargetRecord] = useState<MingRecord | null>(null);
    const [deleteRecordId, setDeleteRecordId] = useState<string | null>(null);
    const { showToast } = useToast();
    const { user, loading: sessionLoading } = useSessionSafe();

    const openAddToKb = useCallback((record: MingRecord) => {
        setKbTargetRecord(record);
    }, []);

    const closeKbModal = useCallback(() => {
        setKbTargetRecord(null);
    }, []);

    // 加载记录
    const loadRecords = useCallback(async () => {
        if (!user) {
            const message = '请先登录后查看命理记录';
            setRecords([]);
            setTotal(0);
            setRecordsError(message);
            setLoading(false);
            return;
        }
        setLoading(true);
        setRecordsError(null);
        try {
            const { records: nextRecords, total: nextTotal } = await getRecords(
                {
                    search: search || undefined,
                    category: category || undefined,
                },
                page,
                PAGE_SIZE,
            );
            setRecords(nextRecords);
            setTotal(nextTotal);
        } catch (error) {
            const message = error instanceof Error ? error.message : '获取记录失败';
            setRecords([]);
            setTotal(0);
            setRecordsError(message);
            showToast('error', message);
        } finally {
            setLoading(false);
        }
    }, [category, page, search, showToast, user]);

    // 加载今日小记
    const loadNotes = useCallback(async () => {
        if (!user) {
            const message = '请先登录后查看今日小记';
            setNotes([]);
            setNotesError(message);
            setNotesLoading(false);
            return;
        }
        setNotesLoading(true);
        setNotesError(null);
        const today = new Date().toISOString().split('T')[0];
        try {
            const nextNotes = await getNotesByDate(today);
            setNotes(nextNotes);
        } catch (error) {
            const message = error instanceof Error ? error.message : '获取小记失败';
            setNotes([]);
            setNotesError(message);
            showToast('error', message);
        } finally {
            setNotesLoading(false);
        }
    }, [showToast, user]);

    const handleKnowledgeBaseSuccess = useCallback((payload: {
        sourceId: string;
        kbId: string;
    }) => {
        setRecords((prev) => prev.map((record) => {
            if (record.id !== payload.sourceId) {
                return record;
            }

            const archivedKbIds = Array.isArray(record.archived_kb_ids)
                ? Array.from(new Set([...record.archived_kb_ids, payload.kbId]))
                : [payload.kbId];
            return {
                ...record,
                is_archived: true,
                archived_kb_ids: archivedKbIds,
            };
        }));
        closeKbModal();
    }, [closeKbModal]);

    useEffect(() => {
        if (sessionLoading) {
            return;
        }
        void loadRecords();
        void loadNotes();
    }, [sessionLoading, user, loadRecords, loadNotes]);

    useEffect(() => {
        if (typeof window === 'undefined') {
            return;
        }

        const handleArchiveChanged = (event: Event) => {
            const detail = (event as CustomEvent<{
                pathname?: string;
                requestBody?: Record<string, unknown> | null;
                responseData?: Record<string, unknown> | null;
            }>).detail;
            const sourceType = detail?.pathname?.startsWith('/api/knowledge-base/ingest')
                ? detail.requestBody?.sourceType
                : detail?.responseData?.sourceType;
            if (sourceType !== 'record' && sourceType !== 'ming_record') {
                return;
            }
            void loadRecords();
        };

        window.addEventListener(KNOWLEDGE_BASE_SYNC_EVENT, handleArchiveChanged as EventListener);
        return () => {
            window.removeEventListener(KNOWLEDGE_BASE_SYNC_EVENT, handleArchiveChanged as EventListener);
        };
    }, [loadRecords]);

    const handleDelete = async (id: string) => {
        try {
            await deleteRecord(id);
            setDeleteRecordId(null);
            const nextTotal = Math.max(total - 1, 0);
            const nextPage = Math.min(page, Math.max(1, Math.ceil(nextTotal / PAGE_SIZE)));
            setTotal(nextTotal);
            if (nextPage !== page) {
                setPage(nextPage);
                return;
            }
            await loadRecords();
        } catch (error) {
            showToast('error', error instanceof Error ? error.message : '删除记录失败');
        }
    };

    const handleTogglePin = async (id: string) => {
        try {
            await toggleRecordPin(id);
            await loadRecords();
        } catch (error) {
            showToast('error', error instanceof Error ? error.message : '更新记录失败');
        }
    };

    const totalPages = Math.ceil(total / PAGE_SIZE);

    return (
        <div className="min-h-screen bg-background text-foreground pb-20 lg:pb-8">
            <div className="max-w-4xl mx-auto px-4 py-8 animate-fade-in space-y-10">
                {/* 标题与操作栏 */}
                <header className="flex flex-col sm:flex-row sm:items-center justify-between gap-6 pb-6 border-b border-border/60">
                    <div className="space-y-1">
                        <h1 className="text-2xl font-bold">命理记录</h1>
                        <p className="text-sm text-foreground/50">追踪运势变化，积累命理智慧</p>
                    </div>
                    <div className="flex items-center gap-2">
                        <button
                            onClick={() => setShowImportExport(true)}
                            className="p-2 rounded-md border border-border hover:bg-background-secondary transition-colors text-foreground/70"
                            title="数据管理"
                        >
                            <Download className="w-4 h-4" />
                        </button>
                        <button
                            onClick={() => setShowRecordForm(true)}
                            className="flex items-center gap-2 px-4 py-1.5 bg-[#2383e2] text-white text-sm font-medium rounded-md hover:bg-[#2383e2]/90 active:bg-[#1a65b0] transition-colors"
                        >
                            <Plus className="w-4 h-4" />
                            <span>新建记录</span>
                        </button>
                    </div>
                </header>

                <div className="space-y-10">
                    {/* 小记区域 */}
                    <section className="space-y-4">
                        <h2 className="text-[11px] font-semibold text-foreground/40 uppercase tracking-widest px-1">今日小记</h2>
                        <div className="bg-background border border-border rounded-md overflow-hidden">
                            {notesError ? (
                                <SectionError message={notesError} onRetry={loadNotes} />
                            ) : notesLoading ? (
                                <div className="p-6">
                                    <SoundWaveLoader variant="block" text="加载小记中" />
                                </div>
                            ) : (
                                <DailyNotes userId={user?.id ?? null} notes={notes} onRefresh={loadNotes} />
                            )}
                        </div>
                    </section>

                    {/* 筛选与列表 */}
                    <section className="space-y-4">
                        <h2 className="text-[11px] font-semibold text-foreground/40 uppercase tracking-widest px-1">所有记录</h2>
                        <div className="space-y-4">
                            <RecordFilters
                                search={search}
                                onSearchChange={(v) => { setSearch(v); setPage(1); }}
                                category={category}
                                onCategoryChange={(v) => { setCategory(v); setPage(1); }}
                            />

                            <div className="bg-background border border-border rounded-md overflow-hidden">
                                {recordsError && !loading ? (
                                    <SectionError message={recordsError} onRetry={loadRecords} />
                                ) : (
                                    <RecordsList
                                        loading={loading}
                                        records={records}
                                        page={page}
                                        totalPages={totalPages}
                                        onPageChange={setPage}
                                        onEdit={(record) => { setEditingRecord(record); setShowRecordForm(true); }}
                                        onDelete={(id) => setDeleteRecordId(id)}
                                        onTogglePin={handleTogglePin}
                                        onAddToKnowledgeBase={openAddToKb}
                                        onCreateNew={() => setShowRecordForm(true)}
                                    />
                                )}
                            </div>
                        </div>
                    </section>
                </div>

                {/* 模态框 */}
                {showRecordForm && (
                    <RecordFormModal
                        userId={user?.id ?? null}
                        record={editingRecord}
                        onClose={() => { setShowRecordForm(false); setEditingRecord(null); }}
                        onSave={() => { setShowRecordForm(false); setEditingRecord(null); void loadRecords(); }}
                    />
                )}

                {showImportExport && (
                    <ImportExportModal
                        userId={user?.id ?? null}
                        onClose={() => setShowImportExport(false)}
                        onImport={() => { void loadRecords(); void loadNotes(); }}
                    />
                )}

                {kbTargetRecord && (
                    <AddToKnowledgeBaseModal
                        open
                        onClose={closeKbModal}
                        onSuccess={({ sourceId, kbId }) => handleKnowledgeBaseSuccess({ sourceId, kbId })}
                        sourceTitle={kbTargetRecord.title}
                        sourceType={MING_RECORD_SOURCE_TYPE}
                        sourceId={kbTargetRecord.id}
                    />
                )}

                <ConfirmDialog
                    isOpen={!!deleteRecordId}
                    onClose={() => setDeleteRecordId(null)}
                    onConfirm={() => deleteRecordId ? handleDelete(deleteRecordId) : undefined}
                    title="确认删除"
                    description="确定要删除这条记录吗？此操作无法撤销。"
                    confirmText="确认删除"
                    variant="danger"
                />
            </div>
        </div>
    );
}

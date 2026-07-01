/**
 * Key管理面板组件
 * 
 * 管理员批量创建、查看、删除激活Key
 */
'use client';

import { useState, useEffect, useCallback } from 'react';
import {
    Plus,
    Copy,
    Check,
    Trash2,
    Key,
    Crown,
    Sparkles,
    Coins,
    Filter
} from 'lucide-react';
import { requestBrowserData } from '@/lib/browser-api';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { ConfirmDialog } from '@/components/ui/ConfirmDialog';
import { useToast } from '@/components/ui/Toast';

interface ActivationKey {
    id: string;
    key_code: string;
    key_type: 'membership' | 'credits';
    membership_type: 'plus' | 'pro' | null;
    credits_amount: number | null;
    is_used: boolean;
    used_by: string | null;
    used_at: string | null;
    created_at: string;
}

type CreateKeyType = 'plus' | 'pro' | 'credits';

export function KeyManagementPanel() {
    const [keys, setKeys] = useState<ActivationKey[]>([]);
    const [loading, setLoading] = useState(true);
    const [creating, setCreating] = useState(false);
    const { showToast } = useToast();
    const [copiedId, setCopiedId] = useState<string | null>(null);
    const [deleteKeyId, setDeleteKeyId] = useState<string | null>(null);

    // 创建表单
    const [showCreateForm, setShowCreateForm] = useState(false);
    const [createType, setCreateType] = useState<CreateKeyType>('plus');
    const [createCount, setCreateCount] = useState(1);
    const [creditsAmount, setCreditsAmount] = useState(10);

    // 筛选
    const [filterUsed, setFilterUsed] = useState<boolean | null>(null);

    const fetchKeys = useCallback(async () => {
        try {
            let url = '/api/activation-keys';
            const params = new URLSearchParams();
            if (filterUsed !== null) {
                params.set('isUsed', String(filterUsed));
            }
            if (params.toString()) {
                url += '?' + params.toString();
            }

            const data = await requestBrowserData<{ success?: boolean; data?: ActivationKey[] }>(
                url,
                { method: 'GET' },
                { fallbackMessage: '获取激活码失败' },
            );
            setKeys(data.data || []);
        } catch (error) {
            console.error('Failed to fetch keys:', error);
        } finally {
            setLoading(false);
        }
    }, [filterUsed]);

    useEffect(() => {
        fetchKeys();
    }, [fetchKeys]);

    const handleCreate = async () => {
        setCreating(true);
        try {
            const body: Record<string, unknown> = {
                action: 'create',
                count: createCount,
            };

            if (createType === 'credits') {
                body.keyType = 'credits';
                body.creditsAmount = creditsAmount;
            } else {
                body.keyType = 'membership';
                body.membershipType = createType;
            }

            const data = await requestBrowserData<{ success?: boolean; error?: string }>(
                '/api/activation-keys',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(body),
                },
                { fallbackMessage: '创建失败' },
            );
            if (data.success) {
                setShowCreateForm(false);
                setCreateCount(1);
                fetchKeys();
            } else {
                showToast('error', data.error || '创建失败');
            }
        } catch (error) {
            console.error('Failed to create keys:', error);
            showToast('error', '创建失败');
        } finally {
            setCreating(false);
        }
    };

    const handleDelete = async (keyId: string) => {
        try {
            const data = await requestBrowserData<{ success?: boolean; error?: string }>(
                `/api/activation-keys?id=${keyId}`,
                {
                    method: 'DELETE',
                },
                { fallbackMessage: '删除失败' },
            );
            if (data.success) {
                setKeys(keys.filter(k => k.id !== keyId));
                setDeleteKeyId(null);
            } else {
                showToast('error', data.error || '删除失败');
            }
        } catch (error) {
            console.error('Failed to delete key:', error);
            showToast('error', '删除失败');
        }
    };

    const handleCopy = async (keyCode: string, keyId: string) => {
        await navigator.clipboard.writeText(keyCode);
        setCopiedId(keyId);
        setTimeout(() => setCopiedId(null), 2000);
    };

    const getKeyTypeLabel = (key: ActivationKey) => {
        if (key.key_type === 'credits') {
            return `${key.credits_amount} 积分`;
        }
        return key.membership_type === 'plus' ? 'Plus 会员' : 'Pro 会员';
    };

    const getKeyTypeIcon = (key: ActivationKey) => {
        if (key.key_type === 'credits') {
            return <Coins className="w-4 h-4 text-blue-500" />;
        }
        return key.membership_type === 'plus'
            ? <Crown className="w-4 h-4 text-amber-500" />
            : <Sparkles className="w-4 h-4 text-purple-500" />;
    };

    if (loading) {
        return <SoundWaveLoader variant="block" />;
    }

    return (
        <div className="space-y-6">
            {/* 头部操作 */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <Key className="w-5 h-5 text-accent" />
                    <h2 className="font-bold">激活码管理</h2>
                    <span className="text-sm text-foreground-secondary">
                        ({keys.length} 个)
                    </span>
                </div>
                <button
                    onClick={() => setShowCreateForm(!showCreateForm)}
                    className="flex items-center gap-2 px-4 py-2 rounded-lg bg-accent text-white text-sm font-medium hover:bg-accent/90 transition-colors"
                >
                    <Plus className="w-4 h-4" />
                    批量创建
                </button>
            </div>

            {/* 创建表单 */}
            {showCreateForm && (
                <div className="bg-background-secondary rounded-xl p-4 space-y-4 border border-border">
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        {/* 类型选择 */}
                        <div>
                            <label className="block text-sm font-medium mb-2">类型</label>
                            <select
                                value={createType}
                                onChange={(e) => setCreateType(e.target.value as CreateKeyType)}
                                className="w-full px-3 py-2 rounded-lg border border-border bg-background focus:border-accent outline-none"
                            >
                                <option value="plus">Plus 会员</option>
                                <option value="pro">Pro 会员</option>
                                <option value="credits">积分发放</option>
                            </select>
                        </div>

                        {/* 积分数量 (仅积分类型) */}
                        {createType === 'credits' && (
                            <div>
                                <label className="block text-sm font-medium mb-2">积分数量</label>
                                <input
                                    type="number"
                                    min={1}
                                    max={1000}
                                    value={creditsAmount}
                                    onChange={(e) => setCreditsAmount(Number(e.target.value))}
                                    className="w-full px-3 py-2 rounded-lg border border-border bg-background focus:border-accent outline-none"
                                />
                            </div>
                        )}

                        {/* 创建数量 */}
                        <div>
                            <label className="block text-sm font-medium mb-2">数量</label>
                            <input
                                type="number"
                                min={1}
                                max={100}
                                value={createCount}
                                onChange={(e) => setCreateCount(Number(e.target.value))}
                                className="w-full px-3 py-2 rounded-lg border border-border bg-background focus:border-accent outline-none"
                            />
                        </div>
                    </div>

                    <div className="flex justify-end gap-2">
                        <button
                            onClick={() => setShowCreateForm(false)}
                            className="px-4 py-2 rounded-lg text-sm text-foreground-secondary hover:bg-background transition-colors"
                        >
                            取消
                        </button>
                        <button
                            onClick={handleCreate}
                            disabled={creating}
                            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-accent text-white text-sm font-medium hover:bg-accent/90 transition-colors disabled:opacity-50"
                        >
                            {creating && <SoundWaveLoader variant="inline" />}
                            创建
                        </button>
                    </div>
                </div>
            )}

            {/* 筛选 */}
            <div className="flex items-center gap-2">
                <Filter className="w-4 h-4 text-foreground-secondary" />
                <button
                    onClick={() => setFilterUsed(null)}
                    className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${filterUsed === null ? 'bg-accent text-white' : 'bg-background-secondary hover:bg-background-secondary/80'
                        }`}
                >
                    全部
                </button>
                <button
                    onClick={() => setFilterUsed(false)}
                    className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${filterUsed === false ? 'bg-accent text-white' : 'bg-background-secondary hover:bg-background-secondary/80'
                        }`}
                >
                    未使用
                </button>
                <button
                    onClick={() => setFilterUsed(true)}
                    className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${filterUsed === true ? 'bg-accent text-white' : 'bg-background-secondary hover:bg-background-secondary/80'
                        }`}
                >
                    已使用
                </button>
            </div>

            {/* Key列表 */}
            {keys.length === 0 ? (
                <div className="text-center py-12 text-foreground-secondary">
                    暂无激活码
                </div>
            ) : (
                <div className="space-y-2">
                    {keys.map((key) => (
                        <div
                            key={key.id}
                            className={`flex items-center justify-between p-4 rounded-xl border ${key.is_used
                                    ? 'bg-background-secondary/50 border-border/50 opacity-60'
                                    : 'bg-background border-border'
                                }`}
                        >
                            <div className="flex items-center gap-4">
                                {/* 图标 */}
                                <div className="p-2 rounded-lg bg-background-secondary">
                                    {getKeyTypeIcon(key)}
                                </div>

                                {/* Key信息 */}
                                <div>
                                    <div className="flex items-center gap-2">
                                        <code className="font-mono text-sm">{key.key_code}</code>
                                        {key.is_used && (
                                            <span className="px-2 py-0.5 rounded-full bg-red-500/10 text-red-500 text-xs">
                                                已使用
                                            </span>
                                        )}
                                    </div>
                                    <div className="flex items-center gap-2 text-xs text-foreground-secondary mt-1">
                                        <span>{getKeyTypeLabel(key)}</span>
                                        <span>•</span>
                                        <span>{new Date(key.created_at).toLocaleDateString()}</span>
                                        {key.used_at && (
                                            <>
                                                <span>•</span>
                                                <span>使用于 {new Date(key.used_at).toLocaleDateString()}</span>
                                            </>
                                        )}
                                    </div>
                                </div>
                            </div>

                            {/* 操作 */}
                            <div className="flex items-center gap-2">
                                {!key.is_used && (
                                    <button
                                        onClick={() => handleCopy(key.key_code, key.id)}
                                        className="p-2 rounded-lg hover:bg-background-secondary transition-colors"
                                        title="复制"
                                    >
                                        {copiedId === key.id ? (
                                            <Check className="w-4 h-4 text-green-500" />
                                        ) : (
                                            <Copy className="w-4 h-4 text-foreground-secondary" />
                                        )}
                                    </button>
                                )}
                                <button
                                    onClick={() => setDeleteKeyId(key.id)}
                                    className="p-2 rounded-lg hover:bg-red-500/10 text-red-500 transition-colors"
                                    title="删除"
                                >
                                    <Trash2 className="w-4 h-4" />
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
            <ConfirmDialog
                isOpen={!!deleteKeyId}
                onClose={() => setDeleteKeyId(null)}
                onConfirm={() => deleteKeyId ? handleDelete(deleteKeyId) : undefined}
                title="确认删除"
                description="确定删除此激活码吗？此操作无法撤销。"
                confirmText="确认删除"
                variant="danger"
            />
        </div>
    );
}

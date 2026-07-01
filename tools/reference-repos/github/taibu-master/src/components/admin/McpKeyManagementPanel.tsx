/**
 * MCP Key 管理面板（管理员）
 */
'use client';

import { useState, useEffect, useCallback } from 'react';
import { Ban, Key, Users, Activity } from 'lucide-react';
import { requestBrowserData } from '@/lib/browser-api';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';

interface McpKeyRow {
    id: string;
    user_id: string;
    key_preview: string;
    is_active: boolean;
    is_banned: boolean;
    created_at: string;
    last_used_at: string | null;
    user_email: string | null;
    user_nickname: string | null;
}

function formatTime(iso: string | null): string {
    if (!iso) return '-';
    return new Date(iso).toLocaleString('zh-CN');
}

export function McpKeyManagementPanel() {
    const [keys, setKeys] = useState<McpKeyRow[]>([]);
    const [loading, setLoading] = useState(true);
    const [revoking, setRevoking] = useState<string | null>(null);
    const [unbanning, setUnbanning] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    const fetchKeys = useCallback(async () => {
        try {
            setError(null);
            const data = await requestBrowserData<{ keys?: McpKeyRow[] }>(
                '/api/admin/mcp-keys',
                { method: 'GET' },
                { fallbackMessage: '获取失败' },
            );
            setKeys(data.keys || []);
        } catch (err) {
            setError(err instanceof Error ? err.message : '获取失败');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => { fetchKeys(); }, [fetchKeys]);

    const handleRevoke = async (userId: string) => {
        setRevoking(userId);
        try {
            await requestBrowserData(
                '/api/admin/mcp-keys',
                {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ userId }),
                },
                { fallbackMessage: '封禁失败' },
            );
            await fetchKeys();
        } catch (err) {
            setError(err instanceof Error ? err.message : '封禁失败');
        } finally {
            setRevoking(null);
        }
    };

    const handleUnban = async (userId: string) => {
        setUnbanning(userId);
        try {
            await requestBrowserData(
                '/api/admin/mcp-keys',
                {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ userId }),
                },
                { fallbackMessage: '解除封禁失败' },
            );
            await fetchKeys();
        } catch (err) {
            setError(err instanceof Error ? err.message : '解除封禁失败');
        } finally {
            setUnbanning(null);
        }
    };

    // 统计
    const totalKeys = keys.length;
    const activeKeys = keys.filter(k => k.is_active).length;
    const recentUsed = keys.filter(k => {
        if (!k.last_used_at) return false;
        const diff = Date.now() - new Date(k.last_used_at).getTime();
        return diff < 24 * 60 * 60 * 1000;
    }).length;

    if (loading) {
        return <SoundWaveLoader variant="block" />;
    }

    return (
        <div>
            {error && (
                <div className="mb-4 p-3 rounded-xl bg-red-500/10 text-red-500 text-sm">
                    {error}
                </div>
            )}

            {/* 统计卡片 */}
            <div className="grid grid-cols-3 gap-3 mb-6">
                <div className="p-3 rounded-xl bg-background-secondary text-center">
                    <Key className="w-4 h-4 mx-auto mb-1 text-foreground-secondary" />
                    <div className="text-lg font-bold">{totalKeys}</div>
                    <div className="text-xs text-foreground-secondary">总 Key 数</div>
                </div>
                <div className="p-3 rounded-xl bg-background-secondary text-center">
                    <Users className="w-4 h-4 mx-auto mb-1 text-green-500" />
                    <div className="text-lg font-bold">{activeKeys}</div>
                    <div className="text-xs text-foreground-secondary">活跃</div>
                </div>
                <div className="p-3 rounded-xl bg-background-secondary text-center">
                    <Activity className="w-4 h-4 mx-auto mb-1 text-accent" />
                    <div className="text-lg font-bold">{recentUsed}</div>
                    <div className="text-xs text-foreground-secondary">24h 内使用</div>
                </div>
            </div>

            {/* Key 列表 */}
            {keys.length === 0 ? (
                <p className="text-center text-foreground-secondary py-8">暂无 MCP Key</p>
            ) : (
                <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                        <thead>
                            <tr className="border-b border-border text-left text-foreground-secondary">
                                <th className="pb-2 font-medium">用户</th>
                                <th className="pb-2 font-medium">Key</th>
                                <th className="pb-2 font-medium">状态</th>
                                <th className="pb-2 font-medium">创建时间</th>
                                <th className="pb-2 font-medium">上次使用</th>
                                <th className="pb-2 font-medium">操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            {keys.map((k) => (
                                <tr key={k.id} className="border-b border-border/50">
                                    <td className="py-2.5">
                                        <div className="font-medium">{k.user_nickname || '-'}</div>
                                        <div className="text-xs text-foreground-secondary">{k.user_email || '-'}</div>
                                    </td>
                                    <td className="py-2.5">
                                        <code className="text-xs">{k.key_preview}</code>
                                    </td>
                                    <td className="py-2.5">
                                        <span className={`text-xs px-2 py-0.5 rounded-full ${k.is_banned
                                            ? 'bg-red-500/10 text-red-500'
                                            : k.is_active
                                                ? 'bg-green-500/10 text-green-500'
                                                : 'bg-orange-500/10 text-orange-500'
                                            }`}>
                                            {k.is_banned ? '已封禁' : '活跃'}
                                        </span>
                                    </td>
                                    <td className="py-2.5 text-xs text-foreground-secondary">
                                        {formatTime(k.created_at)}
                                    </td>
                                    <td className="py-2.5 text-xs text-foreground-secondary">
                                        {formatTime(k.last_used_at)}
                                    </td>
                                    <td className="py-2.5">
                                        {!k.is_banned && (
                                            <button
                                                onClick={() => handleRevoke(k.user_id)}
                                                disabled={revoking === k.user_id || unbanning === k.user_id}
                                                className="flex items-center gap-1 text-xs text-red-500 hover:text-red-600 disabled:opacity-50"
                                            >
                                                {revoking === k.user_id
                                                    ? <SoundWaveLoader variant="inline" />
                                                    : <Ban className="w-3 h-3" />
                                                }
                                                封禁
                                            </button>
                                        )}
                                        {k.is_banned && (
                                            <button
                                                onClick={() => handleUnban(k.user_id)}
                                                disabled={unbanning === k.user_id || revoking === k.user_id}
                                                className="flex items-center gap-1 text-xs text-green-600 hover:text-green-700 disabled:opacity-50"
                                            >
                                                {unbanning === k.user_id
                                                    ? <SoundWaveLoader variant="inline" />
                                                    : <Key className="w-3 h-3" />
                                                }
                                                解除封禁
                                            </button>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}

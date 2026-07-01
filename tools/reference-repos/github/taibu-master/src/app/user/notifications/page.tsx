/**
 * 消息通知页面
 *
 * 支持筛选、多选、批量删除、批量已读
 */
'use client';

import { useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
    Bell,
    CheckCheck,
    ExternalLink,
    Trash2,
    Square,
    CheckSquare,
} from 'lucide-react';
import { useSessionSafe } from '@/components/providers/ClientProviders';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { useToast } from '@/components/ui/Toast';
import {
    deleteNotification,
    deleteNotifications,
    getNotificationsPage,
    markAllAsRead,
    markAsRead,
    markSelectedAsRead,
    type Notification,
} from '@/lib/notification';
import {
    filterNotifications,
    groupNotificationsByDay,
    reconcileSelectedNotificationIds,
    resolveNotificationLink,
    type NotificationFilterState,
} from '@/lib/notification-view';

const typeStyles: Record<string, { icon: string; label: string }> = {
    feature_launch: { icon: '🎉', label: '功能上线' },
    system: { icon: '📢', label: '系统通知' },
    promotion: { icon: '🎁', label: '活动推广' },
};

const readFilterOptions: Array<{ value: NotificationFilterState['read']; label: string }> = [
    { value: 'all', label: '全部' },
    { value: 'unread', label: '未读' },
    { value: 'read', label: '已读' },
];

const typeFilterOptions: Array<{ value: NotificationFilterState['type']; label: string }> = [
    { value: 'all', label: '全部类型' },
    { value: 'system', label: '系统' },
    { value: 'feature_launch', label: '功能' },
    { value: 'promotion', label: '活动' },
];

function formatTime(dateStr: string): string {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return '刚刚';
    if (diffMins < 60) return `${diffMins}分钟前`;
    if (diffHours < 24) return `${diffHours}小时前`;
    if (diffDays < 7) return `${diffDays}天前`;
    return date.toLocaleDateString('zh-CN', { month: 'long', day: 'numeric' });
}

export default function NotificationsPage() {
    return <NotificationsContent />;
}

function NotificationsContent() {
    const router = useRouter();
    const { user, loading: sessionLoading } = useSessionSafe();
    const { showToast } = useToast();
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [loadError, setLoadError] = useState<string | null>(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [selectMode, setSelectMode] = useState(false);
    const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
    const [filters, setFilters] = useState<NotificationFilterState>({
        read: 'all',
        type: 'all',
    });

    useEffect(() => {
        const init = async () => {
            if (sessionLoading) {
                return;
            }
            try {
                if (!user) {
                    router.push('/');
                    return;
                }

                setLoadError(null);
                const data = await getNotificationsPage({ limit: 50 });
                setNotifications(data.notifications);
            } catch (error) {
                const message = error instanceof Error ? error.message : '获取通知失败';
                setNotifications([]);
                setLoadError(message);
                showToast('error', message);
            } finally {
                setIsLoading(false);
            }
        };

        void init();
    }, [router, sessionLoading, showToast, user]);

    const unreadCount = useMemo(() => notifications.filter((item) => !item.is_read).length, [notifications]);
    const visibleNotifications = useMemo(
        () => filterNotifications(notifications, filters),
        [notifications, filters],
    );
    const groupedNotifications = useMemo(
        () => groupNotificationsByDay(visibleNotifications),
        [visibleNotifications],
    );
    const selectedCount = selectedIds.size;
    const allSelected = visibleNotifications.length > 0 && visibleNotifications.every((item) => selectedIds.has(item.id));

    useEffect(() => {
        window.dispatchEvent(
            new CustomEvent('taibu:notifications-unread', { detail: { count: unreadCount } }),
        );
    }, [unreadCount]);

    const toggleSelectMode = () => {
        setSelectMode((current) => !current);
        setSelectedIds(new Set());
    };

    const toggleSelect = (id: string) => {
        setSelectedIds((current) => {
            const next = new Set(current);
            if (next.has(id)) {
                next.delete(id);
            } else {
                next.add(id);
            }
            return next;
        });
    };

    const toggleSelectAll = () => {
        if (allSelected) {
            setSelectedIds(new Set());
            return;
        }
        setSelectedIds(new Set(visibleNotifications.map((item) => item.id)));
    };

    const updateFilters = (patch: Partial<NotificationFilterState>) => {
        const nextFilters = { ...filters, ...patch };
        setFilters(nextFilters);
        setSelectedIds((existing) => reconcileSelectedNotificationIds(
            existing,
            filterNotifications(notifications, nextFilters),
        ));
    };

    const handleMarkRead = async (notification: Notification, e?: React.MouseEvent) => {
        e?.stopPropagation();
        if (notification.is_read) return;

        const success = await markAsRead(notification.id);
        if (success) {
            setNotifications((current) => current.map((item) => (
                item.id === notification.id ? { ...item, is_read: true } : item
            )));
            showToast('success', '已标记为已读');
        } else {
            showToast('error', '标记已读失败');
        }
    };

    const handleDeleteSingle = async (id: string, e: React.MouseEvent) => {
        e.stopPropagation();
        const success = await deleteNotification(id);
        if (success) {
            setNotifications((current) => current.filter((item) => item.id !== id));
            setSelectedIds((current) => {
                const next = new Set(current);
                next.delete(id);
                return next;
            });
            showToast('success', '通知已删除');
        } else {
            showToast('error', '删除通知失败');
        }
    };

    const handleClick = async (notification: Notification) => {
        if (selectMode) {
            toggleSelect(notification.id);
            return;
        }

        await handleMarkRead(notification);
        if (notification.link) {
            router.push(resolveNotificationLink(notification.link));
        }
    };

    const handleMarkAllRead = async () => {
        if (!user) return;
        setIsProcessing(true);
        const success = await markAllAsRead();
        if (success) {
            setNotifications((current) => current.map((item) => ({ ...item, is_read: true })));
            showToast('success', '已将全部通知标记为已读');
        } else {
            showToast('error', '一键已读失败');
        }
        setIsProcessing(false);
    };

    const handleMarkSelectedRead = async () => {
        if (selectedIds.size === 0) return;
        setIsProcessing(true);
        const ids = Array.from(selectedIds);
        const success = await markSelectedAsRead(ids);
        if (success) {
            setNotifications((current) => current.map((item) => (
                selectedIds.has(item.id) ? { ...item, is_read: true } : item
            )));
            setSelectedIds(new Set());
            showToast('success', `已处理 ${ids.length} 条通知`);
        } else {
            showToast('error', '批量已读失败');
        }
        setIsProcessing(false);
    };

    const handleDeleteSelected = async () => {
        if (selectedIds.size === 0) return;
        setIsProcessing(true);
        const ids = Array.from(selectedIds);
        const success = await deleteNotifications(ids);
        if (success) {
            setNotifications((current) => current.filter((item) => !selectedIds.has(item.id)));
            setSelectedIds(new Set());
            if (notifications.length - ids.length <= 0) {
                setSelectMode(false);
            }
            showToast('success', `已删除 ${ids.length} 条通知`);
        } else {
            showToast('error', '批量删除失败');
        }
        setIsProcessing(false);
    };

    if (isLoading) {
        return (
            <div className="min-h-screen bg-background">
                <div className="max-w-3xl mx-auto px-4 py-8 space-y-8">
                    {/* 标题骨架 */}
                    <div className="space-y-2">
                        <div className="h-7 w-24 rounded bg-foreground/10 animate-pulse" />
                        <div className="h-4 w-40 rounded bg-foreground/5 animate-pulse" />
                    </div>
                    {/* 列表骨架 */}
                    <div className="bg-background border border-border rounded-md overflow-hidden divide-y divide-border/60">
                        {[1, 2, 3, 4].map((i) => (
                            <div key={i} className="p-4 flex gap-4 animate-pulse">
                                <div className="w-8 h-8 rounded bg-foreground/10" />
                                <div className="flex-1 space-y-2">
                                    <div className="h-4 w-32 rounded bg-foreground/10" />
                                    <div className="h-3 w-full rounded bg-foreground/5" />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background text-foreground pb-20 lg:pb-8">
            <div className="max-w-3xl mx-auto px-4 py-8 animate-fade-in space-y-10">
                {/* 标题 */}
                <header className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div className="space-y-1">
                        <div className="flex items-center gap-3">
                            <h1 className="text-2xl font-bold">消息通知</h1>
                            {unreadCount > 0 && (
                                <span className="px-2 py-0.5 text-[10px] font-bold bg-blue-50 text-[#2eaadc] rounded uppercase tracking-wider">
                                    {unreadCount} UNREAD
                                </span>
                            )}
                        </div>
                        <p className="text-sm text-foreground/50">查看系统提醒与命理更新</p>
                    </div>

                    <div className="flex items-center gap-2">
                        {notifications.length > 0 && !selectMode && (
                            <button
                                onClick={handleMarkAllRead}
                                disabled={isProcessing || unreadCount === 0}
                                className="px-3 py-1.5 text-xs font-medium rounded-md border border-border hover:bg-background-secondary transition-colors disabled:opacity-50 flex items-center gap-2"
                            >
                                {isProcessing ? <SoundWaveLoader variant="inline" /> : <CheckCheck className="w-3.5 h-3.5" />}
                                一键已读
                            </button>
                        )}
                        {notifications.length > 0 && (
                            <button
                                onClick={toggleSelectMode}
                                className={`px-3 py-1.5 text-xs font-medium rounded-md border transition-colors ${
                                    selectMode ? 'bg-[#2eaadc] text-white border-[#2eaadc]' : 'border-border hover:bg-background-secondary'
                                }`}
                            >
                                {selectMode ? '完成' : '选择'}
                            </button>
                        )}
                    </div>
                </header>

                <div className="space-y-8">
                    {/* 筛选器 - 极简药丸 */}
                    {notifications.length > 0 && (
                        <div className="flex flex-wrap items-center gap-6 text-xs text-foreground/40 border-b border-border/60 pb-4">
                            <div className="flex items-center gap-2">
                                <span className="font-semibold uppercase tracking-widest text-[10px]">阅读状态</span>
                                <div className="flex items-center gap-1">
                                    {readFilterOptions.map((option) => (
                                        <button
                                            key={option.value}
                                            onClick={() => updateFilters({ read: option.value })}
                                            className={`px-2 py-0.5 rounded transition-colors ${
                                                filters.read === option.value
                                                    ? 'bg-background-tertiary text-foreground font-semibold'
                                                    : 'hover:bg-background-secondary hover:text-foreground'
                                            }`}
                                        >
                                            {option.label}
                                        </button>
                                    ))}
                                </div>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className="font-semibold uppercase tracking-widest text-[10px]">通知类型</span>
                                <div className="flex items-center gap-1">
                                    {typeFilterOptions.map((option) => (
                                        <button
                                            key={option.value}
                                            onClick={() => updateFilters({ type: option.value })}
                                            className={`px-2 py-0.5 rounded transition-colors ${
                                                filters.type === option.value
                                                    ? 'bg-background-tertiary text-foreground font-semibold'
                                                    : 'hover:bg-background-secondary hover:text-foreground'
                                            }`}
                                        >
                                            {option.label}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {loadError ? (
                        <div className="text-center py-20 border border-dashed border-border rounded-md">
                            <p className="text-sm text-[#b42318]">{loadError}</p>
                        </div>
                    ) : notifications.length === 0 ? (
                        <div className="text-center py-20 border border-dashed border-border rounded-md">
                            <Bell className="w-8 h-8 text-foreground/10 mx-auto mb-3" />
                            <p className="text-sm text-foreground/40">暂无任何通知</p>
                        </div>
                    ) : visibleNotifications.length === 0 ? (
                        <div className="text-center py-20 border border-dashed border-border rounded-md">
                            <p className="text-sm text-foreground/40">当前筛选下暂无相关消息</p>
                        </div>
                    ) : (
                        <div className={`space-y-8 ${selectMode ? 'mb-24' : ''}`}>
                            {groupedNotifications.map((group) => (
                                <section key={group.label} className="space-y-3">
                                    <h3 className="text-[11px] font-semibold text-foreground/40 uppercase tracking-widest px-1">
                                        {group.label}
                                    </h3>
                                    <div className="bg-background border border-border rounded-md overflow-hidden divide-y divide-border/60">
                                        {group.items.map((notification) => {
                                            const style = typeStyles[notification.type] || typeStyles.system;
                                            const isSelected = selectedIds.has(notification.id);

                                            return (
                                                <div
                                                    key={notification.id}
                                                    onClick={() => handleClick(notification)}
                                                    className={`
                                                        group w-full text-left p-4 cursor-pointer transition-colors flex gap-4
                                                        ${!notification.is_read ? 'bg-blue-50/20' : 'hover:bg-background-secondary'}
                                                        ${isSelected ? 'bg-blue-50/40' : ''}
                                                    `}
                                                >
                                                    {selectMode && (
                                                        <div className="flex items-center shrink-0">
                                                            <div className={`w-4 h-4 rounded border flex items-center justify-center transition-colors ${
                                                                isSelected ? 'bg-[#2eaadc] border-[#2eaadc]' : 'border-border bg-background'
                                                            }`}>
                                                                {isSelected && <CheckSquare className="w-3 h-3 text-white" />}
                                                            </div>
                                                        </div>
                                                    )}

                                                    <span className="text-lg shrink-0 mt-0.5 opacity-80">{style.icon}</span>

                                                    <div className="flex-1 min-w-0 space-y-1">
                                                        <div className="flex items-start justify-between gap-4">
                                                            <div className="flex items-center gap-2 min-w-0">
                                                                <span className="text-[10px] font-bold text-foreground/30 uppercase tracking-wider shrink-0">
                                                                    {style.label}
                                                                </span>
                                                                <h4 className={`text-sm font-medium truncate ${!notification.is_read ? 'text-foreground' : 'text-foreground/50'}`}>
                                                                    {notification.title}
                                                                </h4>
                                                            </div>
                                                            <span className="text-[10px] font-mono text-foreground/30 shrink-0 uppercase">
                                                                {formatTime(notification.created_at)}
                                                            </span>
                                                        </div>
                                                        {notification.content && (
                                                            <p className="text-sm text-foreground/50 leading-relaxed line-clamp-2">
                                                                {notification.content}
                                                            </p>
                                                        )}
                                                        <div className="flex items-center gap-4 pt-1">
                                                            {notification.link && !selectMode && (
                                                                <span className="text-[11px] font-semibold text-[#2eaadc] flex items-center gap-1 hover:underline">
                                                                    查看详情
                                                                    <ExternalLink className="w-3 h-3" />
                                                                </span>
                                                            )}
                                                            {!notification.is_read && !selectMode && (
                                                                <button
                                                                    onClick={(e) => handleMarkRead(notification, e)}
                                                                    className="text-[11px] font-semibold text-foreground/40 hover:text-[#2eaadc] transition-colors"
                                                                >
                                                                    标记已读
                                                                </button>
                                                            )}
                                                        </div>
                                                    </div>

                                                    {!selectMode && (
                                                        <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                                            <button
                                                                onClick={(e) => handleDeleteSingle(notification.id, e)}
                                                                className="p-1.5 rounded hover:bg-[#eb5757]/10 text-[#eb5757]/60 hover:text-[#eb5757] transition-colors"
                                                                title="删除通知"
                                                            >
                                                                <Trash2 className="w-3.5 h-3.5" />
                                                            </button>
                                                        </div>
                                                    )}
                                                </div>
                                            );
                                        })}
                                    </div>
                                </section>
                            ))}
                        </div>
                    )}
                </div>

                {/* 底部批量操作栏 - Notion 浮动条风格 */}
                {selectMode && visibleNotifications.length > 0 && (
                    <div className="fixed bottom-10 left-1/2 -translate-x-1/2 z-50 animate-in slide-in-from-bottom-4">
                        <div className="bg-[#37352f] text-white rounded-lg shadow-xl px-4 py-2 flex items-center gap-6 border border-white/10 backdrop-blur-md">
                            <div className="flex items-center gap-3 pr-6 border-r border-white/10">
                                <button onClick={toggleSelectAll} className="hover:text-[#2eaadc] transition-colors">
                                    {allSelected ? <CheckSquare className="w-4 h-4" /> : <Square className="w-4 h-4" />}
                                </button>
                                <span className="text-xs font-medium">已选择 {selectedCount} 项</span>
                            </div>
                            <div className="flex items-center gap-4">
                                <button
                                    onClick={handleMarkSelectedRead}
                                    disabled={isProcessing || selectedCount === 0}
                                    className="text-xs font-semibold hover:text-[#2eaadc] transition-colors disabled:opacity-30"
                                >
                                    标记已读
                                </button>
                                <button
                                    onClick={handleDeleteSelected}
                                    disabled={isProcessing || selectedCount === 0}
                                    className="text-xs font-semibold text-[#eb5757] hover:text-[#eb5757]/80 transition-colors disabled:opacity-30"
                                >
                                    删除
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

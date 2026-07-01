/**
 * 通用确认弹窗组件
 *
 * 用于危险操作（删除/重置等）的确认提示
 */
'use client';

import { useEffect, useCallback, type ReactNode } from 'react';
import { createPortal } from 'react-dom';
import { AlertTriangle } from 'lucide-react';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';

interface ConfirmDialogProps {
    isOpen: boolean;
    onClose: () => void;
    onConfirm: () => void | Promise<void>;
    title: string;
    description: string;
    children?: ReactNode;
    showActions?: boolean;
    confirmText?: string;
    cancelText?: string;
    variant?: 'danger' | 'warning' | 'default';
    loading?: boolean;
}

export function ConfirmDialog({
    isOpen,
    onClose,
    onConfirm,
    title,
    description,
    children,
    showActions = true,
    confirmText = '确认',
    cancelText = '取消',
    variant = 'danger',
    loading = false,
}: ConfirmDialogProps) {
    // 检查是否在客户端环境
    const isMounted = typeof window !== 'undefined';

    // ESC 键关闭
    useEffect(() => {
        const handleEsc = (e: KeyboardEvent) => {
            if (e.key === 'Escape' && isOpen && !loading) {
                onClose();
            }
        };
        window.addEventListener('keydown', handleEsc);
        return () => window.removeEventListener('keydown', handleEsc);
    }, [isOpen, loading, onClose]);

    // 处理确认
    const handleConfirm = useCallback(async () => {
        await onConfirm();
    }, [onConfirm]);

    if (!isOpen) return null;

    const variantStyles = {
        danger: {
            icon: 'text-red-500',
            button: 'bg-red-500 hover:bg-red-600 text-white',
        },
        warning: {
            icon: 'text-yellow-500',
            button: 'bg-yellow-500 hover:bg-yellow-600 text-white',
        },
        default: {
            icon: 'text-accent',
            button: 'bg-accent hover:bg-accent/90 text-white',
        },
    };

    const styles = variantStyles[variant];

    const dialog = (
        <div className="fixed inset-0 z-[1100] flex items-center justify-center p-4">
            {/* 背景遮罩 */}
            <div
                className="absolute inset-0 bg-black/50 backdrop-blur-sm"
                onClick={loading ? undefined : onClose}
            />

            {/* 弹窗内容 */}
            <div className="relative bg-background rounded-xl border border-border shadow-xl p-6 max-w-sm w-full animate-fade-in">
                {/* 图标 */}
                {variant !== 'default' && (
                    <div className={`flex items-center justify-center w-12 h-12 rounded-full bg-background-secondary mb-4 mx-auto ${styles.icon}`}>
                        <AlertTriangle className="w-6 h-6" />
                    </div>
                )}

                {/* 标题 */}
                <h3 className="text-lg font-semibold mb-2 text-center">
                    {title}
                </h3>

                {/* 描述 */}
                <p className="text-foreground-secondary text-sm mb-6 text-center">
                    {description}
                </p>

                {children ? (
                    <div className="mb-6">
                        {children}
                    </div>
                ) : null}

                {showActions ? (
                    <div className="flex gap-3 justify-center">
                        <button
                            onClick={onClose}
                            disabled={loading}
                            className="flex-1 px-4 py-2.5 rounded-lg border border-border hover:bg-background-secondary transition-colors disabled:opacity-50"
                        >
                            {cancelText}
                        </button>
                        <button
                            onClick={handleConfirm}
                            disabled={loading}
                            className={`flex-1 px-4 py-2.5 rounded-lg transition-colors disabled:opacity-50 flex items-center justify-center gap-2 ${styles.button}`}
                        >
                            {loading && <SoundWaveLoader variant="inline" />}
                            {confirmText}
                        </button>
                    </div>
                ) : null}
            </div>
        </div>
    );

    // 使用 Portal 渲染到 body 下，确保遮罩覆盖全屏
    if (isMounted) {
        return createPortal(dialog, document.body);
    }

    return null;
}

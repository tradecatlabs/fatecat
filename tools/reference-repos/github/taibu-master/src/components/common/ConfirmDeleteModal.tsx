/**
 * 通用删除确认弹窗
 * 'use client' - 需要 onClick 事件处理
 */
'use client';

import { useEffect } from 'react';
import { Trash2 } from 'lucide-react';

interface ConfirmDeleteModalProps {
    open: boolean;
    onClose: () => void;
    onConfirm: () => void;
    message?: string;
}

export function ConfirmDeleteModal({ open, onClose, onConfirm, message }: ConfirmDeleteModalProps) {
    useEffect(() => {
        if (!open) return;
        const handleKeyDown = (e: KeyboardEvent) => {
            if (e.key === 'Escape') onClose();
        };
        document.addEventListener('keydown', handleKeyDown);
        return () => document.removeEventListener('keydown', handleKeyDown);
    }, [open, onClose]);

    if (!open) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 animate-in fade-in duration-200">
            <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />
            <div className="relative bg-background rounded-2xl border border-border shadow-2xl p-6 max-w-sm w-full animate-in zoom-in-95 duration-200">
                <div className="w-12 h-12 rounded-full bg-red-500/10 flex items-center justify-center mb-4 mx-auto text-red-500">
                    <Trash2 className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-semibold mb-2 text-center">确认删除</h3>
                <p className="text-foreground-secondary mb-6 text-center text-sm">
                    {message || '确定要删除这条记录吗？此操作无法撤销。'}
                </p>
                <div className="flex gap-3 justify-center">
                    <button
                        onClick={onClose}
                        className="px-5 py-2.5 rounded-xl border border-border hover:bg-background-secondary transition-colors text-sm font-medium"
                    >
                        取消
                    </button>
                    <button
                        onClick={onConfirm}
                        className="px-5 py-2.5 rounded-xl bg-red-500 text-white hover:bg-red-600 transition-colors text-sm font-medium shadow-lg shadow-red-500/20"
                    >
                        确认删除
                    </button>
                </div>
            </div>
        </div>
    );
}

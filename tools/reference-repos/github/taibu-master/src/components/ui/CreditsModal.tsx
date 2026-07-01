/**
 * 积分不足提示弹窗
 *
 * 当用户积分不足时显示，引导用户前往订阅页面获取积分
 */
'use client';

import { useCallback } from 'react';
import { X, Coins, Crown } from 'lucide-react';
import { openSettingsCenter } from '@/lib/settings-center';

interface CreditsModalProps {
    isOpen: boolean;
    onClose: () => void;
    message?: string;
}

export function CreditsModal({ isOpen, onClose, message }: CreditsModalProps) {
    const handleGoToUpgrade = useCallback(() => {
        onClose();
        openSettingsCenter('upgrade');
    }, [onClose]);

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
            {/* 背景遮罩 */}
            <div
                className="absolute inset-0 bg-black/50 backdrop-blur-sm"
                onClick={onClose}
            />

            {/* 弹窗内容 */}
            <div className="relative bg-background border border-border rounded-2xl shadow-xl w-full max-w-sm mx-4 animate-fade-in">
                {/* 关闭按钮 */}
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 p-1 rounded-full hover:bg-background-secondary transition-colors"
                >
                    <X className="w-5 h-5 text-foreground-secondary" />
                </button>

                {/* 图标 */}
                <div className="pt-8 pb-4 flex justify-center">
                    <div className="w-16 h-16 rounded-full bg-amber-500/10 flex items-center justify-center">
                        <Coins className="w-8 h-8 text-amber-500" />
                    </div>
                </div>

                {/* 标题和描述 */}
                <div className="px-6 pb-4 text-center">
                    <h3 className="text-lg font-bold text-foreground mb-2">
                        积分不足
                    </h3>
                    <p className="text-sm text-foreground-secondary">
                        {message || '您的积分已用完，请前往订阅页面通过签到、激活码或会员权益继续获取积分'}
                    </p>
                </div>

                {/* 按钮 */}
                <div className="px-6 pb-6 space-y-3">
                    <button
                        onClick={handleGoToUpgrade}
                        className="w-full py-3 bg-accent hover:bg-accent/90 text-white rounded-xl font-medium transition-colors flex items-center justify-center gap-2"
                    >
                        <Crown className="w-5 h-5" />
                        前往订阅
                    </button>
                    <button
                        onClick={onClose}
                        className="w-full py-3 bg-background-secondary hover:bg-background-tertiary text-foreground rounded-xl font-medium transition-colors"
                    >
                        稍后再说
                    </button>
                </div>
            </div>
        </div>
    );
}

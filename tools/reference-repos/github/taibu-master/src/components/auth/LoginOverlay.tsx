/**
 * 登录覆盖层组件
 *
 * 'use client' 标记说明：
 * - 使用 React hooks (useState)
 * - 匿名访问关闭后，未登录只显示登录提示
 */
'use client';

import { useState } from 'react';
import { LogIn, Lock } from 'lucide-react';
import { AuthModal } from '@/components/auth/AuthModal';
import { useSessionSafe } from '@/components/providers/ClientProviders';

interface LoginOverlayProps {
    children: React.ReactNode;
    message?: string;
}

/**
 * 登录覆盖层组件
 * 未登录时只显示登录提示，不再渲染匿名预览内容
 */
export function LoginOverlay({ children, message = '登录后查看完整内容' }: LoginOverlayProps) {
    const [showAuthModal, setShowAuthModal] = useState(false);
    const { user, loading } = useSessionSafe();
    const isAuthed = !!user;

    // 加载中或已登录，直接显示内容
    if (loading || isAuthed) {
        return <>{children}</>;
    }

    // 未登录，仅显示登录提示
    return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] px-4 text-center">
            <div className="w-16 h-16 rounded-full bg-accent/10 flex items-center justify-center mx-auto mb-4">
                <Lock className="w-8 h-8 text-accent" />
            </div>
            <h2 className="text-xl font-bold mb-2">需要登录</h2>
            <p className="text-foreground-secondary mb-6 max-w-sm">
                {message}
            </p>
            <button
                onClick={() => setShowAuthModal(true)}
                className="inline-flex items-center gap-2 px-6 py-2.5 rounded-lg bg-accent text-white font-medium hover:bg-accent/90 transition-colors"
            >
                <LogIn className="w-4 h-4" />
                立即登录
            </button>

            <AuthModal
                isOpen={showAuthModal}
                onClose={() => setShowAuthModal(false)}
            />
        </div>
    );
}

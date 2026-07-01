/**
 * 第三方登录按钮组件
 *
 * 'use client' 标记说明：
 * - 使用 window.location 进行导航
 */
'use client';

function buildLinuxDoLoginUrl() {
    const returnTo = `${window.location.pathname}${window.location.search}${window.location.hash}`;
    const params = new URLSearchParams({
        returnTo,
    });
    return `/api/auth/linuxdo?${params.toString()}`;
}

export function OAuthButtons() {
    return (
        <>
            <div className="relative flex items-center gap-4 py-1">
                <div className="flex-1 border-t border-border" />
                <span className="text-xs text-foreground-secondary">或</span>
                <div className="flex-1 border-t border-border" />
            </div>
            <button
                type="button"
                onClick={() => { window.location.href = buildLinuxDoLoginUrl(); }}
                className="w-full py-3 rounded-xl border border-border bg-background-secondary hover:bg-background-secondary/80 font-medium transition-colors flex items-center justify-center gap-2 text-sm"
            >
                <svg width="20" height="20" viewBox="5 5 90 90" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                    <circle fill="#efefef" cx="50" cy="50" r="45"/>
                    <path fill="#feb005" d="M50,92.3c16.64,0,31.03-9.61,37.94-23.57H12.06c6.91,13.97,21.3,23.57,37.94,23.57Z"/>
                    <path fill="#1e1e20" d="M50,7.7c-16.64,0-31.03,9.61-37.94,23.57h75.88c-6.91-13.97-21.3-23.57-37.94-23.57Z"/>
                </svg>
                Linux DO 登录
            </button>
        </>
    );
}

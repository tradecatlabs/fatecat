/**
 * 统一加载指示器组件
 *
 * 音浪（Sound Wave）风格，提供三种使用场景：
 * - inline: 行内小尺寸，替代按钮/文字旁的 Loader2 spinner
 * - block: 区块级，替代页面局部的 spinner + 文字
 * - fullscreen: 全屏遮罩，用于路由切换 / 全页加载
 *
 * 骨架屏（Skeleton）保持各页面自行实现，不在此统一。
 */

interface SoundWaveProps {
    /** 使用场景 */
    variant?: 'inline' | 'block' | 'fullscreen';
    /** 加载提示文字，仅 block / fullscreen 生效 */
    text?: string;
    /** 自定义 className */
    className?: string;
}

const barConfigs = {
    inline: { count: 3, width: 'w-[2px]', height: 'h-4', gap: 'gap-[2px]' },
    block: { count: 5, width: 'w-[3px]', height: 'h-6', gap: 'gap-[3px]' },
    fullscreen: { count: 5, width: 'w-[3px]', height: 'h-8', gap: 'gap-[3px]' },
};

export function SoundWaveLoader({
    variant = 'block',
    text,
    className = '',
}: SoundWaveProps) {
    const config = barConfigs[variant];

    const bars = (
        <div className={`flex items-center ${config.gap} ${config.height}`}>
            {Array.from({ length: config.count }, (_, i) => (
                <span
                    key={i}
                    className={`sound-wave-bar ${config.width} rounded-full bg-accent`}
                    style={{ animationDelay: `${i * 0.12}s` }}
                />
            ))}
        </div>
    );

    if (variant === 'inline') {
        return <span className={`inline-flex items-center ${className}`}>{bars}</span>;
    }

    if (variant === 'fullscreen') {
        return (
            <div className={`fixed inset-0 z-50 flex flex-col items-center justify-center bg-background ${className}`}>
                {bars}
                {text && (
                    <span className="mt-4 text-foreground-secondary text-xs tracking-widest">
                        {text}
                    </span>
                )}
            </div>
        );
    }

    // block
    return (
        <div className={`flex flex-col items-center justify-center py-12 ${className}`}>
            {bars}
            {text && (
                <p className="mt-3 text-foreground-secondary text-sm">{text}</p>
            )}
        </div>
    );
}


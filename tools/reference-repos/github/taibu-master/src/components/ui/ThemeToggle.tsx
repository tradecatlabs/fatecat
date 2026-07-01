/**
 * 主题切换按钮组件
 * 
 * 'use client' 标记说明：
 * - 需要与用户交互（点击事件），必须在客户端运行
 */
'use client';

import { Moon, Sun } from 'lucide-react';
import { useTheme } from '@/components/ui/ThemeProvider';

/**
 * ThemeToggle 组件
 * 点击后在深色/浅色主题之间切换
 */
export function ThemeToggle() {
    const { toggleTheme } = useTheme();

    return (
        <button
            onClick={toggleTheme}
            className="p-2 rounded-lg transition-all duration-200
                 hover:bg-background-secondary
                 focus:outline-none focus:ring-2 focus:ring-accent/50"
            aria-label="切换主题"
            title="切换主题"
        >
            <Sun className="hidden dark:block w-5 h-5 text-foreground-secondary hover:text-accent transition-colors" />
            <Moon className="block dark:hidden w-5 h-5 text-foreground-secondary hover:text-accent transition-colors" />
        </button>
    );
}

import { SoundWaveLoader } from "@/components/ui/SoundWaveLoader";

/**
 * 全局加载组件
 *
 * Next.js App Router 会在页面加载时自动显示此组件
 */

export default function Loading() {
    return (
        <div className="flex min-h-[100vh] items-center justify-center bg-background">
            <SoundWaveLoader variant="block" text="" />
        </div>
    );
}

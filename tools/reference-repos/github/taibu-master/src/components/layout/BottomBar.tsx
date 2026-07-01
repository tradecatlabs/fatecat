/**
 * 底部固定栏组件
 * 
 * 可复用的底部固定栏，自动适应侧边栏宽度
 * 支持可展开模式：expandableContent 会在主内容上方平滑展开
 * 
 * @example
 * <BottomBar show={selectMode}>
 *     <div>左侧内容</div>
 *     <div>右侧内容</div>
 * </BottomBar>
 * 
 * @example 可展开模式
 * <BottomBar show={true} expandableContent={<div>题号网格</div>} expanded={isOpen}>
 *     <button onClick={() => setIsOpen(!isOpen)}>展开</button>
 *     <div>进度信息</div>
 * </BottomBar>
 */
'use client';

import { ReactNode } from 'react';

interface BottomBarProps {
    show: boolean;
    children: ReactNode;
    className?: string;
    /** 可展开的内容，会显示在主内容上方 */
    expandableContent?: ReactNode;
    /** 是否展开 */
    expanded?: boolean;
    /** 展开区域最大高度 */
    expandedMaxHeight?: string;
}

export function BottomBar({
    show,
    children,
    className = '',
    expandableContent,
    expanded = false,
    expandedMaxHeight = '280px',
}: BottomBarProps) {
    if (!show) return null;

    return (
        <>
            {/* 桌面端 - 需要偏移侧边栏宽度 */}
            <div
                className={`hidden lg:block fixed bottom-0 right-0 z-50 transition-all duration-300 ${className}`}
                style={{ left: 'var(--sidebar-width)' }}
            >
                <div className="max-w-2xl mx-auto px-4">
                    <div className="bg-background border border-border rounded-t-xl shadow-lg overflow-hidden">
                        {/* 主内容区 - 始终在上方 */}
                        <div className="px-4 py-3 flex items-center justify-between">
                            {children}
                        </div>

                        {/* 可展开内容区 - 在主内容下方 */}
                        {expandableContent && (
                            <div
                                className="transition-all duration-300 ease-out overflow-hidden border-t border-border"
                                style={{ maxHeight: expanded ? expandedMaxHeight : '0px' }}
                            >
                                <div className="p-4">
                                    {expandableContent}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* 移动端 - 全宽 - 位于底部导航上方 (导航栏约 108px) */}
            <div className={`lg:hidden fixed bottom-[6.5rem] left-0 right-0 z-50 ${className}`}>
                <div className="mx-4 bg-background border border-border rounded-t-xl shadow-lg overflow-hidden">
                    {/* 主内容区 */}
                    <div className="px-4 py-3 flex items-center justify-between">
                        {children}
                    </div>

                    {/* 可展开内容区 */}
                    {expandableContent && (
                        <div
                            className="transition-all duration-300 ease-out overflow-hidden border-t border-border"
                            style={{ maxHeight: expanded ? '200px' : '0px' }}
                        >
                            <div className="p-3">
                                {expandableContent}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </>
    );
}

/**
 * 地点输入模态框组件
 *
 * 'use client' 标记说明：
 * - 使用 useState 管理模态框状态
 * - 包含交互式地点选择
 */
'use client';

import { useState } from 'react';
import { MapPin, X } from 'lucide-react';
import type { BaziFormData } from '@/types';
import { RegionPicker } from '@/components/bazi/form/RegionPicker';

interface PlaceInputModalProps {
    isOpen: boolean;
    onClose: () => void;
    formData: BaziFormData;
    onUpdate: <K extends keyof BaziFormData>(field: K, value: BaziFormData[K]) => void;
}

export function PlaceInputModal({
    isOpen,
    onClose,
    formData,
    onUpdate,
}: PlaceInputModalProps) {
    // 使用 isOpen 作为 key 的一部分，每次打开时重新初始化状态
    const [localPlace, setLocalPlace] = useState(formData.birthPlace || '');

    // 当模态框打开时，同步外部值到本地状态
    // 使用条件初始化而非 useEffect
    const [lastIsOpen, setLastIsOpen] = useState(isOpen);
    if (isOpen && !lastIsOpen) {
        setLocalPlace(formData.birthPlace || '');
    }
    if (isOpen !== lastIsOpen) {
        setLastIsOpen(isOpen);
    }

    const handleConfirm = () => {
        onUpdate('birthPlace', localPlace);
        onClose();
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 animate-fade-in">
            {/* 遮罩层 */}
            <div
                className="absolute inset-0 bg-[#37352f]/20 backdrop-blur-[2px]"
                onClick={onClose}
            />

            {/* 模态框内容 */}
            <div className="relative bg-background rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-border text-foreground">
                {/* 头部 */}
                <div className="sticky top-0 bg-background border-b border-border/60 px-6 py-4 flex items-center justify-between z-10">
                    <h2 className="text-lg font-bold flex items-center gap-2">
                        <MapPin className="w-5 h-5 text-[#2383e2]" />
                        出生地点
                    </h2>
                    <button
                        type="button"
                        onClick={onClose}
                        className="text-foreground/40 hover:text-foreground hover:bg-background-secondary p-1 rounded-md transition-all duration-150"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* 内容 */}
                <div className="p-6 space-y-6">
                    {/* 省市区选择 */}
                    <RegionPicker
                        value={localPlace}
                        onChange={setLocalPlace}
                    />

                    {/* 说明 */}
                    <div className="bg-blue-50 text-[#2eaadc] p-4 rounded-md text-xs flex items-start gap-3 border border-blue-100">
                        <MapPin className="w-4 h-4 mt-0.5 flex-shrink-0" />
                        <p className="leading-relaxed font-medium">
                            出生地点会在提交时通过高德 Web 服务解析经度，用于真太阳时修正。如果无法精确解析到城市或区县，系统会自动回退为北京时间（东八区）排盘。
                        </p>
                    </div>
                </div>

                {/* 底部按钮 */}
                <div className="sticky bottom-0 bg-background/80 backdrop-blur-md border-t border-border/60 px-6 py-4 flex gap-3">
                    <button
                        type="button"
                        onClick={onClose}
                        className="flex-1 px-4 py-2 bg-background border border-border rounded-md text-sm font-semibold text-foreground
                            hover:bg-background-secondary active:bg-background-tertiary transition-all duration-150"
                    >
                        取消
                    </button>
                    <button
                        type="button"
                        onClick={handleConfirm}
                        className="flex-1 px-4 py-2 bg-[#2383e2] text-white rounded-md text-sm font-semibold
                            hover:bg-[#2383e2]/90 active:bg-[#1a65b0] transition-all duration-150"
                    >
                        确定
                    </button>
                </div>
            </div>
        </div>
    );
}

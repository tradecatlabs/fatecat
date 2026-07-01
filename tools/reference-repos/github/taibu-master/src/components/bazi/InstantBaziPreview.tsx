/**
 * 即时排盘预览组件
 *
 * 'use client' 标记说明：
 * - 使用 useState 和 useEffect 管理实时更新
 * - 每秒更新当前时间的四柱
 */
'use client';

import { useState, useEffect, useMemo } from 'react';
import { Sparkles } from 'lucide-react';
import { Solar } from 'lunar-javascript';
import { calculateBazi } from 'taibu-core/bazi';
import type { BaziFormData } from '@/types';
import { getEarthlyBranchByHour } from '@/lib/divination/bazi-form-utils';

interface InstantBaziPreviewProps {
    onUseInstant: () => void;
}

export function InstantBaziPreview({ onUseInstant }: InstantBaziPreviewProps) {
    const [currentTime, setCurrentTime] = useState<Date | null>(null);

    // 每分钟更新当前时间（八字只在分钟变化时可能改变）
    useEffect(() => {
        const updateTime = () => setCurrentTime(new Date());
        updateTime();
        const interval = setInterval(() => {
            updateTime();
        }, 60000); // 改为每分钟更新

        return () => clearInterval(interval);
    }, []);

    // 计算当前时间的八字（使用 useMemo 优化性能）
    const instantBazi = useMemo(() => {
        if (!currentTime) {
            return null;
        }
        const now = currentTime;
        const formData: BaziFormData = {
            name: '',
            gender: 'male',
            birthYear: now.getFullYear(),
            birthMonth: now.getMonth() + 1,
            birthDay: now.getDate(),
            birthHour: now.getHours(),
            birthMinute: now.getMinutes(),
            calendarType: 'solar',
            isLeapMonth: false,
            birthPlace: '',
        };

        try {
            const result = calculateBazi({
                gender: formData.gender,
                birthYear: formData.birthYear,
                birthMonth: formData.birthMonth,
                birthDay: formData.birthDay,
                birthHour: formData.birthHour,
                birthMinute: formData.birthMinute,
                calendarType: 'solar',
                isLeapMonth: false,
                birthPlace: formData.birthPlace,
            });
            return result.fourPillars;
        } catch (error) {
            console.error('计算即时八字失败:', error);
            return null;
        }
    }, [currentTime]);

    // 获取农历信息
    const lunarInfo = useMemo(() => {
        if (!currentTime) {
            return null;
        }
        const solar = Solar.fromYmdHms(
            currentTime.getFullYear(),
            currentTime.getMonth() + 1,
            currentTime.getDate(),
            currentTime.getHours(),
            currentTime.getMinutes(),
            0
        );
        const lunar = solar.getLunar();
        return {
            year: lunar.getYear(),
            month: Math.abs(lunar.getMonth()),
            day: lunar.getDay(),
            hourBranch: getEarthlyBranchByHour(currentTime.getHours()),
        };
    }, [currentTime]);

    if (!instantBazi || !lunarInfo || !currentTime) {
        return null;
    }

    return (
        <div className="bg-background rounded-lg md:p-6 p-4 shadow-sm border border-border animate-fade-in">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold flex items-center gap-2 text-foreground">
                    <Sparkles className="w-5 h-5 text-[#2383e2]" />
                    即时排盘
                </h2>
                <button
                    type="button"
                    onClick={onUseInstant}
                    className="px-4 py-2 bg-[#2383e2] text-white rounded-md text-sm font-semibold
                        hover:bg-[#2383e2]/90 active:bg-[#1a65b0] transition-all duration-150"
                >
                    使用此时间
                </button>
            </div>

            {/* 四柱显示 */}
            <div className="grid grid-cols-4 gap-3 mb-4">
                {[
                    { label: '年柱', pillar: instantBazi.year },
                    { label: '月柱', pillar: instantBazi.month },
                    { label: '日柱', pillar: instantBazi.day },
                    { label: '时柱', pillar: instantBazi.hour },
                ].map(({ label, pillar }) => (
                    <div
                        key={label}
                        className="bg-background rounded-md p-3 text-center border border-border/60"
                    >
                        <div className="text-[11px] font-semibold text-foreground/50 uppercase tracking-wider mb-1">{label}</div>
                        <div className="text-2xl font-bold text-foreground">
                            {pillar.stem}
                        </div>
                        <div className="text-2xl font-bold text-foreground">
                            {pillar.branch}
                        </div>
                    </div>
                ))}
            </div>

            {/* 时间信息 */}
            <div className="text-sm text-foreground/60 space-y-1">
                <div>
                    农历：{lunarInfo.year}年
                    {['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '冬月', '腊月'][lunarInfo.month - 1]}
                    {['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
                        '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
                        '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'][lunarInfo.day - 1]}
                    {' '}
                    {lunarInfo.hourBranch}时
                </div>
                <div>
                    公历：{currentTime.getFullYear()}年
                    {String(currentTime.getMonth() + 1).padStart(2, '0')}月
                    {String(currentTime.getDate()).padStart(2, '0')}日
                    {' '}
                    {String(currentTime.getHours()).padStart(2, '0')}:
                    {String(currentTime.getMinutes()).padStart(2, '0')}:
                    {String(currentTime.getSeconds()).padStart(2, '0')}
                </div>
            </div>
        </div>
    );
}

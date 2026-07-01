/**
 * 紫微斗数结果页面
 *
 * 对齐 Notion 风格：极简列表、柔和边框、线性图标、去除渐变
 */
'use client';

import { useMemo, useState, useEffect, useCallback, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { SettingsCenterLink } from '@/components/settings/SettingsCenterLink';
import { Share2, Edit3, Save, Check, Copy, MapPinned, Clock, Plus, Minus } from 'lucide-react';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { buildZiweiCanonicalJSON, calculateZiweiChartBundle, generateZiweiChartText, type ZiweiFormData } from '@/lib/divination/ziwei';
import type { Gender, CalendarType } from '@/types';
import { ZiweiChartGrid } from '@/components/ziwei/ZiweiChartGrid';
import { ZiweiHoroscopePanel, type HoroscopeInfo, type HoroscopeHighlight } from '@/components/ziwei/ZiweiHoroscopePanel';
import { supabase } from '@/lib/auth';
import { AuthModal } from '@/components/auth/AuthModal';
import { useToast } from '@/components/ui/Toast';
import { useHeaderMenu } from '@/components/layout/HeaderMenuContext';
import { getDayCount } from '@/lib/date-utils';
import { createSavedChart, loadSavedChart } from '@/lib/user/charts-client';
import { parseBirthTimeString } from '@/lib/divination/birth-time';
import { parseLongitude } from '@/lib/divination/place-resolution';
import { useAdminJsonCopy } from '@/lib/admin/useAdminJsonCopy';
import { CopyTextModal } from '@/components/divination/CopyTextModal';
import type { ChartTextDetailLevel } from '@/lib/divination/detail-level';

function ZiweiResultContent() {
    const searchParams = useSearchParams();
    const router = useRouter();
    const { setMenuItems, clearMenuItems } = useHeaderMenu();
    const chartId = searchParams.get('chart');
    const hasFormParams = useMemo(() => {
        const params = ['name', 'gender', 'year', 'month', 'day', 'hour', 'calendar', 'leap', 'place'];
        return params.some((key) => searchParams.has(key));
    }, [searchParams]);
    const [saving, setSaving] = useState(false);
    const [saved, setSaved] = useState(false);
    const [loading, setLoading] = useState(() => Boolean(chartId) && !hasFormParams);
    const [notFound, setNotFound] = useState(false);
    const [loadError, setLoadError] = useState<string | null>(null);
    const [chartFromDb, setChartFromDb] = useState<ZiweiFormData | null>(null);
    const [horoscopeHighlight, setHoroscopeHighlight] = useState<HoroscopeHighlight>({});
    const [horoscopeInfo, setHoroscopeInfo] = useState<HoroscopeInfo | undefined>(undefined);
    const [hourOffset, setHourOffset] = useState(0); // 时辰调整偏移
    const [copyDetailLevel, setCopyDetailLevel] = useState<ChartTextDetailLevel>('default');
    const [copied, setCopied] = useState(false);
    const [showCopyModal, setShowCopyModal] = useState(false);
    const [showAuthModal, setShowAuthModal] = useState(false);
    const { showToast } = useToast();

    type SavedZiweiChartRow = {
        name: string;
        gender: Gender;
        birth_date: string;
        birth_time: string;
        birth_place: string | null;
        longitude?: number | null;
        calendar_type: CalendarType | null;
        is_leap_month: boolean | null;
    };

    // 编辑模式
    useEffect(() => {
        if (hasFormParams) {
            setChartFromDb(null);
            setSaved(false);
            setNotFound(false);
            setLoadError(null);
            setLoading(false);
        }
    }, [hasFormParams]);

    // 加载已保存命盘
    useEffect(() => {
        if (!chartId || hasFormParams) return;

        let cancelled = false;

        const loadChart = async () => {
            setLoading(true);
            setNotFound(false);
            setLoadError(null);

            try {
                const row = await loadSavedChart('ziwei', chartId);
                if (cancelled) return;

                const data = row as SavedZiweiChartRow | null;
                if (!data) {
                    setNotFound(true);
                    return;
                }

                const birthDate = data.birth_date as string;
                const birthTime = data.birth_time as string;
                const parsedBirthTime = parseBirthTimeString(birthTime);
                if (!parsedBirthTime) {
                    setLoadError('该紫微命盘缺少有效出生时辰，无法加载');
                    return;
                }
                const [year, month, day] = birthDate.split('-').map(Number);
                setChartFromDb({
                    name: data.name as string,
                    gender: (data.gender as Gender) || 'male',
                    birthYear: year,
                    birthMonth: month,
                    birthDay: day,
                    birthHour: parsedBirthTime.hour,
                    birthMinute: parsedBirthTime.minute,
                    calendarType: (data.calendar_type as CalendarType) || 'solar',
                    isLeapMonth: (data.is_leap_month as boolean | undefined) ?? false,
                    birthPlace: (data.birth_place as string) || '',
                    longitude: parseLongitude(data.longitude),
                });
                setSaved(true);
            } catch (error) {
                if (!cancelled) {
                    setLoadError(error instanceof Error ? error.message : '加载命盘失败');
                }
            } finally {
                if (!cancelled) {
                    setLoading(false);
                }
            }
        };

        void loadChart();
        return () => {
            cancelled = true;
        };
    }, [chartId, hasFormParams]);

    // 从 URL 参数获取表单数据
    const formData: ZiweiFormData | null = useMemo(() => {
        const hourParam = searchParams.get('hour');
        const minuteParam = searchParams.get('minute') || '0';
        if (!hourParam || hourParam === '-1') {
            return null;
        }

        const birthHour = Number(hourParam);
        const birthMinute = Number(minuteParam);
        if (
            !Number.isInteger(birthHour)
            || birthHour < 0
            || birthHour > 23
            || !Number.isInteger(birthMinute)
            || birthMinute < 0
            || birthMinute > 59
        ) {
            return null;
        }

        return {
            name: searchParams.get('name') || '命主',
            gender: (searchParams.get('gender') as Gender) || 'male',
            birthYear: Number(searchParams.get('year')) || 1990,
            birthMonth: Number(searchParams.get('month')) || 1,
            birthDay: Number(searchParams.get('day')) || 1,
            birthHour,
            birthMinute,
            calendarType: (searchParams.get('calendar') as CalendarType) || 'solar',
            isLeapMonth: searchParams.get('leap') === '1',
            birthPlace: searchParams.get('place') || '',
            longitude: parseLongitude(searchParams.get('longitude')),
        };
    }, [searchParams]);
    const resolvedFormData = chartFromDb || formData;

    // 应用时辰偏移
    const adjustedFormData = useMemo(() => {
        if (!resolvedFormData || hourOffset === 0) return resolvedFormData;

        let adjustedHour = resolvedFormData.birthHour + hourOffset;
        let adjustedDay = resolvedFormData.birthDay;
        let adjustedMonth = resolvedFormData.birthMonth;
        let adjustedYear = resolvedFormData.birthYear;

        while (adjustedHour >= 24) { adjustedHour -= 24; adjustedDay += 1; }
        while (adjustedHour < 0) { adjustedHour += 24; adjustedDay -= 1; }

        let daysInMonth = getDayCount(resolvedFormData.calendarType, adjustedYear, adjustedMonth, resolvedFormData.isLeapMonth);
        while (adjustedDay > daysInMonth) {
            adjustedDay -= daysInMonth; adjustedMonth += 1;
            if (adjustedMonth > 12) { adjustedMonth = 1; adjustedYear += 1; }
            daysInMonth = getDayCount(resolvedFormData.calendarType, adjustedYear, adjustedMonth, resolvedFormData.isLeapMonth);
        }
        while (adjustedDay < 1) {
            adjustedMonth -= 1;
            if (adjustedMonth < 1) { adjustedMonth = 12; adjustedYear -= 1; }
            daysInMonth = getDayCount(resolvedFormData.calendarType, adjustedYear, adjustedMonth, resolvedFormData.isLeapMonth);
            adjustedDay += daysInMonth;
        }

        return { ...resolvedFormData, birthYear: adjustedYear, birthMonth: adjustedMonth, birthDay: adjustedDay, birthHour: adjustedHour };
    }, [resolvedFormData, hourOffset]);

    // 计算紫微命盘
    const bundle = useMemo(() => {
        if (!adjustedFormData) {
            return null;
        }
        try { return calculateZiweiChartBundle(adjustedFormData); } catch (error) { console.error('紫微排盘错误:', error); return null; }
    }, [adjustedFormData]);
    const output = bundle?.output ?? null;
    const astrolabe = bundle?.astrolabe ?? null;
    const canonicalChart = useMemo(() => {
        if (!output) return null;
        return buildZiweiCanonicalJSON(output);
    }, [output]);
    const { isAdmin, jsonCopied, copyJson } = useAdminJsonCopy(canonicalChart);
    const trueSolarTimeText = canonicalChart?.基本信息.真太阳时?.真太阳时 ?? null;

    // 修改命盘
    const handleEdit = useCallback(() => {
        if (!resolvedFormData) return;
        const params = new URLSearchParams({
            name: resolvedFormData.name,
            gender: resolvedFormData.gender,
            year: String(resolvedFormData.birthYear),
            month: String(resolvedFormData.birthMonth),
            day: String(resolvedFormData.birthDay),
            hour: String(resolvedFormData.birthHour),
            minute: String(resolvedFormData.birthMinute || 0),
            calendar: resolvedFormData.calendarType,
        });
        if (resolvedFormData.calendarType === 'lunar' && resolvedFormData.isLeapMonth) params.set('leap', '1');
        if (resolvedFormData.birthPlace) params.set('place', resolvedFormData.birthPlace);
        if (resolvedFormData.longitude != null) params.set('longitude', String(resolvedFormData.longitude));
        if (chartId) params.set('chart', chartId);
        router.push(`/ziwei?${params.toString()}`);
    }, [resolvedFormData, chartId, router]);

    const handleSave = useCallback(async () => {
        if (saving || !output || !resolvedFormData) return;
        const { data: { session } } = await supabase.auth.getSession();
        if (!session?.user) { showToast('warning', '请先登录后再保存命盘'); setShowAuthModal(true); return; }
        setSaving(true);
        try {
            const payload = {
                name: resolvedFormData.name,
                gender: resolvedFormData.gender,
                birth_date: `${resolvedFormData.birthYear}-${String(resolvedFormData.birthMonth).padStart(2, '0')}-${String(resolvedFormData.birthDay).padStart(2, '0')}`,
                birth_time: `${String(resolvedFormData.birthHour).padStart(2, '0')}:${String(resolvedFormData.birthMinute || 0).padStart(2, '0')}`,
                calendar_type: resolvedFormData.calendarType,
                is_leap_month: resolvedFormData.isLeapMonth ?? false,
                birth_place: resolvedFormData.birthPlace || null,
                longitude: resolvedFormData.longitude ?? null,
            };
            if (chartId) {
                const response = await fetch('/api/ziwei/charts/update', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chartId, payload }),
                });
                if (!response.ok) { const result = await response.json().catch(() => null); throw new Error(result?.error || '更新失败'); }
            } else {
                const insertedId = await createSavedChart('ziwei', payload);
                if (insertedId) router.replace(`/ziwei/result?chart=${insertedId}`);
                else throw new Error('保存失败');
            }
            setSaved(true);
            setChartFromDb(resolvedFormData);
        } catch (error) { console.error('保存失败:', error); showToast('error', '保存失败，请重试'); } finally { setSaving(false); }
    }, [saving, output, resolvedFormData, chartId, router, showToast]);

    // 分享
    const handleShare = useCallback(async () => {
        if (!resolvedFormData) {
            return;
        }
        const url = window.location.href;
        if (navigator.share) {
            try { await navigator.share({ title: `${resolvedFormData.name}的紫微命盘 - 太卜`, text: `查看${resolvedFormData.name}的紫微斗数命盘`, url }); } catch { }
        } else {
            try { await navigator.clipboard.writeText(url); showToast('success', '链接已复制到剪贴板'); } catch { showToast('error', '复制链接失败'); }
        }
    }, [resolvedFormData, showToast]);

    const handleConfirmCopy = useCallback(async (level: ChartTextDetailLevel) => {
        if (!output) return;
        try {
            setCopyDetailLevel(level);
            await navigator.clipboard.writeText(generateZiweiChartText(output, { detailLevel: level }));
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
            setShowCopyModal(false);
        } catch {
            showToast('error', '复制失败，请手动复制');
        }
    }, [output, showToast]);

    // Header 菜单项
    useEffect(() => {
        const items = [
            { id: 'edit', label: '修改', icon: <Edit3 className="w-4 h-4" />, onClick: handleEdit },
            { id: 'save', label: saved ? '已保存' : '保存', icon: <Save className="w-4 h-4" />, onClick: handleSave, disabled: saving || saved },
            { id: 'share', label: '分享', icon: <Share2 className="w-4 h-4" />, onClick: handleShare },
            ...(isAdmin && canonicalChart ? [{ id: 'copy-json', label: jsonCopied ? 'JSON 已复制' : '复制 JSON', icon: jsonCopied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />, onClick: () => { void copyJson(); } }] : []),
        ];
        setMenuItems(items);
        return () => clearMenuItems();
    }, [saving, saved, isAdmin, canonicalChart, jsonCopied, copyJson, setMenuItems, clearMenuItems, handleEdit, handleSave, handleShare]);

    if (loading) return <SoundWaveLoader variant="block" text="" />;
    if (notFound) {
        return (
            <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4 text-center">
                <p className="text-sm text-foreground/40 mb-6">未找到该命盘，请返回重新选择</p>
                <SettingsCenterLink tab="charts" className="px-4 py-2 bg-[#2383e2] text-white text-sm font-medium rounded-md hover:bg-[#2383e2]/90 transition-colors">返回我的命盘</SettingsCenterLink>
            </div>
        );
    }
    if (!resolvedFormData || loadError || !output || !astrolabe || !canonicalChart) {
        return (
            <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4 text-center">
                <p className="text-sm text-foreground/40 mb-6">{loadError || '紫微斗数必须提供出生时辰，请返回重新输入'}</p>
                <Link href="/ziwei" className="px-4 py-2 bg-[#2383e2] text-white text-sm font-medium rounded-md hover:bg-[#2383e2]/90 transition-colors">返回重新输入</Link>
            </div>
        );
    }

    const displayFormData = adjustedFormData ?? resolvedFormData;
    const timeText = `${String(displayFormData.birthHour).padStart(2, '0')}:${String(displayFormData.birthMinute || 0).padStart(2, '0')}`;

    return (
        <div className="min-h-screen bg-background">
            <div className="max-w-5xl mx-auto px-4 py-8 animate-fade-in space-y-8">
                {/* 头部操作栏 */}
                <div className="hidden md:flex items-center justify-between">
                    <Link href="/ziwei" className="text-sm font-medium text-foreground/40 hover:text-foreground hover:bg-background-secondary px-2 py-1 rounded-md transition-colors">返回</Link>
                    <div className="flex items-center gap-2">
                        <button onClick={handleEdit} className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm font-medium border border-border hover:bg-background-secondary transition-colors"><Edit3 className="w-3.5 h-3.5" />修改</button>
                        <button onClick={handleSave} disabled={saving || saved} className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${saved ? 'text-[#0f7b6c] bg-[#0f7b6c]/5 border border-[#0f7b6c]/10' : 'bg-[#2383e2] text-white hover:bg-[#2383e2]/90'}`}>{saved ? <><Check className="w-3.5 h-3.5" />已保存</> : saving ? <><SoundWaveLoader variant="inline" />保存中</> : <><Save className="w-3.5 h-3.5" />保存</>}</button>
                        <button onClick={handleShare} className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm font-medium border border-border hover:bg-background-secondary transition-colors"><Share2 className="w-3.5 h-3.5" />分享</button>
                    </div>
                </div>

                <div className="bg-background border border-border rounded-md px-5 py-4 shadow-sm">
                    <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                        <div className="flex flex-wrap items-center gap-2 min-w-0">
                            <h1 className="text-xl font-semibold tracking-tight truncate text-foreground">
                                {resolvedFormData.name}
                            </h1>
                            <span className={`px-2 py-0.5 text-[10px] font-bold rounded uppercase tracking-[0.18em] ${resolvedFormData.gender === 'male' ? 'text-blue-500/70 bg-blue-50' : 'text-pink-500/70 bg-pink-50'}`}>
                                {resolvedFormData.gender === 'male' ? '男' : '女'}
                            </span>
                        </div>

                        <div className="flex flex-wrap items-center gap-x-5 gap-y-2 text-sm text-foreground/60 lg:justify-end lg:min-w-0 lg:pl-6 lg:border-l lg:border-border/60">
                            <div className="flex items-center gap-1.5 min-w-0">
                                <span className="text-[10px] font-bold uppercase tracking-[0.18em] text-foreground/30 shrink-0">
                                    出生时间
                                </span>
                                <Clock className="w-3.5 h-3.5 text-foreground/35 shrink-0" />
                                <span className="font-medium text-foreground/80 truncate">
                                    {displayFormData.birthYear}年{displayFormData.birthMonth}月{displayFormData.birthDay}日 {timeText}
                                </span>
                                {hourOffset !== 0 && (
                                    <span className="text-xs font-medium text-[#2eaadc] shrink-0">
                                        ({hourOffset > 0 ? '+' : ''}{hourOffset}h)
                                    </span>
                                )}
                                <div className="flex items-center bg-background-secondary rounded p-0.5 shrink-0">
                                    <button onClick={() => setHourOffset(prev => prev - 1)} className="p-0.5 hover:bg-background rounded transition-colors"><Minus className="w-3 h-3" /></button>
                                    <button onClick={() => setHourOffset(prev => prev + 1)} className="p-0.5 hover:bg-background rounded transition-colors"><Plus className="w-3 h-3" /></button>
                                    {hourOffset !== 0 && <button onClick={() => setHourOffset(0)} className="px-1 text-[10px] font-bold text-foreground/40 hover:text-foreground">RESET</button>}
                                </div>
                            </div>

                            <div className="flex items-center gap-1.5 min-w-0">
                                <span className="text-[10px] font-bold uppercase tracking-[0.18em] text-foreground/30 shrink-0">
                                    农历
                                </span>
                                <span className="font-medium text-foreground/80 truncate">{canonicalChart.基本信息.农历}</span>
                            </div>

                            {trueSolarTimeText && (
                                <div className="flex items-center gap-1.5 min-w-0">
                                    <span className="text-[10px] font-bold uppercase tracking-[0.18em] text-foreground/30 shrink-0">
                                        真太阳时
                                    </span>
                                    <span className="font-medium text-foreground/80 truncate">{trueSolarTimeText}</span>
                                </div>
                            )}

                            {resolvedFormData.birthPlace && (
                                <div className="flex items-center gap-1.5 min-w-0">
                                    <span className="text-[10px] font-bold uppercase tracking-[0.18em] text-foreground/30 shrink-0">
                                        出生地点
                                    </span>
                                    <MapPinned className="w-3.5 h-3.5 text-foreground/35 shrink-0" />
                                    <span className="font-medium text-foreground/80 truncate">{resolvedFormData.birthPlace}</span>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                <section className="bg-background border border-border rounded-md p-6">
                    <ZiweiChartGrid
                        canonicalChart={canonicalChart}
                        copied={copied}
                        onCopy={() => setShowCopyModal(true)}
                        showJsonCopy={isAdmin && !!canonicalChart}
                        jsonCopied={jsonCopied}
                        onCopyJson={() => { void copyJson(); }}
                        horoscopeHighlight={horoscopeHighlight}
                        horoscopeInfo={horoscopeInfo}
                    />
                </section>

                <ZiweiHoroscopePanel
                    output={output}
                    astrolabe={astrolabe}
                    canonicalChart={canonicalChart}
                    onPalaceHighlight={setHoroscopeHighlight}
                    onHoroscopeChange={setHoroscopeInfo}
                />

                <footer className="py-12 text-center">
                    <p className="text-[11px] text-foreground/30 font-medium italic">* 点击命盘宫位可查看三方四正与详细分析</p>
                </footer>
            </div>

            <CopyTextModal
                isOpen={showCopyModal}
                value={copyDetailLevel}
                onChange={setCopyDetailLevel}
                onClose={() => setShowCopyModal(false)}
                onConfirm={handleConfirmCopy}
            />
            <AuthModal isOpen={showAuthModal} onClose={() => setShowAuthModal(false)} />
        </div>
    );
}

export default function ZiweiResultPage() {
    return (
        <Suspense fallback={<SoundWaveLoader variant="block" text="正在排盘" />}>
            <ZiweiResultContent />
        </Suspense>
    );
}

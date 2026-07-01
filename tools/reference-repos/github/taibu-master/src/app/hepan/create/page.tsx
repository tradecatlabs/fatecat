/**
 * 创建合盘页面
 *
 * 输入双方生日信息，支持从已保存命盘选择
 */
'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, FolderOpen, X, AlertCircle, Sparkles, ChevronDown } from 'lucide-react';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { type HepanType, type BirthInfo, getHepanTypeName, analyzeCompatibility } from '@/lib/divination/hepan';
import { ChartPickerModal, type ChartItem } from '@/components/common/ChartPickerModal';
import { supabase } from '@/lib/auth';
import { writeSessionJSON } from '@/lib/cache/session-storage';
import { saveDivinationAction } from '@/lib/divination/save-client';

function BirthInput({
    label,
    value,
    onChange,
    personIndex,
    userId,
    onPick,
    type
}: {
    label: string;
    value: Partial<BirthInfo>;
    onChange: (v: Partial<BirthInfo>) => void;
    personIndex: 1 | 2;
    userId?: string | null;
    onPick?: (person: 1 | 2) => void;
    type: HepanType;
}) {
    const theme = {
        love: { active: 'focus:border-rose-500', ring: 'focus:ring-rose-500/20', text: 'text-rose-500', bg: 'bg-rose-500' },
        business: { active: 'focus:border-blue-500', ring: 'focus:ring-blue-500/20', text: 'text-blue-500', bg: 'bg-blue-500' },
        family: { active: 'focus:border-emerald-500', ring: 'focus:ring-emerald-500/20', text: 'text-emerald-500', bg: 'bg-emerald-500' },
    }[type];

    return (
        <div className="bg-background/5 backdrop-blur-xl border border-white/10 rounded-3xl p-6 md:p-8 shadow-2xl transition-all duration-300 hover:border-white/20 hover:shadow-3xl group">
            <div className="flex items-center justify-between mb-8">
                <h3 className="text-xl font-bold text-foreground flex items-center gap-3">
                    <div className={`w-1.5 h-6 rounded-full ${theme.bg} shadow-[0_0_10px_rgba(var(--theme-color),0.5)]`} />
                    {label}
                </h3>
                {userId && onPick && (
                    <button
                        onClick={() => onPick(personIndex)}
                        className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-foreground-secondary
                            hover:text-foreground hover:bg-background/10 rounded-xl transition-all border border-transparent hover:border-white/10"
                    >
                        <FolderOpen className="w-4 h-4" />
                        从命盘选择
                    </button>
                )}
            </div>

            <div className="space-y-6">
                {/* 姓名和性别 */}
                <div className="grid grid-cols-2 gap-5">
                    <div className="space-y-2">
                        <label className="text-xs font-semibold text-foreground-secondary uppercase tracking-wider px-1">称呼</label>
                        <input
                            type="text"
                            value={value.name || ''}
                            onChange={(e) => onChange({ ...value, name: e.target.value })}
                            placeholder="请输入称呼"
                            className={`w-full px-4 py-3 bg-background/5 border border-white/10 rounded-xl
                                text-foreground placeholder:text-foreground-secondary/30
                                focus:outline-none ${theme.active} focus:ring-4 ${theme.ring} transition-all duration-300`}
                        />
                    </div>
                    <div className="space-y-2">
                        <label className="text-xs font-semibold text-foreground-secondary uppercase tracking-wider px-1">性别</label>
                        <div className="relative">
                            <select
                                value={value.gender || ''}
                                onChange={(e) => onChange({ ...value, gender: e.target.value as 'male' | 'female' || undefined })}
                                className={`w-full px-4 py-3 bg-background/5 border border-white/10 rounded-xl
                                    text-foreground appearance-none cursor-pointer
                                    focus:outline-none ${theme.active} focus:ring-4 ${theme.ring} transition-all duration-300`}
                            >
                                <option value="">请选择</option>
                                <option value="male">男</option>
                                <option value="female">女</option>
                            </select>
                            <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-foreground-secondary">
                                <ChevronDown className="w-4 h-4" />
                            </div>
                        </div>
                    </div>
                </div>

                {/* 日期 */}
                <div className="space-y-2">
                    <label className="text-xs font-semibold text-foreground-secondary uppercase tracking-wider px-1">出生日期 (公历)</label>
                    <div className="grid grid-cols-3 gap-4">
                        {[
                            { key: 'year', label: '年', min: 1900, max: 2030, placeholder: '2000' },
                            { key: 'month', label: '月', min: 1, max: 12, placeholder: '01' },
                            { key: 'day', label: '日', min: 1, max: 31, placeholder: '01' }
                        ].map(({ key, label, min, max, placeholder }) => (
                            <div key={key} className="relative group/input">
                                <input
                                    type="number"
                                    value={value[key as keyof BirthInfo] as number || ''}
                                    onChange={(e) => {
                                        const val = e.target.value;
                                        // 允许清空
                                        if (val === '') {
                                            onChange({ ...value, [key]: undefined });
                                            return;
                                        }
                                        // 只允许数字
                                        if (!/^\d*$/.test(val)) return;

                                        const num = parseInt(val);
                                        // 长度限制：年4位，其他2位
                                        if (key === 'year' && val.length > 4) return;
                                        if (key !== 'year' && val.length > 2) return;

                                        // 数值范围限制
                                        if (max && num > max) return;

                                        onChange({ ...value, [key]: num });
                                    }}
                                    placeholder={placeholder}
                                    min={min}
                                    max={max}
                                    className={`w-full px-4 py-3 bg-background/5 border border-white/10 rounded-xl
                                        text-foreground placeholder:text-foreground-secondary/30 text-center font-medium
                                        focus:outline-none ${theme.active} focus:ring-4 ${theme.ring} transition-all duration-300
                                        [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none`}
                                />
                                <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs font-medium text-foreground-secondary/70 pointer-events-none group-focus-within/input:text-foreground transition-colors">
                                    {label}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* 时辰 */}
                <div className="space-y-2">
                    <label className="text-xs font-semibold text-foreground-secondary uppercase tracking-wider px-1">出生时辰</label>
                    <div className="relative group/select">
                        <select
                            value={value.hour ?? ''}
                            onChange={(e) => onChange({ ...value, hour: e.target.value ? parseInt(e.target.value) : undefined })}
                            className={`w-full px-4 py-3 bg-background/5 border border-white/10 rounded-xl
                                text-foreground appearance-none cursor-pointer
                                focus:outline-none ${theme.active} focus:ring-4 ${theme.ring} transition-all duration-300`}
                        >
                            <option value="">请选择时辰 (不清楚可不填)</option>
                            <option value="0">子时 (23:00-01:00)</option>
                            <option value="2">丑时 (01:00-03:00)</option>
                            <option value="4">寅时 (03:00-05:00)</option>
                            <option value="6">卯时 (05:00-07:00)</option>
                            <option value="8">辰时 (07:00-09:00)</option>
                            <option value="10">巳时 (09:00-11:00)</option>
                            <option value="12">午时 (11:00-13:00)</option>
                            <option value="14">未时 (13:00-15:00)</option>
                            <option value="16">申时 (15:00-17:00)</option>
                            <option value="18">酉时 (17:00-19:00)</option>
                            <option value="20">戌时 (19:00-21:00)</option>
                            <option value="22">亥时 (21:00-23:00)</option>
                        </select>
                        <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-foreground-secondary group-focus-within/select:text-foreground transition-colors">
                            <ChevronDown className="w-4 h-4" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

function HepanCreateContent() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const type = (searchParams.get('type') || 'love') as HepanType;

    const [person1, setPerson1] = useState<Partial<BirthInfo>>({ name: '' });
    const [person2, setPerson2] = useState<Partial<BirthInfo>>({ name: '' });
    const [loading, setLoading] = useState(false);
    const [userId, setUserId] = useState<string | null>(null);
    const [pickerOpen, setPickerOpen] = useState<1 | 2 | null>(null);
    const [validationError, setValidationError] = useState<string | null>(null);

    // 获取用户 ID
    useEffect(() => {
        supabase.auth.getSession().then(({ data: { session } }) => {
            if (session?.user) {
                setUserId(session.user.id);
            }
        });
    }, []);

    const labels = {
        love: { p1: '您', p2: '对方' },
        business: { p1: '合伙人A', p2: '合伙人B' },
        family: { p1: '父/母', p2: '子/女' },
    };

    const normalizeHourToShichen = (hour?: number) => {
        if (hour === undefined || Number.isNaN(hour)) return undefined;
        const normalized = ((hour % 24) + 24) % 24;
        const slot = Math.floor((normalized + 1) / 2) * 2;
        return slot === 24 ? 0 : slot;
    };

    const handleChartSelect = (chart: ChartItem) => {
        const birthInfo: Partial<BirthInfo> = {
            name: chart.name,
            year: chart.birth_year,
            month: chart.birth_month,
            day: chart.birth_day,
            hour: normalizeHourToShichen(chart.birth_hour),
            gender: chart.gender || undefined,
        };

        if (pickerOpen === 1) {
            setPerson1(birthInfo);
        } else if (pickerOpen === 2) {
            setPerson2(birthInfo);
        }
        setPickerOpen(null);
    };

    const handleSubmit = async () => {
        // 验证必填字段
        if (!person1.name || !person1.year || !person1.month || !person1.day) {
            setValidationError('请填写完整的第一人信息');
            return;
        }
        if (!person2.name || !person2.year || !person2.month || !person2.day) {
            setValidationError('请填写完整的第二人信息');
            return;
        }

        setLoading(true);

        // 计算合盘
        const result = analyzeCompatibility(
            person1 as BirthInfo,
            person2 as BirthInfo,
            type
        );

        // 保存合盘记录到数据库
        let chartId: string | null = null;
        try {
            const { data: { session } } = await supabase.auth.getSession();
            if (session?.user) {
                const saveResult = await saveDivinationAction({
                    endpoint: '/api/hepan',
                    body: { result },
                    idKey: 'chartId',
                    fallbackMessage: '保存合盘记录失败',
                });
                if (!saveResult.ok) {
                    throw new Error(saveResult.error.message || '保存合盘记录失败');
                }
                if (saveResult.id) {
                    chartId = saveResult.id;
                }
            }
        } catch (error) {
            console.error('保存合盘记录失败:', error);
        }

        // 存储结果（包含 chartId）
        writeSessionJSON('hepan_result', { ...result, chartId });

        // 跳转结果页
        setTimeout(() => {
            router.push('/hepan/result');
        }, 500);
    };

    const getAccentColor = () => {
        switch (type) {
            case 'love': return 'bg-rose-500 hover:bg-rose-600 shadow-rose-500/20';
            case 'business': return 'bg-blue-500 hover:bg-blue-600 shadow-blue-500/20';
            case 'family': return 'bg-emerald-500 hover:bg-emerald-600 shadow-emerald-500/20';
        }
    };

    return (
        <div className="min-h-screen bg-background">
            {/* 背景装饰 - 移除渐变，保留柔和光晕 */}
            <div className="fixed inset-0 pointer-events-none overflow-hidden">
                <div className="absolute inset-0 bg-grid-pattern opacity-[0.02]" />
                <div className="absolute top-0 left-0 w-[500px] h-[500px] bg-rose-500/5 rounded-full blur-[100px] -translate-x-1/2 -translate-y-1/2" />
                <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-indigo-500/5 rounded-full blur-[100px] translate-x-1/2 translate-y-1/2" />
            </div>

            <div className="max-w-2xl mx-auto px-4 sm:py-8 py-2 relative z-10 animate-fade-in">
                {/* 返回 - 仅桌面端显示 */}
                <Link
                    href="/hepan"
                    className="hidden md:inline-flex items-center gap-2 text-foreground-secondary hover:text-foreground mb-8 transition-colors px-3 py-1.5 rounded-lg hover:bg-background/5"
                >
                    <ArrowLeft className="w-4 h-4" />
                    <span className="text-sm font-medium">返回列表</span>
                </Link>

                {/* 标题 */}
                <div className="text-center sm:mb-10 mb-2">
                    <div className="hidden md:inline-flex items-center justify-center p-3 rounded-2xl bg-background/5 border border-white/10 mb-4 shadow-xl backdrop-blur-sm">
                        <Sparkles className={`w-8 h-8 ${type === 'love' ? 'text-rose-500' :
                            type === 'business' ? 'text-blue-500' : 'text-emerald-500'
                            }`} />
                    </div>
                    <h1 className="hidden md:block text-3xl font-bold text-foreground tracking-tight">{getHepanTypeName(type)}分析</h1>
                    <p className="text-foreground-secondary md:mt-2 text-lg">请输入双方的出生信息，解读彼此的缘分</p>
                </div>

                {/* 输入表单 */}
                <div className="sm:space-y-6 space-y-3 sm:mb-10 mb-3">
                    <BirthInput
                        label={labels[type].p1}
                        value={person1}
                        onChange={setPerson1}
                        personIndex={1}
                        userId={userId}
                        onPick={(person) => setPickerOpen(person)}
                        type={type}
                    />
                    <BirthInput
                        label={labels[type].p2}
                        value={person2}
                        onChange={setPerson2}
                        personIndex={2}
                        userId={userId}
                        onPick={(person) => setPickerOpen(person)}
                        type={type}
                    />
                </div>

                {/* 提交按钮 */}
                <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className={`w-full py-4 text-white rounded-xl font-bold text-lg
                        shadow-lg hover:shadow-xl hover:scale-[1.01] active:scale-[0.99]
                        disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 disabled:shadow-none
                        transition-all flex items-center justify-center gap-2 ${getAccentColor()}`}
                >
                    {loading ? (
                        <>
                            <SoundWaveLoader variant="inline" />
                            正在深度分析...
                        </>
                    ) : (
                        <>
                            <Sparkles className="w-5 h-5" />
                            开始分析缘分
                        </>
                    )}
                </button>
            </div>

            {/* 命盘选择器弹窗 */}
            {userId && pickerOpen && (
                <ChartPickerModal
                    isOpen={true}
                    onClose={() => setPickerOpen(null)}
                    onSelect={handleChartSelect}
                    userId={userId}
                    title={`选择${pickerOpen === 1 ? labels[type].p1 : labels[type].p2}的命盘`}
                />
            )}

            {/* 验证错误弹窗 */}
            {validationError && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
                    <div
                        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
                        onClick={() => setValidationError(null)}
                    />
                    <div className="relative bg-background/95 backdrop-blur-xl rounded-2xl border border-border shadow-2xl p-6 max-w-sm w-full animate-in zoom-in-95">
                        <button
                            onClick={() => setValidationError(null)}
                            className="absolute top-4 right-4 p-1 rounded-lg hover:bg-background-secondary transition-colors"
                        >
                            <X className="w-5 h-5 text-foreground-secondary" />
                        </button>
                        <div className="flex flex-col items-center text-center gap-4">
                            <div className="p-3 rounded-full bg-amber-500/10 text-amber-500">
                                <AlertCircle className="w-8 h-8" />
                            </div>
                            <div>
                                <h3 className="text-lg font-bold text-foreground mb-1">请检查输入</h3>
                                <p className="text-foreground-secondary">{validationError}</p>
                            </div>
                            <button
                                onClick={() => setValidationError(null)}
                                className="w-full py-2.5 bg-background-secondary hover:bg-background-tertiary text-foreground rounded-xl font-medium transition-colors"
                            >
                                知道了
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default function HepanCreatePage() {
    return (
        <Suspense fallback={
            <div className="min-h-screen bg-background flex items-center justify-center">
                <SoundWaveLoader variant="block" text="" />
            </div>
        }>
            <HepanCreateContent />
        </Suspense>
    );
}

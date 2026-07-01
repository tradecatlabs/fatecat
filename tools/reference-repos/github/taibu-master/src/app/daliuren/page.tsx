/**
 * 大六壬排盘主页面
 * 需要 useState + 路由跳转
 */
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { useToast } from '@/components/ui/Toast';
import { HistoryDrawer } from '@/components/layout/HistoryDrawer';
import { FeatureGate } from '@/components/layout/FeatureGate';
import { writeSessionJSON } from '@/lib/cache/session-storage';

type TimeMode = 'now' | 'custom';

function getNow() {
    const d = new Date();
    return {
        year: d.getFullYear(),
        month: d.getMonth() + 1,
        day: d.getDate(),
        hour: d.getHours(),
        minute: d.getMinutes(),
    };
}

const DEFAULT_FORM_TIME = {
    year: 2000,
    month: 1,
    day: 1,
    hour: 0,
    minute: 0,
};

export default function DaliurenPage() {
    const router = useRouter();
    const { showToast } = useToast();

    const [question, setQuestion] = useState('');
    const [timeMode, setTimeMode] = useState<TimeMode>('now');
    const [localTimeZone, setLocalTimeZone] = useState('Asia/Shanghai');
    const [year, setYear] = useState(DEFAULT_FORM_TIME.year);
    const [month, setMonth] = useState(DEFAULT_FORM_TIME.month);
    const [day, setDay] = useState(DEFAULT_FORM_TIME.day);
    const [hour, setHour] = useState(DEFAULT_FORM_TIME.hour);
    const [minute, setMinute] = useState(DEFAULT_FORM_TIME.minute);

    // 高级设置
    const [birthYear, setBirthYear] = useState('');
    const [gender, setGender] = useState<'male' | 'female' | ''>('');

    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const now = getNow();
        setYear(now.year);
        setMonth(now.month);
        setDay(now.day);
        setHour(now.hour);
        setMinute(now.minute);
        setLocalTimeZone(Intl.DateTimeFormat().resolvedOptions().timeZone || 'Asia/Shanghai');
    }, []);

    const handleStartDivination = async () => {
        const useTime = timeMode === 'now' ? getNow() : { year, month, day, hour, minute };
        if (!useTime.year || !useTime.month || !useTime.day) {
            showToast('error', '请填写完整的日期');
            return;
        }
        setIsLoading(true);
        try {
            const date = `${useTime.year}-${String(useTime.month).padStart(2, '0')}-${String(useTime.day).padStart(2, '0')}`;
            const params = {
                date,
                hour: useTime.hour,
                minute: useTime.minute,
                timezone: localTimeZone,
                question: question.trim() || undefined,
                birthYear: birthYear ? parseInt(birthYear) : undefined,
                gender: gender || undefined,
            };
            writeSessionJSON('daliuren_params', params);
            router.push('/daliuren/result');
        } catch {
            showToast('error', '起课失败，请重试');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <FeatureGate featureId="daliuren">
            <div className="min-h-screen bg-background md:pb-12 text-foreground">
                {/* 页面标题 - 移动端隐藏（顶栏已显示） */}
                <div className="hidden md:block text-center py-8">
                    <h1 className="text-2xl lg:text-3xl font-bold">大六壬</h1>
                    <p className="text-foreground/60 mt-2">三式之一，推演时空吉凶</p>
                </div>

                <div className="max-w-2xl mx-auto px-4 sm:mt-0 mt-8">
                    {/* 占事输入 */}
                    <div className="sm:mt-8 mb-6 text-center">
                        <label className="block text-sm font-medium text-foreground/60 mb-3 uppercase tracking-wider">
                            占事（选填）
                        </label>
                        <input
                            type="text"
                            value={question}
                            onChange={(e) => setQuestion(e.target.value)}
                            placeholder="例如：此事能否顺利？"
                            className="w-full px-6 py-4 bg-background rounded-lg border border-border shadow-sm
                                focus:border-[#2383e2] focus:ring-2 focus:ring-[#2383e2]/10 focus:outline-none
                                text-center text-lg text-foreground placeholder:text-foreground/30
                                transition-all duration-150"
                        />
                    </div>
                    {/* 时间模式 */}
                    <div className="mb-6">
                        <div className="grid grid-cols-2 gap-3">
                            <button
                                onClick={() => setTimeMode('now')}
                                className={`px-4 py-3 rounded-md border text-sm font-semibold transition-all duration-150 ${
                                    timeMode === 'now'
                                        ? 'border-[#2383e2] bg-[#2383e2] text-white'
                                        : 'border-border bg-background text-foreground hover:bg-background-secondary'
                                }`}
                            >
                                正时（当前时间）
                            </button>
                            <button
                                onClick={() => setTimeMode('custom')}
                                className={`px-4 py-3 rounded-md border text-sm font-semibold transition-all duration-150 ${
                                    timeMode === 'custom'
                                        ? 'border-[#2383e2] bg-[#2383e2] text-white'
                                        : 'border-border bg-background text-foreground hover:bg-background-secondary'
                                }`}
                            >
                                活时（自选时间）
                            </button>
                        </div>
                    </div>

                    {/* 自选时间 */}
                    {timeMode === 'custom' && (
                        <div className="mb-6 grid grid-cols-5 gap-2 animate-fade-in">
                            {[
                                { label: '年', value: year, onChange: setYear },
                                { label: '月', value: month, onChange: setMonth, min: 1, max: 12 },
                                { label: '日', value: day, onChange: setDay, min: 1, max: 31 },
                                { label: '时', value: hour, onChange: setHour, min: 0, max: 23 },
                                { label: '分', value: minute, onChange: setMinute, min: 0, max: 59 },
                            ].map((item) => (
                                <div key={item.label}>
                                    <label className="block text-xs text-foreground/60 mb-1">{item.label}</label>
                                    <input 
                                        type="number" 
                                        min={item.min} 
                                        max={item.max} 
                                        value={item.value} 
                                        onChange={e => item.onChange(Number(e.target.value))}
                                        className="w-full px-2 py-2 bg-background rounded-md border border-border text-center text-sm text-foreground focus:border-[#2383e2] focus:ring-2 focus:ring-[#2383e2]/10 focus:outline-none transition-all duration-150" 
                                    />
                                </div>
                            ))}
                        </div>
                    )}
                    {/* 本命设置 */}
                    <div className="mb-8">
                        <div className="space-y-4 p-4 rounded-lg border border-border bg-background shadow-sm">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-xs font-bold text-foreground/60 mb-2 uppercase tracking-wider">出生年份</label>
                                    <input
                                        type="number"
                                        value={birthYear}
                                        onChange={e => setBirthYear(e.target.value)}
                                        placeholder="如 1990"
                                        className="w-full px-3 py-2 bg-transparent rounded-md border border-border text-sm text-foreground focus:border-[#2383e2] focus:ring-2 focus:ring-[#2383e2]/10 focus:outline-none transition-all duration-150"
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs font-bold text-foreground/60 mb-2 uppercase tracking-wider">性别</label>
                                    <select
                                        value={gender}
                                        onChange={e => setGender(e.target.value as 'male' | 'female' | '')}
                                        className="w-full px-3 py-2 bg-transparent rounded-md border border-border text-sm text-foreground focus:border-[#2383e2] focus:ring-2 focus:ring-[#2383e2]/10 focus:outline-none transition-all duration-150"
                                    >
                                        <option value="">不填</option>
                                        <option value="male">男</option>
                                        <option value="female">女</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* 起课按钮 */}
                    <div className="text-center mb-12">
                        <button
                            onClick={handleStartDivination}
                            disabled={isLoading}
                            className="inline-flex items-center gap-2 px-8 py-4 bg-[#2383e2] hover:bg-[#2383e2]/90 active:bg-[#1a65b0] text-white rounded-md font-bold text-lg transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
                        >
                            {isLoading ? (
                                <>
                                    <SoundWaveLoader variant="inline" />
                                    <span>起课中...</span>
                                </>
                            ) : '起课'}
                        </button>
                    </div>

                    {/* 说明 */}
                    <div className="bg-background rounded-lg p-5 md:p-8 border border-border shadow-sm mb-8">
                        <h3 className="text-base md:text-lg font-bold text-foreground mb-4 md:mb-6 flex items-center gap-2">
                            <span className="w-1 h-4 md:h-5 bg-[#37352f] rounded-full" />
                            大六壬说明
                        </h3>
                        <div className="grid md:grid-cols-2 gap-6 md:gap-8 text-sm leading-relaxed">
                            <div className="space-y-4">
                                <div>
                                    <h4 className="font-bold text-foreground mb-2 flex items-center gap-2 text-sm">
                                        <span className="w-1.5 h-1.5 rounded-full bg-[#2383e2]" />
                                        什么是大六壬？
                                    </h4>
                                    <p className="text-xs md:text-sm text-foreground/60 pl-3.5 border-l border-border/60">
                                        大六壬是中国古代三式之一，以天地盘、四课三传为核心，
                                        通过时空信息推演事物发展，判断吉凶趋势。
                                    </p>
                                </div>
                                <div>
                                    <h4 className="font-bold text-foreground mb-2 flex items-center gap-2 text-sm">
                                        <span className="w-1.5 h-1.5 rounded-full bg-[#2383e2]" />
                                        正时与活时
                                    </h4>
                                    <p className="text-xs md:text-sm text-foreground/60 pl-3.5 border-l border-border/60">
                                        正时使用当前时间起课，适合即时预测；
                                        活时可自选时间，适合分析特定时刻的格局。
                                    </p>
                                </div>
                            </div>
                            <div className="space-y-4">
                                <div>
                                    <h4 className="font-bold text-foreground mb-2 flex items-center gap-2 text-sm">
                                        <span className="w-1.5 h-1.5 rounded-full bg-[#2383e2]" />
                                        四课三传
                                    </h4>
                                    <p className="text-xs md:text-sm text-foreground/60 pl-3.5 border-l border-border/60">
                                        四课由日干、日支与天地盘组合而成，
                                        三传从四课中取出，代表事物的起因、经过与结果。
                                    </p>
                                </div>
                                <div>
                                    <h4 className="font-bold text-foreground mb-2 flex items-center gap-2 text-sm">
                                        <span className="w-1.5 h-1.5 rounded-full bg-[#2383e2]" />
                                        注意事项
                                    </h4>
                                    <p className="text-xs md:text-sm text-foreground/60 pl-3.5 border-l border-border/60">
                                        起课时心诚则灵，专注于所问之事。
                                        同一问题不宜反复起课，以第一次结果为准。
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <HistoryDrawer type="daliuren" />
            </div>
        </FeatureGate>
    );
}

'use client';

import { useCallback, useEffect, useMemo, useState, type ReactElement } from 'react';
import { CheckCircle2, ChevronLeft, ChevronRight } from 'lucide-react';
import { requestBrowserJson } from '@/lib/browser-api';

interface CheckinCalendarPanelProps {
  active?: boolean;
}

export function CheckinCalendarPanel({ active = true }: CheckinCalendarPanelProps) {
  const [loading, setLoading] = useState(true);
  const [calendarByMonth, setCalendarByMonth] = useState<Record<string, string[]>>({});
  const [calendarError, setCalendarError] = useState<string | null>(null);
  const [currentMonth, setCurrentMonth] = useState(() => {
    const now = new Date();
    return { year: now.getFullYear(), month: now.getMonth() + 1 };
  });
  const monthKey = `${currentMonth.year}-${String(currentMonth.month).padStart(2, '0')}`;
  const calendar = calendarByMonth[monthKey] ?? null;

  const fetchCalendar = useCallback(async () => {
    if (!active) return;

    setLoading(true);
    setCalendarError(null);
    try {
      const result = await requestBrowserJson<{ calendar?: string[] }>(
        `/api/checkin?action=calendar&year=${currentMonth.year}&month=${currentMonth.month}`,
        { method: 'GET' },
      );
      if (result.error) {
        setCalendarError(result.error.message || '获取签到日历失败');
        return;
      }
      if (!Array.isArray(result.data?.calendar)) {
        setCalendarError('获取签到日历失败');
        return;
      }
      const nextCalendar = result.data.calendar;
      setCalendarByMonth((prev) => ({
        ...prev,
        [monthKey]: nextCalendar,
      }));
      setCalendarError(null);
    } catch (error) {
      console.error('获取签到日历失败:', error);
      setCalendarError('获取签到日历失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  }, [active, currentMonth, monthKey]);

  useEffect(() => {
    if (!active) return;
    void fetchCalendar();
  }, [active, fetchCalendar]);

  const prevMonth = useCallback(() => {
    setCurrentMonth((prev) => {
      if (prev.month === 1) {
        return { year: prev.year - 1, month: 12 };
      }
      return { ...prev, month: prev.month - 1 };
    });
  }, []);

  const nextMonth = useCallback(() => {
    setCurrentMonth((prev) => {
      if (prev.month === 12) {
        return { year: prev.year + 1, month: 1 };
      }
      return { ...prev, month: prev.month + 1 };
    });
  }, []);

  const calendarDays = useMemo(() => {
    const { year, month } = currentMonth;
    const firstDay = new Date(year, month - 1, 1).getDay();
    const daysInMonth = new Date(year, month, 0).getDate();
    const today = new Date().toISOString().split('T')[0];
    const days: ReactElement[] = [];

    for (let index = 0; index < firstDay; index += 1) {
      days.push(<div key={`empty-${index}`} className="h-9" />);
    }

    for (let day = 1; day <= daysInMonth; day += 1) {
      const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      const isCheckedIn = calendar?.includes(dateStr) ?? false;
      const isToday = dateStr === today;

      days.push(
        <div
          key={day}
          className={`flex h-9 items-center justify-center rounded-lg text-sm transition-colors ${
            isCheckedIn
              ? 'bg-amber-500 text-white'
              : isToday
                ? 'border border-amber-500/50 bg-amber-500/10 font-semibold text-amber-600'
                : 'bg-[#f7f6f3] text-[#37352f]/55'
          }`}
        >
          {isCheckedIn ? <CheckCircle2 className="h-4 w-4" /> : day}
        </div>,
      );
    }

    return days;
  }, [calendar, currentMonth]);

  const checkedInThisMonth = useMemo(() => {
    const prefix = `${currentMonth.year}-${String(currentMonth.month).padStart(2, '0')}`;
    return (calendar ?? []).filter((date) => date.startsWith(prefix)).length;
  }, [calendar, currentMonth]);

  return (
    <div className="rounded-lg border border-[#ebe8e2] bg-[#fbfaf7] p-4">
      <div className="mb-3 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={prevMonth}
            className="flex h-7 w-7 items-center justify-center rounded-md text-[#37352f]/55 transition-colors duration-150 hover:bg-[#efedea] hover:text-[#37352f]"
            aria-label="查看上个月"
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
          <div className="text-sm font-medium text-[#37352f]">
            {currentMonth.year} 年 {currentMonth.month} 月
          </div>
          <button
            type="button"
            onClick={nextMonth}
            className="flex h-7 w-7 items-center justify-center rounded-md text-[#37352f]/55 transition-colors duration-150 hover:bg-[#efedea] hover:text-[#37352f]"
            aria-label="查看下个月"
          >
            <ChevronRight className="h-4 w-4" />
          </button>
        </div>
        <div className="text-xs text-[#37352f]/50">
          本月 {checkedInThisMonth} 天
        </div>
      </div>

      {calendarError ? (
        <div className="mb-3 flex items-center justify-between gap-3 rounded-lg border border-[#ead9bf] bg-[#fcf8ee] px-3 py-2 text-xs text-[#946c21]">
          <span className="min-w-0 flex-1">{calendarError}</span>
          <button
            type="button"
            onClick={() => {
              setLoading(true);
              void fetchCalendar();
            }}
            className="shrink-0 rounded-md px-2 py-1 font-medium text-[#7c5f1c] transition-colors hover:bg-[#f4ead3]"
          >
            重试
          </button>
        </div>
      ) : null}

      {loading && !calendar ? (
        <div className="space-y-2">
          <div className="grid grid-cols-7 gap-2">
            {Array.from({ length: 7 }).map((_, index) => (
              <div key={index} className="flex h-8 items-center justify-center">
                <div className="h-3 w-4 rounded bg-[#37352f]/10 animate-pulse" />
              </div>
            ))}
          </div>
          <div className="grid grid-cols-7 gap-2">
            {Array.from({ length: 35 }).map((_, index) => (
              <div key={index} className="h-9 rounded-lg bg-[#37352f]/8 animate-pulse" />
            ))}
          </div>
        </div>
      ) : calendar ? (
        <>
          <div className="mb-2 grid grid-cols-7 gap-2">
            {['日', '一', '二', '三', '四', '五', '六'].map((day) => (
              <div key={day} className="flex h-8 items-center justify-center text-xs text-[#37352f]/40">
                {day}
              </div>
            ))}
          </div>

          <div className="grid grid-cols-7 gap-2">
            {calendarDays}
          </div>
        </>
      ) : null}
    </div>
  );
}

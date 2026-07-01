/**
 * 签到弹窗组件
 */
'use client';

import { useState, useEffect, useCallback } from 'react';
import { CalendarCheck, X } from 'lucide-react';
import { CheckinCalendarPanel } from '@/components/checkin/CheckinCalendarPanel';
import {
  fetchCheckinStatus,
  type CheckinStatus,
} from '@/components/checkin/checkin-client';

interface CheckinModalProps {
  isOpen: boolean;
  onClose: () => void;
  stackLevel?: 'page' | 'settings';
}

export function CheckinModal({
  isOpen,
  onClose,
  stackLevel = 'page',
}: CheckinModalProps) {
  const [loading, setLoading] = useState(true);
  const [status, setStatus] = useState<CheckinStatus | null>(null);
  const [statusError, setStatusError] = useState<string | null>(null);

  const loadStatus = useCallback(async () => {
    setStatusError(null);
    try {
      const nextStatus = await fetchCheckinStatus();
      if (nextStatus.ok) {
        setStatus(nextStatus.status);
        setStatusError(null);
        return;
      }

      console.error('获取签到状态失败:', nextStatus.error);
      setStatusError(nextStatus.error.message || '获取签到状态失败');
    } catch (error) {
      console.error('获取签到状态失败:', error);
      setStatusError('获取签到状态失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!isOpen) return;
    setLoading(true);
    void loadStatus();
  }, [isOpen, loadStatus]);

  useEffect(() => {
    const handleEsc = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const rewardRangeText = status ? `${status.rewardRange[0]}-${status.rewardRange[1]} 积分` : '--';
  const modalLayerClass = stackLevel === 'settings' ? 'z-[100]' : 'z-[60]';
  const statusText = status?.todayCheckedIn
    ? '今天已签到'
    : status?.blockedReason === 'credit_cap_reached'
      ? '当前已封顶'
      : `今日奖励 ${rewardRangeText}`;

  return (
    <div className={`fixed inset-0 flex items-center justify-center p-4 ${modalLayerClass}`}>
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      <div className="relative w-full max-w-md overflow-hidden rounded-2xl border border-border bg-background shadow-xl animate-fade-in">
        <div className="flex items-center justify-between border-b border-border px-5 py-4">
          <h2 className="flex items-center gap-2 text-base font-semibold text-foreground">
            <CalendarCheck className="h-4 w-4 text-amber-500" />
            每日签到
          </h2>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-1.5 transition-colors hover:bg-background-secondary"
            aria-label="关闭"
          >
            <X className="h-4 w-4 text-foreground-secondary" />
          </button>
        </div>

        <div className="space-y-4 px-5 py-5">
          {loading ? (
            <>
              <div className="h-11 rounded-lg bg-foreground/5 animate-pulse" />
              <div className="h-64 rounded-lg bg-foreground/5 animate-pulse" />
            </>
          ) : (
            <>
              {statusError ? (
                <div className="flex items-center justify-between gap-3 rounded-lg border border-[#ead9bf] bg-[#fcf8ee] px-4 py-3 text-sm text-[#946c21]">
                  <span className="min-w-0 flex-1">{statusError}</span>
                  <button
                    type="button"
                    onClick={() => {
                      setLoading(true);
                      void loadStatus();
                    }}
                    className="shrink-0 rounded-md px-2 py-1 font-medium text-[#7c5f1c] transition-colors hover:bg-[#f4ead3]"
                  >
                    重试
                  </button>
                </div>
              ) : null}

              {status ? (
                <div className="rounded-lg border border-[#ebe8e2] bg-[#fbfaf7] px-4 py-3 text-sm text-[#37352f]/65">
                  {statusText}
                </div>
              ) : null}

              <CheckinCalendarPanel active={isOpen} />
            </>
          )}
        </div>
      </div>
    </div>
  );
}

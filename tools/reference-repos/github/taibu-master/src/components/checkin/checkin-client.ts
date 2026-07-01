'use client';

import { requestBrowserJson, type BrowserApiError } from '@/lib/browser-api';

export interface CheckinStatus {
  canCheckin: boolean;
  lastCheckin: string | null;
  todayCheckedIn: boolean;
  rewardRange: [number, number];
  currentCredits: number;
  creditLimit: number;
  blockedReason: 'already_checked_in' | 'credit_cap_reached' | null;
}

export interface CheckinActionResult {
  ok: boolean;
  rewardCredits: number;
  credits?: number;
  creditLimit?: number;
  blockedReason?: 'already_checked_in' | 'credit_cap_reached';
  message?: string;
}

export type CheckinStatusResult =
  | { ok: true; status: CheckinStatus }
  | { ok: false; error: BrowserApiError };

const DEFAULT_CHECKIN_STATUS_ERROR = '获取签到状态失败';

export async function fetchCheckinStatus(): Promise<CheckinStatusResult> {
  const result = await requestBrowserJson<{ status?: CheckinStatus }>('/api/checkin?action=status', {
    method: 'GET',
  });

  if (result.error) {
    return {
      ok: false,
      error: result.error,
    };
  }

  if (!result.data?.status) {
    return {
      ok: false,
      error: { message: DEFAULT_CHECKIN_STATUS_ERROR },
    };
  }

  return {
    ok: true,
    status: result.data.status,
  };
}

export async function performCheckinAction(): Promise<CheckinActionResult> {
  const result = await requestBrowserJson<{
    result?: {
      rewardCredits: number;
      credits?: number;
      creditLimit?: number;
      blockedReason?: 'already_checked_in' | 'credit_cap_reached';
    };
  }>('/api/checkin', {
    method: 'POST',
  });

  const checkinResult = result.data?.result;

  if (result.error) {
    if (checkinResult?.blockedReason) {
      return {
        ok: false,
        rewardCredits: checkinResult.rewardCredits ?? 0,
        credits: checkinResult.credits,
        creditLimit: checkinResult.creditLimit,
        blockedReason: checkinResult.blockedReason,
        message: result.error.message || '签到失败',
      };
    }

    throw new Error(result.error.message || '签到失败');
  }

  if (!checkinResult) {
    throw new Error('签到失败');
  }

  return {
    ok: true,
    rewardCredits: checkinResult.rewardCredits,
    credits: checkinResult.credits,
    creditLimit: checkinResult.creditLimit,
  };
}

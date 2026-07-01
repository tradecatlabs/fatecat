/**
 * 积分进度条组件
 */
'use client';

import { BotMessageSquare } from 'lucide-react';
import type { MembershipType } from '@/lib/user/membership';
import { getPlanConfig } from '@/lib/user/membership';

interface CreditProgressBarProps {
    credits: number;
    membershipType: MembershipType;
}

export function CreditProgressBar({
  credits,
  membershipType,
}: CreditProgressBarProps) {
  const plan = getPlanConfig(membershipType);
  const limit = plan.creditLimit;
  const scaleMax = Math.max(credits, limit, 1);
  const fillPercentage = Math.min((credits / scaleMax) * 100, 100);
  const limitMarkerPercentage = Math.min((limit / scaleMax) * 100, 100);

  return (
    <section className="overflow-hidden rounded-lg border border-[#ebe8e2] bg-[#f7f6f3]">
      <div className="flex items-center justify-between gap-4 border-b border-[#ebe8e2] px-4 py-3">
        <div className="min-w-0">
          <div className="flex items-center gap-2 text-sm font-medium text-[#37352f]">
            <BotMessageSquare className="h-4 w-4 text-[#37352f]/45" />
            <span>当前积分</span>
          </div>
        </div>
        <div className="text-right">
          <div className="text-xl font-semibold tracking-tight text-[#37352f]">{credits}/{limit}</div>
        </div>
      </div>

      <div className="px-4 py-4">
        <div className="relative h-2 overflow-visible rounded-full bg-[#e6ede8]">
          <div
            className="h-full rounded-full bg-[#1f9d6d] transition-[width] duration-150"
            style={{ width: `${fillPercentage}%` }}
          />
          <div
            className="absolute top-1/2 -translate-y-1/2"
            style={{ left: `clamp(0%, calc(${limitMarkerPercentage}% - 5px), calc(100% - 10px))` }}
          >
            <span className="block h-2.5 w-2.5 rounded-full border border-[#1f9d6d] bg-[#f7f6f3]" />
          </div>
        </div>
      </div>
    </section>
  );
}

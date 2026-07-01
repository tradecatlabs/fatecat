'use client';

import { useCallback, useEffect, useState } from 'react';
import { useSessionSafe } from '@/components/providers/ClientProviders';
import { supabase } from '@/lib/auth';
import { requestBrowserJson } from '@/lib/browser-api';

type CreditTransaction = {
  id: string;
  amount: number;
  type: 'earn' | 'spend' | 'refund';
  source: string;
  description: string | null;
  balance_after: number | null;
  created_at: string;
};

const SOURCE_LABELS: Record<string, string> = {
  activation_key: '激活码',
  checkin: '每日签到',
  ai_usage: 'AI 消费',
  ai_refund: 'AI 退款',
};

interface CreditTransactionsPanelProps {
  pageSize?: number;
  refreshKey?: number;
}

export function CreditTransactionsPanel({ pageSize = 5, refreshKey = 0 }: CreditTransactionsPanelProps) {
  const { user, loading: sessionLoading } = useSessionSafe();
  const [transactions, setTransactions] = useState<CreditTransaction[]>([]);
  const [todaySpent, setTodaySpent] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [visibleCount, setVisibleCount] = useState(pageSize);
  const [hasMore, setHasMore] = useState(false);

  const fetchTransactions = useCallback(async (nextVisibleCount: number) => {
    if (!user) {
      setTransactions([]);
      setTodaySpent(0);
      setError(null);
      setHasMore(false);
      setLoading(false);
      return;
    }

    setLoading(true);
    try {
      const loadTransactions = async () => {
        return await requestBrowserJson<{
          items?: CreditTransaction[];
          summary?: {
            todaySpent?: number;
          };
        }>(`/api/credits/transactions?limit=${nextVisibleCount + 1}`, {
          method: 'GET',
        });
      };

      let result = await loadTransactions();
      if (result.error) {
        if (result.status === 401) {
          const { data: { session } } = await supabase.auth.revalidateSession();
          if (session) {
            result = await loadTransactions();
          }
        }

        if (result.error && result.status === 401) {
          setTransactions([]);
          setTodaySpent(0);
          setError(null);
          setHasMore(false);
          return;
        }

        if (result.error) {
          throw new Error(result.error.message || '获取积分流水失败');
        }
      }

      const rows = Array.isArray(result.data?.items) ? result.data.items : [];
      setError(null);
      setTransactions(rows.slice(0, nextVisibleCount));
      setTodaySpent(typeof result.data?.summary?.todaySpent === 'number' ? result.data.summary.todaySpent : 0);
      setHasMore(rows.length > nextVisibleCount);
    } catch (error) {
      console.error('获取积分流水异常:', error);
      setTransactions([]);
      setTodaySpent(0);
      setError(error instanceof Error ? error.message : '获取积分流水失败');
      setHasMore(false);
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    if (sessionLoading) return;
    void fetchTransactions(visibleCount);
  }, [fetchTransactions, refreshKey, sessionLoading, visibleCount]);

  const formatDate = (dateStr: string) => new Date(dateStr).toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });

  const getAmountColor = (item: CreditTransaction) => {
    if (item.type === 'refund') return 'text-[#1f9d6d]';
    return item.amount < 0 ? 'text-[#b42318]' : 'text-[#a16207]';
  };

  const getAmountText = (item: CreditTransaction) => (item.amount > 0 ? `+${item.amount}` : String(item.amount));

  if (!sessionLoading && !user) {
    return null;
  }

  return (
    <section className="overflow-hidden rounded-lg border border-[#ebe8e2] bg-[#f7f6f3]">
      <div className="border-b border-[#ebe8e2] px-4 py-3">
        <div className="flex items-center justify-between gap-4">
          <h2 className="text-sm font-medium text-[#37352f]">积分记录</h2>
          <div className="text-xs text-[#37352f]/48">今日消耗 {todaySpent}</div>
        </div>
      </div>

      {loading ? (
        <div>
          {Array.from({ length: Math.min(pageSize, 5) }).map((_, index) => (
            <div
              key={index}
              className={`h-16 bg-[#37352f]/5 animate-pulse ${index > 0 ? 'border-t border-[#ebe8e2]' : ''}`}
            />
          ))}
        </div>
      ) : error ? (
        <div className="px-4 py-8 text-sm text-[#b42318]">
          {error}
        </div>
      ) : transactions.length > 0 ? (
        <>
          <div>
            {transactions.map((item, index) => (
              <article
                key={item.id}
                className={`px-4 py-3 transition-colors duration-150 hover:bg-[#efedea] ${index > 0 ? 'border-t border-[#ebe8e2]' : ''}`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-x-2 gap-y-1 text-sm">
                      <span className="truncate font-medium text-[#37352f]">
                        {item.description || SOURCE_LABELS[item.source] || item.source}
                      </span>
                      <span className="text-xs text-[#37352f]/48">
                        {formatDate(item.created_at)}
                      </span>
                    </div>
                  </div>
                  <div className={`text-sm font-semibold ${getAmountColor(item)}`}>
                    {getAmountText(item)}
                  </div>
                </div>
              </article>
            ))}
          </div>

          {hasMore ? (
            <div className="border-t border-[#ebe8e2] px-4 py-3">
              <button
                type="button"
                onClick={() => setVisibleCount((count) => count + pageSize)}
                className="text-sm font-medium text-[#37352f]/68 transition-colors duration-150 hover:text-[#37352f]"
              >
                查看更多
              </button>
            </div>
          ) : null}
        </>
      ) : (
        <div className="px-4 py-8 text-sm text-[#37352f]/55">
          暂无积分记录。
        </div>
      )}
    </section>
  );
}

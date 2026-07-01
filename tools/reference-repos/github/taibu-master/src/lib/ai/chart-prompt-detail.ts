import 'server-only';

import type { SupabaseClient } from '@supabase/supabase-js';
import { getSystemAdminClient } from '@/lib/api-utils';
import {
  resolveChartTextDetailLevel,
  type ChartTextDetailLevel,
  type ChartTextDetailTool,
} from '@/lib/divination/detail-level';

type ChartPromptDetailClient = Pick<SupabaseClient, 'from'>;

export async function loadResolvedChartPromptDetailLevel(
  userId: string,
  tool: ChartTextDetailTool,
  options?: { client?: ChartPromptDetailClient },
): Promise<ChartTextDetailLevel> {
  try {
    const client = options?.client ?? getSystemAdminClient();
    const { data } = await client
      .from('user_settings')
      .select('chart_prompt_detail_level')
      .eq('user_id', userId)
      .maybeSingle();
    const saved = data?.chart_prompt_detail_level === 'full'
      ? 'full'
      : data?.chart_prompt_detail_level === 'more'
        ? 'more'
        : 'default';
    return resolveChartTextDetailLevel(tool, saved);
  } catch {
    return resolveChartTextDetailLevel(tool, 'default');
  }
}

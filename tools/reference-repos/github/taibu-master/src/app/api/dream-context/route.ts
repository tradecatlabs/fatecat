/**
 * 解梦上下文 API
 * 
 * 提供解梦模式所需的八字命盘和今日运势上下文数据
 */

import { NextRequest } from 'next/server';
import { jsonError, jsonOk, requireUserContext } from '@/lib/api-utils';
import { buildDreamContextPayload } from '@/lib/chat/chat-context';

export async function GET(request: NextRequest) {
    const auth = await requireUserContext(request);
    if ('error' in auth) {
        return jsonError(auth.error.message, auth.error.status);
    }

    const userId = auth.user.id;
    const { payload, context } = await buildDreamContextPayload(userId);
    return jsonOk({ dreamContext: context, payload });
}

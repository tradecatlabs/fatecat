import type { NextResponse } from 'next/server';

import type { FeatureModuleId } from '@/lib/app-settings';
import { isFeatureModuleEnabled } from '@/lib/app-settings';
import { jsonError } from '@/lib/api-utils';

export async function ensureFeatureRouteEnabled(
    featureId: FeatureModuleId,
    message = '功能暂未开放',
    status = 403
): Promise<NextResponse | null> {
    return (await isFeatureModuleEnabled(featureId))
        ? null
        : jsonError(message, status);
}

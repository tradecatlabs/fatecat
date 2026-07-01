import { fetchBrowserJson } from '@/lib/browser-api';
import {
    type PlaceResolution,
    normalizePlaceQuery,
} from '@/lib/divination/place-resolution';

export async function resolvePlaceWithAmap(place: string): Promise<{
    resolution: PlaceResolution;
    errorMessage?: string;
}> {
    const query = normalizePlaceQuery(place);
    const fallback: PlaceResolution = {
        resolved: false,
        provider: 'amap',
        query,
        reason: 'not_found',
    };

    if (!query) {
        return { resolution: fallback };
    }

    const { ok, result } = await fetchBrowserJson<PlaceResolution>('/api/amap/geocode', {
        method: 'POST',
        body: JSON.stringify({ place }),
    });

    if (!ok || result.error || !result.data) {
        return {
            resolution: fallback,
            errorMessage: result.error?.message || '出生地点解析失败',
        };
    }

    return { resolution: result.data };
}

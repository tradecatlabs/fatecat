import { type NextRequest } from 'next/server';
import { jsonError, jsonOk } from '@/lib/api-utils';
import { geocodePlaceWithAmap } from '@/lib/server/amap-geocode';

export async function POST(request: NextRequest) {
    let body: { place?: unknown };
    try {
        body = await request.json() as { place?: unknown };
    } catch {
        return jsonError('请求体不是合法 JSON', 400);
    }

    if (typeof body.place !== 'string' || !body.place.trim()) {
        return jsonError('place 不能为空', 400);
    }

    if (body.place.trim().length > 120) {
        return jsonError('place 过长', 400);
    }

    try {
        const resolution = await geocodePlaceWithAmap(body.place);
        return jsonOk(resolution);
    } catch (error) {
        console.error('[amap-geocode] failed:', error);
        return jsonError('出生地点解析失败', 502);
    }
}

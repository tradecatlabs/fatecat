import { normalizeYongShenTargets, type LiuQin } from './liuyao';
import type { LiuyaoCanonicalJSON } from 'taibu-core/liuyao';

export type ResultYongShenState = {
    appliedTargets: LiuQin[];
    pendingTargets: LiuQin[];
};

const YAO_POSITION_MARKERS = [
    ['初', 1],
    ['二', 2],
    ['三', 3],
    ['四', 4],
    ['五', 5],
    ['上', 6],
] as const;

function normalizeTraditionalYaoPositionLabel(position?: string): string | null {
    if (typeof position !== 'string') return null;
    const normalized = position.trim().replace(/爻$/u, '');
    return normalized || null;
}

function parseTraditionalYaoPosition(position?: string): number | null {
    const normalized = normalizeTraditionalYaoPositionLabel(position);
    if (!normalized) return null;

    for (const [marker, value] of YAO_POSITION_MARKERS) {
        if (normalized.includes(marker)) return value;
    }

    return null;
}

export function resolveResultYongShenTargets(
    resultTargets?: readonly unknown[],
    pendingTargets?: readonly unknown[],
    questionSessionTargets?: readonly unknown[],
): LiuQin[] {
    const normalizedResultTargets = normalizeYongShenTargets(resultTargets);
    if (normalizedResultTargets.length > 0) {
        return normalizedResultTargets;
    }

    const normalizedPendingTargets = normalizeYongShenTargets(pendingTargets);
    if (normalizedPendingTargets.length > 0) {
        return normalizedPendingTargets;
    }

    return normalizeYongShenTargets(questionSessionTargets);
}

export function resolveResultYongShenState(
    resultTargets?: readonly unknown[],
    pendingTargets?: readonly unknown[],
    questionSessionTargets?: readonly unknown[],
): ResultYongShenState {
    const normResult = normalizeYongShenTargets(resultTargets);
    const normPending = normalizeYongShenTargets(pendingTargets);
    const normSession = normalizeYongShenTargets(questionSessionTargets);

    // appliedTargets: result > questionSession (pending is draft-only, not auto-applied)
    const appliedTargets = normResult.length > 0 ? normResult : normSession;

    return {
        appliedTargets,
        pendingTargets: normPending,
    };
}

export function resolveTraditionalYongShenPositions(
    analysis?: Pick<LiuyaoCanonicalJSON, '六爻' | '用神分析'> | null,
): number[] {
    if (!analysis) return [];

    const positions = new Set<number>();

    for (const group of analysis.用神分析) {
        const normalizedPosition = normalizeTraditionalYaoPositionLabel(group.已选用神.爻位);
        if (!normalizedPosition) continue;

        const visibleYao = analysis.六爻.find((yao) => normalizeTraditionalYaoPositionLabel(yao.爻位) === normalizedPosition);
        if (!visibleYao || visibleYao.六亲 !== group.已选用神.六亲) continue;

        const numericPosition = parseTraditionalYaoPosition(normalizedPosition);
        if (numericPosition) positions.add(numericPosition);
    }

    return [...positions];
}

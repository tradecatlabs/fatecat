export interface ScrollMetrics {
    scrollHeight: number;
    scrollTop: number;
    clientHeight: number;
}

export const DEFAULT_NEAR_BOTTOM_THRESHOLD_PX = 96;

export function distanceFromBottom({ scrollHeight, scrollTop, clientHeight }: ScrollMetrics): number {
    return Math.max(scrollHeight - scrollTop - clientHeight, 0);
}

export function isNearBottom(
    metrics: ScrollMetrics,
    thresholdPx = DEFAULT_NEAR_BOTTOM_THRESHOLD_PX
): boolean {
    return distanceFromBottom(metrics) <= thresholdPx;
}

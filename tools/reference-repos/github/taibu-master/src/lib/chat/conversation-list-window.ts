import { CONVERSATION_PAGE_SIZE } from '@/lib/chat/conversation';

function normalizePositiveInteger(value: number | null | undefined): number {
  if (typeof value !== 'number' || !Number.isFinite(value) || value <= 0) {
    return 0;
  }

  return Math.ceil(value);
}

export function normalizeConversationWindowTargetCount({
  loadedCount,
  requestedCount,
  fallbackCount = CONVERSATION_PAGE_SIZE,
}: {
  loadedCount: number;
  requestedCount?: number | null;
  fallbackCount?: number;
}): number {
  const normalizedLoadedCount = normalizePositiveInteger(loadedCount);
  const normalizedRequestedCount = normalizePositiveInteger(requestedCount);

  if (normalizedRequestedCount > 0) {
    return Math.max(normalizedLoadedCount, normalizedRequestedCount);
  }

  return Math.max(
    normalizedLoadedCount,
    normalizePositiveInteger(fallbackCount),
  );
}

export function resolveConversationRemainingTargetCount({
  loadedCount,
  availableHeight,
  contentHeight,
  rowHeights,
  minimumCount = 0,
}: {
  loadedCount: number;
  availableHeight: number;
  contentHeight: number;
  rowHeights: number[];
  minimumCount?: number;
}): number {
  const normalizedLoadedCount = normalizePositiveInteger(loadedCount);
  const normalizedMinimumCount = normalizePositiveInteger(minimumCount);
  const baseTargetCount = Math.max(normalizedLoadedCount, normalizedMinimumCount);
  const normalizedAvailableHeight = normalizePositiveInteger(availableHeight);
  const normalizedContentHeight = normalizePositiveInteger(contentHeight);
  const validRowHeights = rowHeights
    .map((height) => normalizePositiveInteger(height))
    .filter((height) => height > 0);

  if (
    normalizedAvailableHeight <= normalizedContentHeight
    || validRowHeights.length === 0
  ) {
    return baseTargetCount;
  }

  const averageRowHeight = validRowHeights.reduce((sum, height) => sum + height, 0) / validRowHeights.length;
  const remainingHeight = normalizedAvailableHeight - normalizedContentHeight;
  const additionalCount = Math.ceil(remainingHeight / averageRowHeight);

  return baseTargetCount + Math.max(additionalCount, 0);
}

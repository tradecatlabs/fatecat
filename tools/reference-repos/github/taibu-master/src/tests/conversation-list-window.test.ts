import test from 'node:test';
import assert from 'node:assert/strict';
import {
  normalizeConversationWindowTargetCount,
  resolveConversationRemainingTargetCount,
} from '../lib/chat/conversation-list-window';

test('normalizeConversationWindowTargetCount keeps the larger loaded or requested window', () => {
  assert.equal(normalizeConversationWindowTargetCount({
    loadedCount: 7,
    requestedCount: 21,
  }), 21);

  assert.equal(normalizeConversationWindowTargetCount({
    loadedCount: 14,
    requestedCount: 7,
  }), 14);

  assert.equal(normalizeConversationWindowTargetCount({
    loadedCount: 0,
    requestedCount: 0,
  }), 7);
});

test('resolveConversationRemainingTargetCount uses real remaining height to top up the sidebar list', () => {
  assert.equal(resolveConversationRemainingTargetCount({
    loadedCount: 7,
    availableHeight: 520,
    contentHeight: 404,
    rowHeights: Array.from({ length: 7 }, () => 40),
  }), 10);

  assert.equal(resolveConversationRemainingTargetCount({
    loadedCount: 0,
    availableHeight: 156,
    contentHeight: 0,
    rowHeights: [36],
  }), 5);

  assert.equal(resolveConversationRemainingTargetCount({
    loadedCount: 10,
    availableHeight: 520,
    contentHeight: 520,
    rowHeights: Array.from({ length: 10 }, () => 40),
  }), 10);
});

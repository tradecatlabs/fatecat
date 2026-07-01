import test from 'node:test';
import assert from 'node:assert/strict';
import {
  buildBaziCustomPromptPatch,
  buildZiweiCustomPromptPatch,
  shouldShowPromptShareButton,
} from '../src/lib/prompt-page-rules';

test('桌面端不显示提示词分享按钮，移动端且支持分享时显示', () => {
  assert.equal(
    shouldShowPromptShareButton({ viewportWidth: 1280, hasNavigatorShare: true }),
    false,
  );
  assert.equal(shouldShowPromptShareButton({ viewportWidth: 390, hasNavigatorShare: true }), true);
  assert.equal(
    shouldShowPromptShareButton({ viewportWidth: 390, hasNavigatorShare: false }),
    false,
  );
});

test('八字切换到自定义时会清空已有快捷问题', () => {
  assert.deepEqual(buildBaziCustomPromptPatch(), {
    baziShortcutMode: '自定义',
    baziPresetId: 'ai-mingge-zonglun',
    baziQuickQuestion: '',
  });
});

test('紫微切换到自定义时会清空已有快捷问题', () => {
  assert.deepEqual(buildZiweiCustomPromptPatch(), {
    ziweiShortcutMode: '自定义',
    ziweiTopic: 'chat',
    ziweiQuickQuestion: '',
  });
});

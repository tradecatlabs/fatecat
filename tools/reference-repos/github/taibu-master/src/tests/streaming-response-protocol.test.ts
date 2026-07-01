import test from 'node:test';
import assert from 'node:assert/strict';

import { parseStreamingSSEData } from '@/lib/hooks/useStreamingResponse';

test('streaming response parser should extract terminal error frames', () => {
    const parsed = parseStreamingSSEData('{"error":"保存结果失败，请稍后重试"}');

    assert.equal(parsed.error, '保存结果失败，请稍后重试');
    assert.equal(parsed.contentDelta, undefined);
    assert.equal(parsed.reasoningDelta, undefined);
    assert.equal(parsed.done, false);
});

test('streaming response parser should extract AI SDK errorText frames', () => {
    const parsed = parseStreamingSSEData('{"type":"error","errorText":"积分不足，请先通过签到、激活码或会员权益获取积分"}');

    assert.equal(parsed.error, '积分不足，请先通过签到、激活码或会员权益获取积分');
    assert.equal(parsed.contentDelta, undefined);
    assert.equal(parsed.reasoningDelta, undefined);
    assert.equal(parsed.done, false);
});

test('streaming response parser should ignore AI SDK message metadata frames', () => {
    const parsed = parseStreamingSSEData('{"type":"message-metadata","messageMetadata":{"modelId":"deepseek-v3.2"}}');

    assert.equal(parsed.error, undefined);
    assert.equal(parsed.contentDelta, undefined);
    assert.equal(parsed.reasoningDelta, undefined);
    assert.equal(parsed.done, false);
});

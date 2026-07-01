import { test } from 'node:test';
import assert from 'node:assert/strict';

process.env.MINGAI_FALLBACK_MODELS_JSON = JSON.stringify([
    {
        id: 'deepseek-v3.2',
        name: 'DeepSeek V3.2',
        vendor: 'deepseek',
        usageType: 'chat',
        supportsReasoning: false,
    },
]);

test('resolveModelAccessAsync returns default model and disables reasoning', async () => {
    const { resolveModelAccessAsync } = await import('../lib/ai/ai-access');
    const fallbackModelId = 'deepseek-v3.2';

    const result = await resolveModelAccessAsync(undefined, fallbackModelId, 'free', true);

    assert.equal('error' in result, false);
    if ('error' in result) return;
    assert.equal(result.modelId, fallbackModelId);
    assert.equal(result.reasoningEnabled, false);
});

test('resolveModelAccessAsync rejects non-vision model when vision required', async () => {
    const { resolveModelAccessAsync } = await import('../lib/ai/ai-access');
    const fallbackModelId = 'deepseek-v3.2';

    const result = await resolveModelAccessAsync(undefined, fallbackModelId, 'plus', false, { requireVision: true });

    assert.equal('error' in result, true);
    if (!('error' in result)) return;
    assert.equal(result.status, 400);
});

test('resolveModelAccessAsync returns model unavailable for invalid id', async () => {
    const { resolveModelAccessAsync } = await import('../lib/ai/ai-access');
    const fallbackModelId = 'deepseek-v3.2';

    const result = await resolveModelAccessAsync('invalid-model', fallbackModelId, 'plus');

    assert.equal('error' in result, true);
    if (!('error' in result)) return;
    assert.equal(result.error, '模型不可用');
});

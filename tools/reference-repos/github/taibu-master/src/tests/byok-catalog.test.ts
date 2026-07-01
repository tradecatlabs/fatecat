import { test } from 'node:test';
import assert from 'node:assert/strict';

import { buildByokProviderOptions, getByokProviderLabel } from '../lib/ai/byok-catalog';

test('BYOK catalog should merge Google into one supplier entry and only keep one flagship model per provider', () => {
  const providers = buildByokProviderOptions([
    { id: 'gpt-5.4', name: 'ChatGPT 5.4', vendor: 'openai' },
    { id: 'gemini-3.1-pro-preview', name: 'Gemini 3 Pro', vendor: 'google' },
    { id: 'gemini-2.5-pro', name: 'Gemini 2.5 Pro', vendor: 'gemini' },
    { id: 'grok-4.20', name: 'Grok 4.20', vendor: 'xai' },
  ]);

  const openai = providers.find((provider) => provider.key === 'openai');
  const gemini = providers.find((provider) => provider.key === 'gemini');
  const google = providers.find((provider) => provider.key === 'google');
  const xai = providers.find((provider) => provider.key === 'xai');
  const other = providers.at(-1);

  assert.ok(openai);
  assert.equal(openai?.defaultApiUrl, 'https://api.openai.com/v1');
  assert.deepEqual(openai?.models, [{ id: 'gpt-5.4', name: 'ChatGPT 5.4' }]);

  assert.ok(gemini);
  assert.equal(gemini?.label, 'Google');
  assert.deepEqual(gemini?.models, [{ id: 'gemini-3.1-pro-preview', name: 'Gemini 3 Pro' }]);
  assert.equal(google, undefined);

  assert.ok(xai);
  assert.deepEqual(xai?.models, [{ id: 'grok-4.20', name: 'Grok 4.20' }]);

  assert.equal(other?.key, 'other');
  assert.equal(other?.label, '其他');
});

test('BYOK catalog should fall back to curated flagship models when no mapped models exist', () => {
  const providers = buildByokProviderOptions([]);
  const glm = providers.find((provider) => provider.key === 'glm');
  const qwen = providers.find((provider) => provider.key === 'qwen');
  const moonshot = providers.find((provider) => provider.key === 'moonshot');
  const xai = providers.find((provider) => provider.key === 'xai');

  assert.ok(glm);
  assert.deepEqual(glm?.models, [{ id: 'glm-5.1', name: 'GLM-5.1' }]);
  assert.ok(qwen);
  assert.deepEqual(qwen?.models, [{ id: 'qwen3-max', name: 'Qwen3-Max' }]);
  assert.ok(moonshot);
  assert.equal(moonshot?.label, 'Kimi');
  assert.deepEqual(moonshot?.models, [{ id: 'kimi-k2.5', name: 'Kimi K2.5' }]);
  assert.ok(xai);
  assert.deepEqual(xai?.models, [{ id: 'grok-4.20', name: 'Grok 4.20' }]);
});

test('BYOK labels should normalize Gemini-family providers to Google and keep custom labels', () => {
  assert.equal(getByokProviderLabel('google'), 'Google');
  assert.equal(getByokProviderLabel('gemini'), 'Google');
  assert.equal(getByokProviderLabel('google', 'Google'), 'Google');
  assert.equal(getByokProviderLabel('gemini', 'Gemini'), 'Google');
  assert.equal(getByokProviderLabel('moonshot'), 'Kimi');
  assert.equal(getByokProviderLabel('moonshot', 'Moonshot'), 'Kimi');
  assert.equal(getByokProviderLabel('moonshot', 'Kimi'), 'Kimi');
});

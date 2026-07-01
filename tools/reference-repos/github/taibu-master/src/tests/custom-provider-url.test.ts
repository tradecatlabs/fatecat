import { test } from 'node:test';
import assert from 'node:assert/strict';

import {
  buildCustomProviderChatCompletionsUrl,
  normalizeCustomProviderBaseUrl,
  validateCustomProviderInput,
} from '../lib/ai/custom-provider-url';

test('custom provider input validation accepts normalized https endpoints', () => {
  const errors = validateCustomProviderInput({
    apiUrl: 'https://gateway.example.com/chat/completions',
    apiKey: 'sk-test',
    modelId: 'gpt-4.1-mini',
  });

  assert.deepEqual(errors, {});
  assert.equal(
    normalizeCustomProviderBaseUrl('https://gateway.example.com/chat/completions'),
    'https://gateway.example.com/v1',
  );
  assert.equal(
    normalizeCustomProviderBaseUrl('https://gateway.example.com/openai/chat/completions'),
    'https://gateway.example.com/openai/v1',
  );
  assert.equal(
    buildCustomProviderChatCompletionsUrl('https://gateway.example.com/openai/chat/completions'),
    'https://gateway.example.com/openai/v1/chat/completions',
  );
});

test('custom provider input validation rejects malformed or overlong fields', () => {
  const errors = validateCustomProviderInput({
    apiUrl: 'https://',
    apiKey: 'k'.repeat(513),
    modelId: 'm'.repeat(129),
  });

  assert.equal(errors.apiUrl, 'API URL 格式无效');
  assert.equal(errors.apiKey, 'API Key 过长');
  assert.equal(errors.modelId, 'Model ID 过长');
});

test('custom provider input validation rejects query strings and fragments', () => {
  const queryErrors = validateCustomProviderInput({
    apiUrl: 'https://gateway.example.com/v1?foo=1',
    apiKey: 'sk-test',
    modelId: 'gpt-4.1-mini',
  });
  const hashErrors = validateCustomProviderInput({
    apiUrl: 'https://gateway.example.com/v1#frag',
    apiKey: 'sk-test',
    modelId: 'gpt-4.1-mini',
  });

  assert.equal(queryErrors.apiUrl, 'API URL 不应包含查询参数或片段');
  assert.equal(hashErrors.apiUrl, 'API URL 不应包含查询参数或片段');
});

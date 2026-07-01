import { test } from 'node:test';
import assert from 'node:assert/strict';
import { liuyaoProvider } from '../lib/data-sources/liuyao';

test('liuyao provider keeps raw context but skips formal analysis for questionless records', async () => {
    const content = await liuyaoProvider.formatForAI({
        id: 'rec-1',
        user_id: 'user-1',
        question: '',
        hexagram_code: '111111',
        changed_hexagram_code: null,
        changed_lines: [],
        yongshen_targets: null,
        created_at: '2026-02-10T00:00:00.000Z',
        conversation_id: null,
    });

    assert.equal(content.includes('- 起卦时间：'), true);
    assert.equal(content.includes('- 旬空（年/月/日/时）：'), true);
    assert.equal(content.includes('仅可作为原始卦象记录，不应正式断卦'), true);
    assert.equal(content.includes('- 完整分析数据：'), false);
});

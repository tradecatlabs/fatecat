import test from 'node:test';
import assert from 'node:assert/strict';

test('palmProvider formatForAI should reuse user-visible labels and conversation analysis text', async () => {
    const { palmProvider } = await import('../lib/data-sources/palm');

    const text = await palmProvider.formatForAI({
        id: 'palm-1',
        user_id: 'user-1',
        analysis_type: 'fateline',
        hand_type: 'left',
        created_at: new Date().toISOString(),
        conversation_id: 'conv-1',
        conversation: {
            source_data: {
                question: '我适合什么工作？',
            },
            messages: [
                { role: 'assistant', content: '你的事业线清晰，适合稳定发展。' },
            ],
        },
    });

    assert.match(text, /## 手相分析记录/u);
    assert.match(text, /- 手：左手/u);
    assert.match(text, /- 类型：事业线/u);
    assert.match(text, /- 提问：我适合什么工作/u);
    assert.match(text, /你的事业线清晰，适合稳定发展/u);
    assert.doesNotMatch(text, /conv-1/u);
    assert.doesNotMatch(text, /- 手：left/u);
    assert.doesNotMatch(text, /- 类型：fateline/u);
});

test('faceProvider formatForAI should reuse user-visible labels and conversation analysis text', async () => {
    const { faceProvider } = await import('../lib/data-sources/face');

    const text = await faceProvider.formatForAI({
        id: 'face-1',
        user_id: 'user-1',
        analysis_type: 'career',
        created_at: new Date().toISOString(),
        conversation_id: 'conv-2',
        conversation: {
            source_data: {
                question: '我的事业发展怎么样？',
            },
            messages: [
                { role: 'assistant', content: '额头宽阔，事业上有较强上升空间。' },
            ],
        },
    });

    assert.match(text, /## 面相分析记录/u);
    assert.match(text, /- 类型：事业/u);
    assert.match(text, /- 提问：我的事业发展怎么样/u);
    assert.match(text, /额头宽阔，事业上有较强上升空间/u);
    assert.doesNotMatch(text, /conv-2/u);
    assert.doesNotMatch(text, /- 类型：career/u);
});

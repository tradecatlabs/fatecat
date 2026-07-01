import { test } from 'node:test';
import assert from 'node:assert/strict';

process.env.NEXT_PUBLIC_SUPABASE_URL = 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test-anon';

test('calculateResult chooses dominant dimensions from answers', () => {
    const mbti = require('../lib/divination/mbti') as any;

    const questions = [
        { question: 'Q1', choice_a: { value: 'E', text: 'A' }, choice_b: { value: 'I', text: 'B' } },
        { question: 'Q2', choice_a: { value: 'S', text: 'A' }, choice_b: { value: 'N', text: 'B' } },
        { question: 'Q3', choice_a: { value: 'T', text: 'A' }, choice_b: { value: 'F', text: 'B' } },
        { question: 'Q4', choice_a: { value: 'J', text: 'A' }, choice_b: { value: 'P', text: 'B' } },
    ];

    const answers = [
        { questionIndex: 0, likertValue: 1 },
        { questionIndex: 1, likertValue: 1 },
        { questionIndex: 2, likertValue: 1 },
        { questionIndex: 3, likertValue: 1 },
    ];

    const result = mbti.calculateResult(questions, answers);

    assert.equal(result.type, 'ESTJ');
    assert.equal(result.percentages.EI.E, 100);
    assert.equal(result.percentages.SN.S, 100);
    assert.equal(result.percentages.TF.T, 100);
    assert.equal(result.percentages.JP.J, 100);
});

test('buildViewResult returns defaults for valid type', () => {
    const mbti = require('../lib/divination/mbti') as any;

    assert.equal(typeof mbti.buildViewResult, 'function');

    const result = mbti.buildViewResult('INTJ');
    assert.equal(result?.type, 'INTJ');
    assert.equal(result?.percentages?.EI?.E, 50);
    assert.equal(result?.percentages?.EI?.I, 50);
});

test('buildViewResult rejects invalid type', () => {
    const mbti = require('../lib/divination/mbti') as any;

    assert.equal(mbti.buildViewResult('NOPE'), null);
});

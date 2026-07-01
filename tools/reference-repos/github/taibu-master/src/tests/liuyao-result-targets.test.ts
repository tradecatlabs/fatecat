import { test } from 'node:test';
import assert from 'node:assert/strict';

import { resolveResultYongShenState, resolveResultYongShenTargets } from '../lib/divination/liuyao-result-state';

test('result target resolution falls back to pending and question session targets when result payload is missing', () => {
    assert.deepEqual(
        resolveResultYongShenTargets([], ['官鬼'], ['父母']),
        ['官鬼']
    );

    assert.deepEqual(
        resolveResultYongShenTargets([], [], ['父母', '官鬼']),
        ['父母', '官鬼']
    );

    assert.deepEqual(
        resolveResultYongShenTargets(['子孙'], ['官鬼'], ['父母']),
        ['子孙']
    );
});

test('result page keeps pending targets as draft until the user applies them', () => {
    const state = resolveResultYongShenState([], ['官鬼'], []);

    assert.deepEqual(state.appliedTargets, []);
    assert.deepEqual(state.pendingTargets, ['官鬼']);
});

test('result page can auto-recover previously selected targets from question session', () => {
    const state = resolveResultYongShenState([], [], ['父母', '官鬼']);

    assert.deepEqual(state.appliedTargets, ['父母', '官鬼']);
    assert.deepEqual(state.pendingTargets, []);
});

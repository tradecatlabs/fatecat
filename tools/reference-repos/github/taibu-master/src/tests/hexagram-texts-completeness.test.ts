import { test } from 'node:test';
import assert from 'node:assert/strict';
import { HEXAGRAMS } from '../lib/divination/liuyao';
import { getHexagramText } from '../lib/divination/hexagram-texts';

test('hexagram texts provide gua/xiang/6-yao for all 64 hexagrams', () => {
    assert.equal(HEXAGRAMS.length, 64);

    for (const hex of HEXAGRAMS) {
        const text = getHexagramText(hex.name);
        assert.ok(text, `missing text for ${hex.name}`);
        assert.ok(text?.gua && text.gua.length > 0, `missing gua text for ${hex.name}`);
        assert.ok(text?.xiang && text.xiang.length > 0, `missing xiang text for ${hex.name}`);
        assert.equal(text?.yao.length, 6, `missing full yao texts for ${hex.name}`);
    }
});

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { resolveCoinTossResult } from '@/lib/divination/liuyao';

const CASES: Array<{
    coins: [boolean, boolean, boolean];
    sum: number;
    yaoType: 0 | 1;
    isChanging: boolean;
}> = [
    { coins: [false, false, false], sum: 6, yaoType: 0, isChanging: true },
    { coins: [true, false, false], sum: 7, yaoType: 1, isChanging: false },
    { coins: [true, true, false], sum: 8, yaoType: 0, isChanging: false },
    { coins: [true, true, true], sum: 9, yaoType: 1, isChanging: true },
];

test('resolveCoinTossResult follows 6/7/8/9 mapping', () => {
    for (const item of CASES) {
        const result = resolveCoinTossResult(item.coins);
        assert.equal(result.sum, item.sum);
        assert.equal(result.yaoType, item.yaoType);
        assert.equal(result.isChanging, item.isChanging);
    }
});

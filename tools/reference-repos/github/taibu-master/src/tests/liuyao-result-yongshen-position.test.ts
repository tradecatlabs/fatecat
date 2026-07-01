import { test } from 'node:test';
import assert from 'node:assert/strict';

import { resolveTraditionalYongShenPositions } from '../lib/divination/liuyao-result-state';

test('result page resolves yongshen highlight positions when selected labels include 爻 suffix', () => {
    const positions = resolveTraditionalYongShenPositions({
        六爻: [
            { 爻位: '上九', 六亲: '子孙' },
            { 爻位: '九五', 六亲: '妻财' },
            { 爻位: '九四', 六亲: '兄弟' },
            { 爻位: '六三', 六亲: '官鬼' },
            { 爻位: '六二', 六亲: '父母' },
            { 爻位: '初九', 六亲: '妻财' },
        ],
        用神分析: [{
            已选用神: {
                爻位: '初九爻',
                六亲: '妻财',
            },
        }],
    } as any);

    assert.deepEqual(positions, [1]);
});

test('result page does not highlight yongshen when normalized position matches but liuqin differs', () => {
    const positions = resolveTraditionalYongShenPositions({
        六爻: [
            { 爻位: '上九', 六亲: '子孙' },
            { 爻位: '九五', 六亲: '妻财' },
            { 爻位: '九四', 六亲: '兄弟' },
            { 爻位: '六三', 六亲: '官鬼' },
            { 爻位: '六二', 六亲: '父母' },
            { 爻位: '初九', 六亲: '兄弟' },
        ],
        用神分析: [{
            已选用神: {
                爻位: '初九爻',
                六亲: '妻财',
            },
        }],
    } as any);

    assert.deepEqual(positions, []);
});

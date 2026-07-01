import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
    performFullAnalysis,
    yaosTpCode,
    calculateKongWangByPillar,
    XUN_KONG_TABLE,
    type Yao,
    type YaoType,
    type YaoChange,
    type GanZhiTime,
} from '../lib/divination/liuyao';

test('performFullAnalysis outputs qualitative structured contract', () => {
    const yaos: Yao[] = [
        { type: 1 as YaoType, change: 'changing' as YaoChange, position: 1 },
        { type: 0 as YaoType, change: 'stable' as YaoChange, position: 2 },
        { type: 1 as YaoType, change: 'stable' as YaoChange, position: 3 },
        { type: 0 as YaoType, change: 'changing' as YaoChange, position: 4 },
        { type: 1 as YaoType, change: 'stable' as YaoChange, position: 5 },
        { type: 0 as YaoType, change: 'stable' as YaoChange, position: 6 },
    ];
    const hexagramCode = yaosTpCode(yaos);
    const changedCode = yaosTpCode(yaos.map((yao) => ({
        ...yao,
        type: yao.change === 'changing' ? (yao.type === 1 ? 0 : 1) : yao.type,
    })));

    const analysis = performFullAnalysis(
        yaos,
        hexagramCode,
        changedCode,
        '测试用问题',
        new Date('2024-01-02T00:00:00.000Z'),
        { yongShenTargets: ['兄弟'] }
    );

    assert.ok(Array.isArray(analysis.yongShen));
    assert.ok(Array.isArray(analysis.shenSystemByYongShen));
    assert.ok(Array.isArray(analysis.globalShenSha));

    assert.equal(analysis.fullYaos.length, 6);
    for (const yao of analysis.fullYaos) {
        assert.equal(typeof yao.isChanging, 'boolean');
        assert.ok(['static', 'changing', 'hidden_moving', 'day_break'].includes(yao.movementState));
        assert.equal(typeof yao.movementLabel, 'string');
        assert.ok(Array.isArray(yao.shenSha));
        assert.ok(Array.isArray(yao.strength.evidence));
        assert.equal('score' in yao.strength, false);
        if (yao.isChanging) {
            assert.ok(yao.changedYao);
            assert.equal(typeof yao.changedYao?.relation, 'string');
        } else {
            assert.equal(yao.changedYao, null);
        }
    }

    for (const group of analysis.yongShen) {
        assert.ok(group.selected);
        assert.ok(Array.isArray(group.candidates));
        assert.equal('strengthScore' in group.selected, false);
        assert.equal('rankScore' in group.selected, false);
        assert.equal(typeof group.selectionNote, 'string');
        for (const candidate of group.candidates) {
            assert.equal('strengthScore' in candidate, false);
            assert.equal('rankScore' in candidate, false);
            assert.ok(Array.isArray(candidate.evidence));
        }
    }

    for (const rec of analysis.timeRecommendations) {
        assert.equal(typeof rec.targetLiuQin, 'string');
        assert.equal(typeof rec.trigger, 'string');
        assert.ok(Array.isArray(rec.basis));
        assert.equal(typeof rec.description, 'string');
        assert.equal('confidence' in rec, false);
        assert.equal('startDate' in rec, false);
        assert.equal('endDate' in rec, false);
    }
});

test('calculateKongWangByPillar returns correct kongWang for each pillar', () => {
    const ganZhiTime: GanZhiTime = {
        year: { gan: '甲', zhi: '子' },
        month: { gan: '甲', zhi: '寅' },
        day: { gan: '甲', zhi: '辰' },
        hour: { gan: '甲', zhi: '午' },
        xun: '甲辰旬',
    };

    const kongWangByPillar = calculateKongWangByPillar(ganZhiTime);

    assert.equal(kongWangByPillar.year.xun, '甲子旬');
    assert.deepEqual(kongWangByPillar.year.kongDizhi, XUN_KONG_TABLE['甲子旬']);
    assert.equal(kongWangByPillar.month.xun, '甲寅旬');
    assert.deepEqual(kongWangByPillar.month.kongDizhi, XUN_KONG_TABLE['甲寅旬']);
    assert.equal(kongWangByPillar.day.xun, '甲辰旬');
    assert.deepEqual(kongWangByPillar.day.kongDizhi, XUN_KONG_TABLE['甲辰旬']);
    assert.equal(kongWangByPillar.hour.xun, '甲午旬');
    assert.deepEqual(kongWangByPillar.hour.kongDizhi, XUN_KONG_TABLE['甲午旬']);
});

test('performFullAnalysis keeps kongWang equal to day pillar kongWang', () => {
    const yaos: Yao[] = [
        { type: 1 as YaoType, change: 'stable' as YaoChange, position: 1 },
        { type: 1 as YaoType, change: 'stable' as YaoChange, position: 2 },
        { type: 1 as YaoType, change: 'stable' as YaoChange, position: 3 },
        { type: 1 as YaoType, change: 'stable' as YaoChange, position: 4 },
        { type: 1 as YaoType, change: 'stable' as YaoChange, position: 5 },
        { type: 1 as YaoType, change: 'stable' as YaoChange, position: 6 },
    ];

    const analysis = performFullAnalysis(
        yaos,
        yaosTpCode(yaos),
        undefined,
        '测试用问题',
        new Date('2024-01-02T00:00:00.000Z'),
        { yongShenTargets: ['兄弟'] }
    );

    assert.equal(analysis.kongWang.xun, analysis.kongWangByPillar.day.xun);
    assert.deepEqual(analysis.kongWang.kongDizhi, analysis.kongWangByPillar.day.kongDizhi);
});

test('performFullAnalysis supports explicit multi yongshen groups for exam questions', () => {
    const yaos: Yao[] = [
        { type: 1 as YaoType, change: 'stable' as YaoChange, position: 1 },
        { type: 1 as YaoType, change: 'stable' as YaoChange, position: 2 },
        { type: 1 as YaoType, change: 'stable' as YaoChange, position: 3 },
        { type: 1 as YaoType, change: 'changing' as YaoChange, position: 4 },
        { type: 1 as YaoType, change: 'stable' as YaoChange, position: 5 },
        { type: 1 as YaoType, change: 'changing' as YaoChange, position: 6 },
    ];
    const hexagramCode = yaosTpCode(yaos);
    const changedCode = yaosTpCode(yaos.map((yao) => ({
        ...yao,
        type: yao.change === 'changing' ? (yao.type === 1 ? 0 : 1) : yao.type,
    })));

    const analysis = performFullAnalysis(
        yaos,
        hexagramCode,
        changedCode,
        '考试结果和排名怎么样',
        new Date('2026-02-10T00:00:00.000Z'),
        { yongShenTargets: ['官鬼', '父母'] }
    );

    assert.ok(analysis.yongShen.some(group => group.targetLiuQin === '官鬼'));
    assert.ok(analysis.yongShen.some(group => group.targetLiuQin === '父母'));
    for (const group of analysis.yongShen) {
        assert.ok(group.selected);
        assert.ok(Array.isArray(group.candidates));
        assert.equal(typeof group.selectionNote, 'string');
        assert.ok(['resolved', 'ambiguous', 'from_changed', 'from_temporal', 'from_fushen', 'missing'].includes(group.selectionStatus));
        if (group.candidates.length > 0) {
            assert.ok(Array.isArray(group.candidates[0].evidence));
        }
    }
});

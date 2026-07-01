import { test } from 'node:test';
import assert from 'node:assert/strict';

const tarotModulePath = require.resolve('../lib/divination/tarot');

const loadTarotModule = () => {
    delete require.cache[tarotModulePath];
    return require('../lib/divination/tarot') as typeof import('../lib/divination/tarot');
};

function cardSignature(cards: Array<{ card: { nameChinese: string }; orientation: string }>): string {
    return cards.map(card => `${card.card.nameChinese}:${card.orientation}`).join('|');
}

function dailyCardSignature(card: { card: { nameChinese: string }; orientation: string }): string {
    return `${card.card.nameChinese}:${card.orientation}`;
}

test('drawCards should not repeat the same result for every draw when no explicit seed is provided', async () => {
    const { drawCards } = loadTarotModule();
    const signatures = new Set<string>();

    for (let index = 0; index < 5; index += 1) {
        const cards = await drawCards(1, true);
        signatures.add(cardSignature(cards));
    }

    assert.ok(
        signatures.size > 1,
        'drawCards currently falls back to a deterministic daily seed when seed is omitted',
    );
});

test('drawForSpread should not repeat the same spread for every draw when no explicit seed is provided', async () => {
    const { drawForSpread } = loadTarotModule();
    const signatures = new Set<string>();

    for (let index = 0; index < 5; index += 1) {
        const result = await drawForSpread('three-card', true);
        assert.ok(result, 'three-card spread should exist');
        signatures.add(cardSignature(result.cards));
    }

    assert.ok(
        signatures.size > 1,
        'drawForSpread currently falls back to a deterministic daily seed when seed is omitted',
    );
});

test('drawForSpread should remain deterministic when caller provides an explicit seed', async () => {
    const { drawForSpread } = loadTarotModule();

    const first = await drawForSpread('three-card', true, { seed: 'fixed-seed' });
    const second = await drawForSpread('three-card', true, { seed: 'fixed-seed' });

    assert.ok(first);
    assert.ok(second);
    assert.equal(cardSignature(first.cards), cardSignature(second.cards));
});

test('getDailyCard should derive the daily seed from the caller local date when timezone is omitted', async (t) => {
    const originalTZ = process.env.TZ;

    t.after(() => {
        delete require.cache[tarotModulePath];
        if (originalTZ === undefined) {
            delete process.env.TZ;
            return;
        }
        process.env.TZ = originalTZ;
    });

    process.env.TZ = 'America/New_York';
    const { getDailyCard } = loadTarotModule();
    const dates = [
        '2026-03-16T00:30:00Z',
        '2026-03-17T00:30:00Z',
        '2026-03-18T00:30:00Z',
    ];

    const implicitCards = await Promise.all(
        dates.map(async (value) => dailyCardSignature(await getDailyCard(new Date(value))))
    );
    const newYorkCards = await Promise.all(
        dates.map(async (value) => dailyCardSignature(await getDailyCard(new Date(value), { timezone: 'America/New_York' })))
    );
    const shanghaiCards = await Promise.all(
        dates.map(async (value) => dailyCardSignature(await getDailyCard(new Date(value), { timezone: 'Asia/Shanghai' })))
    );

    assert.deepEqual(implicitCards, newYorkCards);
    assert.notDeepEqual(implicitCards, shanghaiCards);
});

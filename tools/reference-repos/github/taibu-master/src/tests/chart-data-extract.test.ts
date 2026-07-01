import test from 'node:test';
import assert from 'node:assert/strict';

process.env.NEXT_PUBLIC_SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'test-anon';

test('extractChartBlocks should parse valid chart blocks from markdown', async () => {
    const { extractChartBlocks } = await import('../lib/visualization/chart-data-extract');

    const markdown = `这是分析文本...

\`\`\`chart
{
  "chartType": "fortune_radar",
  "title": "当前运势评分",
  "data": { "period": "2026年", "scores": {}, "overallScore": 75, "overallLabel": "良好" }
}
\`\`\`

继续分析...

\`\`\`chart
{
  "chartType": "life_fortune_trend",
  "title": "大运趋势",
  "data": { "currentAge": 35, "currentYear": 2026, "periods": [] }
}
\`\`\`
`;

    const results = extractChartBlocks(markdown);
    assert.equal(results.length, 2);
    assert.equal(results[0].chartType, 'fortune_radar');
    assert.equal(results[0].title, '当前运势评分');
    assert.equal(results[1].chartType, 'life_fortune_trend');
    assert.equal(results[1].title, '大运趋势');
});

test('extractChartBlocks should skip malformed JSON blocks', async () => {
    const { extractChartBlocks } = await import('../lib/visualization/chart-data-extract');

    const markdown = `\`\`\`chart
{ invalid json }
\`\`\`

\`\`\`chart
{ "chartType": "fortune_radar", "title": "有效图表", "data": {} }
\`\`\``;

    const results = extractChartBlocks(markdown);
    assert.equal(results.length, 1);
    assert.equal(results[0].title, '有效图表');
});

test('extractChartsFromMessages should deduplicate by chartType + title', async () => {
    const { extractChartsFromMessages } = await import('../lib/visualization/chart-data-extract');

    const messages = [
        {
            role: 'assistant',
            content: '```chart\n{"chartType":"fortune_radar","title":"运势","data":{"v":1}}\n```',
        },
        {
            role: 'user',
            content: '再分析一下',
        },
        {
            role: 'assistant',
            content: '```chart\n{"chartType":"fortune_radar","title":"运势","data":{"v":2}}\n```',
        },
    ];

    const results = extractChartsFromMessages(messages);
    assert.equal(results.length, 1);
    // Should keep the latest version
    assert.equal((results[0].raw as any).data.v, 2);
    assert.deepEqual((results[0].raw as any).data.scores, {});
});

test('formatPreviousChartsForPrompt should produce non-empty text for non-empty input', async () => {
    const { formatPreviousChartsForPrompt } = await import('../lib/visualization/chart-data-extract');

    const charts = [
        { chartType: 'fortune_radar' as const, title: '运势评分', raw: {} as any },
        { chartType: 'life_fortune_trend' as const, title: '大运趋势', raw: {} as any },
    ];

    const text = formatPreviousChartsForPrompt(charts);
    assert.ok(text.includes('运势评分'));
    assert.ok(text.includes('大运趋势'));
    assert.ok(text.includes('fortune_radar'));
});

test('formatPreviousChartsForPrompt should return empty string for empty input', async () => {
    const { formatPreviousChartsForPrompt } = await import('../lib/visualization/chart-data-extract');
    assert.equal(formatPreviousChartsForPrompt([]), '');
});

test('normalizeChartData should sanitize malformed life fortune trend payloads', async () => {
    const { normalizeChartData } = await import('../lib/visualization/chart-data-extract');

    const normalized = normalizeChartData({
        chartType: 'life_fortune_trend',
        title: '大运趋势',
        data: {
            currentAge: '35岁',
            currentYear: '2026年',
            periods: [
                {
                    label: '',
                    startAge: '30',
                    endAge: '39岁',
                    startYear: '2021',
                    endYear: '2030',
                    scores: {
                        事业学业: '81.6',
                        未知维度: 99,
                    },
                    summary: '机会增长',
                    highlights: '贵人出现',
                    warnings: [null, '慎投机'],
                    yearlyScores: [
                        { age: '30岁', year: '2021年', overall: '88.4' },
                        { age: 'bad', year: 2022, overall: 50 },
                    ],
                },
                {
                    label: '无效周期',
                    startAge: null,
                    endAge: null,
                    scores: {
                        未知维度: 90,
                    },
                    yearlyScores: [{ age: 'bad', year: 'bad', overall: 'bad' }],
                },
            ],
            lifeHighlight: {
                bestPeriod: { label: '黄金期', ages: '30-39', reason: '势能强' },
                currentStatus: '稳中向上',
                nextTurningPoint: { age: '41岁', direction: 'sideways', reason: '调整中' },
            },
        },
    } as any) as any;

    assert.equal(normalized.data.currentAge, 35);
    assert.equal(normalized.data.currentYear, 2026);
    assert.equal(normalized.data.periods.length, 1);
    assert.equal(normalized.data.periods[0].label, '阶段1');
    assert.deepEqual(normalized.data.periods[0].scores, { career: 82 });
    assert.deepEqual(normalized.data.periods[0].highlights, ['贵人出现']);
    assert.deepEqual(normalized.data.periods[0].warnings, ['慎投机']);
    assert.deepEqual(normalized.data.periods[0].yearlyScores, [{ age: 30, year: 2021, overall: 88 }]);
    assert.equal(normalized.data.lifeHighlight.nextTurningPoint.age, 41);
    assert.equal(normalized.data.lifeHighlight.nextTurningPoint.direction, 'up');
});

test('normalizeChartData should coerce and filter malformed radar scores', async () => {
    const { normalizeChartData } = await import('../lib/visualization/chart-data-extract');

    const normalized = normalizeChartData({
        chartType: 'fortune_radar',
        title: '当前运势',
        data: {
            period: '2026',
            scores: {
                事业学业: '79.6',
                财富: { score: '65.2', label: '财运', trend: 'down' },
                野生字段: { score: 91, label: '未知', trend: 'up' },
            },
            previousScores: {
                事业学业: '70',
                野生字段: 50,
            },
            overallScore: 'bad',
            overallLabel: '良好',
            topAdvice: '稳健推进',
        },
    } as any) as any;

    assert.deepEqual(normalized.data.scores, {
        career: { score: 80, label: '事业/学业', trend: 'stable' },
        wealth: { score: 65, label: '财运', trend: 'down' },
    });
    assert.deepEqual(normalized.data.previousScores, { career: 70 });
    assert.equal(normalized.data.overallScore, 73);
});

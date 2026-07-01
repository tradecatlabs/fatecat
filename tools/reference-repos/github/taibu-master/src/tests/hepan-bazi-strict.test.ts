import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Solar } from 'lunar-javascript';
import { calculateBaZi } from '@/lib/divination/hepan';

test('hepan calculateBaZi should match lunar-javascript pillars', () => {
    const solar = Solar.fromYmdHms(1990, 1, 1, 10, 0, 0);
    const eightChar = solar.getLunar().getEightChar();

    const result = calculateBaZi({
        name: 'A',
        year: 1990,
        month: 1,
        day: 1,
        hour: 10,
    });

    assert.equal(result.yearGan, eightChar.getYearGan());
    assert.equal(result.yearZhi, eightChar.getYearZhi());
    assert.equal(result.monthGan, eightChar.getMonthGan());
    assert.equal(result.monthZhi, eightChar.getMonthZhi());
    assert.equal(result.dayGan, eightChar.getDayGan());
    assert.equal(result.dayZhi, eightChar.getDayZhi());
    assert.equal(result.hourGan, eightChar.getTimeGan());
    assert.equal(result.hourZhi, eightChar.getTimeZhi());
});

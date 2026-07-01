import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
function runUnderTimeZone(timeZone) {
  const script = `
    import { calculateDaliuren } from 'taibu-core';
    const result = calculateDaliuren({
      date: '2024-01-01',
      hour: 10,
      minute: 0,
      question: '时区回归测试',
      timezone: 'Asia/Shanghai',
    });
    console.log(JSON.stringify({
      solarDate: result.dateInfo.solarDate,
      bazi: result.dateInfo.bazi,
      yueJiang: result.dateInfo.yueJiang,
      keName: result.keName,
      sanChuan: result.sanChuan,
    }));
  `;

  return JSON.parse(
    execFileSync(process.execPath, ['--input-type=module', '-e', script], {
      cwd: process.cwd(),
      env: { ...process.env, TZ: timeZone },
      encoding: 'utf8',
    }).trim(),
  );
}

test('daliuren calculation should be stable across process time zones for the same wall-clock input', () => {
  const utcResult = runUnderTimeZone('UTC');
  const shanghaiResult = runUnderTimeZone('Asia/Shanghai');

  assert.deepEqual(
    utcResult,
    shanghaiResult,
    'same input should not produce different daliuren charts just because the process TZ changed',
  );
});

#!/usr/bin/env node
/**
 * 真太阳时计算（复用 paipan-master 原生算法）
 * 输入：--dt "YYYY-MM-DD HH:MM:SS"  --lon 114.1  --lat 22.5
 * 输出：单行 ISO8601 字符串（本地真太阳时，对应北京时区的日期时间）
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

function loadPaipan() {
  const code = fs.readFileSync(
    // 从 scripts/ 回到仓库根：../../../
    path.resolve(__dirname, '../../../assets/vendor/github/paipan-master/js/paipan.js'),
    'utf-8'
  );
  const sandbox = { window: {}, console };
  vm.createContext(sandbox);
  vm.runInContext(code, sandbox, { filename: 'paipan.js' });
  if (sandbox.window && sandbox.window.p) {
    return sandbox.window.p;
  }
  if (sandbox.paipan) {
    return new sandbox.paipan();
  }
  throw new Error('paipan not loaded');
}

function parseArgs() {
  const args = process.argv.slice(2);
  const out = { json: false };
  for (let i = 0; i < args.length; i++) {
    const k = args[i];
    if (k === '--json') {
      out.json = true;
      continue;
    }
    const v = args[i + 1];
    if (k === '--dt') {
      out.dt = v;
      i++;
      continue;
    }
    if (k === '--lon') {
      out.lon = parseFloat(v);
      i++;
      continue;
    }
    if (k === '--lat') {
      out.lat = parseFloat(v);
      i++;
      continue;
    }
  }
  if (!out.dt || isNaN(out.lon) || isNaN(out.lat)) {
    throw new Error('usage: true_solar_time.js --dt "YYYY-MM-DD HH:MM:SS" --lon 116.4 --lat 39.9 [--json]');
  }
  return out;
}

function pad(n, w = 2) {
  return String(Math.floor(n)).padStart(w, '0');
}

function main() {
  const { dt, lon, lat, json } = parseArgs();
  const [datePart, timePart] = dt.trim().split(/\s+/);
  const [Y, M, D] = datePart.split('-').map(Number);
  const [h, m, s] = timePart.split(':').map(Number);

  const p = loadPaipan();
  const jdStd = p.Jdays(Y, M, D, h, m, s); // 标准时间（默认以 paipan 内置经度/时区为准）
  const [utrise, utset, noonOffsetDays] = p.risenset(jdStd, lon, lat, 2); // noonOffsetDays 即 zty() 使用的 dt
  const jdTrue = p.zty(jdStd, lon, lat); // 转真太阳时
  const [y2, m2, d2, h2, mi2, s2] = p.Jtime(jdTrue);

  const trueIso = `${pad(y2, 4)}-${pad(m2)}-${pad(d2)} ${pad(h2)}:${pad(mi2)}:${pad(Math.round(s2))}`;
  if (!json) {
    process.stdout.write(trueIso);
    return;
  }

  const longitudeOffsetMinutes = (lon - p.J) * 4;
  const astroOffsetMinutes = noonOffsetDays * 24 * 60;
  const totalOffsetMinutes = longitudeOffsetMinutes + astroOffsetMinutes;

  // 早晚子时：直接复用 paipan 的 zwz 规则，比较日柱是否发生“前移一柱”
  function dayPillarAt(dtParts, zwz) {
    const [yy, mm, dd, hh, mt, ss] = dtParts;
    p.zwz = !!zwz;
    const gz = p.GetGZ(yy, mm, dd, hh, mt, ss);
    if (!gz) throw new Error('GetGZ failed');
    const tg = gz[0];
    const dz = gz[1];
    return `${p.ctg[tg[2]]}${p.cdz[dz[2]]}`;
  }
  const trueParts = [y2, m2, d2, h2, mi2, Math.round(s2)];
  const dayNormal = dayPillarAt(trueParts, false);
  const dayZwz = dayPillarAt(trueParts, true);
  const zwzShift = dayNormal !== dayZwz;
  const timeZhi = (() => {
    p.zwz = false;
    const gz = p.GetGZ(...trueParts);
    const dz = gz[1];
    return p.cdz[dz[3]];
  })();

  const ziTimeAnalysis = {
    rule: '启用早晚子时后，23:00-24:00 日柱前移一柱（早晚子规则）',
    timeZhi,
    dayPillarNormal: dayNormal,
    dayPillarZwz: dayZwz,
    zwzShift,
  };

  const payload = {
    input: { dt, lon, lat },
    trueSolarTime: trueIso,
    offsets: {
      longitudeOffsetMinutes,
      astronomicalOffsetMinutes: astroOffsetMinutes,
      totalOffsetMinutes,
      noonOffsetDays,
      utrise,
      utset,
    },
    ziTimeAnalysis,
  };
  process.stdout.write(JSON.stringify(payload));
}

try {
  main();
} catch (e) {
  console.error(e.message || e);
  process.exit(1);
}

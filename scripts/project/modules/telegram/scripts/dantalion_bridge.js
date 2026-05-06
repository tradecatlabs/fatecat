#!/usr/bin/env node
/**
 * 调用 dantalion-core 生成现代化性格分析
 * 输入参数：
 *   --birth YYYY-MM-DD (日期字符串，忽略时间)
 * 输出：单行 JSON 字符串，如失败输出错误到 stderr 并返回非零
 */
const path = require('path');

function parseArgs() {
  const args = process.argv.slice(2);
  const out = {};
  for (let i = 0; i < args.length; i += 2) {
    const k = args[i];
    const v = args[i + 1];
    if (k === '--birth') out.birth = v;
  }
  if (!out.birth) {
    throw new Error('usage: dantalion_bridge.js --birth YYYY-MM-DD');
  }
  return out;
}

function main() {
  const { birth } = parseArgs();
  const corePath = path.resolve(__dirname, '../../../assets/vendor/github/dantalion-master/packages/dantalion-core/dist/index.js');
  const core = require(corePath);
  if (!core.getPersonality) {
    throw new Error('dantalion-core getPersonality not found');
  }
  const result = core.getPersonality(birth);
  if (!result) {
    throw new Error('dantalion-core returned empty result');
  }
  process.stdout.write(JSON.stringify(result));
}

main();

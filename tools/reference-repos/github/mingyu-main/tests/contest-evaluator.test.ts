import test from 'node:test';
import assert from 'node:assert/strict';
import { validateExistingRankingResultFromMarkdown } from '../scripts/evaluate-fortune-contest-model.js';

function buildReportRows(answerForQuestion: (question: number) => string) {
  return Array.from({ length: 40 }, (_, index) => {
    const question = index + 1;
    const actual = answerForQuestion(question);
    const result = actual === 'A' ? '正确' : '错误';
    return `| Q${question} | A | ${actual} | ${result} |`;
  }).join('\n');
}

test('历史比赛评测结果自检应拒绝未解析答案', () => {
  const result = validateExistingRankingResultFromMarkdown(
    {
      Label: '测试模型',
      Model: 'test/model',
      Status: '成功',
      Score: 100,
      Accuracy: 100,
      Correct: 40,
      Total: 40,
      ReportFile: 'report.md',
      Error: '',
    },
    buildReportRows((question) => (question === 7 ? '未解析' : 'A')),
  );

  assert.equal(result.Status, '失败');
  assert.equal(result.Score, null);
  assert.match(result.Error, /未解析或非法答案/);
  assert.match(result.Error, /Q7=未解析/);
});

test('历史比赛评测结果自检应按报告明细重新计算成绩', () => {
  const result = validateExistingRankingResultFromMarkdown(
    {
      Label: '测试模型',
      Model: 'test/model',
      Status: '成功',
      Score: 0,
      Accuracy: 0,
      Correct: 0,
      Total: 40,
      ReportFile: 'report.md',
      Error: '旧错误',
    },
    buildReportRows((question) => (question <= 20 ? 'A' : 'B')),
  );

  assert.equal(result.Status, '成功');
  assert.equal(result.Correct, 20);
  assert.equal(result.Total, 40);
  assert.equal(result.Score, 50);
  assert.equal(result.Accuracy, 50);
  assert.equal(result.Error, '');
});

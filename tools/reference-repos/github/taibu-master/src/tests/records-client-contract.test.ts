import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

test('records page no longer keeps a parallel fetch client next to src/lib/records.ts', () => {
  const pageSource = readFileSync(resolve(process.cwd(), 'src/app/records/page.tsx'), 'utf8');

  assert.equal(pageSource.includes('await fetch(`/api/records?'), false);
  assert.equal(pageSource.includes("await fetch(`/api/records/${id}`"), false);
  assert.equal(pageSource.includes('await fetch(`/api/notes?date='), false);
  assert.equal(pageSource.includes('getRecords('), true);
  assert.equal(pageSource.includes('getNotesByDate('), true);
  assert.equal(pageSource.includes('deleteRecord('), true);
  assert.equal(pageSource.includes('toggleRecordPin('), true);
  assert.equal(pageSource.includes('useSessionSafe('), true);
  assert.equal(pageSource.includes('<AddToKnowledgeBaseModal'), true);
  assert.equal(pageSource.includes('ImportExportModal,\n    KnowledgeBaseModal,'), false);
  assert.equal(pageSource.includes('listKnowledgeBases('), false);
});

test('records detail components reuse src/lib/records.ts instead of maintaining raw records/nodes fetchers', () => {
  const detailSource = readFileSync(resolve(process.cwd(), 'src/components/records/RecordDetail.tsx'), 'utf8');

  assert.equal(detailSource.includes("fetch(record ? `/api/records/${record.id}` : '/api/records'"), false);
  assert.equal(detailSource.includes("fetch('/api/notes'"), false);
  assert.equal(detailSource.includes("fetch(`/api/notes?id=${id}`"), false);
  assert.equal(detailSource.includes("fetch('/api/records/import'"), false);
  assert.equal(detailSource.includes("window.open('/api/records/export'"), false);
  assert.equal(detailSource.includes('createRecord('), true);
  assert.equal(detailSource.includes('updateRecord('), true);
  assert.equal(detailSource.includes('createNote('), true);
  assert.equal(detailSource.includes('deleteNote('), true);
  assert.equal(detailSource.includes('exportData('), true);
  assert.equal(detailSource.includes('importData('), true);
});

test('records client should not keep dead allowNotFound fallback for removed single-record helpers', () => {
  const source = readFileSync(resolve(process.cwd(), 'src/lib/records.ts'), 'utf8');

  assert.equal(source.includes('allowNotFound: true'), false);
  assert.equal(source.includes('/不存在|404/u.test'), false);
});

test('records notes and import-export helpers should not keep fake userId passthrough signatures', () => {
  const source = readFileSync(resolve(process.cwd(), 'src/lib/records.ts'), 'utf8');
  const pageSource = readFileSync(resolve(process.cwd(), 'src/app/records/page.tsx'), 'utf8');
  const detailSource = readFileSync(resolve(process.cwd(), 'src/components/records/RecordDetail.tsx'), 'utf8');

  assert.equal(source.includes('void userId;'), false);
  assert.equal(source.includes('getNotesByDate(userId:'), false);
  assert.equal(source.includes('createNote(userId:'), false);
  assert.equal(source.includes('exportData(userId:'), false);
  assert.equal(source.includes('importData(\n    userId,'), false);
  assert.equal(pageSource.includes('getNotesByDate(user.id,'), false);
  assert.equal(detailSource.includes('createNote(userId,'), false);
  assert.equal(detailSource.includes('exportData(userId)'), false);
  assert.equal(detailSource.includes('importData(userId,'), false);
});

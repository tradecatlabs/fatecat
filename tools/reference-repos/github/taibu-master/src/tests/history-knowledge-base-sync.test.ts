import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

test('history page template should keep append retry state and listen to shared sync events', () => {
  const source = readFileSync(resolve(process.cwd(), 'src/components/history/HistoryPageTemplate.tsx'), 'utf8');

  assert.match(source, /const \[appendError, setAppendError\] = useState<string \| null>\(null\);/u);
  assert.match(source, /const appendRequestKeyRef = useRef<string \| null>\(null\);/u);
  assert.match(source, /window\.addEventListener\(HISTORY_SUMMARY_DELETED_EVENT, handleHistorySummaryDeleted as EventListener\)/u);
  assert.match(source, /window\.addEventListener\(KNOWLEDGE_BASE_SYNC_EVENT, handleArchiveChanged as EventListener\)/u);
  assert.match(source, /重试加载更多/u);
});

test('history drawer should dedupe append pages and expose retry-on-append-failure', () => {
  const source = readFileSync(resolve(process.cwd(), 'src/components/layout/HistoryDrawer.tsx'), 'utf8');

  assert.match(source, /function mergeHistoryItemsById\(current: HistorySummaryItem\[\], incoming: HistorySummaryItem\[\]\)/u);
  assert.match(source, /const \[appendError, setAppendError\] = useState<string \| null>\(null\);/u);
  assert.match(source, /const inFlightRequestKeyRef = useRef<string \| null>\(null\);/u);
  assert.match(source, /setItems\(\(prev\) => append \? mergeHistoryItemsById\(prev, result\.items\) : result\.items\);/u);
  assert.match(source, /重试加载更多/u);
});

test('knowledge-base management should split top-level errors and reuse shared sync events', () => {
  const source = readFileSync(resolve(process.cwd(), 'src/components/settings/panels/KnowledgeBasePanel.tsx'), 'utf8');
  const clientSource = readFileSync(resolve(process.cwd(), 'src/lib/knowledge-base/browser-client.ts'), 'utf8');

  assert.match(source, /const \[listError, setListError\] = useState<string \| null>\(null\);/u);
  assert.match(source, /const \[createError, setCreateError\] = useState<string \| null>\(null\);/u);
  assert.match(source, /const archiveRequestKeyRef = useRef<Record<string, string>>\(\{\}\);/u);
  assert.match(source, /appendError: string \| null;/u);
  assert.match(source, /window\.addEventListener\(KNOWLEDGE_BASE_SYNC_EVENT, handleArchiveChanged as EventListener\)/u);
  assert.equal(clientSource.includes('KNOWLEDGE_BASE_ARCHIVE_CHANGED_EVENT'), false);
  assert.equal(clientSource.includes('dispatchKnowledgeBaseArchiveChanged'), false);
  assert.equal(source.includes('removeKnowledgeBaseArchive(archive.id, {'), false);
  assert.match(source, /重试加载更多/u);
});

test('records page should rely on knowledge-base sync events instead of forcing a second reload after KB success', () => {
  const source = readFileSync(resolve(process.cwd(), 'src/app/records/page.tsx'), 'utf8');

  assert.match(source, /window\.addEventListener\(KNOWLEDGE_BASE_SYNC_EVENT, handleArchiveChanged as EventListener\)/u);
  assert.match(
    source,
    /const handleKnowledgeBaseSuccess = useCallback\(\(payload:[\s\S]*closeKbModal\(\);\s*\}, \[closeKbModal\]\);/u,
  );
});

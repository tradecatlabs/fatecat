import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const SOURCE = readFileSync(
  resolve(process.cwd(), 'src/components/layout/SidebarAnnouncementCenter.tsx'),
  'utf8',
);

test('announcement center clears announcement pagination after append failures', () => {
  assert.match(
    SOURCE,
    /if \(result\.error\) \{[\s\S]*setAnnouncementHasMore\(false\);[\s\S]*setAnnouncementNextOffset\(null\);[\s\S]*if \(!append\)/u,
  );
});

test('announcement center clears notification pagination after append failures without dropping loaded items', () => {
  assert.match(
    SOURCE,
    /catch \(error\) \{[\s\S]*setNotificationHasMore\(false\);[\s\S]*setNotificationNextOffset\(null\);[\s\S]*if \(!append\) \{[\s\S]*setNotifications\(\[\]\);[\s\S]*setNotificationError\(message\);/u,
  );
});

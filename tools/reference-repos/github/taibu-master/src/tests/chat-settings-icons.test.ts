import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

test('chat page settings entries reuse shared settings center icons', () => {
  const headerSource = readFileSync(resolve(process.cwd(), 'src/components/chat/ChatHeader.tsx'), 'utf8');
  const chatPageSource = readFileSync(resolve(process.cwd(), 'src/app/chat/page.tsx'), 'utf8');

  assert.equal(headerSource.includes("import { SETTINGS_CENTER_TAB_ICONS } from '@/components/settings/settings-center-icons'"), true);
  assert.equal(headerSource.includes('const PersonalizationIcon = SETTINGS_CENTER_TAB_ICONS.personalization'), true);
  assert.equal(headerSource.includes('<PersonalizationIcon size={20}'), true);
  assert.equal(headerSource.includes('MessageCircleHeart'), false);

  assert.equal(chatPageSource.includes("import { SETTINGS_CENTER_TAB_ICONS } from '@/components/settings/settings-center-icons'"), true);
  assert.equal(chatPageSource.includes('createElement(SETTINGS_CENTER_TAB_ICONS.personalization'), true);
  assert.equal(chatPageSource.includes('MessageCircleHeart'), false);
});

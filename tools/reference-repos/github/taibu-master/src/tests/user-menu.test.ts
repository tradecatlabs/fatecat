import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

test('user menu uses registry icons and removes heavy account shortcuts', () => {
  const source = readFileSync(resolve(process.cwd(), 'src/components/layout/UserMenu.tsx'), 'utf8');
  const hostSource = readFileSync(resolve(process.cwd(), 'src/components/settings/SettingsCenterHost.tsx'), 'utf8');
  const iconSource = readFileSync(resolve(process.cwd(), 'src/components/settings/settings-center-icons.tsx'), 'utf8');

  assert.equal(source.includes("import { SETTINGS_CENTER_TAB_ICONS } from '@/components/settings/settings-center-icons'"), true);
  assert.equal(source.includes('createElement(SETTINGS_CENTER_TAB_ICONS[tab]'), true);
  assert.equal(source.includes("{ tab: 'general', label: '设置' }"), true);
  assert.equal(source.includes("{ tab: 'personalization', label: '个性化' }"), true);
  assert.equal(source.includes("{ tab: 'charts', label: '命盘' }"), true);
  assert.equal(source.includes('PROJECT_REPO_URL'), true);
  assert.equal(source.includes('PROJECT_ISSUES_URL'), true);
  assert.equal(source.includes('https://github.com/hhszzzz/taibu'), true);
  assert.equal(source.includes('https://docs.qq.com/smartsheet/DS3JSQ0dHTUdrVWFh'), true);
  assert.equal(source.includes('tab="help"'), true);
  assert.equal(source.includes('帮助中心'), true);
  assert.equal(source.includes('报告错误/需求'), true);
  assert.equal(hostSource.includes("from '@/components/settings/settings-center-icons'"), true);
  assert.equal(hostSource.includes('SETTINGS_CENTER_TAB_ICONS'), true);
  assert.equal(iconSource.includes('MetaLogoIcon'), true);
  assert.equal(iconSource.includes('GearSixIcon'), true);
  assert.equal(iconSource.includes('QuestionMarkIcon'), true);
  assert.equal(source.includes('tab="upgrade"'), false);
  assert.equal(source.includes('tab="profile"'), false);
  assert.equal(source.includes('tab="admin-announcements"'), false);
  assert.equal(source.includes('rounded-2xl'), true);
  assert.equal(source.includes('rounded-xl'), true);
  assert.equal(source.includes('HELP_SUBMENU_CLASS'), true);
});

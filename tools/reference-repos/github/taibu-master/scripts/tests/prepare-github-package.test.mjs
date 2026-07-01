import test from 'node:test';
import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';

const execFileAsync = promisify(execFile);
const repoRoot = path.resolve(import.meta.dirname, '..', '..');
const scriptPath = path.join(repoRoot, 'scripts', 'prepare-github-package.mjs');
const coreManifestPath = path.join(repoRoot, 'packages', 'core', 'package.json');

async function runPrintManifest(packageKey) {
  const { stdout } = await execFileAsync(process.execPath, [
    scriptPath,
    '--package',
    packageKey,
    '--print-manifest',
  ], {
    cwd: repoRoot,
  });

  return JSON.parse(stdout);
}

test('prepare-github-package rewrites core metadata for GitHub Packages', async () => {
  const sourceCoreManifest = JSON.parse(await readFile(coreManifestPath, 'utf8'));
  const manifest = await runPrintManifest('core');

  assert.equal(manifest.name, '@hhszzzz/taibu-core');
  assert.equal(manifest.version, sourceCoreManifest.version);
  assert.equal(manifest.publishConfig.registry, 'https://npm.pkg.github.com');
  assert.deepEqual(manifest.repository, {
    type: 'git',
    url: 'https://github.com/hhszzzz/taibu.git',
  });
});

test('prepare-github-package copies the package-local LICENSE when available', async () => {
  const tempRoot = await mkdtemp(path.join(tmpdir(), 'taibu-license-check-'));

  try {
    await execFileAsync(process.execPath, [
      scriptPath,
      '--package',
      'core',
      '--output',
      tempRoot,
    ], {
      cwd: repoRoot,
    });

    const preparedLicense = await readFile(path.join(tempRoot, 'core', 'LICENSE'), 'utf8');
    const sourceLicense = await readFile(path.join(repoRoot, 'packages', 'core', 'LICENSE'), 'utf8');

    assert.equal(preparedLicense, sourceLicense);
  } finally {
    await rm(tempRoot, { recursive: true, force: true });
  }
});

test('prepare-github-package rewrites workspace dependencies for GitHub Packages', async () => {
  const sourceCoreManifest = JSON.parse(await readFile(coreManifestPath, 'utf8'));
  const manifest = await runPrintManifest('mcp');

  assert.equal(manifest.name, '@hhszzzz/taibu-mcp');
  assert.equal(manifest.dependencies['@hhszzzz/taibu-core'], sourceCoreManifest.version);
  assert.equal(manifest.dependencies['taibu-core'], undefined);
  assert.equal(manifest.publishConfig.registry, 'https://npm.pkg.github.com');
  assert.deepEqual(manifest.repository, {
    type: 'git',
    url: 'https://github.com/hhszzzz/taibu.git',
  });
});

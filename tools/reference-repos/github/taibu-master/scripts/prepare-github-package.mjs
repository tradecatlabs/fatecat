import { cp, mkdir, readFile, rm, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

export const GITHUB_REGISTRY = 'https://npm.pkg.github.com';
export const GITHUB_REPOSITORY = {
  type: 'git',
  url: 'https://github.com/hhszzzz/taibu.git',
};
export const GITHUB_PACKAGE_TARGETS = {
  core: {
    sourceDir: 'packages/core',
    githubName: '@hhszzzz/taibu-core',
  },
  mcp: {
    sourceDir: 'packages/mcp',
    githubName: '@hhszzzz/taibu-mcp',
  },
};

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DEPENDENCY_FIELDS = [
  'dependencies',
  'devDependencies',
  'peerDependencies',
  'optionalDependencies',
];

function cloneJson(value) {
  return JSON.parse(JSON.stringify(value));
}

async function readJson(filePath) {
  return JSON.parse(await readFile(filePath, 'utf8'));
}

async function pathExists(filePath) {
  try {
    await stat(filePath);
    return true;
  } catch (error) {
    if (error && typeof error === 'object' && 'code' in error && error.code === 'ENOENT') {
      return false;
    }
    throw error;
  }
}

function rewriteDependencyBlock(block, workspacePackageMap) {
  if (!block) {
    return block;
  }

  const nextBlock = {};

  for (const [dependencyName, dependencyVersion] of Object.entries(block)) {
    const workspacePackage = workspacePackageMap[dependencyName];

    if (!workspacePackage) {
      nextBlock[dependencyName] = dependencyVersion;
      continue;
    }

    const nextVersion = dependencyVersion.startsWith('workspace:')
      ? workspacePackage.version
      : dependencyVersion;

    nextBlock[workspacePackage.githubName] = nextVersion;
  }

  return nextBlock;
}

export function buildGitHubPackageManifest({
  manifest,
  githubName,
  workspacePackageMap,
}) {
  const nextManifest = cloneJson(manifest);

  nextManifest.name = githubName;
  nextManifest.repository = cloneJson(GITHUB_REPOSITORY);
  nextManifest.publishConfig = {
    ...(nextManifest.publishConfig ?? {}),
    registry: GITHUB_REGISTRY,
  };

  for (const fieldName of DEPENDENCY_FIELDS) {
    if (nextManifest[fieldName]) {
      nextManifest[fieldName] = rewriteDependencyBlock(
        nextManifest[fieldName],
        workspacePackageMap,
      );
    }
  }

  return nextManifest;
}

async function buildWorkspacePackageMap(repoRoot) {
  const entries = await Promise.all(
    Object.entries(GITHUB_PACKAGE_TARGETS).map(async ([packageKey, target]) => {
      const manifest = await readJson(path.join(repoRoot, target.sourceDir, 'package.json'));
      return [
        packageKey,
        {
          sourceName: manifest.name,
          version: manifest.version,
          githubName: target.githubName,
          sourceDir: target.sourceDir,
        },
      ];
    }),
  );

  return Object.fromEntries(entries);
}

function toWorkspaceDependencyMap(packageMap) {
  return Object.fromEntries(
    Object.values(packageMap).map((entry) => [
      entry.sourceName,
      {
        version: entry.version,
        githubName: entry.githubName,
      },
    ]),
  );
}

export async function getGitHubPackageManifest(packageKey, repoRoot = REPO_ROOT) {
  const target = GITHUB_PACKAGE_TARGETS[packageKey];
  if (!target) {
    throw new Error(`Unknown package key: ${packageKey}`);
  }

  const packageMap = await buildWorkspacePackageMap(repoRoot);
  const workspacePackageMap = toWorkspaceDependencyMap(packageMap);
  const manifest = await readJson(path.join(repoRoot, target.sourceDir, 'package.json'));

  return buildGitHubPackageManifest({
    manifest,
    githubName: target.githubName,
    workspacePackageMap,
  });
}

export async function prepareGitHubPackage({
  packageKey,
  outputRoot,
  repoRoot = REPO_ROOT,
}) {
  if (!outputRoot) {
    throw new Error('outputRoot is required');
  }

  const target = GITHUB_PACKAGE_TARGETS[packageKey];
  if (!target) {
    throw new Error(`Unknown package key: ${packageKey}`);
  }

  const manifest = await getGitHubPackageManifest(packageKey, repoRoot);
  const sourceDir = path.join(repoRoot, target.sourceDir);
  const outputDir = path.resolve(repoRoot, outputRoot, packageKey);
  const distSource = path.join(sourceDir, 'dist');

  if (!(await pathExists(distSource))) {
    throw new Error(`Missing built dist for ${target.sourceDir}. Run pnpm -C ${target.sourceDir} build first.`);
  }

  await rm(outputDir, { recursive: true, force: true });
  await mkdir(outputDir, { recursive: true });
  await cp(distSource, path.join(outputDir, 'dist'), { recursive: true });

  const readmeSource = path.join(sourceDir, 'README.md');
  if (await pathExists(readmeSource)) {
    await cp(readmeSource, path.join(outputDir, 'README.md'));
  }

  const localLicenseSource = path.join(sourceDir, 'LICENSE');
  const licenseSource = await pathExists(localLicenseSource)
    ? localLicenseSource
    : path.join(repoRoot, 'LICENSE');
  if (await pathExists(licenseSource)) {
    await cp(licenseSource, path.join(outputDir, 'LICENSE'));
  }

  await writeFile(
    path.join(outputDir, 'package.json'),
    `${JSON.stringify(manifest, null, 2)}\n`,
    'utf8',
  );

  return {
    outputDir,
    manifest,
  };
}

function parseArgs(argv) {
  const args = {
    packages: [],
    output: null,
    printManifest: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];

    if (arg === '--package') {
      args.packages.push(argv[index + 1]);
      index += 1;
      continue;
    }

    if (arg === '--output') {
      args.output = argv[index + 1];
      index += 1;
      continue;
    }

    if (arg === '--print-manifest') {
      args.printManifest = true;
      continue;
    }

    throw new Error(`Unknown argument: ${arg}`);
  }

  if (args.packages.length === 0) {
    throw new Error('At least one --package is required');
  }

  if (args.printManifest && args.packages.length !== 1) {
    throw new Error('--print-manifest requires exactly one --package');
  }

  if (!args.printManifest && !args.output) {
    throw new Error('--output is required unless --print-manifest is used');
  }

  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.printManifest) {
    const manifest = await getGitHubPackageManifest(args.packages[0]);
    process.stdout.write(`${JSON.stringify(manifest, null, 2)}\n`);
    return;
  }

  for (const packageKey of args.packages) {
    const { outputDir } = await prepareGitHubPackage({
      packageKey,
      outputRoot: args.output,
    });
    process.stderr.write(`Prepared ${packageKey} -> ${outputDir}\n`);
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = 1;
  });
}

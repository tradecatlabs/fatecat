import crypto from 'crypto';

const UINT32_MAX_PLUS_ONE = 0x1_0000_0000;

function seedToUint32(seed: string): number {
  const hash = crypto.createHash('sha256').update(seed).digest();
  const value = hash.readUInt32BE(0);
  return value === 0 ? 0x9e3779b9 : value;
}

export function createSeededRng(seed: string): () => number {
  let state = seedToUint32(seed);

  return () => {
    // xorshift32
    state ^= state << 13;
    state ^= state >>> 17;
    state ^= state << 5;
    return (state >>> 0) / UINT32_MAX_PLUS_ONE;
  };
}

function hashSeed(input: string): string {
  return crypto.createHash('sha256').update(input).digest('hex').slice(0, 24);
}

export function resolveSeed(
  inputSeed: string | undefined,
  fallback: string,
  scope?: string
): string {
  const normalized = inputSeed?.trim();
  const base = normalized || hashSeed(fallback);
  const scoped = scope?.trim();
  if (!scoped) return base;
  return hashSeed(`${scoped}|${base}`);
}

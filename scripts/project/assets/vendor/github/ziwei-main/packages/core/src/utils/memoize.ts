// biome-ignore-all lint/suspicious/noExplicitAny: false positive
// biome-ignore-all lint/style/noNonNullAssertion: false positive
export function memoize<F extends (...args: any) => any>(
  fn: F,
  options: {
    cache?: MemoizeCache<any, ReturnType<F>>;
    getCacheKey?: (args: Parameters<F>[0]) => unknown;
  } = {},
): F & { cache: MemoizeCache<any, ReturnType<F>> } {
  const { cache = new Map<unknown, ReturnType<F>>(), getCacheKey } = options;

  const memoizedFn = function (this: unknown, arg: Parameters<F>[0]): ReturnType<F> {
    const key = getCacheKey ? getCacheKey(arg) : arg;

    if (cache.has(key)) {
      return cache.get(key)!;
    }

    const result = fn.call(this, arg);

    cache.set(key, result);

    return result;
  };

  memoizedFn.cache = cache;

  return memoizedFn as F & { cache: MemoizeCache<any, ReturnType<F>> };
}
export interface MemoizeCache<K, V> {
  set(key: K, value: V): void;
  get(key: K): V | undefined;
  has(key: K): boolean;
  delete(key: K): boolean | undefined;
  clear(): void;
  size: number;
}

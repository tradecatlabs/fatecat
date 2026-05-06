import { type GlobalConfigs, getGlobalConfigs } from "../infra/configs";
import { createZiWeiI18n } from "../infra/i18n";

export interface ZiWeiRuntimeOptions {
  i18n?: ReturnType<typeof createZiWeiI18n>;
  configs?: GlobalConfigs;
  now?: () => Date;
}

export function createZiWeiRuntime(options: ZiWeiRuntimeOptions = {}) {
  return {
    i18n: options.i18n ?? createZiWeiI18n(),
    configs: options.configs ?? getGlobalConfigs(),
    now: options.now ?? (() => new Date()),
  };
}

export type ZiWeiRuntime = ReturnType<typeof createZiWeiRuntime>;

export interface ResolveZiWeiRuntimeOptions extends ZiWeiRuntimeOptions {
  runtime?: ZiWeiRuntime;
}

export function resolveZiWeiRuntime(options?: ResolveZiWeiRuntimeOptions): ZiWeiRuntime {
  if (!options) {
    return defaultRuntime;
  }

  const { runtime, ...runtimeOptions } = options;
  return runtime ?? createZiWeiRuntime(runtimeOptions);
}

export function withRuntime<R>(
  fn: (runtime: ZiWeiRuntime) => R,
  options?: ResolveZiWeiRuntimeOptions,
) {
  const runtime = resolveZiWeiRuntime(options);
  return fn(runtime);
}

export const defaultRuntime: ZiWeiRuntime = createZiWeiRuntime();

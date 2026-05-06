import type {
  CreateZiWeiByStemBranchParams,
  CreateZiWeiLunisolarParams,
  CreateZiWeiSolarParams,
} from "./typings";

import {
  createZiWeiRuntime,
  type ResolveZiWeiRuntimeOptions,
  resolveZiWeiRuntime,
  withRuntime,
  type ZiWeiRuntime,
  type ZiWeiRuntimeOptions,
} from "./context";
import {
  calculateNatalByLunisolar,
  calculateNatalBySolar,
  calculateNatalByStemBranch,
} from "./pipelines/natal";

type CreateZiWeiOptions = ResolveZiWeiRuntimeOptions;

export { createZiWeiRuntime, type ZiWeiRuntime, type ZiWeiRuntimeOptions };

export function withZiWeiRuntime(options?: CreateZiWeiOptions) {
  const runtime = resolveZiWeiRuntime(options);
  return {
    createZiWeiBySolar: (params: CreateZiWeiSolarParams) => calculateNatalBySolar(params)(runtime),
    createZiWeiByLunisolar: (params: CreateZiWeiLunisolarParams) =>
      calculateNatalByLunisolar(params)(runtime),
  };
}

export function createZiWeiBySolar(params: CreateZiWeiSolarParams, options?: CreateZiWeiOptions) {
  return withRuntime(calculateNatalBySolar(params), options);
}

export function createZiWeiByLunisolar(
  params: CreateZiWeiLunisolarParams,
  options?: CreateZiWeiOptions,
) {
  return withRuntime(calculateNatalByLunisolar(params), options);
}

export function createZiWeiByStemBranch(
  params: CreateZiWeiByStemBranchParams,
  options?: CreateZiWeiOptions,
) {
  return withRuntime(calculateNatalByStemBranch(params), options);
}

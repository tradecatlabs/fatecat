import type { PalaceKey, StarKey } from "@ziweijs/core";

import { useState } from "react";

import { createContainer } from "../tools/hooks";

export function useRuntime() {
  const [flyingTransformations, setFlyingTransformations] = useState<StarKey[]>([]);
  const [flyingPalaceKey, setFlyingPalaceKey] = useState<PalaceKey>();

  return {
    flyingTransformations,
    setFlyingTransformations,
    flyingPalaceKey,
    setFlyingPalaceKey,
  };
}

export const RuntimeContainer = createContainer(useRuntime);

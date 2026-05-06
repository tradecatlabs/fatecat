import { type BranchKey, createZiWeiByStemBranch, type Locale, type StemKey } from "@ziweijs/core";
import { useState } from "react";

import type { ZiWeiSimulatorOptions } from "./typings";

import DestinyBoard from "./components/DestinyBoard";
import { ConfigContext, type ConfigContextProps } from "./context/config";
import { RenderContext, useRender } from "./context/render";
import { useConfig } from "./hooks/useConfig";
import { RuntimeContainer } from "./hooks/useRuntime";

export interface ZiWeiSimulatorProps {
  side: number;
  ziweiBranchKey: BranchKey;
  birthYearStemKey: StemKey;
  mainPalaceBranchKey: BranchKey;
  language?: Locale;
  options?: ZiWeiSimulatorOptions;
  config?: Partial<ConfigContextProps>;
}

export function ZiWeiSimulator({
  side,
  ziweiBranchKey,
  birthYearStemKey,
  mainPalaceBranchKey,
  language,
  options,
  config: _config,
}: ZiWeiSimulatorProps) {
  const config = useConfig({ side, ..._config });

  const render = useRender(options);

  const [palaces] = useState(() =>
    createZiWeiByStemBranch({
      birthYearStemKey,
      branchKey: ziweiBranchKey,
      mainPalaceBranchKey,
      language,
    }),
  );

  return (
    <ConfigContext value={config}>
      <RenderContext value={render}>
        <RuntimeContainer.Provider>
          <DestinyBoard side={side} palaces={palaces} decade={[]} decadeIndex={0} />
        </RuntimeContainer.Provider>
      </RenderContext>
    </ConfigContext>
  );
}

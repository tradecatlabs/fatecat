import { createZiWeiByLunisolar, type GenderKey, type Locale } from "@ziweijs/core";
import { useState } from "react";

import DestinyBoard from "./components/DestinyBoard";
import { ConfigContext } from "./context/config";
import { useConfig } from "./hooks/useConfig";
import { RuntimeContainer } from "./hooks/useRuntime";

export interface ZiWeiProps {
  side?: number;
  name: string;
  date: string;
  gender: GenderKey;
  language?: Locale;
}

export default function ZiWei({ side = 600, name, date, gender, language }: ZiWeiProps) {
  const config = useConfig({ side });

  const [natal] = useState(() =>
    createZiWeiByLunisolar({
      name,
      date,
      gender,
      language,
    }),
  );

  return (
    <ConfigContext value={config}>
      <RuntimeContainer.Provider>
        <DestinyBoard
          side={side}
          palaces={natal.palaces}
          decade={natal.decade}
          decadeIndex={natal.decadeIndex}
        />
      </RuntimeContainer.Provider>
    </ConfigContext>
  );
}

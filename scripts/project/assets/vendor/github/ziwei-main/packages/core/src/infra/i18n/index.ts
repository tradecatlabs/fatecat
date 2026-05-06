import { createI18n } from "@ziweijs/i18n";

import type { Locale } from "../../typings";

import ZH_HANS from "./locales/zh-Hans";
import ZH_HANT from "./locales/zh-Hant";

export function createZiWeiI18n(lang: Locale = "zh-Hans") {
  return createI18n({
    lang,
    resources: {
      "zh-Hans": ZH_HANS,
      "zh-Hant": ZH_HANT,
    },
  });
}

export const i18n = createZiWeiI18n();

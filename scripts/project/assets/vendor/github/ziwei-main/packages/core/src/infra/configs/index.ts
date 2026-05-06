import { merge } from "remeda";

import type { DeepPartial } from "../../typings";

export interface GlobalConfigs {
  /** 分界点配置 */
  division: DivisionConfig;
  star: StarConfig;
}

export interface DivisionConfig {
  /**
   * 年分界点参数，默认为正月初一分界。
   *
   * - normal：正月初一分界
   * - spring：立春分界
   */
  year: "normal" | "spring";

  /**
   * 月分界点参数，默认为月中分界。
   *
   * - normal：正月中分界
   * - last：视为上月
   * - next：视为下月
   */
  month: "normal" | "last" | "next";

  /**
   * 日分界点参数，默认为子时为次日。
   *
   * - normal：子时为次日
   * - current：当前子时为当日
   */
  day: "normal" | "current";
}

export type StarConfig = "normal" | "onlyMajor" | "onlyTransformation";

const DEFAULT_GLOBAL_CONFIGS: GlobalConfigs = {
  division: {
    year: "normal",
    month: "normal",
    day: "normal",
  },
  star: "normal",
};

export function getGlobalConfigs(configs?: DeepPartial<GlobalConfigs>): GlobalConfigs {
  return merge(DEFAULT_GLOBAL_CONFIGS, configs);
}

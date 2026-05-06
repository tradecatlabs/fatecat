import type { Palace, PalaceProps } from "../typings";

import { STEM_TRANSFORMATIONS } from "../constants";

export function createPalace(props: PalaceProps): Palace {
  return {
    ...props,
    flying() {
      return STEM_TRANSFORMATIONS[props.stem.key];
    },
  };
}

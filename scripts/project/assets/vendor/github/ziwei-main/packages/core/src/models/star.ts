import type { Star, StarProps } from "../typings";

export function createStar(props: StarProps): Star {
  return {
    ...props,
  };
}

import { use, useMemo } from "react";

import { ConfigContext } from "../context/config";

export function useCentripetal() {
  const { fontSize, palaceSide, palaceStrokeWidth } = use(ConfigContext);
  const _CP: Array<{
    points: [number, number][];
    text: {
      x: number;
      y: number;
    };
  }> = useMemo(
    () => [
      // 0
      {
        points: [
          [palaceSide * 3, -palaceSide * 2],
          [palaceSide + palaceStrokeWidth * 2, -palaceStrokeWidth * 2],
        ],
        text: {
          x: palaceSide + palaceStrokeWidth * 2 + fontSize * 1.5,
          y: -palaceStrokeWidth * 2 - fontSize / 3,
        },
      },
      // 1
      {
        points: [
          [palaceSide * 3 - palaceStrokeWidth, -palaceSide * 0.5 + palaceStrokeWidth],
          [palaceSide + palaceStrokeWidth * 2, palaceSide * 0.5 - palaceStrokeWidth * 1.5],
        ],
        text: {
          x: palaceSide + palaceStrokeWidth * 3 + fontSize,
          y: palaceSide * 0.5 - palaceStrokeWidth * 2 - fontSize,
        },
      },
      // 2
      {
        points: [
          [palaceSide * 3, palaceSide * 1.5],
          [palaceSide + palaceStrokeWidth * 2, palaceSide * 0.5 - palaceStrokeWidth],
        ],
        text: {
          x: palaceSide + palaceStrokeWidth * 2 + fontSize * 1.5,
          y: palaceSide * 0.5 - palaceStrokeWidth + fontSize / 3,
        },
      },

      // 3
      {
        points: [
          [palaceSide * 3, palaceSide * 3],
          [palaceSide + palaceStrokeWidth * 2, palaceSide + palaceStrokeWidth * 2],
        ],
        text: {
          x: palaceSide + palaceStrokeWidth * 2 + fontSize * 1.5,
          y: palaceSide + palaceStrokeWidth * 2 + fontSize,
        },
      },

      // 4
      {
        points: [
          [palaceSide * 1.5, palaceSide * 3],
          [palaceSide * 0.5 + palaceStrokeWidth * 2, palaceSide + palaceStrokeWidth * 2],
        ],
        text: {
          x: palaceSide * 0.5 + palaceStrokeWidth * 2 + fontSize * 1.5,
          y: palaceSide + palaceStrokeWidth * 2 + fontSize,
        },
      },
      // 5
      {
        points: [
          [-palaceSide * 0.5 - palaceStrokeWidth, palaceSide * 3],
          [palaceSide * 0.5 - palaceStrokeWidth * 1.5, palaceSide + palaceStrokeWidth * 2],
        ],
        text: {
          x: palaceSide * 0.5 + palaceStrokeWidth - fontSize * 1.5,
          y: palaceSide + palaceStrokeWidth * 2 + fontSize,
        },
      },
      // 6
      {
        points: [
          [-palaceSide * 2, palaceSide * 3],
          [-palaceStrokeWidth * 2, palaceSide + palaceStrokeWidth * 2],
        ],
        text: {
          x: -palaceStrokeWidth * 2 - fontSize * 1.5,
          y: palaceSide + palaceStrokeWidth * 2 + fontSize,
        },
      },

      // 7
      {
        points: [
          [-palaceSide * 2 + palaceStrokeWidth, palaceSide * 1.5 - palaceStrokeWidth],
          [-palaceStrokeWidth * 2, palaceSide * 0.5 + palaceStrokeWidth * 1.5],
        ],
        text: {
          x: -palaceStrokeWidth * 2 - fontSize * 1.5,
          y: palaceSide * 0.5 + palaceStrokeWidth * 2,
        },
      },

      // 8
      {
        points: [
          [-palaceSide * 2 + palaceStrokeWidth, -palaceSide * 0.5 - palaceStrokeWidth * 1.5],
          [-palaceStrokeWidth * 2, palaceSide * 0.5 - palaceStrokeWidth],
        ],
        text: {
          x: -palaceStrokeWidth * 3 - fontSize * 0.7,
          y: palaceSide * 0.5 - palaceStrokeWidth - fontSize,
        },
      },
      // 9
      {
        points: [
          [-palaceSide * 2 + palaceStrokeWidth, -palaceSide * 2 + palaceStrokeWidth],
          [-palaceStrokeWidth * 2, -palaceStrokeWidth * 2],
        ],
        text: {
          x: -palaceStrokeWidth * 2 - fontSize / 2,
          y: -palaceStrokeWidth * 2 - palaceStrokeWidth - fontSize,
        },
      },
      // 10
      {
        points: [
          [-palaceSide * 0.5 + palaceStrokeWidth * 1.5, -palaceSide * 2 + palaceStrokeWidth],
          [palaceSide * 0.5 - palaceStrokeWidth * 1, -palaceStrokeWidth * 2],
        ],
        text: {
          x: palaceSide * 0.5 - fontSize * 1.5,
          y: -palaceStrokeWidth * 2 - fontSize / 3,
        },
      },
      // 11
      {
        points: [
          [palaceSide * 1.5 - palaceStrokeWidth, -palaceSide * 2 + palaceStrokeWidth],
          [palaceSide * 0.5, -palaceStrokeWidth * 2],
        ],
        text: {
          x: palaceSide * 0.5 + fontSize * 1.5,
          y: -palaceStrokeWidth * 2 - fontSize / 3,
        },
      },
    ],
    [palaceSide, fontSize, palaceStrokeWidth],
  );

  return _CP;
}

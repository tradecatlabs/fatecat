import { useCallback, useMemo } from "react";

import type { ConfigContextProps } from "../context/config";

import { colorPalette } from "../theme/color";

export interface UseConfigProps extends Partial<ConfigContextProps> {
  side: number;
}

export function useConfig({ side, ...props }: UseConfigProps) {
  const $n = useCallback(
    (n: number) => {
      return (n / 600) * side;
    },
    [side],
  );

  const config = useMemo<ConfigContextProps>(() => {
    const padding = $n(20);
    const [boardSide, boardPadding, boardStrokeWidth] = [side - padding * 2, $n(10), $n(6)];
    const [palaceSide, palacePadding, palaceStrokeWidth] = [
      (boardSide - boardPadding * 2) / 4,
      $n(4),
      $n(2),
    ];
    const [verticalRectWidth, verticalRectHeight] = [palaceSide / 6, palaceSide / 3];

    const centralPalaceSide = palaceSide * 2 - palaceStrokeWidth * 2;
    const centralPalaceX = padding + boardPadding + palaceSide + palaceStrokeWidth;
    const centralPalaceY = centralPalaceX;

    return {
      padding,
      boardSide,
      boardFill: colorPalette.w1,
      boardStroke: colorPalette.b1,
      boardStrokeWidth,
      boardPadding,
      boardX: padding,
      boardY: padding,
      palaceSide,
      palacePadding,
      palaceStrokeWidth,
      palaceFlyFill: colorPalette.w5,
      palaceHoroscopeFill: colorPalette.w8,
      fontSize: $n(16),
      fontColor: colorPalette.b1,
      fontLineHeight: 1.1875,
      horizontalRectWidth: palaceSide - verticalRectWidth * 2,
      horizontalRectHeight: verticalRectWidth,
      verticalRectWidth,
      verticalRectHeight,
      horoscopeRangesFontSize: $n(12),
      selfTransformationFontSize: $n(14),
      selfTransformationStroke: colorPalette.r2,
      selfTransformationMarginTop: 2,
      laiYinFlagWidth: $n(22),
      laiYinFlagHeight: $n(38),
      laiYinFlagFontSize: $n(10),
      laiYinFlagStroke: colorPalette.r2,
      laiYinFlagStrokeWidth: $n(0),
      laiYinFlagX: $n(2),
      laiYinFlagY: $n(2),
      laiYinFlagFill: "transparent",
      laiYinFlagFontColor: colorPalette.r2,
      palaceRectStrokeWidth: $n(2),
      arrowWidth: $n(2),
      arrowSize: $n(2),
      // Star
      ziweiColor: colorPalette.p1,
      ziweiPalaceFill: "transparent",
      minorStarColor: colorPalette.p3,
      flyingTransformationFill: [
        colorPalette.c5,
        colorPalette.p1,
        colorPalette.l3,
        colorPalette.r1,
      ],
      flyingTransformationColor: colorPalette.w1,
      yearlyFontSize: $n(10),
      centralPalaceSide,
      centralPalacePadding: $n(20),
      centralPalaceX,
      centralPalaceY,
      centralPalaceFontSize: $n(12),
      centralPalaceVersionFontSize: $n(10),
    };
  }, [side, $n]);

  return { ...config, ...props };
}

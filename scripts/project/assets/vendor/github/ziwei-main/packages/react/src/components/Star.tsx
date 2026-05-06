import type { Palace, StarProps as ZiWeiStarProps } from "@ziweijs/core";

import { memo, use } from "react";

import { ConfigContext } from "../context/config";
import { RenderContext } from "../context/render";
import { RuntimeContainer } from "../hooks/useRuntime";
import {
  computeBaseMetrics,
  computeExitArrowLayout,
  orientationFromPalaceIndex,
} from "../tools/starUtil";
import ArrowLine from "./ArrowLine";

export interface StarProps extends ZiWeiStarProps {
  index: number;
  x: number;
  y: number;
  fill?: string;
  palace: Palace;
  starKey: ZiWeiStarProps["key"];
}

function Star({ index, x, y, name, fill, palace, starKey, YT, ST }: StarProps) {
  const {
    palaceSide,
    palacePadding,
    palaceStrokeWidth,
    selfTransformationFontSize,
    fontSize,
    boardStrokeWidth,
    boardPadding,
    selfTransformationStroke,
    selfTransformationMarginTop,
    fontLineHeight,
    arrowSize,
    flyingTransformationFill,
    flyingTransformationColor,
  } = use(ConfigContext);
  const { showTransformation, showSelf } = use(RenderContext);
  const { flyingTransformations } = RuntimeContainer.useContainer();

  // Base metrics needed by multiple elements
  const { width, height, padding, centerX } = computeBaseMetrics({
    x,
    fontSize,
    fontLineHeight,
    palaceStrokeWidth,
  });
  const flyingIndex = flyingTransformations.indexOf(starKey);
  const hasFlying = flyingIndex !== -1;
  const highlightFill = hasFlying ? flyingTransformationFill[flyingIndex] : undefined;
  const exitKey = ST?.exit?.key;
  const orientation = orientationFromPalaceIndex(palace.index);
  const exitLayout =
    ST?.exit &&
    computeExitArrowLayout({
      x,
      y,
      index,
      orientation,
      fontSize,
      fontLineHeight,
      palaceStrokeWidth,
      selfTransformationMarginTop,
      palaceSide,
      boardStrokeWidth,
      boardPadding,
      selfTransformationFontSize,
      palacePadding,
    });

  console.log(starKey, ST?.exit);

  return (
    <g>
      {/* Background highlight for flying transformation; omit node entirely if not active */}
      {hasFlying && (
        <rect
          x={x}
          y={y}
          width={width}
          height={height + padding}
          fill={highlightFill}
          pointerEvents="none"
        />
      )}
      <text
        x={centerX}
        y={y + padding / 2}
        writingMode="vertical-rl"
        fontSize={fontSize}
        letterSpacing={0}
        wordSpacing={0}
        fill={hasFlying ? flyingTransformationColor : fill}
      >
        {name}
      </text>
      {/*生年四化*/}
      {showTransformation && YT?.key && (
        <text
          x={centerX}
          y={y + fontSize * 3 + padding / 2}
          fontSize={fontSize}
          letterSpacing={0}
          wordSpacing={0}
          textAnchor="middle"
          fill={selfTransformationStroke}
          fontWeight={900}
        >
          {YT.key}
        </text>
      )}
      {/*离心自化：根据宫位方向绘制箭头与标签 */}
      {showSelf && exitLayout && (
        <g>
          <ArrowLine
            points={exitLayout.points}
            arrowSize={arrowSize}
            stroke={selfTransformationStroke}
            strokeWidth={palaceStrokeWidth}
          />
          <text
            x={exitLayout.label.x}
            y={exitLayout.label.y}
            fontSize={selfTransformationFontSize}
            textAnchor="middle"
            fill={selfTransformationStroke}
          >
            {exitKey}
          </text>
        </g>
      )}
    </g>
  );
}

export default memo(Star);

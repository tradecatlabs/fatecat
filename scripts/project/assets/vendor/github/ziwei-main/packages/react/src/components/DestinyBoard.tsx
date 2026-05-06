import {
  type DecadeVO,
  i18n,
  type Palace as PalaceModel,
  type TransformationKey,
} from "@ziweijs/core";
import { Activity, use, useRef, useState } from "react";

import { ConfigContext } from "../context/config";
import { RenderContext } from "../context/render";
import { useCentripetal } from "../hooks/useCentripetal";
import { useCoordinates } from "../hooks/useCoordinates";
import { RuntimeContainer } from "../hooks/useRuntime";
import ArrowLine from "./ArrowLine";
import CentralPalace from "./CentralPalace";
import ContextMenu from "./ContextMenu";
import LaiYin from "./LaiYin";
import Palace from "./Palace";
import Stars from "./Stars";

export interface DestinyBoardProps {
  side: number;
  palaces: PalaceModel[];
  decade: DecadeVO[][];
  decadeIndex: number;
}

export default function DestinyBoard({ side = 600, palaces, ...props }: DestinyBoardProps) {
  const {
    boardSide,
    boardX,
    boardY,
    boardFill,
    boardStroke,
    boardStrokeWidth,
    palaceSide,
    palaceFlyFill,
    palaceHoroscopeFill,
    palacePadding,
    fontLineHeight,
    fontSize,
    horizontalRectWidth,
    horizontalRectHeight,
    verticalRectWidth,
    verticalRectHeight,
    horoscopeRangesFontSize,
    arrowWidth,
    palaceRectStrokeWidth,
    selfTransformationFontSize,
    selfTransformationStroke,
    laiYinFlagX,
    laiYinFlagY,
    arrowSize,
    yearlyFontSize,
    centralPalaceSide,
    centralPalaceX,
    centralPalaceY,
    ziweiPalaceFill,
  } = use(ConfigContext);

  const { showPalaceName, showStem, showBranch, showLaiYin, showSelf } = use(RenderContext);

  const [decadeIndex, setDecadeIndex] = useState<number>(props.decadeIndex);

  const [menuPosition, setMenuPosition] = useState({ x: 0, y: 0 });

  const ref = useRef(null);

  const selectedRef = useRef<number>(decadeIndex);

  const coordinates = useCoordinates();

  const { flyingPalaceKey, setFlyingPalaceKey, setFlyingTransformations } =
    RuntimeContainer.useContainer();

  const _CP = useCentripetal();

  const getPalaceFill = (palace: PalaceModel) => {
    const hasZiWei = palace.stars.some((star) => star.key === "ZiWei");
    if (flyingPalaceKey === palace.key) {
      return palaceFlyFill;
    }
    if (decadeIndex === palace.index) {
      return palaceHoroscopeFill;
    }
    if (hasZiWei) {
      return ziweiPalaceFill;
    }
    return boardFill;
  };

  return (
    <svg width={side} height={side} ref={ref}>
      <title>紫微斗数</title>
      <g>
        <rect width={side} height={side} fill={boardFill} />
        <rect
          x={boardX}
          y={boardY}
          width={boardSide}
          height={boardSide}
          fill={boardFill}
          stroke={boardStroke}
          strokeWidth={boardStrokeWidth}
          shapeRendering="crispEdges"
        />
        {palaces.map((palace, index) => {
          const currentTransformations = palace.stars.reduce<TransformationKey[]>(
            (result, star) => {
              if (star.ST?.entry) {
                result.push(star.ST.entry.key);
              }
              return result;
            },
            [],
          );
          const hasCP = currentTransformations.length > 0;
          return (
            <Palace
              key={palace.key}
              name={palace.name}
              width={palaceSide}
              height={palaceSide}
              x={coordinates[index].x}
              y={coordinates[index].y}
              fill={getPalaceFill(palace)}
              onClick={() => {
                if (flyingPalaceKey === palace.key) {
                  setFlyingTransformations([]);
                  setFlyingPalaceKey(undefined);
                } else {
                  setFlyingTransformations(palace.flying());
                  setFlyingPalaceKey(palace.key);
                }
              }}
              onContextMenu={(e) => {
                e.preventDefault();
                e.stopPropagation();
                selectedRef.current = index;
                setMenuPosition({ x: e.clientX, y: e.clientY });
              }}
              onLongPress={(e) => {
                if (e instanceof MouseEvent) {
                  selectedRef.current = index;
                  setMenuPosition({ x: e.clientX, y: e.clientY });
                }

                if (e instanceof TouchEvent) {
                  selectedRef.current = index;
                  setMenuPosition({
                    x: e.touches[0].clientX,
                    y: e.touches[0].clientY,
                  });
                }
              }}
            >
              {/* 宫位信息 */}
              {showLaiYin && palace.isLaiYin && <LaiYin x={laiYinFlagX} y={laiYinFlagY} type="D" />}
              {/* 宫位信息 - 干支 */}
              <g transform={`translate(0, ${verticalRectHeight * 2})`}>
                <title>干支</title>
                <rect
                  width={verticalRectWidth}
                  height={verticalRectHeight}
                  fill="transparent"
                  stroke={boardStroke}
                  strokeWidth={showBranch && showStem ? palaceRectStrokeWidth : 0}
                  shapeRendering="crispEdges"
                />
                <text
                  x={verticalRectWidth / 2}
                  y={horizontalRectHeight - fontSize}
                  writingMode="vertical-rl"
                  fontSize={fontSize}
                  letterSpacing={0}
                  wordSpacing={0}
                >
                  {showStem && palace.stem.name}
                  {showBranch && palace.branch.name}
                </text>
              </g>
              {/* 宫位信息 - 大限宫职 */}
              {showPalaceName && props.decade[decadeIndex]?.[index] && (
                <g transform={`translate(${verticalRectWidth}, ${verticalRectHeight * 2})`}>
                  <title>大限宫职</title>
                  <rect
                    width={horizontalRectWidth}
                    height={horizontalRectHeight}
                    fill="transparent"
                    stroke={boardStroke}
                    strokeWidth={palaceRectStrokeWidth}
                    shapeRendering="crispEdges"
                  />
                  <text
                    x={horizontalRectWidth / 2 - fontSize}
                    y={
                      fontSize * fontLineHeight -
                      (horizontalRectHeight - fontSize * fontLineHeight) / 2
                    }
                    fontSize={fontSize}
                    letterSpacing={0}
                    wordSpacing={0}
                  >
                    {props.decade[decadeIndex][index].name}
                  </text>
                </g>
              )}
              {/* 宫位信息 - 运限间隔 */}
              {palace.decadeRanges.length > 0 && (
                <g transform={`translate(${verticalRectWidth}, ${verticalRectHeight * 2.5})`}>
                  <title>运限间隔</title>
                  <rect
                    width={horizontalRectWidth}
                    height={horizontalRectHeight}
                    fill="transparent"
                    stroke={boardStroke}
                    strokeWidth={palaceRectStrokeWidth}
                    shapeRendering="crispEdges"
                  />
                  <text
                    x={horizontalRectWidth / 2}
                    y={horizontalRectHeight / 2 + fontLineHeight}
                    textAnchor="middle"
                    dominantBaseline="middle"
                    fontSize={horoscopeRangesFontSize}
                    letterSpacing={0}
                    wordSpacing={0}
                  >
                    {palace.decadeRanges.join(" ~ ")}
                  </text>
                </g>
              )}
              {/* 宫位信息 - 原局宫职 */}
              {showPalaceName && (
                <g transform={`translate(${verticalRectWidth * 5}, ${verticalRectHeight * 2})`}>
                  <title>干支</title>
                  <rect
                    width={verticalRectWidth}
                    height={verticalRectHeight}
                    fill="transparent"
                    stroke={boardStroke}
                    strokeWidth={palaceRectStrokeWidth}
                    shapeRendering="crispEdges"
                  />
                  <text
                    x={verticalRectWidth / 2}
                    y={horizontalRectHeight - fontSize}
                    writingMode="vertical-rl"
                    fontSize={fontSize}
                    letterSpacing={0}
                    wordSpacing={0}
                  >
                    {palace.name}
                  </text>
                </g>
              )}
              {/* 流年 */}
              {props.decade[decadeIndex]?.[index]?.yearly?.age > 0 && (
                <text
                  x={palaceSide / 2}
                  y={verticalRectHeight * 2 - yearlyFontSize / 2}
                  fontSize={yearlyFontSize}
                  letterSpacing={0}
                  wordSpacing={0}
                  textAnchor="middle"
                >
                  {`${props.decade[decadeIndex][index].yearly.name}${i18n.$t("year")}${props.decade[decadeIndex][index].yearly.age}${i18n.$t("age")}`}
                </text>
              )}
              {/* 星辰信息 */}
              <Stars
                x={palaceSide - palacePadding - fontSize * fontLineHeight}
                y={palacePadding}
                palace={palace}
                data={palace.stars}
              />
              {/* 向心自化部分 */}
              {showSelf && hasCP && _CP[index] && (
                <g>
                  <ArrowLine
                    points={_CP[index].points}
                    arrowSize={arrowSize}
                    stroke={selfTransformationStroke}
                    strokeWidth={arrowWidth}
                  />
                  <text
                    x={_CP[index].text.x}
                    y={_CP[index].text.y}
                    fontSize={selfTransformationFontSize}
                    fill={selfTransformationStroke}
                    textAnchor="middle"
                  >
                    {currentTransformations.join("")}
                  </text>
                </g>
              )}
            </Palace>
          );
        })}
        <CentralPalace
          x={centralPalaceX}
          y={centralPalaceY}
          width={centralPalaceSide}
          height={centralPalaceSide}
        />
      </g>
      <Activity mode={menuPosition.x > 0 && menuPosition.y > 0 ? "visible" : "hidden"}>
        <ContextMenu
          x={menuPosition.x}
          y={menuPosition.y}
          menuItems={[
            {
              label: "入限",
              onClick: () => {
                setDecadeIndex(selectedRef.current);
              },
            },
          ]}
          onClose={() => {
            setMenuPosition({ x: 0, y: 0 });
          }}
        />
      </Activity>
    </svg>
  );
}

// Utilities for Star component: pure functions for orientation and coordinates
export type Orientation = "left" | "right" | "top" | "bottom";

// Lookup table for palace index (0..11) -> orientation
// bottom: [0, 11, 10, 9], left: [1, 2], top: [3, 4, 5, 6], right: [7, 8]
export const ORIENTATION_LOOKUP: Orientation[] = [
  "bottom", // 0
  "left", // 1
  "left", // 2
  "top", // 3
  "top", // 4
  "top", // 5
  "top", // 6
  "right", // 7
  "right", // 8
  "bottom", // 9
  "bottom", // 10
  "bottom", // 11
];

export function orientationFromPalaceIndex(index: number): Orientation {
  // Clamp to a safe range to avoid undefined; default to 'top'
  return ORIENTATION_LOOKUP[index] ?? "top";
}

export interface BaseMetricsInput {
  x: number;
  fontSize: number;
  fontLineHeight: number;
  palaceStrokeWidth: number;
}

export interface BaseMetrics {
  width: number;
  height: number;
  padding: number;
  centerX: number;
}

// Basic text block metrics for a star cell
export function computeBaseMetrics({
  x,
  fontSize,
  fontLineHeight,
  palaceStrokeWidth,
}: BaseMetricsInput): BaseMetrics {
  const width = fontSize * fontLineHeight;
  const height = fontSize * 2;
  const padding = palaceStrokeWidth * 2;
  const centerX = x + width / 2;
  return { width, height, padding, centerX };
}

export interface ExitArrowInput extends BaseMetricsInput {
  y: number;
  index: number;
  orientation: Orientation;
  selfTransformationMarginTop: number;
  palaceSide: number;
  boardStrokeWidth: number;
  boardPadding: number;
  selfTransformationFontSize: number;
  palacePadding: number;
}

export interface ExitArrowLayout {
  points: [number, number][];
  label: { x: number; y: number };
}

// Tunable factors for label optical alignment
export const SIDE_LABEL_OFFSET_FACTOR = 0.7;
export const BOTTOM_LABEL_OFFSET_FACTOR = 0.7285;

// Compute arrow polyline points and label position for self-transformation "exit"
export function computeExitArrowLayout(input: ExitArrowInput): ExitArrowLayout {
  const {
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
  } = input;

  const { height, padding, centerX } = computeBaseMetrics({
    x,
    fontSize,
    fontLineHeight,
    palaceStrokeWidth,
  });

  const startY = y + height + selfTransformationMarginTop + padding;
  const lrArrowY = y + fontSize * (2 + 1.5 + SIDE_LABEL_OFFSET_FACTOR * index);
  const halfExitChar = (SIDE_LABEL_OFFSET_FACTOR * selfTransformationFontSize) / 2;

  switch (orientation) {
    case "left":
      return {
        points: [
          [centerX, startY],
          [centerX, lrArrowY],
          [-boardStrokeWidth, lrArrowY],
        ],
        label: {
          x: 0 - boardStrokeWidth - boardPadding - halfExitChar,
          y: lrArrowY + halfExitChar,
        },
      };
    case "right":
      return {
        points: [
          [centerX, startY],
          [centerX, lrArrowY],
          [palaceSide + boardStrokeWidth, lrArrowY],
        ],
        label: {
          x: palaceSide + boardStrokeWidth + boardPadding + halfExitChar,
          y: lrArrowY + halfExitChar,
        },
      };
    case "top":
      return {
        points: [
          [centerX, y - selfTransformationMarginTop],
          [centerX, y - palacePadding - boardStrokeWidth],
        ],
        label: {
          x: centerX,
          y: y - palacePadding - boardStrokeWidth - boardPadding,
        },
      };
    default:
      return {
        points: [
          [centerX, startY],
          [centerX, palaceSide + boardStrokeWidth],
        ],
        label: {
          x: centerX,
          y:
            palaceSide +
            boardPadding +
            boardStrokeWidth +
            BOTTOM_LABEL_OFFSET_FACTOR * selfTransformationFontSize,
        },
      };
  }
}

// Public exports
export default {
  orientationFromPalaceIndex,
  computeBaseMetrics,
  computeExitArrowLayout,
  SIDE_LABEL_OFFSET_FACTOR,
  BOTTOM_LABEL_OFFSET_FACTOR,
};

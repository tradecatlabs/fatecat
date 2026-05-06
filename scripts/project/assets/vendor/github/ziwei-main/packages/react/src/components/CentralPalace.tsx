export interface CentralBoardProps {
  width: number;
  height: number;
  x?: number;
  y?: number;
}

import { memo } from "react";

function CentralPalace({ width, height, x, y }: CentralBoardProps) {
  return (
    <svg x={x} y={y}>
      <title>中宫</title>
      <rect x="0" y="0" width={width} height={height} fill="transparent" />
    </svg>
  );
}

export default memo(CentralPalace);

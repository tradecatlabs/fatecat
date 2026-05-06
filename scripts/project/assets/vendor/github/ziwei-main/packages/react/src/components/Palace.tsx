import { useLongPress } from "ahooks";
import { type MouseEventHandler, memo, type PropsWithChildren, use, useRef } from "react";

import { ConfigContext } from "../context/config";

export interface PalaceProps {
  name: string;
  x: number;
  y: number;
  width: number;
  height: number;
  fill?: string;
  onClick?: (e: MouseEvent | TouchEvent) => void;
  onContextMenu?: MouseEventHandler<SVGSVGElement>;
  onLongPress?: (e: MouseEvent | TouchEvent) => void;
}

function Palace({
  name,
  x,
  y,
  width,
  height,
  fill = "#fff",
  children,
  onClick,
  onContextMenu,
  onLongPress,
}: PropsWithChildren<PalaceProps>) {
  const { palaceStrokeWidth } = use(ConfigContext);
  const ref = useRef(null);

  useLongPress(
    (e) => {
      onLongPress?.(e);
    },
    ref,
    {
      onClick,
    },
  );

  return (
    <svg
      x={x}
      y={y}
      ref={ref}
      overflow="visible"
      onKeyUp={() => {
        //
      }}
      onContextMenu={onContextMenu}
    >
      <title>{name}</title>
      <rect
        width={width}
        height={height}
        stroke="#000"
        strokeWidth={palaceStrokeWidth}
        shapeRendering="crispEdges"
        fill={fill}
      />
      {children}
    </svg>
  );
}

export default memo(Palace);

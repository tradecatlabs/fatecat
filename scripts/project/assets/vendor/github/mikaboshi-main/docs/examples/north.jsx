import React, { useRef, useMemo, useEffect, useCallback } from 'react';
import { compose, tap } from 'ramda';
import tw, { css } from 'twin.macro';
import Snap from 'snapsvg-cjs';

import { RADIAN_45, RADIAN_90, Z_INDEX_FENGSHUI_NORTH } from '@/constants';
import { int, rad_to_deg, normalize_angle, get_position } from '@/lib/utils';

import { useWorld } from '@/contexts/World';
import { useDeviceOrientation } from '@/contexts/DeviceOrientation';

const FILL_COLOR = '#ef4444';
const OUTER_RATIO = 0.8;
const INNER_RATIO = 0.7;
const ARROW_SIZE = (OUTER_RATIO - INNER_RATIO) * 0.5;

const wrapperStyle = css`
  ${tw`absolute w-full flex flex-col justify-center items-center`}
  z-index: ${Z_INDEX_FENGSHUI_NORTH};
`;

export const FengShuiNorth = () => {
  const { worldInfo: world } = useWorld();
  const deviceOrientation = useDeviceOrientation();

  const snap = useRef(null);

  const chart_w = world?.chart?.width;
  const chart_h = world?.chart?.height;
  const alpha = deviceOrientation?.alpha;

  const northStyle = useMemo(() => {
    const rotation = normalize_angle(alpha - rad_to_deg(Math.PI / 2));
    return css`
      width: ${chart_w}px;
      height: ${chart_h}px;
      transform: rotate(${rotation}deg);
    `;
  }, [chart_w, alpha]);

  //  A: rx,ry x-axis-rotation large-flag,sweep-flag end-x,end-y
  const draw = useCallback(
    ({ index }) => {
      const s = snap.current && Snap(snap.current);

      if (s) {
      }
    },
    [chart_w, chart_h]
  );

  useEffect(() => {
    const s = snap.current && Snap(snap.current);
    if (s) {
      const g = s.path('');
      g.remove();

      const pos = [];
      pos[0] = {
        x: INNER_RATIO,
        y: -ARROW_SIZE,
      };
      pos[1] = {
        x: OUTER_RATIO,
        y: 0,
      };
      pos[2] = {
        x: INNER_RATIO,
        y: ARROW_SIZE,
      };

      const path = [
        `M${pos[0].x},${pos[0].y}`,
        `L${pos[1].x},${pos[1].y}`,
        `L${pos[2].x},${pos[2].y}`,
        `L${pos[0].x},${pos[0].y}`,
      ].join(' ');

      s.path(path).attr({
        fill: FILL_COLOR,
      });
    }
  }, [chart_w, chart_h]);

  return (
    <div id="north-wrapper" css={wrapperStyle}>
      <svg id="north" ref={snap} viewBox="-1 -1 2 2" css={northStyle}></svg>
    </div>
  );
};

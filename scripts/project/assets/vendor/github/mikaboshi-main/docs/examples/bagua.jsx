import React, { useRef, useMemo, useEffect, useCallback } from 'react';
import { compose, tap } from 'ramda';
import tw, { css } from 'twin.macro';
import Snap from 'snapsvg-cjs';

import { RADIAN_45, RADIAN_90, Z_INDEX_FENGSHUI_BAGUA } from '@/constants';
import { int, rad_to_deg, normalize_angle, get_position } from '@/lib/utils';

import { useWorld } from '@/contexts/World';
import { useDeviceOrientation } from '@/contexts/DeviceOrientation';

const FILL_COLOR = '#ef4444';
const STROKE_COLOR = '#ffffff';
const OUTER_RATIO = 0.8;

const wrapperStyle = css`
  ${tw`absolute w-full flex flex-col justify-center items-center`}
  z-index: ${Z_INDEX_FENGSHUI_BAGUA};
`;

export const FengShuiBagua = () => {
  const { worldInfo: world } = useWorld();
  const deviceOrientation = useDeviceOrientation();

  const snap = useRef(null);

  const chart_w = world?.chart?.width;
  const chart_h = world?.chart?.height;
  const alpha = deviceOrientation?.alpha;

  const draw = useCallback(
    ({ index }) => {
      const s = snap.current && Snap(snap.current);

      if (s) {
        const beg = get_position(index * RADIAN_45, OUTER_RATIO);
        const end = get_position(index * RADIAN_45 + RADIAN_45, OUTER_RATIO);
        const large = end.deg - beg.deg > 180 ? 1 : 0;

        // Remember, the whole wrapper is rotated later
        // by 112.5 (= 90 + 45/2), degrees so that
        // the first slice which originally sits
        // at the 3 o'clock position will come
        // to the 12 o'clock position.
        //
        // Also, we apply `viewbox="-1 -1 2 2"` for the SVG,
        // meaning, the origin of SVG is situated
        // at the very center of the wrapper.
        // That is to say, we have `x = 0`.
        // When we have `x = 1`, it means `x` is reaching
        // all the way at the right edge of the wrapper.
        //
        // For each slice, we use SVG's arc function
        // which is defined as:
        //
        //   A rx ry x-axis-rotation large-arc-flag sweep-flag x y
        //
        // At first, we will first move (`M`) to where
        // it is close to the right edge of the screen.
        // If `OUTER_RATIO = 0.8`, it will probably
        // be like `M0.8,0`. Next, for the arc, we will
        // probably have `A0.8,0.8 0 0,1 0.56,0.56`.
        // So, it is an arc having `0.8` for the radius,
        // and it will draw the arc for 45 degrees.
        // Lastly, we have `L0,0` to go back to the origin,
        // otherwise, it won't fill (with given color)
        // the region surrounded by the path.

        const path = [
          `M${beg.x},${beg.y}`,
          `A${OUTER_RATIO},${OUTER_RATIO} 0 ${large},1 ${end.x},${end.y}`,
          `L0,0`,
        ].join(' ');

        const fill =
          index === 0
            ? {
                fill: FILL_COLOR,
              }
            : {};

        s.path(path).attr({
          ...fill,
          stroke: STROKE_COLOR,
          strokeWidth: world?.stroke_size,
        });
      }
    },
    [chart_w]
  );

  const baguaStyle = useMemo(() => {
    const rotation = normalize_angle(
      alpha - rad_to_deg(Math.PI / 2 + RADIAN_45 / 2)
    );
    return css`
      width: ${chart_w}px;
      height: ${chart_h}px;
      transform: rotate(${rotation}deg);
    `;
  }, [chart_w, alpha]);

  useEffect(() => {
    const s = snap.current && Snap(snap.current);
    if (s) {
      [...new Array(8)].map((_, i) => {
        draw({ index: i });
      });
    }
  }, [chart_w, draw]);

  return (
    <div id="bagua-wrapper" css={wrapperStyle}>
      <svg id="bagua" ref={snap} viewBox="-1 -1 2 2" css={baguaStyle}></svg>
    </div>
  );
};

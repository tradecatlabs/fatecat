import React, { useRef, useMemo, useEffect, useCallback } from 'react';
import { compose, tap } from 'ramda';
import tw, { css } from 'twin.macro';
import Snap from 'snapsvg-cjs';

import { RADIAN_15, Z_INDEX_FENGSHUI_ER_SHI_SI } from '@/constants';

import {
  rad_to_deg,
  deg_to_rad,
  normalize_angle,
  get_position,
} from '@/lib/utils';

import { TW_CUSTOM_COLORS } from '@/styles/shared';

import { useWorld } from '@/contexts/World';
import { useDeviceOrientation } from '@/contexts/DeviceOrientation';
import { useFengShui } from '@/contexts/FengShui';

const FILL_COLOR = '#303030';
const FILL_COLOR_DARK = '#000000';
const STROKE_COLOR = '#ffffff';

const wrapperStyle = css`
  ${tw`absolute w-full flex flex-col justify-center items-center`}
  z-index: ${Z_INDEX_FENGSHUI_ER_SHI_SI};
`;

export const FengShuiTwentyFour = () => {
  const { worldInfo: world } = useWorld();
  const deviceOrientation = useDeviceOrientation();
  const {
    ready,
    xiang_xing,
    get_twentyfour_direction_from_index,
    get_twentyfour_data_from_index,
  } = useFengShui();

  const snap = useRef(null);

  const chart_w = world?.chart?.width;
  const chart_h = world?.chart?.height;
  const alpha = deviceOrientation?.alpha || 0;

  const svgStyle = useMemo(() => {
    const rotation = normalize_angle(
      alpha - rad_to_deg(Math.PI / 2 + RADIAN_15 / 2)
    );

    return css`
      transform: rotate(${rotation}deg);
      width: ${chart_w}px;
      height: ${chart_h}px;
    `;
  }, [chart_w, alpha]);

  const draw = useCallback(
    ({ index }) => {
      const s = snap.current && Snap(snap.current);

      if (s && ready) {
        const beg = get_position(index * RADIAN_15);
        const end = get_position(index * RADIAN_15 + RADIAN_15);
        const large = end.deg - beg.deg > 180 ? 1 : 0;

        // Remember, the whole wrapper is rotated later
        // by 262.5 (= 90 + 15/2), degrees so that
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
        // A1,1 0 0,1 0.965,0.258
        //
        // At first, we will first move (`M`) to where
        // it is close to the right edge of the screen.
        // Since we have no ratio specified, and the SVG
        // will fill up the whole space for the wrapper,
        // we will have it being `M1,0`.
        // Next, for the arc, we will probably have
        // `A1,1 0 0,1 0.965,0.258`.
        // So, it is an arc having `1` for the radius,
        // and it will draw the arc for 15 degrees.
        // Lastly, we have `L0,0` to go back to the origin,
        // otherwise, it won't fill (with given color)
        // the region surrounded by the path.

        const path = [
          `M${beg.x},${beg.y}`,
          `A1,1 0 ${large},1 ${end.x},${end.y}`,
          `L0,0`,
        ].join(' ');

        const er_shi_si = get_twentyfour_data_from_index(index);
        const { direction, sector } =
          get_twentyfour_direction_from_index(index);

        let fill = er_shi_si[0] === 2 ? FILL_COLOR : FILL_COLOR_DARK;
        if (
          xiang_xing &&
          direction === xiang_xing.direction &&
          sector === xiang_xing.sector
        ) {
          fill = TW_CUSTOM_COLORS['abura-lightest'];
        }

        s.path(path).attr({
          fill,
          stroke: STROKE_COLOR,
          strokeWidth: world?.stroke_size,
        });
      }
    },
    [ready, chart_w, xiang_xing]
  );

  useEffect(() => {
    const s = snap.current && Snap(snap.current);
    if (s && ready) {
      [...new Array(24)].map((_, i) => {
        draw({ index: i });
      });
    }
  }, [ready, chart_w, xiang_xing, draw]);

  return (
    <div id="er-shi-si-wrapper" css={wrapperStyle}>
      <svg id="er-shi-si" ref={snap} viewBox="-1 -1 2 2" css={svgStyle}></svg>
    </div>
  );
};

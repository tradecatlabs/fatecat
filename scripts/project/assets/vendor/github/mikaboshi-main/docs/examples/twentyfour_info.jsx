import React, { useState, useMemo, useEffect, useCallback } from 'react';
import { compose, tap } from 'ramda';
import tw, { css } from 'twin.macro';

import { RADIAN_15, Z_INDEX_FENGSHUI_ER_SHI_SI_INFO } from '@/constants';

import {
  int,
  fixed,
  deg_to_rad,
  get_position_clock,
  gen_code_12,
} from '@/lib/utils';

import { useWorld } from '@/contexts/World';
import { useDeviceOrientation } from '@/contexts/DeviceOrientation';
import { useFengShui } from '@/contexts/FengShui';

const RATIO = 0.9;
const RADIAN_15_HALF = RADIAN_15 / 2;

const fix2 = fixed(2);

const boxBaseStyle = css`
  ${tw`absolute flex flex-col justify-center items-center`}
  line-height: 1em;
  transform: translate(-50%, -50%);
`;

const sectorStyle = css`
  font-size: 0.94em;
`;

export const FengShuiTwentyFourInfo = () => {
  const { worldInfo: world } = useWorld();
  const deviceOrientation = useDeviceOrientation();
  const {
    ready,
    xiang_xing,
    get_twentyfour_direction_from_index,
    get_twentyfour_direction_from_degrees,
    get_twentyfour_data_from_index,
  } = useFengShui();

  const [boxes, setBoxes] = useState([]);

  const chart_w = world?.chart?.width;
  const chart_h = world?.chart?.height;
  const alpha = deviceOrientation?.alpha || 0;

  const wrapperStyle = useMemo(
    () => css`
      ${tw`absolute text-white`}
      width: ${chart_w}px;
      height: ${chart_h}px;
    `,
    [chart_w]
  );

  const update = useCallback(
    index => {
      if (!ready) return;

      const z_index = Z_INDEX_FENGSHUI_ER_SHI_SI_INFO + index * 1;
      const chart_w_half = chart_w / 2;
      const chart_h_half = chart_h / 2;
      const angle = index * RADIAN_15 + deg_to_rad(alpha);
      const radius = chart_w_half * RATIO;

      const pos = get_position_clock(angle, radius, {
        x: chart_w_half,
        y: chart_h_half,
      });

      const { direction, sector } = get_twentyfour_direction_from_index(index);

      const color =
        xiang_xing &&
        direction === xiang_xing.direction &&
        sector === xiang_xing.sector
          ? 'color: #000000'
          : '';

      return {
        style: css`
          z-index: ${z_index};
          top: ${fix2(pos.y)}px;
          left: ${fix2(pos.x)}px;
          font-size: ${world?.text_base}px;
          ${color}
        `,
      };
    },
    [ready, chart_w, alpha, xiang_xing]
  );

  useEffect(() => {
    if (ready) {
      const arr = [...new Array(24)].map((_, i) => {
        const er_shi_si = get_twentyfour_data_from_index(i);
        const name = er_shi_si?.name;
        const degrees = i * 15;

        const { direction, sector } =
          get_twentyfour_direction_from_degrees(degrees);

        const text = name?.zh_cn?.alphabet || '';
        const text2 = `${direction.toUpperCase()}${sector}`;

        return {
          key: gen_code_12(),
          text,
          text2,
        };
      });

      setBoxes(arr);
    }
  }, [ready]);

  useEffect(() => {
    if (ready) {
      setBoxes(prev => prev.map((p, i) => ({ ...p, ...update(i) })));
    }
  }, [ready, chart_w, alpha, update]);

  return (
    <div id="er-shi-si-info-wrapper" css={wrapperStyle}>
      {boxes.map((box, i) => (
        <div
          id={`er-shi-si-info-box-${i}`}
          key={box.key}
          css={[boxBaseStyle, box.style]}
        >
          <div>{box.text}</div>
          <div css={sectorStyle}>{box.text2}</div>
        </div>
      ))}
    </div>
  );
};

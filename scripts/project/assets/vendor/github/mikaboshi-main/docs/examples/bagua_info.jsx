import React, {
  useRef,
  useState,
  useMemo,
  useEffect,
  useCallback,
} from 'react';
import { compose, tap } from 'ramda';
import tw, { css } from 'twin.macro';

import { RADIAN_45, RADIAN_90, Z_INDEX_FENGSHUI_BAGUA_INFO } from '@/constants';
import {
  fixed,
  deg_to_rad,
  get_position_clock,
  gen_code_12,
} from '@/lib/utils';

import { useWorld } from '@/contexts/World';
import { useDeviceOrientation } from '@/contexts/DeviceOrientation';
import { useFengShui } from '@/contexts/FengShui';
import { BaguaIcon } from '@/components/icons/bagua';

const RADIUS_RATIO = 0.66;
const ICON_RATIO = 0.094;
const RADIAN_45_HALF = RADIAN_45 / 2;

const fix2 = fixed(2);
const fix3 = fixed(3);

export const FengShuiBaguaInfo = () => {
  const { worldInfo: world } = useWorld();
  const deviceOrientation = useDeviceOrientation();
  const { ready, get_gua_compass_order } = useFengShui();

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
      const chart_w_half = chart_w / 2;
      const chart_h_half = chart_h / 2;
      const icon_size = fix3(chart_w_half * ICON_RATIO);
      const angle = index * RADIAN_45 + deg_to_rad(alpha);
      const radius = chart_w_half * RADIUS_RATIO;
      const pos = get_position_clock(angle, radius, {
        x: chart_w_half,
        y: chart_h_half,
      });
      const z_index = Z_INDEX_FENGSHUI_BAGUA_INFO + index * 1;
      const style = css`
        ${tw`absolute flex flex-col justify-center items-center`}
        top: ${fix2(pos.y)}px;
        left: ${fix2(pos.x)}px;
        z-index: ${z_index};
        font-size: ${world?.text_lg}px;
        line-height: 1em;
        transform: translate(-50%, -50%);
      `;
      return { icon_size, style };
    },
    [chart_w, alpha]
  );

  useEffect(() => {
    if (ready) {
      setBoxes(
        [...new Array(8)].map((_, index) => {
          const bagua = get_gua_compass_order(index);
          const name = bagua?.name;
          return name
            ? {
                key: gen_code_12(),
                en: name.en,
                ch: name.zh_cn?.alphabet,
              }
            : {};
        })
      );
    }
  }, [ready]);

  useEffect(() => {
    if (ready && chart_w > 0) {
      setBoxes(prev => prev.map((p, i) => ({ ...p, ...update(i) })));
    }
  }, [ready, chart_w, alpha, update]);

  return (
    <div id="bagua-info-wrapper" css={wrapperStyle}>
      {boxes.map((box, i) => (
        <div id={`bagua-info-box-${i}`} key={box.key} css={box.style}>
          <BaguaIcon name={box.en} styles={{ size: box.icon_size }} />
          <div tw="mt-1">{box.ch}</div>
        </div>
      ))}
    </div>
  );
};

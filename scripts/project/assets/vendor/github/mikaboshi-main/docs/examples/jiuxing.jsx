/**
 * This component renders 下卦図 (Xia-Gua-Tu)
 * (also known as 飞星図; Fei-Xing-Tu; "Flying Star Chart").
 * Like any other Feng-Shui charts, it consists of 9 boxes.
 * Each box holds 3 different kinds of 九星 (Jiu-Xing),
 * namely,
 * 運盤星 (Un-Pan Xing) at the BOTTOM CENTER,
 * 山星 (Shan-Xing) at the TOP LEFT, and
 * 向星 (Xiang-Xing) at the TOP RIGHT.
 * It also displays (in each box) the star's
 * 生死衰旺 (Sheng-Si Shuai-Wang) status.
 */
import React, {
  useRef,
  useState,
  useMemo,
  useEffect,
  useCallback,
} from 'react';
import { compose, tap } from 'ramda';
import tw, { css } from 'twin.macro';

import { Z_INDEX_FENGSHUI_JIU_XING_BOXES } from '@/constants';
import { fixed, gen_code_12 } from '@/lib/utils';

import { useWorld } from '@/contexts/World';
import { useDeviceOrientation } from '@/contexts/DeviceOrientation';
import { useFengShui } from '@/contexts/FengShui';

const BOX_RATIO = 0.55;

const SHENG_SI_COLOR = {
  si: tw`bg-tomato-dark text-gray-100`,
  shuai: tw`bg-abura-dark text-gray-100`,
};

const fix2 = fixed(2);

// This is the inner most wrapper which holds 9 boxes.
// As you can see, we have 3 rows and 3 columns.
const wrapperStyle = css`
  width: calc(100% - 2px);
  height: calc(100% - 2px);
  display: grid;
  grid-gap: 1px;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
`;

// This is the wrapper for each box.
// As you can see, it has 2 rows and 2 columns.
// However, the bottom row will fill up
// using all 2 columns, and 運盤星 (Un-Pan Xing)
// is placed in the middle.
const boxStyle = css`
  ${tw`text-gray-900 text-sm`}
  display: grid;
  grid-gap: 1px;
  grid-template-columns: repeat(2, 0.5fr);
  grid-template-rows: 0.333fr 0.666fr;
`;

const xingStyle = tw`
  flex flex-col justify-center items-center text-sm font-medium
`;

export const FengShuiJiuXing = () => {
  const { worldInfo: world } = useWorld();
  const deviceOrientation = useDeviceOrientation();
  const {
    ready,
    unpan_xing,
    shan_xing,
    xiang_xing,
    get_xiaguatu_from_unpan_index,
    get_jiuxing_dipan_positions_from_direction,
    get_twentyfour_direction_from_degrees,
    get_shengsi_mapping,
  } = useFengShui();

  const [flyingStarChart, setFlyingStarChart] = useState([]);

  const chart_w = world?.chart?.width;
  const chart_h = world?.chart?.height;
  const body_h = world?.body?.height;

  // Passing current degrees for the device, and obtaining
  // the compass direction: "n", "ne", "e", "se", etc.
  const alpha = deviceOrientation?.alpha || 0;

  // `alpha` is a value that you get from Web API,
  // but what you get for `alpha` is counterintuitive...
  // When you have 10 degrees, it means that your device
  // is not pointing toward the compass NE, but NW.
  // When the device is pointing NW, you will see
  // the red arrow (which usually points the magnetic N)
  // will come to the top right. There, getting 10 degrees
  // means that your device is rotating counter-clockwise,
  // but we want the opposite. When it gives us 10 degrees,
  // we want it to mean it is rotating clockwise,
  // and the device to be pointing NE (instead of NW).
  // That is why we are passing the complementary angle
  // as a function argument (by subtracting the degree
  // from 360).
  const { direction: curr_dir } = get_twentyfour_direction_from_degrees(
    360 - alpha
  );

  // This is the outer most wrapper, and is positioned `absolute`.
  const wrapperWrapperWrapperStyle = useMemo(
    () => css`
      ${tw`absolute w-full flex flex-col justify-center items-center`}
      height: ${fix2(body_h)}px;
      z-index: ${Z_INDEX_FENGSHUI_JIU_XING_BOXES};
    `,
    [body_h]
  );

  // The 2nd wrapper which basically defines width and height,
  // and place the inner wrapper vertically and horizontally
  // in the center.
  const wrapperWrapperStyle = useMemo(() => {
    const width = chart_w * BOX_RATIO;
    return css`
      ${tw`flex flex-col justify-center items-center bg-gray-900`}
      width: ${fix2(width)}px;
      height: ${fix2(width)}px;
    `;
  }, [chart_w]);

  // As long as you have information for the current
  // 運盤星 (Un-Pan Xing) and  向星 (Xiang-Xing),
  // you can have `get_xiaguatu_from_unpan_index()`
  // calculates 下卦図 (Xia-Gua-Tu) for you.
  // Once you obtain 下卦図 (Xia-Gua-Tu)
  // (expressed as `xiagua` in the program),
  // you will get charts for all 3 stars.
  // For 生死衰旺 (Sheng-Si Shuai-Wang) is
  // calculated from 運盤星 (Un-Pan Xing) only.
  useEffect(() => {
    if (ready && unpan_xing && shan_xing && xiang_xing) {
      // console.log('[fengshui/jiuxing] curr_dir: ', curr_dir);

      // The current 運盤星 (Un-Pan Xing) holds the key to everything!
      const u_id = unpan_xing.center;

      // When calculating for 下卦図 (Xia-Gua-Tu), not only
      // the current 運盤星 (Un-Pan Xing), but we also want
      // all 九星 (Jiu-Xing) in the 洛書 (Lo-Shu) order.
      // Although we have `JIU_XING_DI_PAN_POSITIONS`
      // which defines 洛書 (Lo-Shu) order, we want it
      // in re-arranged order for the current device rotation,
      // and that is what we pass for the second argument
      // of `get_xiaguatu_from_unpan_index()`.
      const u_order = get_jiuxing_dipan_positions_from_direction(curr_dir);

      // Now, calculate for 下卦図 (Xia-Gua-Tu).
      const xiagua = get_xiaguatu_from_unpan_index({
        unpan_xing_center: u_id,
        unpan_xing_order: u_order,
        xiang_xing_direction: xiang_xing.direction,
        xiang_xing_sector: xiang_xing.sector,
      });

      const u_chart = xiagua?.unpan_xing?.chart || [];
      const s_chart = xiagua?.shan_xing?.chart || [];
      const x_chart = xiagua?.xiang_xing?.chart || [];

      if (u_chart.length > 0 && s_chart.length > 0 && x_chart.length > 0) {
        // 生死衰旺 (Sheng-Si Shuai-Wang) for the current 運盤星 (Un-Pan Xing).
        const shengsi = get_shengsi_mapping({
          unpan_id: u_id,
          unpan_xing_chart: u_chart,
        });

        let arr = [];

        // Iterating for 9 boxes, and for each box, we have 3 stars.
        // For each star, we are simply adding 1 to the star's "index"
        // to get the star's "number" which is to be displayed.
        for (let i = 0; i < 9; i++) {
          const kanji = shengsi[i]?.kanji;

          arr.push({
            key: gen_code_12(),
            style: SHENG_SI_COLOR[kanji] || tw`bg-cream`,
            unpan_xing: { num: u_chart[i] + 1, kanji },
            shan_xing: { num: s_chart[i] + 1 },
            xiang_xing: { num: x_chart[i] + 1 },
          });
        }

        if (arr.length > 0) {
          setFlyingStarChart(arr);
        }
      }
    }
  }, [
    ready,
    unpan_xing?.center,
    shan_xing?.center,
    xiang_xing?.center,
    curr_dir,
  ]);

  return (
    <div id="jiuxing-wrapper-wrapper-wrapper" css={wrapperWrapperWrapperStyle}>
      <div id="jiuxing-wrapper-wrapper" css={wrapperWrapperStyle}>
        <div id="jiuxing-wrapper" css={wrapperStyle}>
          {flyingStarChart.map((box, i) => (
            <div key={box.key} id={`box-${i}`} css={[boxStyle, box.style]}>
              <div
                id={`shan-xing-${i}`}
                css={[
                  xingStyle,
                  css`
                    grid-column: 1 / 2;
                    grid-row: 1 / 2;
                  `,
                ]}
              >
                {box.shan_xing.num}
              </div>

              <div
                id={`xiang-xing-${i}`}
                css={[
                  xingStyle,
                  css`
                    grid-column: 2 / -1;
                    grid-row: 1 / 2;
                  `,
                ]}
              >
                {box.xiang_xing.num}
              </div>

              <div
                id={`un-pan-${i}`}
                css={[
                  xingStyle,
                  css`
                    grid-column: 1 / -1;
                    grid-row: 2 / -1;
                    justify-content: flex-start;
                  `,
                ]}
              >
                <div>{box.unpan_xing.num}</div>
                <div tw="text-xs font-bold">{box.unpan_xing.kanji}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

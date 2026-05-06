import React, { useMemo } from 'react';
import tw, { css } from 'twin.macro';

import { gen_code_12 } from '@/lib/utils';
import { useErrors } from '@/contexts/Errors';
import { useWorld } from '@/contexts/World';
import { useFengShuiSync } from '@/contexts/FengShui';

import { FengShuiTwentyFour } from '@/components/fengshui/twentyfour';
import { FengShuiTwentyFourInfo } from '@/components/fengshui/twentyfour_info';
import { FengShuiCircle } from '@/components/fengshui/circle';
import { FengShuiNorth } from '@/components/fengshui/north';
import { FengShuiJiuXing } from '@/components/fengshui/jiuxing';

const wrapperStyleBase = tw`flex-none relative overflow-hidden w-full flex flex-col justify-center items-center`;

export const ChartChart = () => {
  const { errors } = useErrors();
  const { worldInfo: world } = useWorld();

  const chart_w = world?.chart?.width;
  const chart_h = world?.chart?.height;

  const wrapperStyle = useMemo(
    () => css`
      width: ${chart_w || 0}px;
      height: ${chart_h || 0}px;
    `,
    [chart_w]
  );

  // Sync the latest primary profile to FengShuiContext.profile
  useFengShuiSync();

  return errors.length ? (
    <div id="chart-main-wrapper" tw="text-white text-xs">
      {errors.map(err => (
        <div key={err.key}>{err.error}</div>
      ))}
    </div>
  ) : (
    <div id="chart-main-wrapper" css={[wrapperStyleBase, wrapperStyle]}>
      <FengShuiTwentyFour key={gen_code_12()} />
      <FengShuiTwentyFourInfo key={gen_code_12()} />
      <FengShuiCircle key={gen_code_12()} ratio={0.33} />
      <FengShuiNorth key={gen_code_12()} />
      <FengShuiJiuXing key={gen_code_12()} />
    </div>
  );
};

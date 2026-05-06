import { MINOR_STARS, type Palace, type StarKey, type Star as StarModel } from "@ziweijs/core";
import { memo, use, useCallback, useMemo } from "react";

import { ConfigContext } from "../context/config";
import Star from "./Star";

export interface StarsProps {
  data: StarModel[];
  x: number;
  y: number;
  palace: Palace;
}

function Stars({ data, x, y, palace }: StarsProps) {
  const { fontSize, fontLineHeight, fontColor, ziweiColor, minorStarColor } = use(ConfigContext);

  const starColor = useCallback(
    (starKey: StarKey) => {
      if (starKey === "ZiWei") {
        return ziweiColor;
      }
      if (MINOR_STARS.includes(starKey)) {
        return minorStarColor;
      }
      return fontColor;
    },
    [ziweiColor, fontColor, minorStarColor],
  );

  // 预先构建自化序号索引，渲染时 O(1) 查询，避免 indexOf 带来的 O(n^2)
  const onlyCfIndex = useMemo(() => {
    const map = new Map<StarModel, number>();
    let idx = 0;
    for (const s of data) {
      if (s.ST?.exit) {
        map.set(s, idx);
        idx += 1;
      }
    }
    return map;
  }, [data]);

  return (
    <g>
      {data.map((star, i) => {
        const index = onlyCfIndex.get(star);
        return (
          <Star
            {...star}
            index={typeof index === "number" ? index : 0}
            starKey={star.key}
            key={star.key}
            x={x - fontLineHeight * fontSize * i}
            y={y}
            fill={starColor(star.key)}
            palace={palace}
          />
        );
      })}
    </g>
  );
}

export default memo(Stars);

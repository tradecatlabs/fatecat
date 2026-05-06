import { memo, useId } from "react";

// 箭头类型：支持单向/双向，未来新增类型只需在此扩展
type ArrowType = "triangle" | "triangle-double" | "diamond" | "diamond-double";

// 定义箭头配置接口：规范每种箭头的起点/终点样式
interface ArrowConfig {
  end: {
    element: React.ReactNode; // 终点箭头元素
    refX: number; // 终点箭头参考点X
    refY: number; // 终点箭头参考点Y
  };
  start?: {
    element: React.ReactNode; // 起点箭头元素（可选，单向箭头可省略）
    refX: number;
    refY: number;
  };
}

export interface ArrowLineProps {
  /** 折线点坐标数组，格式：[[x1,y1], [x2,y2], ..., [xn,yn]]，至少需要2个点 */
  points: [number, number][];
  /** 线条颜色 */
  stroke?: string;
  /** 线条宽度 */
  strokeWidth?: number;
  /** 线条末端箭头大小（影响箭头宽度和长度） */
  arrowSize?: number;
  /** 箭头样式（内置或自定义） */
  arrowType?: ArrowType;
  /** 线条是否为虚线，格式：[线段长度, 间隔长度]，如 [5,3] */
  dashArray?: [number, number];
  /** 线条端点样式（round/square/butt） */
  strokeLinecap?: "round" | "square" | "butt";
}

function ArrowLine({
  points,
  stroke = "#333",
  strokeWidth = 2,
  arrowSize = 6,
  arrowType = "triangle",
  dashArray,
  strokeLinecap = "square",
}: ArrowLineProps) {
  const arrowStartId = useId();
  const arrowEndId = useId();

  // 校验路径点数量（至少2个点才能形成线）
  if (points.length < 2) {
    console.warn("折线箭头至少需要2个点坐标");
    return null;
  }

  // 生成折线path的d属性（M:起点，L:后续点）
  const d = () => {
    const [firstX, firstY] = points[0];
    let pathData = `M ${firstX},${firstY}`;
    for (let i = 1; i < points.length; i++) {
      const [x, y] = points[i];
      pathData += ` L ${x},${y}`;
    }
    return pathData;
  };

  // 箭头配置映射表：新增箭头类型时，只需在此添加配置
  const arrowConfigMap: Record<ArrowType, ArrowConfig> = {
    // 三角形单向箭头
    triangle: {
      end: {
        element: (
          <polygon
            points={`0,0 ${arrowSize * 2},${arrowSize} 0,${arrowSize * 2}`}
            fill={stroke}
            stroke={stroke}
            strokeWidth={strokeWidth / 8}
          />
        ),
        refX: arrowSize,
        refY: arrowSize,
      },
    },
    // 三角形双向箭头
    "triangle-double": {
      end: {
        element: (
          <polygon
            points={`0,0 ${arrowSize * 2},${arrowSize} 0,${arrowSize * 2}`}
            fill={stroke}
            stroke={stroke}
            strokeWidth={strokeWidth / 8}
          />
        ),
        refX: arrowSize,
        refY: arrowSize,
      },
      start: {
        element: (
          <polygon
            points={`${arrowSize * 2},0 0,${arrowSize} ${arrowSize * 2},${arrowSize * 2}`}
            fill={stroke}
            stroke={stroke}
            strokeWidth={strokeWidth / 8}
          />
        ),
        refX: arrowSize,
        refY: arrowSize,
      },
    },
    // 新增：菱形单向箭头（示例）
    diamond: {
      end: {
        element: (
          <polygon
            points={`0,${arrowSize} ${arrowSize},0 ${arrowSize * 2},${arrowSize} ${arrowSize},${arrowSize * 2}`}
            fill={stroke}
            stroke={stroke}
            strokeWidth={strokeWidth / 8}
          />
        ),
        refX: arrowSize * 2, // 菱形箭头尖端在右侧，参考点需调整
        refY: arrowSize,
      },
    },
    // 新增：菱形双向箭头（示例）
    "diamond-double": {
      end: {
        element: (
          <polygon
            points={`0,${arrowSize} ${arrowSize},0 ${arrowSize * 2},${arrowSize} ${arrowSize},${arrowSize * 2}`}
            fill={stroke}
            stroke={stroke}
            strokeWidth={strokeWidth / 8}
          />
        ),
        refX: arrowSize * 2,
        refY: arrowSize,
      },
      start: {
        element: (
          <polygon
            points={`0,${arrowSize} ${arrowSize},0 ${arrowSize * 2},${arrowSize} ${arrowSize},${arrowSize * 2}`}
            fill={stroke}
            stroke={stroke}
            strokeWidth={strokeWidth / 8}
          />
        ),
        refX: 0, // 菱形起点箭头尖端在左侧，参考点调整
        refY: arrowSize,
      },
    },
  };

  // 获取当前类型的箭头配置
  const currentConfig = arrowConfigMap[arrowType];
  const hasStartArrow = !!currentConfig.start;

  return (
    <svg overflow="visible">
      <title>自化</title>
      <defs>
        {/* 终点箭头标记（所有类型都需要） */}
        <marker
          id={arrowEndId}
          markerWidth={arrowSize * 2}
          markerHeight={arrowSize * 2}
          refX={currentConfig.end.refX}
          refY={currentConfig.end.refY}
          orient="auto"
        >
          {currentConfig.end.element}
        </marker>

        {/* 起点箭头标记（仅双向类型需要） */}
        {hasStartArrow && (
          <marker
            id={arrowStartId}
            markerWidth={arrowSize * 2}
            markerHeight={arrowSize * 2}
            refX={currentConfig?.start?.refX}
            refY={currentConfig?.start?.refY}
            orient="auto"
          >
            {currentConfig?.start?.element}
          </marker>
        )}
      </defs>
      <path
        d={d()}
        stroke={stroke}
        strokeWidth={strokeWidth}
        strokeLinecap={strokeLinecap}
        strokeDasharray={dashArray ? `${dashArray[0]},${dashArray[1]}` : undefined}
        fill="none" // 路径不填充
        vectorEffect="non-scaling-stroke"
        pointerEvents="none"
        markerStart={hasStartArrow ? `url(#${arrowStartId})` : undefined}
        markerEnd={`url(#${arrowEndId})`} // 末端添加箭头
      />
    </svg>
  );
}

export default memo(ArrowLine);

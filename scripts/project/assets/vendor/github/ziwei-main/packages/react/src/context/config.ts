import { createContext } from "react";

export interface ConfigContextProps {
  /** 画布的padding  */
  padding: number;
  /** 命盘的宽高  */
  boardSide: number;
  /** 命盘的padding  */
  boardPadding: number;
  /** 命盘的背景颜色  */
  boardFill: string;
  /** 命盘的边框颜色  */
  boardStroke: string;
  /** 命盘的边框宽度  */
  boardStrokeWidth: number;
  /** 命盘的x坐标  */
  boardX: number;
  /** 命盘的y坐标  */
  boardY: number;
  /** 宫位的宽高  */
  palaceSide: number;
  /** 宫位的padding  */
  palacePadding: number;
  /** 宫位的边框宽度  */
  palaceStrokeWidth: number;
  /** 宫位飞化的背景色  */
  palaceFlyFill: string;
  /** 大命踏入时宫位的背景色 */
  palaceHoroscopeFill: string;
  /** 命盘的字体大小  */
  fontSize: number;
  /** 命盘的字体颜色  */
  fontColor: string;
  /** 命盘的字体（思源宋体）行高比例  */
  fontLineHeight: number;
  /** 宫位矩形的边框宽度  */
  palaceRectStrokeWidth: number;
  /** 横向矩形的宽度  */
  horizontalRectWidth: number;
  /** 横向矩形的高度  */
  horizontalRectHeight: number;
  /** 纵向矩形的宽度  */
  verticalRectWidth: number;
  /** 纵向矩形的高度  */
  verticalRectHeight: number;
  /** 离心自化的 Y 轴起始间距  */
  selfTransformationMarginTop: number;
  /** 自化的字体大小  */
  selfTransformationFontSize: number;
  /** 自化的颜色  */
  selfTransformationStroke: string;
  /** 大周期范围的字体大小  */
  horoscopeRangesFontSize: number;
  /** 来因宫标识的宽度  */
  laiYinFlagWidth: number;
  /** 来因宫标识的高度  */
  laiYinFlagHeight: number;
  /** 来因宫标识的字体大小  */
  laiYinFlagFontSize: number;
  /** 来因宫标识的字体颜色  */
  laiYinFlagFontColor: string;
  /** 来因宫标识的边框颜色  */
  laiYinFlagStroke: string;
  /** 来因宫标识的边框大小  */
  laiYinFlagStrokeWidth: number;
  /** 来因宫标识的背景颜色 */
  laiYinFlagFill: string;
  /** 来因宫标识的 X 轴坐标系 */
  laiYinFlagX: number;
  /** 来因宫标识的 Y 轴坐标系 */
  laiYinFlagY: number;
  /** 箭头大小 */
  arrowSize: number;
  /** 飞化的背景颜色 */
  flyingTransformationFill: [string, string, string, string];
  /** 飞化的字体颜色 */
  flyingTransformationColor: string;
  /** 紫微星的颜色 */
  ziweiColor: string;
  /** 紫微宫的填充颜色 */
  ziweiPalaceFill: string;
  /** 左右昌曲的颜色 */
  minorStarColor: string;
  /** 流年的字体大小 */
  yearlyFontSize: number;
  /** 中宫的宽高大小 */
  centralPalaceSide: number;
  /** 中宫的padding */
  centralPalacePadding: number;
  /** 中宫的X坐标 */
  centralPalaceX: number;
  /** 中宫的Y坐标 */
  centralPalaceY: number;
  /** 中宫的字体大小 */
  centralPalaceFontSize: number;
  /** 中宫的版本字体大小 */
  centralPalaceVersionFontSize: number;
  /** 箭头的宽度 */
  arrowWidth: number;
}

export const ConfigContext = createContext<ConfigContextProps>({} as ConfigContextProps);

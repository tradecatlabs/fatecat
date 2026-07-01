/**
 * iztro 紫微斗数库的类型汇总
 * 从 iztro 包重新导出公共接口，给项目内部一个统一别名层。
 */
import type { IFunctionalAstrolabe } from 'iztro/lib/astro/FunctionalAstrolabe';
import type { IFunctionalHoroscope } from 'iztro/lib/astro/FunctionalHoroscope';
import type { IFunctionalPalace } from 'iztro/lib/astro/FunctionalPalace';
import type { IFunctionalStar } from 'iztro/lib/star/FunctionalStar';
import type { IFunctionalSurpalaces } from 'iztro/lib/astro/FunctionalSurpalaces';
import type { Mutagen } from 'iztro/lib/i18n';

export type IztroAstrolabe = IFunctionalAstrolabe;
export type IztroHoroscope = IFunctionalHoroscope;
export type IztroPalace = IFunctionalPalace;
export type IztroStar = IFunctionalStar;
export type IztroSurpalaces = IFunctionalSurpalaces;
export type IztroMutagen = Mutagen;

export type IztroHoroscopeScope =
  | IztroHoroscope['decadal']
  | IztroHoroscope['yearly']
  | IztroHoroscope['monthly']
  | IztroHoroscope['daily']
  | IztroHoroscope['hourly'];

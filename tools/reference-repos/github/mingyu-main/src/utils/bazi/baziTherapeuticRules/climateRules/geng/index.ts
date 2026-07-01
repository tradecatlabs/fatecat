import type { ClimateRule } from '../../types';
import { GENG_YIN_CLIMATE_RULES } from './yin';
import { GENG_MAO_CLIMATE_RULES } from './mao';
import { GENG_CHEN_CLIMATE_RULES } from './chen';
import { GENG_SI_CLIMATE_RULES } from './si';
import { GENG_WU_CLIMATE_RULES } from './wu';
import { GENG_WEI_CLIMATE_RULES } from './wei';
import { GENG_SHEN_CLIMATE_RULES } from './shen';
import { GENG_YOU_CLIMATE_RULES } from './you';
import { GENG_XU_CLIMATE_RULES } from './xu';
import { GENG_HAI_CLIMATE_RULES } from './hai';
import { GENG_ZI_CLIMATE_RULES } from './zi';
import { GENG_CHOU_CLIMATE_RULES } from './chou';

export const GENG_CLIMATE_RULES: ClimateRule[] = [
  ...GENG_YIN_CLIMATE_RULES,
  ...GENG_MAO_CLIMATE_RULES,
  ...GENG_CHEN_CLIMATE_RULES,
  ...GENG_SI_CLIMATE_RULES,
  ...GENG_WU_CLIMATE_RULES,
  ...GENG_WEI_CLIMATE_RULES,
  ...GENG_SHEN_CLIMATE_RULES,
  ...GENG_YOU_CLIMATE_RULES,
  ...GENG_XU_CLIMATE_RULES,
  ...GENG_HAI_CLIMATE_RULES,
  ...GENG_ZI_CLIMATE_RULES,
  ...GENG_CHOU_CLIMATE_RULES,
];

import type { ClimateRule } from '../../types';
import { GUI_YIN_CLIMATE_RULES } from './yin';
import { GUI_MAO_CLIMATE_RULES } from './mao';
import { GUI_CHEN_CLIMATE_RULES } from './chen';
import { GUI_SI_CLIMATE_RULES } from './si';
import { GUI_WU_CLIMATE_RULES } from './wu';
import { GUI_WEI_CLIMATE_RULES } from './wei';
import { GUI_SHEN_CLIMATE_RULES } from './shen';
import { GUI_YOU_CLIMATE_RULES } from './you';
import { GUI_XU_CLIMATE_RULES } from './xu';
import { GUI_HAI_CLIMATE_RULES } from './hai';
import { GUI_ZI_CLIMATE_RULES } from './zi';
import { GUI_CHOU_CLIMATE_RULES } from './chou';

export const GUI_CLIMATE_RULES: ClimateRule[] = [
  ...GUI_YIN_CLIMATE_RULES,
  ...GUI_MAO_CLIMATE_RULES,
  ...GUI_CHEN_CLIMATE_RULES,
  ...GUI_SI_CLIMATE_RULES,
  ...GUI_WU_CLIMATE_RULES,
  ...GUI_WEI_CLIMATE_RULES,
  ...GUI_SHEN_CLIMATE_RULES,
  ...GUI_YOU_CLIMATE_RULES,
  ...GUI_XU_CLIMATE_RULES,
  ...GUI_HAI_CLIMATE_RULES,
  ...GUI_ZI_CLIMATE_RULES,
  ...GUI_CHOU_CLIMATE_RULES,
];

import type { ClimateRule } from '../../types';
import { XIN_CHEN_CLIMATE_RULES } from './chen';
import { XIN_SI_CLIMATE_RULES } from './si';
import { XIN_WU_CLIMATE_RULES } from './wu';
import { XIN_WEI_CLIMATE_RULES } from './wei';
import { XIN_SHEN_CLIMATE_RULES } from './shen';
import { XIN_YOU_CLIMATE_RULES } from './you';
import { XIN_XU_CLIMATE_RULES } from './xu';
import { XIN_HAI_CLIMATE_RULES } from './hai';
import { XIN_ZI_CLIMATE_RULES } from './zi';
import { XIN_CHOU_CLIMATE_RULES } from './chou';
import { XIN_YIN_CLIMATE_RULES } from './yin';
import { XIN_MAO_CLIMATE_RULES } from './mao';

export const XIN_CLIMATE_RULES: ClimateRule[] = [
  ...XIN_CHEN_CLIMATE_RULES,
  ...XIN_SI_CLIMATE_RULES,
  ...XIN_WU_CLIMATE_RULES,
  ...XIN_WEI_CLIMATE_RULES,
  ...XIN_SHEN_CLIMATE_RULES,
  ...XIN_YOU_CLIMATE_RULES,
  ...XIN_XU_CLIMATE_RULES,
  ...XIN_HAI_CLIMATE_RULES,
  ...XIN_ZI_CLIMATE_RULES,
  ...XIN_CHOU_CLIMATE_RULES,
  ...XIN_YIN_CLIMATE_RULES,
  ...XIN_MAO_CLIMATE_RULES,
];

import type { ClimateRule } from '../../types';
import { JIA_YIN_CLIMATE_RULES } from './yin';
import { JIA_MAO_CLIMATE_RULES } from './mao';
import { JIA_CHEN_CLIMATE_RULES } from './chen';
import { JIA_SI_CLIMATE_RULES } from './si';
import { JIA_WU_CLIMATE_RULES } from './wu';
import { JIA_WEI_CLIMATE_RULES } from './wei';
import { JIA_SHEN_CLIMATE_RULES } from './shen';
import { JIA_YOU_CLIMATE_RULES } from './you';
import { JIA_XU_CLIMATE_RULES } from './xu';
import { JIA_HAI_CLIMATE_RULES } from './hai';
import { JIA_ZI_CLIMATE_RULES } from './zi';
import { JIA_CHOU_CLIMATE_RULES } from './chou';

export const JIA_CLIMATE_RULES: ClimateRule[] = [
  ...JIA_YIN_CLIMATE_RULES,
  ...JIA_MAO_CLIMATE_RULES,
  ...JIA_CHEN_CLIMATE_RULES,
  ...JIA_SI_CLIMATE_RULES,
  ...JIA_WU_CLIMATE_RULES,
  ...JIA_WEI_CLIMATE_RULES,
  ...JIA_SHEN_CLIMATE_RULES,
  ...JIA_YOU_CLIMATE_RULES,
  ...JIA_XU_CLIMATE_RULES,
  ...JIA_HAI_CLIMATE_RULES,
  ...JIA_ZI_CLIMATE_RULES,
  ...JIA_CHOU_CLIMATE_RULES,
];

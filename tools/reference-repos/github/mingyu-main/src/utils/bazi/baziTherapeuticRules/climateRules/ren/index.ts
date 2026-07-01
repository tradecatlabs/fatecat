import type { ClimateRule } from '../../types';
import { REN_YIN_CLIMATE_RULES } from './yin';
import { REN_MAO_CLIMATE_RULES } from './mao';
import { REN_CHEN_CLIMATE_RULES } from './chen';
import { REN_SI_CLIMATE_RULES } from './si';
import { REN_WU_CLIMATE_RULES } from './wu';
import { REN_WEI_CLIMATE_RULES } from './wei';
import { REN_SHEN_CLIMATE_RULES } from './shen';
import { REN_YOU_CLIMATE_RULES } from './you';
import { REN_XU_CLIMATE_RULES } from './xu';
import { REN_HAI_CLIMATE_RULES } from './hai';
import { REN_ZI_CLIMATE_RULES } from './zi';
import { REN_CHOU_CLIMATE_RULES } from './chou';

export const REN_CLIMATE_RULES: ClimateRule[] = [
  ...REN_YIN_CLIMATE_RULES,
  ...REN_MAO_CLIMATE_RULES,
  ...REN_CHEN_CLIMATE_RULES,
  ...REN_SI_CLIMATE_RULES,
  ...REN_WU_CLIMATE_RULES,
  ...REN_WEI_CLIMATE_RULES,
  ...REN_SHEN_CLIMATE_RULES,
  ...REN_YOU_CLIMATE_RULES,
  ...REN_XU_CLIMATE_RULES,
  ...REN_HAI_CLIMATE_RULES,
  ...REN_ZI_CLIMATE_RULES,
  ...REN_CHOU_CLIMATE_RULES,
];

import type { StrengthHintRule } from './types';

export const STRENGTH_HINT_RULES: StrengthHintRule[] = [
  {
    id: 'strength-strong-stagnation',
    label: '身强壅滞病药提示',
    description: '身强多壅，宜疏泄流通。',
    strengths: ['身强', '偏强', '极强'],
    hint: '病在壅滞，宜疏泄流通',
  },
  {
    id: 'strength-weak-deficiency',
    label: '身弱不足病药提示',
    description: '身弱多虚，宜扶助培元。',
    strengths: ['身弱', '偏弱', '极弱'],
    hint: '病在不足，宜扶助培元',
  },
];

/**
 * Fortune dimension system — 12 scoring dimensions for visualization.
 */

export type FortuneDimensionKey =
  | 'career'
  | 'wealth'
  | 'love'
  | 'health'
  | 'family'
  | 'social'
  | 'windfall'
  | 'travel'
  | 'creativity'
  | 'children'
  | 'legal'
  | 'spiritual';

export interface DimensionConfig {
  key: FortuneDimensionKey;
  label: string;
  icon: string;
  color: string;
  description: string;
  tier: 'core' | 'advanced';
}

const DIMENSION_KEYS = new Set<string>([
  'career', 'wealth', 'love', 'health', 'family', 'social',
  'windfall', 'travel', 'creativity', 'children', 'legal', 'spiritual',
]);

export const ALL_DIMENSIONS: DimensionConfig[] = [
  { key: 'career', label: '事业/学业', icon: '💼', color: '#3b82f6', description: '职场晋升、学业成绩、能力发展', tier: 'core' },
  { key: 'wealth', label: '财富', icon: '💰', color: '#22c55e', description: '正财收入、投资回报、理财运', tier: 'core' },
  { key: 'love', label: '感情/婚姻', icon: '❤️', color: '#ec4899', description: '桃花运、婚姻关系、情感状态', tier: 'core' },
  { key: 'health', label: '健康', icon: '🏥', color: '#ef4444', description: '身体状况、精力旺衰、疾病风险', tier: 'core' },
  { key: 'family', label: '家庭/长辈', icon: '👨‍👩‍👧‍👦', color: '#f97316', description: '父母健康、家庭和睦、六亲关系', tier: 'core' },
  { key: 'social', label: '人际/贵人', icon: '🤝', color: '#8b5cf6', description: '社交运、贵人相助、人脉拓展', tier: 'core' },
  { key: 'windfall', label: '偏财/投资', icon: '🎰', color: '#14b8a6', description: '偏财运、投机运、意外收入', tier: 'advanced' },
  { key: 'travel', label: '出行/迁移', icon: '✈️', color: '#06b6d4', description: '出行顺利度、搬迁运、异地发展', tier: 'advanced' },
  { key: 'creativity', label: '创意/灵感', icon: '🎨', color: '#a855f7', description: '文昌运、创作灵感、学习新技能', tier: 'advanced' },
  { key: 'children', label: '子女', icon: '👶', color: '#f472b6', description: '子女运势、生育、亲子关系', tier: 'advanced' },
  { key: 'legal', label: '官非/法律', icon: '⚖️', color: '#64748b', description: '官司风险、合同纠纷（越高越安全）', tier: 'advanced' },
  { key: 'spiritual', label: '精神/心灵', icon: '🧘', color: '#d946ef', description: '情绪状态、精神内耗、内心平静', tier: 'advanced' },
];

export const DEFAULT_DIMENSIONS: FortuneDimensionKey[] = [
  'career', 'wealth', 'love', 'health', 'family', 'social',
];

export const CORE_DIMENSIONS = ALL_DIMENSIONS.filter(d => d.tier === 'core');
export const ADVANCED_DIMENSIONS = ALL_DIMENSIONS.filter(d => d.tier === 'advanced');

const dimensionMap = new Map(ALL_DIMENSIONS.map(d => [d.key, d]));

// 中文 label → 英文 key 反向映射（容错 AI 输出中文 key 的情况）
const labelToKeyMap = new Map<string, FortuneDimensionKey>();
for (const d of ALL_DIMENSIONS) {
  labelToKeyMap.set(d.label, d.key);
  // 支持无分隔符的变体（如"事业学业"→"career"）
  const normalized = d.label.replace(/[/／·、]/g, '');
  if (normalized !== d.label) {
    labelToKeyMap.set(normalized, d.key);
  }
}

/**
 * 将可能的中文 label 或英文 key 归一化为标准 FortuneDimensionKey。
 * 无法识别时返回 undefined。
 */
export function normalizeDimensionKey(raw: string): FortuneDimensionKey | undefined {
  if (DIMENSION_KEYS.has(raw)) return raw as FortuneDimensionKey;
  return labelToKeyMap.get(raw);
}

export function getDimensionConfig(key: FortuneDimensionKey): DimensionConfig {
  const config = dimensionMap.get(key);
  if (!config) throw new Error(`Unknown dimension key: ${key}`);
  return config;
}

export function getDimensionsByKeys(keys: FortuneDimensionKey[]): DimensionConfig[] {
  return keys.map(getDimensionConfig);
}

export function isDimensionKey(value: string): value is FortuneDimensionKey {
  return DIMENSION_KEYS.has(value);
}

import type {
  MeihuaExternalAnimal,
  MeihuaExternalColor,
  MeihuaExternalDirection,
  MeihuaExternalObject,
  MeihuaExternalPerson,
  MeihuaExternalSound,
} from '../types/divination';

type MeihuaOmenOption<T extends string> = {
  name: T;
  displayName?: string;
  remark: string;
  trigramIndex: number;
  trigramName: string;
};

export const meihuaDirectionOptions: MeihuaOmenOption<MeihuaExternalDirection>[] = [
  { name: '东', remark: '东方场景，对应震卦', trigramIndex: 4, trigramName: '震' },
  { name: '东南', remark: '东南场景，对应巽卦', trigramIndex: 5, trigramName: '巽' },
  { name: '南', remark: '南方场景，对应离卦', trigramIndex: 3, trigramName: '离' },
  { name: '西南', remark: '西南场景，对应坤卦', trigramIndex: 8, trigramName: '坤' },
  { name: '西', remark: '西方场景，对应兑卦', trigramIndex: 2, trigramName: '兑' },
  { name: '西北', remark: '西北场景，对应乾卦', trigramIndex: 1, trigramName: '乾' },
  { name: '北', remark: '北方场景，对应坎卦', trigramIndex: 6, trigramName: '坎' },
  { name: '东北', remark: '东北场景，对应艮卦', trigramIndex: 7, trigramName: '艮' },
];

export const meihuaPersonOptions: MeihuaOmenOption<MeihuaExternalPerson>[] = [
  {
    name: '老父',
    displayName: '领导/决策者',
    remark: '传统取象“老父”，对应乾卦',
    trigramIndex: 1,
    trigramName: '乾',
  },
  {
    name: '老妇',
    displayName: '照护者/后勤型',
    remark: '传统取象“老妇”，对应坤卦',
    trigramIndex: 8,
    trigramName: '坤',
  },
  {
    name: '长男',
    displayName: '行动派/执行型',
    remark: '传统取象“长男”，对应震卦',
    trigramIndex: 4,
    trigramName: '震',
  },
  {
    name: '长女',
    displayName: '沟通者/策划型',
    remark: '传统取象“长女”，对应巽卦',
    trigramIndex: 5,
    trigramName: '巽',
  },
  {
    name: '中男',
    displayName: '通勤者/夜归型',
    remark: '传统取象“中男”，对应坎卦',
    trigramIndex: 6,
    trigramName: '坎',
  },
  {
    name: '中女',
    displayName: '表达者/创作者',
    remark: '传统取象“中女”，对应离卦',
    trigramIndex: 3,
    trigramName: '离',
  },
  {
    name: '少男',
    displayName: '学生/安静型',
    remark: '传统取象“少男”，对应艮卦',
    trigramIndex: 7,
    trigramName: '艮',
  },
  {
    name: '少女',
    displayName: '社交者/轻快型',
    remark: '传统取象“少女”，对应兑卦',
    trigramIndex: 2,
    trigramName: '兑',
  },
];

export const meihuaAnimalOptions: MeihuaOmenOption<MeihuaExternalAnimal>[] = [
  {
    name: '马',
    displayName: '大型犬/速度型动物',
    remark: '传统取象“马”，对应乾卦',
    trigramIndex: 1,
    trigramName: '乾',
  },
  {
    name: '牛',
    displayName: '温顺厚重型动物',
    remark: '传统取象“牛”，对应坤卦',
    trigramIndex: 8,
    trigramName: '坤',
  },
  {
    name: '龙',
    displayName: '爆发型/稀有感动物',
    remark: '传统取象“龙”，对应震卦',
    trigramIndex: 4,
    trigramName: '震',
  },
  {
    name: '鸡',
    displayName: '轻快鸣叫型动物',
    remark: '传统取象“鸡”，对应巽卦',
    trigramIndex: 5,
    trigramName: '巽',
  },
  {
    name: '猪',
    displayName: '水边/夜行型动物',
    remark: '传统取象“猪”，对应坎卦',
    trigramIndex: 6,
    trigramName: '坎',
  },
  {
    name: '雉',
    displayName: '高辨识度羽色动物',
    remark: '传统取象“雉”，对应离卦',
    trigramIndex: 3,
    trigramName: '离',
  },
  {
    name: '狗',
    displayName: '守门/宅家型动物',
    remark: '传统取象“狗”，对应艮卦',
    trigramIndex: 7,
    trigramName: '艮',
  },
  {
    name: '羊',
    displayName: '温和亲近型动物',
    remark: '传统取象“羊”，对应兑卦',
    trigramIndex: 2,
    trigramName: '兑',
  },
];

export const meihuaObjectOptions: MeihuaOmenOption<MeihuaExternalObject>[] = [
  {
    name: '金玉圆器',
    displayName: '金属设备/圆形物',
    remark: '传统取象“金玉圆器”，对应乾卦',
    trigramIndex: 1,
    trigramName: '乾',
  },
  {
    name: '布帛陶器',
    displayName: '收纳容器/家居用品',
    remark: '传统取象“布帛陶器”，对应坤卦',
    trigramIndex: 8,
    trigramName: '坤',
  },
  {
    name: '竹木乐器',
    displayName: '运动器材/木质装置',
    remark: '传统取象“竹木乐器”，对应震卦',
    trigramIndex: 4,
    trigramName: '震',
  },
  {
    name: '绳索长木',
    displayName: '线缆/通讯配件',
    remark: '传统取象“绳索长木”，对应巽卦',
    trigramIndex: 5,
    trigramName: '巽',
  },
  {
    name: '水器液体',
    displayName: '饮品/液体容器',
    remark: '传统取象“水器液体”，对应坎卦',
    trigramIndex: 6,
    trigramName: '坎',
  },
  {
    name: '火电文书',
    displayName: '屏幕/灯光/电子设备',
    remark: '传统取象“火电文书”，对应离卦',
    trigramIndex: 3,
    trigramName: '离',
  },
  {
    name: '石块门板',
    displayName: '家具/门锁/硬质结构',
    remark: '传统取象“石块门板”，对应艮卦',
    trigramIndex: 7,
    trigramName: '艮',
  },
  {
    name: '刀剪口器',
    displayName: '饰品/美妆/锐器',
    remark: '传统取象“刀剪口器”，对应兑卦',
    trigramIndex: 2,
    trigramName: '兑',
  },
];

export const meihuaSoundOptions: MeihuaOmenOption<MeihuaExternalSound>[] = [
  {
    name: '洪亮金石',
    displayName: '金属撞击/广播声',
    remark: '传统取象“洪亮金石”，对应乾卦',
    trigramIndex: 1,
    trigramName: '乾',
  },
  {
    name: '沉厚低缓',
    displayName: '低频轰鸣/底噪',
    remark: '传统取象“沉厚低缓”，对应坤卦',
    trigramIndex: 8,
    trigramName: '坤',
  },
  {
    name: '雷鸣震动',
    displayName: '突发提醒/震动声',
    remark: '传统取象“雷鸣震动”，对应震卦',
    trigramIndex: 4,
    trigramName: '震',
  },
  {
    name: '风声呼啸',
    displayName: '风噪/通风声',
    remark: '传统取象“风声呼啸”，对应巽卦',
    trigramIndex: 5,
    trigramName: '巽',
  },
  {
    name: '流水滴答',
    displayName: '水流/滴水声',
    remark: '传统取象“流水滴答”，对应坎卦',
    trigramIndex: 6,
    trigramName: '坎',
  },
  {
    name: '爆裂鸣叫',
    displayName: '铃声/提示音',
    remark: '传统取象“爆裂鸣叫”，对应离卦',
    trigramIndex: 3,
    trigramName: '离',
  },
  {
    name: '闷阻叩击',
    displayName: '敲门/施工闷响',
    remark: '传统取象“闷阻叩击”，对应艮卦',
    trigramIndex: 7,
    trigramName: '艮',
  },
  {
    name: '清脆笑语',
    displayName: '聊天/笑声/音乐片段',
    remark: '传统取象“清脆笑语”，对应兑卦',
    trigramIndex: 2,
    trigramName: '兑',
  },
];

export const meihuaColorOptions: MeihuaOmenOption<MeihuaExternalColor>[] = [
  {
    name: '金白',
    displayName: '银白/灰白',
    remark: '传统取象“金白”，对应乾卦',
    trigramIndex: 1,
    trigramName: '乾',
  },
  {
    name: '土黄',
    displayName: '米黄/卡其',
    remark: '传统取象“土黄”，对应坤卦',
    trigramIndex: 8,
    trigramName: '坤',
  },
  {
    name: '青碧',
    displayName: '青绿/亮绿',
    remark: '传统取象“青碧”，对应震卦',
    trigramIndex: 4,
    trigramName: '震',
  },
  {
    name: '青绿',
    displayName: '薄荷绿/蓝绿',
    remark: '传统取象“青绿”，对应巽卦',
    trigramIndex: 5,
    trigramName: '巽',
  },
  {
    name: '黑蓝',
    displayName: '深蓝/黑色',
    remark: '传统取象“黑蓝”，对应坎卦',
    trigramIndex: 6,
    trigramName: '坎',
  },
  {
    name: '赤紫',
    displayName: '红橙/亮紫',
    remark: '传统取象“赤紫”，对应离卦',
    trigramIndex: 3,
    trigramName: '离',
  },
  {
    name: '棕黄',
    displayName: '棕褐/岩土色',
    remark: '传统取象“棕黄”，对应艮卦',
    trigramIndex: 7,
    trigramName: '艮',
  },
  {
    name: '银白',
    displayName: '粉白/亮银',
    remark: '传统取象“银白”，对应兑卦',
    trigramIndex: 2,
    trigramName: '兑',
  },
];

export const meihuaOmenPriority = [
  'direction',
  'person',
  'animal',
  'object',
  'sound',
  'color',
] as const;

export const meihuaDirectionMap = Object.fromEntries(
  meihuaDirectionOptions.map((option) => [option.name, option]),
) as Record<MeihuaExternalDirection, MeihuaOmenOption<MeihuaExternalDirection>>;

export const meihuaPersonMap = Object.fromEntries(
  meihuaPersonOptions.map((option) => [option.name, option]),
) as Record<MeihuaExternalPerson, MeihuaOmenOption<MeihuaExternalPerson>>;

export const meihuaAnimalMap = Object.fromEntries(
  meihuaAnimalOptions.map((option) => [option.name, option]),
) as Record<MeihuaExternalAnimal, MeihuaOmenOption<MeihuaExternalAnimal>>;

export const meihuaObjectMap = Object.fromEntries(
  meihuaObjectOptions.map((option) => [option.name, option]),
) as Record<MeihuaExternalObject, MeihuaOmenOption<MeihuaExternalObject>>;

export const meihuaSoundMap = Object.fromEntries(
  meihuaSoundOptions.map((option) => [option.name, option]),
) as Record<MeihuaExternalSound, MeihuaOmenOption<MeihuaExternalSound>>;

export const meihuaColorMap = Object.fromEntries(
  meihuaColorOptions.map((option) => [option.name, option]),
) as Record<MeihuaExternalColor, MeihuaOmenOption<MeihuaExternalColor>>;

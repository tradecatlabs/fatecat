/**
 * 塔罗牌核心引擎
 */

import { createSeededRng, resolveSeed } from '../../shared/seeded-rng.js';
import type {
  TarotCardDefinition,
  TarotCardResult,
  TarotInput,
  TarotOutput,
  TarotSpreadDefinition,
} from './types.js';

export type {
  TarotCardDefinition,
  TarotCardResult,
  TarotInput,
  TarotOutput,
  TarotSpreadDefinition,
} from './types.js';

// 大阿卡纳牌
const MAJOR_ARCANA: TarotCardDefinition[] = [
  { name: 'The Fool', nameChinese: '愚者', number: 0, keywords: ['新开始', '冒险', '天真'], reversedKeywords: ['鲁莽冒失', '冲动决策', '缺乏计划'], suit: 'major', element: '风', astrologicalCorrespondence: '天王星' },
  { name: 'The Magician', nameChinese: '魔术师', number: 1, keywords: ['创造力', '技能', '意志力'], reversedKeywords: ['欺骗操控', '浪费潜力', '缺乏专注'], suit: 'major', element: '风', astrologicalCorrespondence: '水星' },
  { name: 'The High Priestess', nameChinese: '女祭司', number: 2, keywords: ['直觉', '神秘', '内在智慧'], reversedKeywords: ['忽视直觉', '情感疏离', '内心封闭'], suit: 'major', element: '水', astrologicalCorrespondence: '月亮' },
  { name: 'The Empress', nameChinese: '女皇', number: 3, keywords: ['丰饶', '母性', '创造'], reversedKeywords: ['创造力受阻', '过度依赖', '精力耗竭'], suit: 'major', element: '土', astrologicalCorrespondence: '金星' },
  { name: 'The Emperor', nameChinese: '皇帝', number: 4, keywords: ['权威', '稳定', '领导'], reversedKeywords: ['滥用权力', '刚愎自用', '混乱失序'], suit: 'major', element: '火', astrologicalCorrespondence: '白羊座' },
  { name: 'The Hierophant', nameChinese: '教皇', number: 5, keywords: ['传统', '信仰', '指导'], reversedKeywords: ['质疑传统', '盲目顺从', '教条主义'], suit: 'major', element: '土', astrologicalCorrespondence: '金牛座' },
  { name: 'The Lovers', nameChinese: '恋人', number: 6, keywords: ['爱情', '选择', '和谐'], reversedKeywords: ['关系不和', '选择失误', '沟通不畅'], suit: 'major', element: '风', astrologicalCorrespondence: '双子座' },
  { name: 'The Chariot', nameChinese: '战车', number: 7, keywords: ['胜利', '意志', '决心'], reversedKeywords: ['失去控制', '方向迷失', '意志薄弱'], suit: 'major', element: '水', astrologicalCorrespondence: '巨蟹座' },
  { name: 'Strength', nameChinese: '力量', number: 8, keywords: ['勇气', '耐心', '内在力量'], reversedKeywords: ['软弱无力', '缺乏自信', '情绪失控'], suit: 'major', element: '火', astrologicalCorrespondence: '狮子座' },
  { name: 'The Hermit', nameChinese: '隐士', number: 9, keywords: ['内省', '寻求', '智慧'], reversedKeywords: ['过度孤立', '逃避现实', '迷失困惑'], suit: 'major', element: '土', astrologicalCorrespondence: '处女座' },
  { name: 'Wheel of Fortune', nameChinese: '命运之轮', number: 10, keywords: ['转变', '机遇', '命运'], reversedKeywords: ['厄运挫折', '抗拒变化', '错失良机'], suit: 'major', element: '火', astrologicalCorrespondence: '木星' },
  { name: 'Justice', nameChinese: '正义', number: 11, keywords: ['公平', '真相', '因果'], reversedKeywords: ['不诚实', '不公正', '逃避责任'], suit: 'major', element: '风', astrologicalCorrespondence: '天秤座' },
  { name: 'The Hanged Man', nameChinese: '倒吊人', number: 12, keywords: ['牺牲', '等待', '新视角'], reversedKeywords: ['停滞不前', '抗拒改变', '执着旧观念'], suit: 'major', element: '水', astrologicalCorrespondence: '海王星' },
  { name: 'Death', nameChinese: '死神', number: 13, keywords: ['结束', '转变', '重生'], reversedKeywords: ['抗拒转变', '恐惧结束', '执着过去'], suit: 'major', element: '水', astrologicalCorrespondence: '天蝎座' },
  { name: 'Temperance', nameChinese: '节制', number: 14, keywords: ['平衡', '耐心', '调和'], reversedKeywords: ['失衡失调', '急躁冲动', '过度放纵'], suit: 'major', element: '火', astrologicalCorrespondence: '射手座' },
  { name: 'The Devil', nameChinese: '恶魔', number: 15, keywords: ['束缚', '欲望', '物质'], reversedKeywords: ['挣脱束缚', '否认压抑', '沉溺恶习'], suit: 'major', element: '土', astrologicalCorrespondence: '摩羯座' },
  { name: 'The Tower', nameChinese: '塔', number: 16, keywords: ['突变', '觉醒', '解放'], reversedKeywords: ['恐惧变革', '否认问题', '执着幻象'], suit: 'major', element: '火', astrologicalCorrespondence: '火星' },
  { name: 'The Star', nameChinese: '星星', number: 17, keywords: ['希望', '灵感', '宁静'], reversedKeywords: ['绝望失望', '丧失信念', '创造力受阻'], suit: 'major', element: '风', astrologicalCorrespondence: '水瓶座' },
  { name: 'The Moon', nameChinese: '月亮', number: 18, keywords: ['幻觉', '直觉', '潜意识'], reversedKeywords: ['幻象消散', '直觉受阻', '自我欺骗'], suit: 'major', element: '水', astrologicalCorrespondence: '双鱼座' },
  { name: 'The Sun', nameChinese: '太阳', number: 19, keywords: ['成功', '快乐', '活力'], reversedKeywords: ['短暂挫折', '过度自信', '缺乏清晰'], suit: 'major', element: '火', astrologicalCorrespondence: '太阳' },
  { name: 'Judgement', nameChinese: '审判', number: 20, keywords: ['觉醒', '重生', '召唤'], reversedKeywords: ['自我怀疑', '否认召唤', '严苛自我批判'], suit: 'major', element: '火', astrologicalCorrespondence: '冥王星' },
  { name: 'The World', nameChinese: '世界', number: 21, keywords: ['完成', '整合', '成就'], reversedKeywords: ['目标未竟', '缺乏圆满', '困于循环'], suit: 'major', element: '土', astrologicalCorrespondence: '土星' },
];

// ===== 小阿卡纳：权杖 (Wands / 火) =====
const WANDS: TarotCardDefinition[] = [
  { name: 'Ace of Wands', nameChinese: '权杖一', keywords: ['创造力', '意志力', '灵感'], reversedKeywords: ['缺乏热情', '精力不足', '无聊倦怠'], suit: 'wands', element: '火' },
  { name: 'Two of Wands', nameChinese: '权杖二', keywords: ['规划', '决策', '远见'], reversedKeywords: ['恐惧变化', '犹豫不决', '缺乏计划'], suit: 'wands', element: '火' },
  { name: 'Three of Wands', nameChinese: '权杖三', keywords: ['扩展', '远见', '快速成长'], reversedKeywords: ['障碍阻碍', '延误挫折', '缺乏远见'], suit: 'wands', element: '火' },
  { name: 'Four of Wands', nameChinese: '权杖四', keywords: ['庆祝', '家庭', '和谐'], reversedKeywords: ['缺乏支持', '家庭冲突', '动荡不安'], suit: 'wands', element: '火' },
  { name: 'Five of Wands', nameChinese: '权杖五', keywords: ['竞争', '冲突', '对抗'], reversedKeywords: ['逃避冲突', '压抑愤怒', '内心矛盾'], suit: 'wands', element: '火' },
  { name: 'Six of Wands', nameChinese: '权杖六', keywords: ['胜利', '成功', '公众认可'], reversedKeywords: ['过度骄傲', '缺乏认可', '名不副实'], suit: 'wands', element: '火' },
  { name: 'Seven of Wands', nameChinese: '权杖七', keywords: ['坚守', '防御', '毅力'], reversedKeywords: ['信心崩溃', '不堪重负', '放弃退让'], suit: 'wands', element: '火' },
  { name: 'Eight of Wands', nameChinese: '权杖八', keywords: ['迅速行动', '进展', '果断决策'], reversedKeywords: ['恐慌焦虑', '停滞等待', '进展缓慢'], suit: 'wands', element: '火' },
  { name: 'Nine of Wands', nameChinese: '权杖九', keywords: ['坚韧', '勇气', '最后坚守'], reversedKeywords: ['精疲力竭', '过度防备', '质疑动机'], suit: 'wands', element: '火' },
  { name: 'Ten of Wands', nameChinese: '权杖十', keywords: ['责任', '重担', '坚持完成'], reversedKeywords: ['不堪重负', '过度压力', '无法委托'], suit: 'wands', element: '火' },
  { name: 'Page of Wands', nameChinese: '权杖侍从', keywords: ['探索', '热情', '自由'], reversedKeywords: ['缺乏方向', '拖延犹豫', '制造冲突'], suit: 'wands', element: '火' },
  { name: 'Knight of Wands', nameChinese: '权杖骑士', keywords: ['行动', '冒险', '无畏'], reversedKeywords: ['愤怒冲动', '鲁莽行事', '缺乏承诺'], suit: 'wands', element: '火' },
  { name: 'Queen of Wands', nameChinese: '权杖王后', keywords: ['自信', '决心', '热情魅力'], reversedKeywords: ['自私嫉妒', '缺乏安全感', '隐藏真我'], suit: 'wands', element: '火' },
  { name: 'King of Wands', nameChinese: '权杖国王', keywords: ['领导力', '远见卓识', '创业精神'], reversedKeywords: ['冲动专断', '期望过高', '缺乏执行'], suit: 'wands', element: '火' },
];

// ===== 小阿卡纳：圣杯 (Cups / 水) =====
const CUPS: TarotCardDefinition[] = [
  { name: 'Ace of Cups', nameChinese: '圣杯一', keywords: ['新感情', '灵性', '直觉'], reversedKeywords: ['情感失落', '创造力受阻', '内心空虚'], suit: 'cups', element: '水' },
  { name: 'Two of Cups', nameChinese: '圣杯二', keywords: ['伙伴关系', '吸引', '和谐'], reversedKeywords: ['失衡', '沟通破裂', '关系紧张'], suit: 'cups', element: '水' },
  { name: 'Three of Cups', nameChinese: '圣杯三', keywords: ['庆祝', '友谊', '合作'], reversedKeywords: ['过度放纵', '流言蜚语', '孤立疏离'], suit: 'cups', element: '水' },
  { name: 'Four of Cups', nameChinese: '圣杯四', keywords: ['冷漠', '沉思', '不满足'], reversedKeywords: ['突然觉醒', '选择快乐', '接纳现实'], suit: 'cups', element: '水' },
  { name: 'Five of Cups', nameChinese: '圣杯五', keywords: ['失落', '悲伤', '自怜'], reversedKeywords: ['接受释怀', '走出悲伤', '找到平静'], suit: 'cups', element: '水' },
  { name: 'Six of Cups', nameChinese: '圣杯六', keywords: ['怀旧', '美好回忆', '疗愈'], reversedKeywords: ['向前看', '离开过去', '独立成长'], suit: 'cups', element: '水' },
  { name: 'Seven of Cups', nameChinese: '圣杯七', keywords: ['幻想', '选择', '白日梦'], reversedKeywords: ['缺乏目标', '注意力分散', '迷茫困惑'], suit: 'cups', element: '水' },
  { name: 'Eight of Cups', nameChinese: '圣杯八', keywords: ['离开', '放下', '寻求更深意义'], reversedKeywords: ['逃避现实', '恐惧改变', '害怕失去'], suit: 'cups', element: '水' },
  { name: 'Nine of Cups', nameChinese: '圣杯九', keywords: ['满足', '情感稳定', '愿望成真'], reversedKeywords: ['内心不满', '自满自得', '物质主义'], suit: 'cups', element: '水' },
  { name: 'Ten of Cups', nameChinese: '圣杯十', keywords: ['幸福', '圆满', '梦想成真'], reversedKeywords: ['梦想破碎', '家庭不和', '关系失调'], suit: 'cups', element: '水' },
  { name: 'Page of Cups', nameChinese: '圣杯侍从', keywords: ['惊喜', '梦想家', '敏感'], reversedKeywords: ['情感不成熟', '不安全感', '失望沮丧'], suit: 'cups', element: '水' },
  { name: 'Knight of Cups', nameChinese: '圣杯骑士', keywords: ['追随内心', '理想主义', '浪漫'], reversedKeywords: ['情绪化', '不切实际', '失望'], suit: 'cups', element: '水' },
  { name: 'Queen of Cups', nameChinese: '圣杯王后', keywords: ['慈悲', '平静', '关怀'], reversedKeywords: ['自我牺牲', '不安全感', '过度依赖'], suit: 'cups', element: '水' },
  { name: 'King of Cups', nameChinese: '圣杯国王', keywords: ['情感成熟', '掌控', '平衡'], reversedKeywords: ['冷漠疏离', '情绪波动', '判断失误'], suit: 'cups', element: '水' },
];

// ===== 小阿卡纳：宝剑 (Swords / 风) =====
const SWORDS: TarotCardDefinition[] = [
  { name: 'Ace of Swords', nameChinese: '宝剑一', keywords: ['突破', '清晰', '真相'], reversedKeywords: ['混乱', '误解', '残忍'], suit: 'swords', element: '风' },
  { name: 'Two of Swords', nameChinese: '宝剑二', keywords: ['抉择', '僵局', '平衡'], reversedKeywords: ['逃避决定', '优柔寡断', '信息过载'], suit: 'swords', element: '风' },
  { name: 'Three of Swords', nameChinese: '宝剑三', keywords: ['心碎', '悲伤', '分离'], reversedKeywords: ['恢复疗愈', '释怀宽恕', '走出伤痛'], suit: 'swords', element: '风' },
  { name: 'Four of Swords', nameChinese: '宝剑四', keywords: ['休息', '恢复', '沉思'], reversedKeywords: ['焦躁不安', '精疲力竭', '压力过大'], suit: 'swords', element: '风' },
  { name: 'Five of Swords', nameChinese: '宝剑五', keywords: ['冲突', '不择手段', '争斗'], reversedKeywords: ['怨恨不散', '渴望和解', '学会宽恕'], suit: 'swords', element: '风' },
  { name: 'Six of Swords', nameChinese: '宝剑六', keywords: ['过渡', '离开', '前行'], reversedKeywords: ['情感包袱', '未解问题', '抗拒转变'], suit: 'swords', element: '风' },
  { name: 'Seven of Swords', nameChinese: '宝剑七', keywords: ['欺骗', '策略', '隐秘行动'], reversedKeywords: ['坦白真相', '重新思考', '良心不安'], suit: 'swords', element: '风' },
  { name: 'Eight of Swords', nameChinese: '宝剑八', keywords: ['困境', '束缚', '自我设限'], reversedKeywords: ['自我接纳', '新视角', '重获自由'], suit: 'swords', element: '风' },
  { name: 'Nine of Swords', nameChinese: '宝剑九', keywords: ['焦虑', '绝望', '噩梦'], reversedKeywords: ['重燃希望', '寻求帮助', '走出绝望'], suit: 'swords', element: '风' },
  { name: 'Ten of Swords', nameChinese: '宝剑十', keywords: ['失败', '崩溃', '终结'], reversedKeywords: ['触底反弹', '否极泰来', '不可避免的结束'], suit: 'swords', element: '风' },
  { name: 'Page of Swords', nameChinese: '宝剑侍从', keywords: ['好奇', '求知', '思维敏捷'], reversedKeywords: ['欺骗操控', '言行不一', '空谈无行'], suit: 'swords', element: '风' },
  { name: 'Knight of Swords', nameChinese: '宝剑骑士', keywords: ['果断行动', '直言不讳', '坚定信念'], reversedKeywords: ['思维混乱', '精力分散', '强加于人'], suit: 'swords', element: '风' },
  { name: 'Queen of Swords', nameChinese: '宝剑王后', keywords: ['清醒判断', '果断决策', '坦诚沟通'], reversedKeywords: ['缺乏清晰', '犹豫不决', '情感冷漠'], suit: 'swords', element: '风' },
  { name: 'King of Swords', nameChinese: '宝剑国王', keywords: ['理性成熟', '洞察真相', '公正权威'], reversedKeywords: ['思维僵化', '过度理性', '固执己见'], suit: 'swords', element: '风' },
];

// ===== 小阿卡纳：星币 (Pentacles / 土) =====
const PENTACLES: TarotCardDefinition[] = [
  { name: 'Ace of Pentacles', nameChinese: '星币一', keywords: ['新财运', '机遇', '繁荣'], reversedKeywords: ['错失机会', '自我怀疑', '犹豫不决'], suit: 'pentacles', element: '土' },
  { name: 'Two of Pentacles', nameChinese: '星币二', keywords: ['平衡', '适应', '灵活'], reversedKeywords: ['不堪重负', '失衡混乱', '顾此失彼'], suit: 'pentacles', element: '土' },
  { name: 'Three of Pentacles', nameChinese: '星币三', keywords: ['团队合作', '技艺', '学习'], reversedKeywords: ['缺乏合作', '目标不一', '沟通不畅'], suit: 'pentacles', element: '土' },
  { name: 'Four of Pentacles', nameChinese: '星币四', keywords: ['保守', '安全感', '守护资源'], reversedKeywords: ['贪婪吝啬', '匮乏心态', '过度控制'], suit: 'pentacles', element: '土' },
  { name: 'Five of Pentacles', nameChinese: '星币五', keywords: ['困难', '匮乏', '艰难时期'], reversedKeywords: ['走出困境', '逐渐恢复', '重获希望'], suit: 'pentacles', element: '土' },
  { name: 'Six of Pentacles', nameChinese: '星币六', keywords: ['慷慨', '给予', '财务稳定'], reversedKeywords: ['能量失衡', '施恩图报', '不平等'], suit: 'pentacles', element: '土' },
  { name: 'Seven of Pentacles', nameChinese: '星币七', keywords: ['长期投资', '耐心', '评估'], reversedKeywords: ['急于求成', '进展缓慢', '质疑回报'], suit: 'pentacles', element: '土' },
  { name: 'Eight of Pentacles', nameChinese: '星币八', keywords: ['技能提升', '专注', '精益求精'], reversedKeywords: ['迷失方向', '过度执着细节', '视野狭隘'], suit: 'pentacles', element: '土' },
  { name: 'Nine of Pentacles', nameChinese: '星币九', keywords: ['丰收', '自给自足', '享受成果'], reversedKeywords: ['急于求成', '忽视享受', '缺乏感恩'], suit: 'pentacles', element: '土' },
  { name: 'Ten of Pentacles', nameChinese: '星币十', keywords: ['财富传承', '家族繁荣', '愿景实现'], reversedKeywords: ['脱离目标', '方向迷失', '缺乏成就感'], suit: 'pentacles', element: '土' },
  { name: 'Page of Pentacles', nameChinese: '星币侍从', keywords: ['新机遇', '学习成长', '潜力'], reversedKeywords: ['恐惧失败', '完美主义', '犹豫不前'], suit: 'pentacles', element: '土' },
  { name: 'Knight of Pentacles', nameChinese: '星币骑士', keywords: ['稳步前进', '坚持不懈', '务实'], reversedKeywords: ['急躁不耐', '厌倦乏味', '精力耗尽'], suit: 'pentacles', element: '土' },
  { name: 'Queen of Pentacles', nameChinese: '星币王后', keywords: ['务实关怀', '滋养', '脚踏实地'], reversedKeywords: ['能量失衡', '忽视身体', '脱离自然'], suit: 'pentacles', element: '土' },
  { name: 'King of Pentacles', nameChinese: '星币国王', keywords: ['财富成就', '长远成功', '实干家'], reversedKeywords: ['物质失衡', '思维僵化', '方法固执'], suit: 'pentacles', element: '土' },
];

// 完整的78张塔罗牌
export const TAROT_CARDS: TarotCardDefinition[] = [...MAJOR_ARCANA, ...WANDS, ...CUPS, ...SWORDS, ...PENTACLES];

// 牌阵定义
export const TAROT_SPREADS: TarotSpreadDefinition[] = [
  { id: 'single', name: '单牌', positions: ['当前状况'] },
  { id: 'three-card', name: '三牌阵', positions: ['过去', '现在', '未来'] },
  { id: 'love', name: '爱情牌阵', positions: ['你的状态', '对方状态', '关系现状', '建议'] },
  {
    id: 'celtic-cross',
    name: '凯尔特十字',
    positions: ['现状', '交叉/挑战', '根基', '近期过去', '冠冕/最佳可能', '近期未来', '自我态度', '外部影响', '希望与恐惧', '结果'],
  },
  {
    id: 'horseshoe',
    name: '马蹄形',
    positions: ['过去', '现在', '潜在影响', '障碍', '外部环境', '建议', '可能结果'],
  },
  {
    id: 'decision',
    name: '抉择',
    positions: ['当前处境', '选项A', '选项B', '选项A结果', '选项B结果'],
  },
  { id: 'mind-body-spirit', name: '身心灵', positions: ['心智', '身体', '灵性'] },
  { id: 'situation', name: '处境/障碍/建议', positions: ['处境', '障碍', '建议'] },
  { id: 'yes-no', name: '是否', positions: ['答案'] },
];

const SPREADS: Record<string, TarotSpreadDefinition> = Object.fromEntries(TAROT_SPREADS.map((item) => [item.id, item]));

// 随机抽牌
function drawCards(count: number, allowReversed: boolean, rng: () => number): Array<{
  card: TarotCardDefinition;
  orientation: 'upright' | 'reversed';
}> {
  const deck = [...TAROT_CARDS];
  const drawn: Array<{ card: TarotCardDefinition; orientation: 'upright' | 'reversed'; }> = [];

  for (let i = 0; i < count && deck.length > 0; i++) {
    const idx = Math.floor(rng() * deck.length);
    const card = deck.splice(idx, 1)[0];
    const orientation = allowReversed && rng() > 0.5 ? 'reversed' : 'upright';
    drawn.push({ card, orientation });
  }

  return drawn;
}

// 获取牌义
function getMeaning(orientation: 'upright' | 'reversed', keywords: string[], reversedKeywords?: string[]): string {
  if (orientation === 'upright') {
    return `正位：${keywords.join('、')}`;
  }
  if (reversedKeywords && reversedKeywords.length > 0) {
    return `逆位：${reversedKeywords.join('、')}`;
  }
  return `逆位：需要反思${keywords.join('、')}相关的问题`;
}

// 数字缩减到 1-21 范围（塔罗数秘术，对应大阿卡纳 I-XXI）
// 22 继续缩减为 4（皇帝），这是主流做法
function reduceToArcana(num: number): number {
  while (num > 21) {
    num = String(num).split('').reduce((s, d) => s + Number(d), 0);
  }
  return num;
}

// 计算生命牌/人格牌和灵魂牌
function calculatePersonalityAndSoulCards(birthYear: number, birthMonth: number, birthDay: number): { personalityCard: number; soulCard: number; } {
  const digits = `${birthMonth}${birthDay}${birthYear}`.split('').reduce((s, d) => s + Number(d), 0);
  const personalityCard = reduceToArcana(digits);
  const soulCard = personalityCard > 9
    ? String(personalityCard).split('').reduce((s, d) => s + Number(d), 0)
    : personalityCard;
  return { personalityCard, soulCard };
}

// 计算年度牌
function calculateYearlyCard(birthMonth: number, birthDay: number, currentYear: number): number {
  const digits = `${birthMonth}${birthDay}${currentYear}`.split('').reduce((s, d) => s + Number(d), 0);
  return reduceToArcana(digits);
}

// 根据大阿卡纳编号获取牌名
function getMajorArcanaByNumber(num: number): TarotCardDefinition | undefined {
  return MAJOR_ARCANA.find(c => c.number === num);
}

export async function calculateTarotData(input: TarotInput): Promise<TarotOutput> {
  const { spreadType = 'single', question, allowReversed = true } = input;
  const dateKey = new Date().toISOString().slice(0, 10);
  const seed = resolveSeed(input.seed, `${spreadType}|${question || ''}|${dateKey}`, input.seedScope);
  const rng = createSeededRng(seed);

  const spread = SPREADS[spreadType] || SPREADS['single'];
  const drawnCards = drawCards(spread.positions.length, allowReversed, rng);

  const cards: TarotCardResult[] = drawnCards.map((drawn, index) => {
    const result: TarotCardResult = {
      position: spread.positions[index],
      card: {
        name: drawn.card.name,
        nameChinese: drawn.card.nameChinese,
        keywords: drawn.card.keywords,
      },
      orientation: drawn.orientation,
      meaning: getMeaning(drawn.orientation, drawn.card.keywords, drawn.card.reversedKeywords),
    };
    if (drawn.card.number !== undefined) {
      result.number = drawn.card.number;
    }
    if (drawn.card.reversedKeywords) {
      result.reversedKeywords = drawn.card.reversedKeywords;
    }
    if (drawn.card.element) {
      result.element = drawn.card.element;
    }
    if (drawn.card.astrologicalCorrespondence) {
      result.astrologicalCorrespondence = drawn.card.astrologicalCorrespondence;
    }
    return result;
  });

  const output: TarotOutput = {
    spreadId: spreadType,
    spreadName: spread.name,
    question,
    seed,
    cards,
  };

  if (input.birthYear && input.birthMonth && input.birthDay) {
    output.birthDate = `${input.birthYear}-${String(input.birthMonth).padStart(2, '0')}-${String(input.birthDay).padStart(2, '0')}`;
  }

  // 如果提供了生日信息，计算生命牌/灵魂牌/年度牌
  if (input.birthMonth && input.birthDay && input.birthYear) {
    const { personalityCard, soulCard } = calculatePersonalityAndSoulCards(input.birthYear, input.birthMonth, input.birthDay);
    const currentYear = new Date().getFullYear();
    const yearlyCard = calculateYearlyCard(input.birthMonth, input.birthDay, currentYear);

    const personalityArcana = getMajorArcanaByNumber(personalityCard);
    const soulArcana = getMajorArcanaByNumber(soulCard);
    const yearlyArcana = getMajorArcanaByNumber(yearlyCard);

    output.numerology = {
      personalityCard: {
        number: personalityCard,
        name: personalityArcana?.name || '',
        nameChinese: personalityArcana?.nameChinese || '',
        keywords: personalityArcana?.keywords,
        element: personalityArcana?.element,
        astrologicalCorrespondence: personalityArcana?.astrologicalCorrespondence,
      },
      soulCard: {
        number: soulCard,
        name: soulArcana?.name || '',
        nameChinese: soulArcana?.nameChinese || '',
        keywords: soulArcana?.keywords,
        element: soulArcana?.element,
        astrologicalCorrespondence: soulArcana?.astrologicalCorrespondence,
      },
      yearlyCard: {
        number: yearlyCard,
        name: yearlyArcana?.name || '',
        nameChinese: yearlyArcana?.nameChinese || '',
        keywords: yearlyArcana?.keywords,
        element: yearlyArcana?.element,
        astrologicalCorrespondence: yearlyArcana?.astrologicalCorrespondence,
        year: currentYear,
      },
    };
  }

  return output;
}

/**
 * 简化的问题分析器
 * 从 enhanced-shared.ts 中提取核心功能，去除冗余
 */

// ============================================================================
// 问题分析相关类型（从 types.ts 合并）
// ============================================================================

/** 问题类型检测结果 */
interface QuestionType {
  isQuestion: boolean;
  isChoice: boolean;
  isTime: boolean;
  isAction: boolean;
  isFeasibility: boolean;
  isRelationship: boolean;
  isCareer: boolean;
  isFinance: boolean;
  isHealth: boolean;
  isStudy: boolean;
  isReason: boolean;
  isPrediction: boolean;
  isAdvice: boolean;
  isComparison: boolean;
  isQuantity: boolean;
  isLocation: boolean;
  isPerson: boolean;
}

/** 复杂度评估结果 */
interface ComplexityLevel {
  complexity: 'simple' | 'medium' | 'complex';
  factors: string[];
  requiredDepth: number;
  timeUrgency: 'low' | 'medium' | 'high';
  importance: 'low' | 'medium' | 'high';
}

/** 情感状态检测结果 */
interface EmotionState {
  emotion: 'anxious' | 'hopeful' | 'confused' | 'determined' | 'neutral';
  intensity: number;
  supportNeeded: string;
}

/** 用户经验水平 */
interface UserExperienceLevel {
  level: 'beginner' | 'intermediate' | 'advanced';
  familiarity: number;
  terminologyTolerance: number;
}

/** 问题分析完整结果 */
export interface QuestionAnalysis {
  types: QuestionType;
  complexity: ComplexityLevel;
  emotion: EmotionState;
  userExperience: UserExperienceLevel;
}

/**
 * 检测问题类型
 */
export function detectQuestionTypes(question: string): QuestionType {
  return {
    // 判断类问题
    isQuestion:
      /能不能|可不可以|是不是|能否|可以吗|对吗|好吗|行吗|会不会|有没有|值得吗|该不该|要不要/.test(
        question,
      ),

    // 选择类问题
    isChoice: /还是|或者|选哪个|选择哪个|哪一个更好|比较一下|哪个好/.test(question),

    // 时间类问题
    isTime: /什么时候|何时|几时|多久|什么时候能|何时能|几时能|多久能|时间|期限|日程|安排|时机/.test(
      question,
    ),

    // 行动类问题
    isAction: /怎么做|如何|怎么办|怎么处理|怎么解决|方法|步骤|流程|策略|方案/.test(question),

    // 可行性类问题
    isFeasibility: /可行|合适|适合|有利|成功|能成|能实现|能达成|可能性|概率|机会|希望/.test(
      question,
    ),

    // 感情类问题
    isRelationship:
      /感情|爱情|关系|恋爱|结婚|分手|复合|喜欢|爱|暗恋|表白|约会|夫妻|情侣|恋人|伴侣/.test(
        question,
      ),

    // 事业类问题
    isCareer: /工作|事业|职业|job|职位|就业|失业|跳槽|升职|加薪|老板|同事|公司|创业|生意|业务/.test(
      question,
    ),

    // 财运类问题
    isFinance: /钱|财富|财运|收入|支出|投资|理财|赚钱|赔钱|债务|贷款|财务|经济|买卖|交易/.test(
      question,
    ),

    // 健康类问题
    isHealth: /健康|身体|疾病|病情|治疗|康复|医院|医生|药|体检|症状|疼痛|不舒服|养生|保健/.test(
      question,
    ),

    // 学业类问题
    isStudy: /学习|考试|成绩|学校|老师|同学|升学|毕业|论文|作业|课程|专业|技能|知识|教育/.test(
      question,
    ),

    // 原因类问题
    isReason: /为什么|为何|什么原因|怎么回事|什么情况|为什么能|为什么不能/.test(question),

    // 预测类问题
    isPrediction: /会怎么样|将来|未来|前景|趋势|发展|结果|后果|命运|运势|预示|预兆/.test(question),

    // 建议类问题
    isAdvice: /建议|意见|看法|想法|推荐|指导|指点|提醒|告诉|告知/.test(question),

    // 比较类问题
    isComparison: /对比|比较|区别|差异|优劣|好坏|强弱|哪个更好|哪个更适合/.test(question),

    // 数量类问题
    isQuantity: /多少|几个|几岁|多长|多高|多重|多深|多宽|程度|比例|百分比/.test(question),

    // 地点类问题
    isLocation: /哪里|哪儿|什么地方|哪个地方|位置|地点|地址|方向/.test(question),

    // 人物类问题
    isPerson: /谁|什么人|什么样的人|哪个|哪位|人物|人|他|她|他们|她们/.test(question),
  };
}

/**
 * 评估问题复杂度
 */
export function evaluateQuestionComplexity(question: string): ComplexityLevel {
  const factors: string[] = [];
  let complexityScore = 0;

  // 基于问题长度
  if (question.length > 50) {
    factors.push('问题描述详细');
    complexityScore += 1;
  }

  // 基于问题类型数量
  const types = detectQuestionTypes(question);
  const typeCount = Object.values(types).filter(Boolean).length;
  if (typeCount > 2) {
    factors.push('多维度问题');
    complexityScore += 2;
  }

  // 基于关键词复杂度
  const complexKeywords =
    /策略|规划|长期|影响|后果|风险|机会|挑战|平衡|协调|整合|优化|提升|改善|解决|处理|应对|预防|避免|促进|推动|实现|达成|获得|取得|达到|满足|符合|适应|调整|改变|转变|发展|进步|成长|突破|创新|改革|转型|升级|迭代|完善|健全|建立|构建|打造|创建|设计|制定|规划|安排|组织|协调|管理|控制|监督|指导|引导|支持|帮助|协助|配合|合作|联合|整合|融合|结合|混合|综合|全面|系统|整体|部分|细节|具体|抽象|理论|实践|经验|知识|技能|能力|素质|素养|品质|特性|特征|特点|优势|劣势|机会|威胁/i;

  if (complexKeywords.test(question)) {
    factors.push('涉及复杂概念');
    complexityScore += 2;
  }

  // 基于时间紧急程度
  const urgentKeywords =
    /紧急|马上|立刻|尽快|现在|今天|明天|本周|本月|急需|急切|迫在眉睫|火烧眉毛|十万火急|刻不容缓|当务之急|首当其冲|迫不及待|心急如焚|焦虑不安|忧心忡忡|寝食难安|坐立不安|辗转反侧|夜不能寐|日思夜想|朝思暮想|牵肠挂肚|魂牵梦绕|念念不忘|耿耿于怀|难以释怀|放不下心|操碎了心|费尽心机|绞尽脑汁|煞费苦心|苦心经营|精心策划|周密安排|详细计划|认真考虑|仔细思考|深入分析|全面评估|综合判断|权衡利弊|斟酌再三|三思而后行|深思熟虑|反复推敲|仔细琢磨|认真研究|深入探讨|广泛征求意见|集思广益|群策群力|同心协力|齐心协力|共同努力|共同奋斗|携手并进|并肩作战|同舟共济|风雨同舟|患难与共|生死与共|荣辱与共|休戚相关|息息相关|密不可分|缺一不可|相辅相成|相得益彰|相映成趣|相映生辉|相映成章|相映成趣|相映生辉|相映成章/i;

  const timeUrgency: 'low' | 'medium' | 'high' = urgentKeywords.test(question)
    ? 'high'
    : /什么时候|何时|几时|多久/.test(question)
      ? 'medium'
      : 'low';

  // 基于重要性关键词
  const importantKeywords =
    /重要|关键|核心|主要|首要|根本|基本|基础|本质|实质|关键|核心|要害|重点|焦点|中心|重心|重心|核心|关键|要害|重点|焦点|中心|重心|重心|重要|重大|严重|厉害|强烈|激烈|剧烈|猛烈|强烈/i;

  const importance: 'low' | 'medium' | 'high' = importantKeywords.test(question)
    ? 'high'
    : /决定|影响|关系|涉及|关于|相关|有关|联系|关联|连接|衔接|过渡|转换|变化|改变|转变|发展|进步|成长|提升|改善|优化|完善|健全|建立|构建|打造|创建|设计|制定|规划|安排|组织|协调|管理|控制|监督|指导|引导|支持|帮助|协助|配合|合作|联合|整合|融合|结合|混合|综合|全面|系统|整体|部分|细节|具体|抽象|理论|实践|经验|知识|技能|能力|素质|素养|品质|特性|特征|特点|优势|劣势|机会|威胁/i.test(
          question,
        )
      ? 'medium'
      : 'low';

  // 确定复杂度等级
  let complexity: 'simple' | 'medium' | 'complex';
  if (complexityScore <= 1) {
    complexity = 'simple';
  } else if (complexityScore <= 3) {
    complexity = 'medium';
  } else {
    complexity = 'complex';
  }

  // 计算所需深度
  const requiredDepth = complexity === 'simple' ? 3 : complexity === 'medium' ? 5 : 7;

  return {
    complexity,
    factors,
    requiredDepth,
    timeUrgency,
    importance,
  };
}

/**
 * 检测情感状态
 */
export function detectEmotionalState(question: string): EmotionState {
  const anxiousKeywords =
    /担心|焦虑|害怕|恐惧|紧张|不安|忧虑|忧愁|烦恼|困扰|痛苦|难受|煎熬|折磨|压力|负担|重担|累|疲惫|筋疲力尽|心力交瘁|身心俱疲|疲惫不堪|精疲力竭|力不从心|无能为力|无可奈何|束手无策|走投无路|山穷水尽|穷途末路|日暮途穷|穷途末路|走投无路|山穷水尽|日暮途穷|穷途末路|走投无路|山穷水尽|日暮途穷|穷途末路/i;

  const hopefulKeywords =
    /希望|期待|盼望|渴望|向往|憧憬|梦想|理想|目标|愿望|心愿|期盼|等待|守候|盼望|期望|指望|企盼|企望|希冀|希求|希图|企图|想要|愿意|乐意|喜欢|热爱|钟爱|深爱|挚爱|热爱|喜爱|爱好|嗜好|兴趣|乐趣|娱乐|消遣|休闲|放松|休息|休假|度假|旅游|旅行|出游|出门|外出|离开|走开|避开|逃避|躲开|藏起来|隐藏|隐匿|潜伏|埋伏|等候|等待|守候|期待|盼望|期望|指望|企盼|企望|希冀|希求|希图|企图|想要|愿意|乐意|喜欢|热爱|钟爱|深爱|挚爱|热爱|喜爱|爱好|嗜好|兴趣|乐趣|娱乐|消遣|休闲|放松|休息|休假|度假|旅游|旅行|出游|出门|外出|离开|走开|避开|逃避|躲开|藏起来|隐藏|隐匿|潜伏|埋伏/i;

  const confusedKeywords = /困惑|迷茫|糊涂|不明白|不理解|不清楚|不知道|不晓得|不了解|不熟悉/i;

  const determinedKeywords =
    /决心|决定|坚定|坚持|努力|奋斗|拼搏|争取|追求|目标|计划|行动|执行|实施|落实|完成|实现|达成|成功|胜利|克服|战胜|解决|处理|应对|面对|接受|承担|负责|担当|勇敢|坚强|坚定|坚决|果断|迅速|及时|主动|积极|乐观|自信|信任|相信|肯定|确定|明确|清晰|具体|详细|周密|完善|健全|建立|构建|打造|创建|设计|制定|规划|安排|组织|协调|管理|控制|监督|指导|引导|支持|帮助|协助|配合|合作|联合|整合|融合|结合|混合|综合|全面|系统|整体|部分|细节|具体|抽象|理论|实践|经验|知识|技能|能力|素质|素养|品质|特性|特征|特点|优势|劣势|机会|威胁/i;

  // 确定主要情感状态
  let emotion: EmotionState['emotion'] = 'neutral';
  let intensity = 0;

  if (anxiousKeywords.test(question)) {
    emotion = 'anxious';
    intensity = 0.8;
  } else if (hopefulKeywords.test(question)) {
    emotion = 'hopeful';
    intensity = 0.7;
  } else if (confusedKeywords.test(question)) {
    emotion = 'confused';
    intensity = 0.6;
  } else if (determinedKeywords.test(question)) {
    emotion = 'determined';
    intensity = 0.9;
  }

  // 计算支持需求
  let supportNeeded: string;
  switch (emotion) {
    case 'anxious':
      supportNeeded = '需要安抚和鼓励，提供安全感和确定性';
      break;
    case 'hopeful':
      supportNeeded = '需要肯定和指引，帮助实现目标';
      break;
    case 'confused':
      supportNeeded = '需要清晰的解释和方向指引';
      break;
    case 'determined':
      supportNeeded = '需要具体的行动建议和策略支持';
      break;
    default:
      supportNeeded = '需要客观分析和实用建议';
  }

  return {
    emotion,
    intensity,
    supportNeeded,
  };
}

/**
 * 评估用户经验水平
 */
function evaluateUserExperienceLevel(question: string): UserExperienceLevel {
  // 基于问题内容评估经验水平
  const beginnerKeywords =
    /简单|基础|入门|新手|第一次|刚开始|不懂|不会|不知道|请教|学习|了解|解释|说明|什么是|怎么用|如何做/i;

  const advancedKeywords =
    /深度|专业|详细|分析|解读|原理|机制|系统|全面|综合|多维度|深层次|内在|本质|规律|趋势|预测|预判|策略|规划|优化|提升|改善|解决|处理|应对|预防|避免|促进|推动|实现|达成|获得|取得|达到|满足|符合|适应|调整|改变|转变|发展|进步|成长|突破|创新|改革|转型|升级|迭代|完善|健全|建立|构建|打造|创建|设计|制定|规划|安排|组织|协调|管理|控制|监督|指导|引导|支持|帮助|协助|配合|合作|联合|整合|融合|结合|混合|综合|全面|系统|整体|部分|细节|具体|抽象|理论|实践|经验|知识|技能|能力|素质|素养|品质|特性|特征|特点|优势|劣势|机会|威胁/i;

  let level: UserExperienceLevel['level'] = 'intermediate';
  let familiarity = 0.5;
  let terminologyTolerance = 0.5;

  if (beginnerKeywords.test(question)) {
    level = 'beginner';
    familiarity = 0.2;
    terminologyTolerance = 0.3;
  } else if (advancedKeywords.test(question)) {
    level = 'advanced';
    familiarity = 0.8;
    terminologyTolerance = 0.9;
  }

  return {
    level,
    familiarity,
    terminologyTolerance,
  };
}

/**
 * 完整的问题分析
 */
export function analyzeQuestion(question: string): QuestionAnalysis {
  const types = detectQuestionTypes(question);
  const complexity = evaluateQuestionComplexity(question);
  const emotion = detectEmotionalState(question);
  const userExperience = evaluateUserExperienceLevel(question);

  return {
    types,
    complexity,
    emotion,
    userExperience,
  };
}

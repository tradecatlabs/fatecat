/**
 * 沟通建议模板库
 *
 * 根据冲突类型和关系类型提供针对性的沟通建议
 */

import type { HepanType } from '@/lib/divination/hepan';

// 冲突触发因素
export interface TriggerFactor {
    scenario: string;    // 触发情境
    trigger: string;     // 触发行为
    warning: string;     // 警示信息
    prevention: string;  // 预防建议
}

// 沟通建议模板
export interface CommunicationTemplate {
    title: string;
    context: string;           // 适用情境
    script: string;            // 沟通话术
    tips: string[];            // 沟通技巧
    avoidPhrases: string[];    // 避免用语
}

// 冲突类型
type ConflictType = '五行相克' | '五行被克' | '日支相冲' | '年支相冲' | 'default';

/**
 * 冲突触发因素配置
 * 每种冲突类型对应的常见触发情境
 */
export const CONFLICT_TRIGGERS: Record<ConflictType, TriggerFactor[]> = {
    '五行相克': [
        {
            scenario: '重大决策时刻',
            trigger: '一方强势主导决策，忽视对方意见',
            warning: '容易让被克方感到不被尊重，产生抵触心理',
            prevention: '重要决定前先征求对方意见，给予充分表达空间',
        },
        {
            scenario: '日常意见分歧',
            trigger: '以"我是为你好"为由强行干预',
            warning: '这种表达方式会加剧压制感',
            prevention: '用"我的建议是..."替代"你应该..."',
        },
        {
            scenario: '情绪紧张时期',
            trigger: '压力大时对对方提出过多要求',
            warning: '疲惫时更容易表现出控制欲',
            prevention: '双方都有压力时，先各自冷静，再沟通',
        },
    ],
    '五行被克': [
        {
            scenario: '寻求认可时',
            trigger: '被克方努力表现却得不到肯定',
            warning: '长期被忽视会导致关系疏离',
            prevention: '主动表达欣赏和认可，即使是小事',
        },
        {
            scenario: '个人空间需求',
            trigger: '被克方需要独处时间被打扰',
            warning: '缺乏喘息空间会积累负面情绪',
            prevention: '尊重对方的独处时间，这是充电的方式',
        },
        {
            scenario: '自信心受挫时',
            trigger: '无意中的批评或比较',
            warning: '被克方更敏感于负面评价',
            prevention: '注意措辞，多鼓励少批评',
        },
    ],
    '日支相冲': [
        {
            scenario: '日常生活习惯差异',
            trigger: '作息、饮食、家务分工等小事积累',
            warning: '日支相冲意味着生活节奏不同步',
            prevention: '制定双方都接受的家庭规则，相互妥协',
        },
        {
            scenario: '沟通方式冲突',
            trigger: '一方需要即时回应，另一方需要思考时间',
            warning: '沟通节奏不同易产生误解',
            prevention: '了解对方的沟通风格，给予适当等待',
        },
        {
            scenario: '计划安排分歧',
            trigger: '周末安排、节假日规划意见不合',
            warning: '频繁的计划冲突会消耗感情',
            prevention: '提前沟通，轮流决定，保持弹性',
        },
    ],
    '年支相冲': [
        {
            scenario: '家庭观念讨论',
            trigger: '对待双方父母的态度和资源分配',
            warning: '年支相冲往往反映家庭背景差异',
            prevention: '尊重彼此原生家庭，不评判对方家人',
        },
        {
            scenario: '价值观讨论',
            trigger: '对金钱、事业、人生目标的看法不同',
            warning: '根本性的价值观差异需要更多包容',
            prevention: '求同存异，专注共同目标',
        },
        {
            scenario: '传统习俗处理',
            trigger: '节日习俗、礼仪规矩的差异',
            warning: '各自坚持原生家庭习惯会产生摩擦',
            prevention: '创建属于你们的新传统',
        },
    ],
    'default': [
        {
            scenario: '压力累积期',
            trigger: '长期忽视小问题导致爆发',
            warning: '不沟通不代表没问题',
            prevention: '定期进行关系check-in，及时处理小矛盾',
        },
    ],
};

/**
 * 沟通建议模板配置
 * 根据关系类型和冲突类型提供针对性话术
 */
export const COMMUNICATION_TEMPLATES: Record<HepanType, Record<ConflictType, CommunicationTemplate>> = {
    love: {
        '五行相克': {
            title: '克制与尊重的平衡',
            context: '当你感到需要"指导"对方时',
            script: '我注意到这件事，想和你分享一下我的看法。你怎么想？我们可以一起讨论。',
            tips: [
                '用"我"开头表达感受，而非"你"开头指责',
                '提问多于断言，邀请对方参与决策',
                '承认对方的专业或判断力',
            ],
            avoidPhrases: [
                '你应该...',
                '你怎么又...',
                '我早就告诉过你...',
                '听我的准没错...',
            ],
        },
        '五行被克': {
            title: '表达需求的勇气',
            context: '当你感到被忽视或压制时',
            script: '我最近有些感受想和你分享。我需要更多的...，这对我很重要。',
            tips: [
                '直接表达需求，不要期待对方猜到',
                '肯定对方的好意，同时说明自己的感受',
                '设定健康的边界，温和但坚定',
            ],
            avoidPhrases: [
                '算了，说了你也不懂',
                '随便你吧',
                '我无所谓',
            ],
        },
        '日支相冲': {
            title: '差异中寻找共识',
            context: '日常习惯产生摩擦时',
            script: '我们在这件事上有不同的习惯，我想我们可以找个折中的方案。你觉得怎么安排比较好？',
            tips: [
                '承认差异是正常的，不是对错问题',
                '寻找双方都能接受的中间地带',
                '轮流让步，保持公平感',
            ],
            avoidPhrases: [
                '你就不能改一改吗',
                '正常人都是...',
                '我受不了你这样',
            ],
        },
        '年支相冲': {
            title: '家庭背景的融合',
            context: '家庭观念产生分歧时',
            script: '我理解我们的家庭背景不同，这些差异让我们更完整。我们可以创造属于我们自己的方式。',
            tips: [
                '尊重对方的原生家庭，不做评判',
                '理解习惯的形成需要时间改变',
                '创建新的共同记忆和传统',
            ],
            avoidPhrases: [
                '你们家就是这样...',
                '我家从来不这样',
                '你爸妈怎么教的你',
            ],
        },
        'default': {
            title: '开放式沟通',
            context: '需要增进了解时',
            script: '我想更了解你的想法，你愿意和我分享一下吗？',
            tips: [
                '保持好奇心和开放态度',
                '倾听时不要急于给建议',
                '定期安排两人时间进行深入交流',
            ],
            avoidPhrases: [
                '你总是...',
                '你从来不...',
            ],
        },
    },
    business: {
        '五行相克': {
            title: '决策权力的边界',
            context: '业务决策出现分歧时',
            script: '这个决定涉及你负责的领域，我想先听听你的专业判断。我的顾虑是...，我们一起权衡一下？',
            tips: [
                '明确各自的决策范围和权限',
                '在对方专业领域给予充分尊重',
                '用数据和事实支持观点，减少主观争论',
            ],
            avoidPhrases: [
                '这事你不懂，听我的',
                '我说了算',
                '你就负责执行就好',
            ],
        },
        '五行被克': {
            title: '争取话语权',
            context: '感觉意见被忽视时',
            script: '关于这个方案，我有一些不同的思考，想请你花几分钟听一下。这对我们的项目可能有帮助。',
            tips: [
                '准备充分再发言，用专业性赢得尊重',
                '选择合适的时机提出异议',
                '书面形式记录重要建议，避免被忽视',
            ],
            avoidPhrases: [
                '反正说了也没用',
                '你看着办吧',
            ],
        },
        '日支相冲': {
            title: '工作风格的协调',
            context: '工作节奏和方式不同时',
            script: '我们的工作方式有些不同，我想我们可以制定一个双方都舒服的协作流程。',
            tips: [
                '明确交付时间和质量标准',
                '建立定期同步机制',
                '尊重各自的工作习惯，结果导向',
            ],
            avoidPhrases: [
                '你效率太低了',
                '我不管你怎么做，反正要...',
            ],
        },
        '年支相冲': {
            title: '商业理念的融合',
            context: '经营理念产生分歧时',
            script: '我理解我们对公司发展有不同的愿景，也许我们可以找到一个结合双方优势的方向。',
            tips: [
                '定期进行战略对齐会议',
                '用试点验证想法，减少争论',
                '聘请第三方顾问提供客观意见',
            ],
            avoidPhrases: [
                '你那套过时了',
                '我的方法才是对的',
            ],
        },
        'default': {
            title: '专业协作',
            context: '日常业务沟通',
            script: '关于这个项目，我想和你同步一下进展，看看有什么需要协调的。',
            tips: [
                '保持定期沟通，信息透明',
                '就事论事，对事不对人',
                '记录重要决定，避免歧义',
            ],
            avoidPhrases: [
                '这不是我的问题',
            ],
        },
    },
    family: {
        '五行相克': {
            title: '关爱与控制的边界',
            context: '想要帮助但可能越界时',
            script: '我很关心你，想知道你对这件事的想法。如果需要我的建议或帮助，我随时都在。',
            tips: [
                '尊重孩子/父母的独立人格',
                '提供选择而非命令',
                '表达关心时避免附加条件',
            ],
            avoidPhrases: [
                '我都是为了你好',
                '你必须...',
                '不听老人言，吃亏在眼前',
            ],
        },
        '五行被克': {
            title: '建立健康的边界',
            context: '感到过度干预时',
            script: '我知道你是关心我的，但这件事我想自己处理。我会好好考虑的，有需要会告诉你。',
            tips: [
                '温和但坚定地表达边界',
                '感谢对方的关心，同时坚持立场',
                '适时分享进展，减少对方担忧',
            ],
            avoidPhrases: [
                '你别管了',
                '烦死了',
                '你不懂',
            ],
        },
        '日支相冲': {
            title: '代际生活习惯的包容',
            context: '生活方式产生冲突时',
            script: '我们的生活习惯有些不同，这是时代的差异。我们可以相互理解，找到平衡。',
            tips: [
                '接受代际差异是客观存在的',
                '在原则问题上坚持，小事上灵活',
                '找到共同喜欢的活动，增进感情',
            ],
            avoidPhrases: [
                '你们那一代...',
                '现在的年轻人...',
            ],
        },
        '年支相冲': {
            title: '传承与创新的平衡',
            context: '传统观念与现代思想碰撞时',
            script: '我尊重我们家的传统，也希望你能理解时代在变化。我们可以保留好的传统，同时接纳新的方式。',
            tips: [
                '理解长辈的价值观有其时代背景',
                '用实际行动而非争论来证明观点',
                '寻找传统与现代的结合点',
            ],
            avoidPhrases: [
                '老一套不管用了',
                '你们落伍了',
            ],
        },
        'default': {
            title: '家庭关爱',
            context: '日常家庭交流',
            script: '最近怎么样？有什么想和我说的吗？',
            tips: [
                '创造轻松的交流氛围',
                '多倾听，少说教',
                '表达爱意，即使不习惯',
            ],
            avoidPhrases: [
                '别人家的孩子...',
                '你看看人家...',
            ],
        },
    },
};

/**
 * 获取冲突触发因素
 */
export function getConflictTriggers(conflictTitle: string): TriggerFactor[] {
    const conflictType = conflictTitle as ConflictType;
    return CONFLICT_TRIGGERS[conflictType] || CONFLICT_TRIGGERS['default'];
}

/**
 * 获取沟通建议模板
 */
export function getCommunicationTemplate(
    hepanType: HepanType,
    conflictTitle: string
): CommunicationTemplate {
    const conflictType = conflictTitle as ConflictType;
    const templates = COMMUNICATION_TEMPLATES[hepanType];
    return templates[conflictType] || templates['default'];
}

/**
 * 根据冲突严重程度获取通用建议
 */
export function getSeverityAdvice(severity: 'low' | 'medium' | 'high'): string[] {
    const adviceMap: Record<typeof severity, string[]> = {
        high: [
            '建议寻求专业婚姻/家庭咨询师的帮助',
            '设定冷静期，避免在情绪激动时做决定',
            '制定明确的冲突处理规则，双方共同遵守',
        ],
        medium: [
            '定期进行深入的关系复盘',
            '学习一些情绪管理技巧',
            '在矛盾升级前主动暂停',
        ],
        low: [
            '保持开放的沟通态度',
            '及时表达感受，不要积压',
            '多关注对方的积极面',
        ],
    };
    return adviceMap[severity];
}

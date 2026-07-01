import type { ZiweiScopeMode } from '@/lib/query-state';
import type { InspirationCategory, QuestionInspirationIntent } from './ResultPage.types';

export const inspirationCategories: InspirationCategory[] = [
  '全部',
  '近期',
  '事业',
  '财运',
  '婚恋',
  '子女',
  '六亲',
  '家庭',
  '人际',
  '情绪',
  '健康',
  '学业',
  '成长',
  '天赋',
];

export const commonQuestionInspirations: Array<{
  category: Exclude<InspirationCategory, '全部'>;
  question: string;
  intent?: QuestionInspirationIntent;
}> = [
  { category: '近期', question: '我近期最该优先推进的事情是什么？' },
  { category: '近期', question: '我最近更适合主动出击，还是先稳住节奏？' },
  { category: '近期', question: '我近期最需要回避的风险点是什么？' },
  { category: '近期', question: '如果我最近想做调整，最值得先动哪一块？' },
  { category: '近期', question: '我现在这段时间的主线课题到底是什么？' },
  { category: '近期', question: '我近期更适合守成、变动，还是试探新机会？' },
  {
    category: '事业',
    question: '我现在适合换工作，还是先留在原岗位继续积累？',
    intent: 'job-change',
  },
  {
    category: '事业',
    question: '这次跳槽机会更值得抓住，还是先稳住现有节奏？',
    intent: 'job-change',
  },
  {
    category: '事业',
    question: '如果我现在想转方向，更适合留在原行业深耕，还是切换赛道？',
    intent: 'job-change',
  },
  {
    category: '事业',
    question: '我现在更适合创业、找人合作，还是先继续上班积累？',
    intent: 'startup-partnership',
  },
  {
    category: '事业',
    question: '如果我想自己做点事，现在更适合单干、合伙，还是先小范围试水？',
    intent: 'startup-partnership',
  },
  {
    category: '事业',
    question: '这条创业方向现在值得投入吗，还是更适合先观望准备？',
    intent: 'startup-partnership',
  },
  { category: '事业', question: '我更适合走稳定上班路线，还是尝试主动开拓发展？' },
  { category: '事业', question: '我在工作中更适合做执行、管理、专业技术，还是资源整合？' },
  { category: '事业', question: '我现在的事业卡点主要出在能力、人际还是选择方向？' },
  { category: '事业', question: '如果想换工作，我更该优先看平台、收入还是成长空间？' },
  { category: '事业', question: '我适不适合创业，还是更适合在体系内发展？' },
  { category: '事业', question: '我更适合留在熟悉领域深耕，还是切换到新方向？' },
  { category: '事业', question: '我在职场里最容易被看到的优势是什么？' },
  { category: '事业', question: '我在工作合作中更适合主导还是辅助？' },
  { category: '事业', question: '如果想提升事业发展，我最该先补哪一项能力？' },
  { category: '事业', question: '我的事业压力更多来自外部环境还是自己选择？' },
  { category: '财运', question: '我的财运更偏正财还是偏财？' },
  { category: '财运', question: '我更适合靠工资积累，还是靠副业、项目、经营来赚钱？' },
  { category: '财运', question: '我在财务上最容易踩的坑是什么？' },
  { category: '财运', question: '我更适合求稳理财，还是适度冒险争取更大收益？' },
  { category: '财运', question: '我的财富积累重点更在开源还是守财？' },
  { category: '财运', question: '我赚钱时更该依赖专业能力还是资源整合能力？' },
  { category: '财运', question: '我在金钱决策上更容易冲动还是保守？' },
  { category: '财运', question: '我是否容易出现赚得快但留不住的情况？' },
  {
    category: '财运',
    question: '我现在适合自己投、跟人合作求财，还是先守住现金流继续观望？',
    intent: 'investment-partnership',
  },
  {
    category: '财运',
    question: '这次投资或合作机会更像能放大的机会，还是容易带来额外风险和牵扯？',
    intent: 'investment-partnership',
  },
  {
    category: '财运',
    question: '如果我想靠项目、投资或合作赚钱，现在更适合主动布局还是先把风险控住？',
    intent: 'investment-partnership',
  },
  { category: '财运', question: '我适不适合和别人一起做生意或投资？' },
  { category: '财运', question: '如果要改善财务状态，我最该先管住哪一块？' },
  { category: '婚恋', question: '我的感情模式更容易主动、被动，还是反复拉扯？' },
  {
    category: '婚恋',
    question: '我现在更适合主动推进这段关系，还是先观察一段时间？',
    intent: 'relationship-push',
  },
  {
    category: '婚恋',
    question: '这段关系现在值得继续投入，还是该慢下来重新判断？',
    intent: 'relationship-push',
  },
  {
    category: '婚恋',
    question: '面对这段感情，我更该主动争取、稳定经营，还是及时止损？',
    intent: 'relationship-push',
  },
  {
    category: '婚恋',
    question: '这段关系我现在该继续投入，还是该及时抽身止损？',
    intent: 'relationship-decision',
  },
  {
    category: '婚恋',
    question: '如果继续这段关系，我是在等结果，还是在消耗自己？',
    intent: 'relationship-decision',
  },
  {
    category: '婚恋',
    question: '这段感情现在更适合继续观察，还是该尽快做去留判断？',
    intent: 'relationship-decision',
  },
  {
    category: '婚恋',
    question: '这段旧关系现在还有没有复合空间，我更适合争取、观察还是直接放下？',
    intent: 'reconciliation-decision',
  },
  {
    category: '婚恋',
    question: '如果我还想回头看这段关系，现在是在等机会，还是在继续消耗自己？',
    intent: 'reconciliation-decision',
  },
  {
    category: '婚恋',
    question: '这段旧感情当前更像能重新连接的机会，还是该趁早收口止损？',
    intent: 'reconciliation-decision',
  },
  { category: '婚恋', question: '我适合什么类型的伴侣？' },
  { category: '婚恋', question: '我的未来对象大概是怎样的人？' },
  { category: '婚恋', question: '我更容易在哪类场景或圈层遇到未来对象？' },
  { category: '婚恋', question: '未来对象出现时，我应该重点观察哪些信号？' },
  { category: '婚恋', question: '我在亲密关系里最需要调整的地方是什么？' },
  { category: '婚恋', question: '我感情不顺更容易出在选择对象还是相处方式？' },
  { category: '婚恋', question: '如果进入长期关系，我最需要注意什么问题？' },
  { category: '婚恋', question: '我在感情里更容易付出过多还是防备过重？' },
  { category: '婚恋', question: '我更适合慢热稳定型关系，还是强吸引型关系？' },
  { category: '婚恋', question: '我在关系中最容易触发的矛盾点是什么？' },
  { category: '婚恋', question: '我该怎么判断一段关系值不值得继续投入？' },
  { category: '婚恋', question: '我的婚恋重点更在遇到合适的人，还是学会正确相处？' },
  { category: '子女', question: '我的子女缘分深不深？' },
  { category: '子女', question: '我未来更可能有几个孩子，性别倾向分别是什么？' },
  { category: '子女', question: '我的孩子大概会是什么性格，我适合怎样教育和陪伴？' },
  { category: '子女', question: '如果出生时辰不准，子女数量和性别判断哪些地方最需要保守？' },
  { category: '子女', question: '我在亲子关系里更适合温和引导还是严格管理？' },
  { category: '子女', question: '我未来与子女的互动重点会体现在哪些方面？' },
  { category: '子女', question: '在子女教育上，我最需要避免什么做法？' },
  { category: '子女', question: '我与子女的关系更容易亲近还是有距离感？' },
  { category: '子女', question: '我在对子女的期待上会不会给自己太大压力？' },
  { category: '子女', question: '面对子女问题，我更该重视沟通还是规则建立？' },
  { category: '子女', question: '我的亲子关系中最需要注意的情绪模式是什么？' },
  { category: '六亲', question: '我和父母之间的关系重点与压力点是什么？' },
  {
    category: '六亲',
    question: '我六亲家人的健康整体怎么样，哪些亲人更需要多关注？',
    intent: 'family-health',
  },
  {
    category: '六亲',
    question: '父母、兄弟姐妹、伴侣和子女各自更需要注意哪些健康或照护问题？',
    intent: 'family-health',
  },
  {
    category: '六亲',
    question: '面对家人健康和照护压力，我现在最该提前做哪些安排？',
    intent: 'family-health',
  },
  { category: '六亲', question: '我和兄弟姐妹之间更容易互助还是有隐性消耗？' },
  { category: '六亲', question: '我在家庭关系中更容易承担责任，还是容易被关系拖累？' },
  { category: '六亲', question: '面对家人问题，我更适合主动介入还是保持边界？' },
  { category: '六亲', question: '我在家庭里更像支持者、协调者，还是承压者？' },
  { category: '六亲', question: '我与家人之间最需要厘清的边界问题是什么？' },
  { category: '六亲', question: '我在家庭责任分配上是否容易失衡？' },
  { category: '六亲', question: '我和原生家庭的影响更偏助力还是牵制？' },
  { category: '六亲', question: '我应该怎样处理亲情中的愧疚感和责任感？' },
  { category: '家庭', question: '我现在最需要调整的家庭边界问题是什么？' },
  { category: '家庭', question: '我的安全感更多要靠家庭关系，还是靠自己建立秩序？' },
  { category: '家庭', question: '我当前的家庭压力主要来自责任、情绪还是现实安排？' },
  { category: '家庭', question: '我更适合怎样经营居住环境，才能让状态更稳定？' },
  {
    category: '家庭',
    question: '我现在适合搬家、换城市或调整居住安排吗？',
    intent: 'home-move',
  },
  {
    category: '家庭',
    question: '如果考虑买房或长期定居，现在是合适的时机吗？',
    intent: 'home-move',
  },
  {
    category: '家庭',
    question: '这次居住调整更像机会，还是会带来额外压力和消耗？',
    intent: 'home-move',
  },
  {
    category: '家庭',
    question: '我现在更适合长期留在当前城市，还是考虑换城市重新扎根发展？',
    intent: 'settle-relocate',
  },
  {
    category: '家庭',
    question: '如果我要考虑长期定居，这一步更像顺势落地，还是还需要再观察一段时间？',
    intent: 'settle-relocate',
  },
  {
    category: '家庭',
    question: '这次换城或定居调整，真正要优先看的，是事业机会、生活稳定还是家庭牵动？',
    intent: 'settle-relocate',
  },
  { category: '家庭', question: '面对家里的长期议题，我现在更该协调、扛住，还是先立边界？' },
  { category: '家庭', question: '我和家人之间最需要先修复的是沟通、距离感还是责任分工？' },
  { category: '人际', question: '我在人际关系里最容易被误解的地方是什么？' },
  { category: '人际', question: '我当前最该筛掉哪类消耗型关系？' },
  { category: '人际', question: '我更适合主动经营人脉，还是把重心放在稳定合作关系上？' },
  { category: '人际', question: '我在合作中最容易吃亏的点是表达、边界还是利益分配？' },
  { category: '人际', question: '我现在的人际阻力主要来自外部环境，还是自己的互动方式？' },
  { category: '人际', question: '我更容易吸引到帮助我的贵人，还是让自己分心的关系？' },
  { category: '情绪', question: '我当前最容易被什么事情触发情绪波动？' },
  { category: '情绪', question: '我现在的内耗更像压力累积，还是安全感不足？' },
  { category: '情绪', question: '当我状态不稳时，最该先调整的是节奏、边界还是表达方式？' },
  { category: '情绪', question: '我是不是容易把关系问题、工作压力或家庭责任压在心里？' },
  { category: '情绪', question: '我最需要建立的情绪修复方式是什么？' },
  { category: '情绪', question: '我现在最该先处理哪种情绪模式，才能让状态稳下来？' },
  { category: '健康', question: '我的身体最需要注意哪些方面？' },
  { category: '健康', question: '我当前更容易出现情绪压力，还是身体透支问题？' },
  { category: '健康', question: '我的作息、饮食、运动里最该先调整哪一项？' },
  { category: '健康', question: '我在健康管理上最容易忽视的隐患是什么？' },
  { category: '健康', question: '我更需要注意慢性消耗，还是突然性的身体失衡？' },
  { category: '健康', question: '我的健康问题更容易和情绪、压力有关吗？' },
  { category: '健康', question: '如果只调整一个生活习惯，最该先改什么？' },
  { category: '健康', question: '我在休息和恢复方面最容易出现什么问题？' },
  { category: '学业', question: '我现在更适合稳扎稳打复习，还是集中突破短板？' },
  { category: '学业', question: '我的学习效率更依赖方法、节奏，还是环境管理？' },
  { category: '学业', question: '我在考试或面试场景里最容易出问题的环节是什么？' },
  {
    category: '学业',
    question: '我现在适合考证、读研进修，还是先把现实节奏稳住？',
    intent: 'study-advance',
  },
  {
    category: '学业',
    question: '如果继续深造，我更适合短期考证、长期进修，还是跨领域学习？',
    intent: 'study-advance',
  },
  {
    category: '学业',
    question: '这次学习投入对我来说更像值得冲刺的机会，还是成本过高的消耗？',
    intent: 'study-advance',
  },
  {
    category: '学业',
    question: '这次考试、面试或申请，我现在更适合全力冲刺、稳住发挥，还是先调整预期？',
    intent: 'exam-landing',
  },
  {
    category: '学业',
    question: '如果我想争取这次上岸机会，现在最大的关键在准备节奏、临场发挥还是目标选择？',
    intent: 'exam-landing',
  },
  {
    category: '学业',
    question: '这次考试或申请更像值得硬冲的窗口，还是该先稳住节奏避免失误？',
    intent: 'exam-landing',
  },
  { category: '学业', question: '如果继续进修，我更适合偏理论、偏实践，还是跨领域学习？' },
  { category: '学业', question: '我当前学业上的主要卡点更在专注力、理解力还是执行力？' },
  { category: '学业', question: '我现在最该先补哪一种学习能力，才能更快看到提升？' },
  { category: '成长', question: '我现在最需要先突破的性格卡点是什么？' },
  { category: '成长', question: '我反复卡住的旧模式，更多出现在关系、事业还是情绪里？' },
  { category: '成长', question: '我当前的人生课题更偏向学会坚持，还是学会放下？' },
  { category: '成长', question: '如果想让自己真正往前走，我最该先改哪一个习惯或观念？' },
  { category: '成长', question: '我现在更适合主动变动，还是先把内部状态整稳？' },
  { category: '成长', question: '我最需要整合的矛盾，是想要安全感还是想要更大空间？' },
  { category: '天赋', question: '我最值得长期放大的核心优势是什么？' },
  { category: '天赋', question: '我的表达、创造或组织能力更适合在哪类场景里发挥？' },
  { category: '天赋', question: '我最容易被别人看见和认可的能力是什么？' },
  { category: '天赋', question: '我的优势更适合做专业深耕、内容表达，还是资源整合？' },
  { category: '天赋', question: '我有哪些天赋其实已经有了，只是还没有用对地方？' },
  { category: '天赋', question: '如果只挑一个最该重点投资的能力方向，会是哪一个？' },
];

export const baziSingleShortcutActions = [
  {
    label: '综合' as const,
    promptId: 'ai-mingge-zonglun',
    question:
      '请做一份综合分析，按“命局特点、性格优势与短板、事业发展、财运节奏、婚恋关系、六亲互动、健康隐患、学业与成长、当前阶段提醒、落地建议”这几个部分展开，结论尽量具体。',
  },
  {
    label: '近期' as const,
    promptId: 'ai-recent',
    question:
      '请重点分析我当前阶段的主线、近期适合主动推进的事项、应该暂缓或规避的风险、节奏变化点，以及接下来更稳妥的行动建议。',
  },
  {
    label: '事业' as const,
    promptId: 'ai-career',
    question:
      '请重点分析我的事业方向、适合的发展路径、职场优势、容易遇到的阻力、适合上班还是创业、当前阶段的突破口，以及接下来更值得投入的方向。',
  },
  {
    label: '换工作' as const,
    promptId: 'ai-job-change',
    question:
      '请重点分析我现在适不适合换工作、转方向或试探新机会，并说明平台、收入、成长空间和短期风险的取舍重点。',
  },
  {
    label: '创业合作' as const,
    promptId: 'ai-startup-partnership',
    question:
      '请重点分析我现在适不适合创业、单干还是找人合作，并说明方向选择、资源来源、合作分工、现金流压力和现实风险。',
  },
  {
    label: '投资合作' as const,
    promptId: 'ai-investment-partnership',
    question:
      '请重点分析我现在适不适合投资、独立布局、跟人合作求财还是继续观望，并说明收益模式、资金压力、合作分工、风险边界和现实代价。',
  },
  {
    label: '财运' as const,
    promptId: 'ai-wealth-timing',
    question:
      '请重点分析我的财运类型、正财偏财表现、赚钱方式、起财时机、守财能力、容易破财的风险点，以及现阶段更稳妥的财务建议。',
  },
  {
    label: '婚恋' as const,
    promptId: 'ai-marriage',
    question:
      '请重点分析我的婚恋观与关系模式、适合的伴侣类型、感情中的优势和问题、婚缘节奏、进入长期关系后的注意点，以及当前最该调整的重点。',
  },
  {
    label: '关系推进' as const,
    promptId: 'ai-relationship-push',
    question:
      '请重点分析这段关系现在更适合主动推进、稳定经营、放慢观察还是及时止损，并说明投入价值、风险边界和接下来的判断标准。',
  },
  {
    label: '关系去留' as const,
    promptId: 'ai-relationship-decision',
    question:
      '请重点分析这段关系现在更适合继续投入、放慢观察、重新建立边界还是及时止损，并说明止损信号、继续条件和现实代价。',
  },
  {
    label: '复合判断' as const,
    promptId: 'ai-reconciliation-decision',
    question:
      '请重点分析这段旧关系现在还有没有复合空间，更适合争取、观察、先立边界还是及时放下，并说明复合条件、现实阻力、风险信号和判断标准。',
  },
  {
    label: '子女' as const,
    promptId: 'ai-children-fate',
    question:
      '请重点分析我的子女缘、子女互动模式、亲子关系中的优势与压力、教育相处重点、需要注意的阶段性问题，以及更适合的引导方式。',
  },
  {
    label: '六亲' as const,
    promptId: 'ai-family',
    question:
      '请重点分析我的六亲关系，分别说明与父母、兄弟姐妹、伴侣、子女之间的互动模式、助力与牵制、边界问题、责任压力，以及最需要改善的关系重点。',
  },
  {
    label: '家庭' as const,
    promptId: 'ai-home',
    question:
      '请重点分析我的原生家庭影响、安全感来源、家庭边界、居住秩序与现实责任分工，以及当前最需要调整的家庭议题。',
  },
  {
    label: '搬家置业' as const,
    promptId: 'ai-home-move',
    question:
      '请重点分析我现在适不适合搬家、换城市、买房置业或调整居住安排，并说明时机、成本压力、稳定性和风险重点。',
  },
  {
    label: '定居换城' as const,
    promptId: 'ai-settle-relocate',
    question:
      '请重点分析我现在适不适合长期定居、换城市发展、两地过渡还是继续留在当前城市，并说明稳定性、事业机会、家庭牵动、成本压力和行动顺序。',
  },
  {
    label: '人际' as const,
    promptId: 'ai-social',
    question:
      '请重点分析我的社交风格、合作关系、贵人来源、沟通短板、人脉筛选方式，以及当前更适合采取的人际策略。',
  },
  {
    label: '情绪' as const,
    promptId: 'ai-emotion',
    question:
      '请重点分析我的情绪触发点、压力来源、安全感需求、内耗模式与修复方式，以及当前最值得先调整的状态。',
  },
  {
    label: '健康' as const,
    promptId: 'ai-health',
    question:
      '请重点分析我最需要注意的健康隐患，说明更容易受影响的身心方向、压力与作息对健康的影响、生活习惯中的主要问题、日常调理重点，以及当前阶段的提醒。',
  },
  {
    label: '学业' as const,
    promptId: 'ai-study',
    question:
      '请重点分析我的学业运、理解力与专注力特点、考试发挥、适合的学习方式、容易拖后腿的问题、进修深造潜力，以及当前最有效的提升建议。',
  },
  {
    label: '考证进修' as const,
    promptId: 'ai-study-advance',
    question:
      '请重点分析我现在适不适合考证、读研进修或跨领域学习，并说明投入产出、执行压力、现实节奏和更稳妥的选择。',
  },
  {
    label: '考试上岸' as const,
    promptId: 'ai-exam-landing',
    question:
      '请重点分析这次考试、面试或申请更适合冲刺、稳住发挥还是调整预期，并说明上岸机会、失误风险、准备节奏和接下来最关键的动作。',
  },
  {
    label: '成长' as const,
    promptId: 'ai-growth',
    question:
      '请重点分析我最需要突破的性格卡点、长期成长课题、反复卡住的旧模式，以及可以直接执行的调整建议。',
  },
  {
    label: '天赋' as const,
    promptId: 'ai-talent',
    question:
      '请重点分析我的核心天赋、学习吸收、表达输出、组织执行和资源整合能力，以及最值得长期放大的优势方向。',
  },
] as const;

export const baziCompatibilityShortcutActions = [
  {
    label: '合婚' as const,
    promptId: 'ai-compat-marriage',
    question: '请重点分析我们两人的婚恋匹配度、长期磨合点和相处建议。',
  },
  {
    label: '合伙' as const,
    promptId: 'ai-compat-career',
    question: '请重点分析我们两人的合作模式、分工建议和利益风险。',
  },
  {
    label: '友情' as const,
    promptId: 'ai-compat-friendship',
    question: '请重点分析我们两人的相处默契、冲突点和关系建议。',
  },
  {
    label: '子女' as const,
    promptId: 'ai-compat-children',
    question: '请重点分析我们两人的子女缘分深浅、子女性格倾向和亲子相处重点。',
  },
  {
    label: '父母' as const,
    promptId: 'ai-compat-parents',
    question: '请重点分析我们双方父母的健康状况、需关注的风险方向和赡养建议。',
  },
  {
    label: '兄弟' as const,
    promptId: 'ai-compat-siblings',
    question: '请重点分析我们两人之间兄弟朋友关系的亲疏、助力与牵制、相处建议。',
  },
] as const;

export const ziweiSingleShortcutActions = [
  {
    label: '综合' as const,
    topic: 'life',
    question:
      '请做一份综合分析，按“人生主线、性格优势与短板、事业发展、财运节奏、婚恋关系、六亲互动、健康隐患、学业与成长、当前阶段提醒、落地建议”这几个部分展开，结论尽量具体。',
  },
  {
    label: '近期' as const,
    topic: 'recent',
    question:
      '请重点分析我当前阶段的主线、近期适合主动推进的事项、应该暂缓或规避的风险、节奏变化点，以及接下来更稳妥的行动建议。',
  },
  {
    label: '事业' as const,
    topic: 'career-wealth',
    question:
      '请重点分析我的事业方向、适合的发展路径、职场优势、容易遇到的阻力、适合上班还是创业、当前阶段的突破口，以及接下来更值得投入的方向。',
  },
  {
    label: '换工作' as const,
    topic: 'job-change',
    question:
      '请重点分析我现在适不适合换工作、转方向或试探新机会，并说明平台、收入、成长空间和短期风险的取舍重点。',
  },
  {
    label: '创业合作' as const,
    topic: 'startup-partnership',
    question:
      '请重点分析我现在适不适合创业、单干还是找人合作，并说明方向选择、资源来源、合作分工、现金流压力和现实风险。',
  },
  {
    label: '投资合作' as const,
    topic: 'investment-partnership',
    question:
      '请重点分析我现在适不适合投资、独立布局、跟人合作求财还是继续观望，并说明收益模式、资金压力、合作分工、风险边界和现实代价。',
  },
  {
    label: '财运' as const,
    topic: 'career-wealth',
    question:
      '请重点分析我的财运类型、赚钱抓手、正财偏财表现、起财节奏、守财能力、容易破财的风险点，以及现阶段更稳妥的财务建议。',
  },
  {
    label: '婚恋' as const,
    topic: 'relationship',
    question:
      '请重点分析我的婚恋观与关系模式、适合的伴侣类型、感情中的优势和问题、婚缘节奏、进入长期关系后的注意点，以及当前最该调整的重点。',
  },
  {
    label: '关系推进' as const,
    topic: 'relationship-push',
    question:
      '请重点分析这段关系现在更适合主动推进、稳定经营、放慢观察还是及时止损，并说明投入价值、风险边界和接下来的判断标准。',
  },
  {
    label: '关系去留' as const,
    topic: 'relationship-decision',
    question:
      '请重点分析这段关系现在更适合继续投入、放慢观察、重新建立边界还是及时止损，并说明止损信号、继续条件和现实代价。',
  },
  {
    label: '复合判断' as const,
    topic: 'reconciliation-decision',
    question:
      '请重点分析这段旧关系现在还有没有复合空间，更适合争取、观察、先立边界还是及时放下，并说明复合条件、现实阻力、风险信号和判断标准。',
  },
  {
    label: '子女' as const,
    topic: 'children',
    question:
      '请重点分析我的子女缘、子女互动模式、亲子关系中的优势与压力、教育相处重点、需要注意的阶段性问题，以及更适合的引导方式。',
  },
  {
    label: '六亲' as const,
    topic: 'family',
    question:
      '请重点分析我的六亲关系，分别说明与父母、兄弟姐妹、伴侣、子女之间的互动模式、助力与牵制、边界问题、责任压力，以及最需要改善的关系重点。',
  },
  {
    label: '家庭' as const,
    topic: 'family',
    question:
      '请重点分析我的原生家庭影响、安全感来源、家庭边界、居住秩序与现实责任分工，以及当前最需要调整的家庭议题。',
  },
  {
    label: '搬家置业' as const,
    topic: 'home-move',
    question:
      '请重点分析我现在适不适合搬家、换城市、买房置业或调整居住安排，并说明时机、成本压力、稳定性和风险重点。',
  },
  {
    label: '定居换城' as const,
    topic: 'settle-relocate',
    question:
      '请重点分析我现在适不适合长期定居、换城市发展、两地过渡还是继续留在当前城市，并说明稳定性、事业机会、家庭牵动、成本压力和行动顺序。',
  },
  {
    label: '人际' as const,
    topic: 'social',
    question:
      '请重点分析我的社交风格、合作关系、贵人来源、沟通短板、人脉筛选方式，以及当前更适合采取的人际策略。',
  },
  {
    label: '情绪' as const,
    topic: 'emotion',
    question:
      '请重点分析我的情绪触发点、压力来源、安全感需求、内耗模式与修复方式，以及当前最值得先调整的状态。',
  },
  {
    label: '健康' as const,
    topic: 'health',
    question:
      '请重点分析我最需要注意的健康隐患，说明更容易受影响的身心方向、压力与作息对健康的影响、生活习惯中的主要问题、日常养护重点，以及当前阶段的提醒。',
  },
  {
    label: '学业' as const,
    topic: 'study',
    question:
      '请重点分析我的学业运、理解力与专注力特点、考试发挥、适合的学习方式、容易拖后腿的问题、进修深造潜力，以及当前最有效的提升建议。',
  },
  {
    label: '考证进修' as const,
    topic: 'study-advance',
    question:
      '请重点分析我现在适不适合考证、读研进修或跨领域学习，并说明投入产出、执行压力、现实节奏和更稳妥的选择。',
  },
  {
    label: '考试上岸' as const,
    topic: 'exam-landing',
    question:
      '请重点分析这次考试、面试或申请更适合冲刺、稳住发挥还是调整预期，并说明上岸机会、失误风险、准备节奏和接下来最关键的动作。',
  },
  {
    label: '成长' as const,
    topic: 'growth',
    question:
      '请重点分析我最需要突破的性格卡点、长期成长课题、反复卡住的旧模式，以及可以直接执行的调整建议。',
  },
  {
    label: '天赋' as const,
    topic: 'talent',
    question:
      '请重点分析我的核心天赋、学习吸收、表达输出、组织执行和资源整合能力，以及最值得长期放大的优势方向。',
  },
] as const;

export const ziweiCompatibilityShortcutActions = [
  {
    label: '感情' as const,
    topic: 'relationship',
    question: '请重点分析双方关系匹配度、吸引点、冲突点和相处建议。',
  },
  {
    label: '合作' as const,
    topic: 'career-wealth',
    question: '请重点分析双方合作默契、优势互补和潜在风险。',
  },
  {
    label: '相处' as const,
    topic: 'chat',
    question: '请从双方盘面看互动模式、沟通盲点和长期建议。',
  },
] as const;

export const ziweiScopeLabelMap: Record<ZiweiScopeMode, string> = {
  origin: '本命',
  decadal: '大限',
  yearly: '流年',
  monthly: '流月',
  daily: '流日',
  hourly: '流时',
};

export const singlePromptShortcutSections = [
  {
    key: 'overview',
    title: '先看整体',
    description: '适合先判断大方向和近期主线。',
    labels: ['综合', '近期'],
  },
  {
    key: 'career',
    title: '工作与财务',
    description: '事业选择、跳槽、创业、合作和财运都放在这里。',
    labels: ['事业', '换工作', '创业合作', '投资合作', '财运'],
  },
  {
    key: 'relationship',
    title: '关系与家庭',
    description: '婚恋推进、关系去留、亲子和家庭议题集中处理。',
    labels: ['婚恋', '关系推进', '关系去留', '复合判断', '子女', '六亲', '家庭'],
  },
  {
    key: 'life',
    title: '生活与成长',
    description: '搬家、人际、情绪、健康、学习和天赋相关问题。',
    labels: [
      '搬家置业',
      '定居换城',
      '人际',
      '情绪',
      '健康',
      '学业',
      '考证进修',
      '考试上岸',
      '成长',
      '天赋',
    ],
  },
] as const;

export const ZIWEI_GRID_ORDER = [
  3,
  4,
  5,
  6,
  2,
  'center',
  'center-skip',
  7,
  1,
  'center-skip',
  'center-skip',
  8,
  0,
  11,
  10,
  9,
] as const;
export const PROMPT_DRAFT_STORAGE_PREFIX = 'result-prompt-draft';

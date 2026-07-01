export function getBaziDefaultQuestion(
  scene?: string,
  options: { isCustomQuestion?: boolean } = {},
) {
  if (options.isCustomQuestion) {
    return '请先做整体解读。';
  }

  switch (scene) {
    case 'recent':
      return '请先从当前阶段主线、近期节奏变化和风险提醒开始分析。';
    case 'career':
      return '请先从事业方向、工作模式和当前风险开始分析。';
    case 'job-change':
      return '请先从现在适不适合换工作、转方向和如何判断时机开始分析。';
    case 'startup-partnership':
      return '请先从适不适合创业、单干还是合作，以及如何判断当前时机开始分析。';
    case 'investment-partnership':
      return '请先从我现在适不适合投资、跟人合作求财还是继续观望开始分析。';
    case 'wealth':
      return '请先从财运节奏、赚钱方式和破财风险开始分析。';
    case 'marriage':
      return '请先从感情模式、适合对象和关系建议开始分析。';
    case 'relationship-push':
      return '请先从这段关系该主动推进、稳定经营还是先放慢开始分析。';
    case 'relationship-decision':
      return '请先从这段关系该继续投入、放手止损还是保持观察开始分析。';
    case 'reconciliation-decision':
      return '请先从这段旧关系现在还有没有复合空间，以及更适合争取、观察还是放下开始分析。';
    case 'children':
      return '请先从子女缘分、相处方式和教育重点开始分析。';
    case 'family':
      return '请先从家庭边界、安全感来源和现实分工开始分析。';
    case 'home-move':
      return '请先从现在适不适合搬家、换城市、买房置业和居住调整开始分析。';
    case 'settle-relocate':
      return '请先从我现在适不适合长期定居、换城市发展还是留在当前城市开始分析。';
    case 'social':
      return '请先从社交风格、合作关系和人际策略开始分析。';
    case 'emotion':
      return '请先从情绪触发点、压力反应和调节方式开始分析。';
    case 'health':
      return '请先从体质倾向、生活习惯和需要注意的风险开始分析。';
    case 'parents':
      return '请先从父母家人议题、支持压力和相处建议开始分析。';
    case 'study':
      return '请先从学习吸收、考试进修和提升方式开始分析。';
    case 'study-advance':
      return '请先从我适不适合考证、读研进修或跨领域学习开始分析。';
    case 'exam-landing':
      return '请先从这次考试、面试或申请更适合冲刺、稳住发挥还是调整预期开始分析。';
    case 'growth':
      return '请先从性格卡点、成长课题和改变抓手开始分析。';
    case 'talent':
      return '请先从核心天赋、优势放大和适合深耕的方向开始分析。';
    default:
      return '请先做整体解读。';
  }
}

export function getBaziCompatibilityDefaultQuestion(compatType?: string) {
  if (compatType === 'career') return '请先从合作分工、利益风险和长期建议开始分析。';
  if (compatType === 'friendship') return '请先从相处模式、边界感和关系建议开始分析。';
  if (compatType === 'children') return '请先从子女缘分、养育配合和亲子建议开始分析。';
  if (compatType === 'parents') return '请先从双方父母议题、照护压力和现实建议开始分析。';
  if (compatType === 'siblings') return '请先从亲疏模式、资源往来和相处建议开始分析。';
  return '请先从整体关系匹配度和相处建议开始分析。';
}

export function getZiweiDefaultQuestion(
  topic?: string,
  options: { isCustomQuestion?: boolean } = {},
) {
  if (options.isCustomQuestion) {
    return '请先做整体解读。';
  }

  switch (topic) {
    case 'recent':
      return '请先从当前阶段重点、推进节奏和风险提醒开始分析。';
    case 'destiny':
      return '请先从命格主线、性格优势和整体发展开始分析。';
    case 'relationship':
      return '请先从感情关系模式、适合对象和相处建议开始分析。';
    case 'relationship-push':
      return '请先从这段关系该主动推进、稳定经营还是先放慢开始分析。';
    case 'relationship-decision':
      return '请先从这段关系该继续投入、放手止损还是保持观察开始分析。';
    case 'reconciliation-decision':
      return '请先从这段旧关系现在还有没有复合空间，以及更适合争取、观察还是放下开始分析。';
    case 'children':
      return '请先从子女缘分、亲子互动和教育陪伴重点开始分析。';
    case 'career-wealth':
      return '请先从事业路径、财富方式和当前风险开始分析。';
    case 'job-change':
      return '请先从现在适不适合换工作、转方向和如何判断时机开始分析。';
    case 'startup-partnership':
      return '请先从适不适合创业、单干还是合作，以及如何判断当前时机开始分析。';
    case 'investment-partnership':
      return '请先从我现在适不适合投资、跟人合作求财还是继续观望开始分析。';
    case 'family':
      return '请先从家庭关系重点、责任压力和相处边界开始分析。';
    case 'home-move':
      return '请先从现在适不适合搬家、换城市、买房置业和居住调整开始分析。';
    case 'settle-relocate':
      return '请先从我现在适不适合长期定居、换城市发展还是留在当前城市开始分析。';
    case 'health':
      return '请先从身心压力、健康隐患和日常养护重点开始分析。';
    case 'study':
      return '请先从学习吸收、考试发挥和提升方向开始分析。';
    case 'study-advance':
      return '请先从我适不适合考证、读研进修或跨领域学习开始分析。';
    case 'exam-landing':
      return '请先从这次考试、面试或申请更适合冲刺、稳住发挥还是调整预期开始分析。';
    case 'social':
      return '请先从人际互动、合作模式和贵人阻力开始分析。';
    case 'emotion':
      return '请先从情绪触发点、内耗模式和修复方式开始分析。';
    case 'growth':
      return '请先从性格矛盾、成长课题和现实突破口开始分析。';
    case 'talent':
      return '请先从核心天赋、优势场景和长期投入方向开始分析。';
    case 'chat':
      return '请先根据盘面回答当前最值得关注的重点。';
    default:
      return '请先做整体解读。';
  }
}

export function getZiweiCompatibilityDefaultQuestion(topic?: string) {
  if (topic === 'recent') return '请先从当前阶段重点、近期互动节奏和风险提醒开始分析。';
  if (topic === 'relationship') return '请先从双方关系匹配度、互动模式和相处建议开始分析。';
  if (topic === 'career-wealth') return '请先从合作默契、优势互补和潜在风险开始分析。';
  return '请先从互动模式、沟通盲点和长期建议开始分析。';
}

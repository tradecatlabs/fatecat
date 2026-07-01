import type { ScopeType } from '../../types/analysis';

export function formatPalaceName(name: string) {
  return name.endsWith('宫') ? name : `${name}宫`;
}

export function normalizePalaceName(name: string) {
  return name.endsWith('宫') ? name.slice(0, -1) : name;
}

export function mapTopicLabel(selectedTopic: string) {
  switch (selectedTopic) {
    case 'destiny':
      return '命局解读';
    case 'relationship':
      return '婚姻感情';
    case 'relationship-push':
      return '关系推进';
    case 'relationship-decision':
      return '关系去留';
    case 'children':
      return '子女亲缘';
    case 'career-wealth':
      return '事业财运';
    case 'job-change':
      return '工作变动';
    case 'startup-partnership':
      return '创业合作';
    case 'investment-partnership':
      return '投资合作';
    case 'recent':
      return '近期趋势';
    case 'family':
      return '六亲家庭';
    case 'home-move':
      return '搬家置业';
    case 'settle-relocate':
      return '定居换城';
    case 'social':
      return '人际合作';
    case 'emotion':
      return '情绪调节';
    case 'health':
      return '健康养护';
    case 'study':
      return '学业成长';
    case 'study-advance':
      return '考证进修';
    case 'exam-landing':
      return '考试上岸';
    case 'reconciliation-decision':
      return '复合判断';
    case 'growth':
      return '成长课题';
    case 'talent':
      return '天赋优势';
    case 'life':
      return '人生解析';
    case 'chat':
      return '自由聊天';
    default:
      return '提示词解读';
  }
}

export function mapReportTypeLabel(reportType: string) {
  switch (reportType) {
    case 'destiny-overview':
      return '命局综述';
    case 'palace':
      return '宫位详解';
    case 'scope':
      return '阶段报告';
    case 'relationship':
      return '婚姻感情专题';
    case 'relationship-push':
      return '关系推进专题';
    case 'relationship-decision':
      return '关系去留专题';
    case 'children':
      return '子女亲缘专题';
    case 'career-wealth':
      return '事业财运专题';
    case 'job-change':
      return '工作变动专题';
    case 'startup-partnership':
      return '创业合作专题';
    case 'investment-partnership':
      return '投资合作专题';
    case 'recent':
      return '近期趋势专题';
    case 'family':
      return '六亲家庭专题';
    case 'home-move':
      return '搬家置业专题';
    case 'settle-relocate':
      return '定居换城专题';
    case 'social':
      return '人际合作专题';
    case 'emotion':
      return '情绪调节专题';
    case 'health':
      return '健康养护专题';
    case 'study':
      return '学业成长专题';
    case 'study-advance':
      return '考证进修专题';
    case 'exam-landing':
      return '考试上岸专题';
    case 'reconciliation-decision':
      return '复合判断专题';
    case 'growth':
      return '成长课题专题';
    case 'talent':
      return '天赋优势专题';
    case 'life':
      return '人生解析专题';
    case 'chat':
      return '自由问答';
    default:
      return 'AI 解读报告';
  }
}

export function mapScopeLabel(scope: ScopeType) {
  switch (scope) {
    case 'origin':
      return '本命';
    case 'decadal':
      return '大限';
    case 'yearly':
      return '流年';
    case 'monthly':
      return '流月';
    case 'daily':
      return '流日';
    case 'hourly':
      return '流时';
    case 'age':
      return '小限';
  }
}

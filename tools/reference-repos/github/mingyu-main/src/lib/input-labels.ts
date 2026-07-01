import type { AnalysisMode } from './query-state';

export type PersonRole = 'self' | 'partner';

export function getPersonSectionTitle(analysisMode: AnalysisMode, role: PersonRole) {
  if (role === 'partner') {
    return '第二人信息';
  }

  return analysisMode === 'compatibility' ? '第一人信息' : '个人信息';
}

export function getPersonReferenceLabel(analysisMode: AnalysisMode, role: PersonRole) {
  if (role === 'partner') {
    return '第二人';
  }

  return analysisMode === 'compatibility' ? '第一人' : '个人';
}

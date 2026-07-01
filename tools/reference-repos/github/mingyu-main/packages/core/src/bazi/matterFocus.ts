
import type { MatterFocusItem, MatterFocusProfile } from '../types/analysis';

export function analyzeMatterFocusProfile(
  gender: string,
  favorableWuxing: string[],
): MatterFocusProfile {
  const items: MatterFocusItem[] = [
    { topic: '事业', relatedPalaces: ['官禄','迁移'], keyStars: [''], priority: 10 },
    { topic: '财运', relatedPalaces: ['财帛','田宅'], keyStars: [''], priority: 9 },
    { topic: '感情', relatedPalaces: ['夫妻','子女'], keyStars: [''], priority: 8 },
    { topic: '健康', relatedPalaces: ['疾厄'], keyStars: [''], priority: 7 },
    { topic: '人际', relatedPalaces: ['兄弟','父母'], keyStars: [''], priority: 6 },
  ];
  return { items };
}

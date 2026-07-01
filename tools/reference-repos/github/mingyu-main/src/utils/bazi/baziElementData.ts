/**
 * 五行与十神基础参考数据
 */

export const TEN_GODS_DEFINITIONS: Record<
  string,
  { wuxing: string; yinyang: string; description: string }
> = {
  比肩: { wuxing: '同我', yinyang: '同性', description: '代表兄弟、朋友、同事，主自尊、独立。' },
  劫财: { wuxing: '同我', yinyang: '异性', description: '代表姐妹、异性朋友，主竞争、合作。' },
  食神: { wuxing: '我生', yinyang: '同性', description: '代表福气、才华、口福，主温和、享受。' },
  伤官: { wuxing: '我生', yinyang: '异性', description: '代表智慧、技艺、叛逆，主聪明、傲气。' },
  偏财: {
    wuxing: '我克',
    yinyang: '同性',
    description: '代表父亲、情人、意外之财，主大方、投机。',
  },
  正财: { wuxing: '我克', yinyang: '异性', description: '代表妻子、稳定收入，主勤劳、踏实。' },
  七杀: { wuxing: '克我', yinyang: '同性', description: '代表小人、压力、权威，主刚强、果断。' },
  正官: { wuxing: '克我', yinyang: '异性', description: '代表上司、事业、名誉，主正直、自律。' },
  偏印: { wuxing: '生我', yinyang: '同性', description: '代表继母、偏门学问，主孤独、敏感。' },
  正印: { wuxing: '生我', yinyang: '异性', description: '代表母亲、正统学问，主仁慈、善良。' },
};

export const SEASON_STATUS: Record<string, Record<string, string>> = {
  寅: { 木: '旺', 火: '相', 土: '死', 金: '囚', 水: '休' },
  卯: { 木: '旺', 火: '相', 土: '死', 金: '囚', 水: '休' },
  辰: { 土: '旺', 金: '相', 水: '死', 木: '囚', 火: '休' },
  巳: { 火: '旺', 土: '相', 金: '死', 水: '囚', 木: '休' },
  午: { 火: '旺', 土: '相', 金: '死', 水: '囚', 木: '休' },
  未: { 土: '旺', 金: '相', 水: '死', 木: '囚', 火: '休' },
  申: { 金: '旺', 水: '相', 木: '死', 火: '囚', 土: '休' },
  酉: { 金: '旺', 水: '相', 木: '死', 火: '囚', 土: '休' },
  戌: { 土: '旺', 金: '相', 水: '死', 木: '囚', 火: '休' },
  亥: { 水: '旺', 木: '相', 火: '死', 土: '囚', 金: '休' },
  子: { 水: '旺', 木: '相', 火: '死', 土: '囚', 金: '休' },
  丑: { 土: '旺', 金: '相', 水: '死', 木: '囚', 火: '休' },
};

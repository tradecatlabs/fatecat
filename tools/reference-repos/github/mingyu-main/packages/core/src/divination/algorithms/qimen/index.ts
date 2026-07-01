/**
 * @file 奇门遁甲排盘算法（主入口）
 * @description 基于转盘法，实现时家奇门完整排盘，含定局、布盘、格局识别、方位建议、应期判断。
 * @流派 转盘奇门（拆补法定局）
 * @古籍依据 《烟波钓叟歌》《遁甲演义》《奇门遁甲秘籍大全》
 *
 * @核心流程
 * 1. 定局数（拆补法）：根据节气和日干支三元确定阴阳遁和局数
 * 2. 寻值符值使：由时辰干支旬首定位值符星和值使门
 * 3. 排九宫格：布地盘三奇六仪 -> 定值符值使落宫 -> 排天盘九星 -> 排人盘八门 -> 排神盘八神
 * 4. 识格局：基础标签（伏吟/反吟/门迫等）+ 经典双元格局（九遁、三奇格局、门迫、击刑、入墓）
 * 5. 辅助分析：方位吉凶、应期估算
 *
 * 《烟波钓叟歌》核心法理（下称《歌》）：
 *   "阴阳二遁分顺逆，一气三元人莫测"        —— 拆补法定局
 *   "直符直使各有时，时干直符时支使"        —— 旬首寻值符值使
 *   "星随符转，门随地转，八神随遁顺逆"      —— 转盘排盘
 *   "星反吟兮门反吟，门迫宫兮事难行"        —— 格局判读
 *   "天遁地遁与人遁，龙遁虎遁与风遁"        —— 九遁格局
 *   "三奇得使最为良，玉女守门喜非常"        —— 吉格判据
 *   "十干入墓主事迟，击刑之处防官非"        —— 凶格判据
 */

import type { QimenData, QimenJiuGongGe } from '../../../types/divination';
import type { ClassicPattern, PatternContext, StemRelation } from './helpers/classic-patterns';
import type { QimenMethod } from './helpers/layout';
import { getDivinationTime } from '../../../calendar/timeManager';
import { getVoidBranches } from '../../../calendar/lunar';
import { diPanPalaces } from './helpers/_constants';
import { getQimenJuShu, getZhiFuZhiShi, getDunJiaStem } from './helpers/jushu';
import { arrangeJiuGongGe } from './helpers/layout';
import { getQimenPatternTags, buildPatternDetails, buildPalaceInsights } from './helpers/patterns';
import { getStemRelations, getClassicPatterns } from './helpers/classic-patterns';
import { buildDirectionAdvice } from './helpers/directions';
import { estimateYingQi } from './helpers/ying-qi';

// ============================================================================
// 内部工具函数
// ============================================================================

/**
 * 获取宫位中文名
 * @param jiuGongGe 九宫格数据
 * @param palace    宫位编号（1-9）
 * @returns 宫位中文名（如"坎一宫"）
 */
function getPalaceName(jiuGongGe: QimenJiuGongGe[], palace: number): string {
  return jiuGongGe.find((item) => item.gong === palace)?.name || `${palace}宫`;
}

/**
 * 根据地支解析所属宫位
 *
 * @param branch     地支（如"子""午"）
 * @param jiuGongGe  九宫格数据
 * @returns 宫位对象（含地支、宫号、宫名），找不到时返回 null
 */
function resolveQimenBranchPalace(
  branch: string,
  jiuGongGe: QimenJiuGongGe[],
): { branch: string; palace: number; name: string } | null {
  const palace = diPanPalaces[branch];
  if (!palace) return null;
  return { branch, palace, name: getPalaceName(jiuGongGe, palace) };
}

/**
 * 获取驿马地支
 *
 * 《烟波钓叟歌》：「天马方为动应之神，驿马冲则事速」
 * 寅午戌马在申，申子辰马在寅，
 * 巳酉丑马在亥，亥卯未马在巳。
 *
 * @param sourceBranch 时支
 * @returns 驿马地支，无匹配时返回空字符串
 */
function getHorseBranch(sourceBranch: string): string {
  if (['申', '子', '辰'].includes(sourceBranch)) return '寅';
  if (['寅', '午', '戌'].includes(sourceBranch)) return '申';
  if (['亥', '卯', '未'].includes(sourceBranch)) return '巳';
  if (['巳', '酉', '丑'].includes(sourceBranch)) return '亥';
  return '';
}

/**
 * 将 ClassicPattern（classic-patterns 模块原始输出）映射为 QimenData 兼容的格式
 *
 * classic-patterns 使用 tone/palace 字段，
 * 而 QimenData.classicPatterns 使用 type/palaces 字段。
 *
 * @param patterns 原始 ClassicPattern 列表
 * @returns 映射后的 QimenData.classicPatterns 列表
 */
function mapClassicPatterns(
  patterns: ClassicPattern[],
): Exclude<QimenData['classicPatterns'], undefined> {
  return patterns.map((p) => ({
    name: p.name,
    type: p.tone,
    score: p.score,
    summary: p.summary,
    palaces: p.palace ? [p.palace] : [],
  }));
}

/**
 * 将 StemRelation（classic-patterns 模块原始输出）映射为 QimenData 兼容的格式
 *
 * stem-pair-patterns 使用 heaven/earth/palace/type/note 字段，
 * 而 QimenData.stemRelations 使用 gong/heavenStem/earthStem/relation/pattern 字段。
 *
 * @param relations 原始 StemRelation 列表
 * @returns 映射后的 QimenData.stemRelations 列表
 */
function mapStemRelations(
  relations: StemRelation[],
): Exclude<QimenData['stemRelations'], undefined> {
  return relations.map((r) => ({
    gong: r.palace,
    heavenStem: r.heaven,
    earthStem: r.earth,
    relation: r.type,
    pattern: r.note,
  }));
}

// ============================================================================
// 主入口函数
// ============================================================================

/**
 * 生成奇门遁甲完整排盘
 *
 * 遵循拆补法定局、转盘法排盘，完整输出九宫四盘（天地人神）、
 * 格局标签、经典格局（九遁、三奇、门迫、击刑、入墓等）、
 * 宫位洞察、方位吉凶指引和应期估算。
 *
 * ── 排盘流程 ──
 *
 * 1. **时间信息**：《歌》"先须掌上排九宫，纵横十五在其中"
 *    - 获取公历、农历、节气、干支等完整时间数据
 *
 * 2. **定局数（拆补法）**：《歌》"阴阳二遁分顺逆，一气三元人莫测"
 *    - 根据当前节气与日干支三元确定阴阳遁和局数
 *
 * 3. **寻值符值使（旬首法）**：《歌》"直符直使各有时，时干直符时支使"
 *    - 由时辰干支的旬首定位值符星和值使门
 *
 * 4. **排九宫格（转盘法）**：《歌》"星随符转，门随地转，八神随遁顺逆"
 *    - 布地盘三奇六仪 -> 定值符值使落宫 -> 排天盘九星 -> 排人盘八门 -> 排神盘八神
 *
 * 5. **辅助数据**：空亡地支配对、驿马定位
 *
 * 6. **基础格局标签**：《歌》"星反吟兮门反吟，门迫宫兮事难行"
 *    - 伏吟/反吟、门迫、击刑、入墓、三奇得、符使同宫、三奇得使、马星
 *
 * 7. **经典格局（advanced）**：《歌》"天遁地遁与人遁，龙遁虎遁与风遁"
 *    - 九大遁格、三奇得使/升殿/入墓/会甲、符使同宫、天乙飞干/伏干、
 *      玉女守门、门宫生克、击刑、入墓等
 *
 * 8. **天地盘干关系**：每个宫位天盘干与地盘干的五行生克/奇仪相合/入墓/击刑
 *
 * 9. **宫位洞察**：综合门、神、星、格局标签判定各宫有利/风险/关注等级
 *
 * 10. **方位建议**：《歌》"八门若遇开休生，诸事逢之总称情"
 *     - 按门、神、星、三奇综合评分，推荐 Top 3 吉方与 1 个避方
 *
 * 11. **应期估算**：《奇门遁甲大全》庚格应期法
 *     - 用神落宫基线 + 值符值使调整 + 庚格定应期 + 伏吟/反吟/马星/空亡微调
 *
 * @param customDate 自定义时间（可选，默认当前时间）
 * @param method     排盘方法，默认 'zhuanpan'（转盘法）
 * @returns 完整的奇门遁甲数据 QimenData
 *
 * @example
 * ```ts
 * const result = generateQimen();
 * // 返回值示例：
 * // {
 * //   timeInfo: { solarTerm: '冬至', epoch: '上元' },
 * //   ganzhi: { year: '甲辰', month: '丙子', day: '戊辰', hour: '壬子' },
 * //   isYangDun: true,
 * //   juShu: 1,
 * //   zhiFu: '天蓬',
 * //   zhiShi: '休门',
 * //   patternTags: ['星伏吟', '三奇得（乙奇到震三宫）'],
 * //   patternDetails: [{ tag: '星伏吟', summary: '九星回原位...' }],
 * //   classicPatterns: [{ name: '天遁', type: 'good', score: 9, ... }],
 * //   stemRelations: [{ gong: 1, heavenStem: '戊', earthStem: '癸', relation: '比和', ... }],
 * //   palaceInsights: [{ gong: 1, name: '坎一宫', level: '关注', ... }],
 * //   directions: { goodDirections: [...], avoidDirections: [...] },
 * //   yingQi: { minDays: 7, maxDays: 15, rhythm: '快', ... },
 * //   timestamp: 1703980800000,
 * // }
 * ```
 */
export function generateQimen(customDate?: Date, method: QimenMethod = 'zhuanpan'): QimenData {
  // ──────────────────────────────────────────────────────────────────────────
  // 步骤 1：获取统一占卜时间信息
  // ──────────────────────────────────────────────────────────────────────────
  // 《烟波钓叟歌》："先须掌上排九宫，纵横十五在其中。
  //   次将八卦论八节，一气统三为正宗。"
  const { timeInfo, ganzhi, timestamp } = getDivinationTime(customDate);
  const { jieQi } = timeInfo;

  // ──────────────────────────────────────────────────────────────────────────
  // 步骤 2：定局数（拆补法）
  // ──────────────────────────────────────────────────────────────────────────
  // 《烟波钓叟歌》：
  //   "阴阳二遁分顺逆，一气三元人莫测。
  //    五日都来换一元，接气超神为准则。"
  //
  // 拆补法以节气为界，不置闰：
  //   - 阳遁：冬至 -> 芒种（顺布六仪，逆布三奇）
  //   - 阴遁：夏至 -> 大雪（逆布六仪，顺布三奇）
  const jushuResult = getQimenJuShu({
    jieQi,
    ganzhi: { day: ganzhi.day },
    solar: {
      year: timeInfo.solar.year,
      month: timeInfo.solar.month,
      day: timeInfo.solar.day,
    },
  });

  // ──────────────────────────────────────────────────────────────────────────
  // 步骤 3：寻值符与值使（旬首法）
  // ──────────────────────────────────────────────────────────────────────────
  // 《烟波钓叟歌》："直符直使各有时，时干直符时支使。"
  //
  // 值符（九星之主）与值使（八门之主）由时辰干支的旬首决定：
  //   旬首地支 -> 地盘宫位 -> 该宫星为值符、门为值使
  const { zhiFu, zhiShi, specialConditions } = getZhiFuZhiShi(ganzhi.hour);

  // ──────────────────────────────────────────────────────────────────────────
  // 步骤 4：排九宫格（转盘法）
  // ──────────────────────────────────────────────────────────────────────────
  // 《烟波钓叟歌》：
  //   "星随符转，门随地转，八神随遁顺逆"
  //
  // 转盘法五大步骤：
  //   1) 布地盘三奇六仪（阳顺阴逆）
  //   2) 定值符落宫（时干遁干所在宫）与值使落宫（时支所在宫）
  //   3) 排天盘九星（值符为把手，九星整体旋转）
  //   4) 排人盘八门（值使为把手，沿洛书轨迹排列）
  //   5) 排神盘八神（值符神随天盘值符星，阳顺阴逆排列）
  const jiuGongGe = arrangeJiuGongGe(
    jushuResult.isYangDun,
    jushuResult.juShu,
    zhiFu,
    zhiShi,
    { hour: ganzhi.hour },
    method,
  );

  // ──────────────────────────────────────────────────────────────────────────
  // 步骤 5：辅助数据（空亡、驿马）
  // ──────────────────────────────────────────────────────────────────────────
  const hourZhi = ganzhi.hour.charAt(1);
  const hourGanForFind = getDunJiaStem(ganzhi.hour);

  // 空亡：时辰干支所在旬对应的空亡地支
  // 用于判断宫位能量虚浮、不宜行动
  const voidBranches = getVoidBranches(ganzhi.hour) || [];
  const voidPalaces = voidBranches
    .map((branch: string) => resolveQimenBranchPalace(branch, jiuGongGe))
    .filter((item): item is { branch: string; palace: number; name: string } => Boolean(item));

  // 驿马（天马）：时支对应的驿马地支
  // 《烟波钓叟歌》："天马方为动应之神，驿马冲则事速"
  const horseBranch = getHorseBranch(hourZhi);
  const horsePalace = horseBranch ? resolveQimenBranchPalace(horseBranch, jiuGongGe) : null;

  // 值符落宫与值使落宫（用于后续格局判断和应期估算）
  const zhiFuLandingPalace = jiuGongGe.find((gong) => gong.tianPan.star === zhiFu)?.gong;
  if (zhiFuLandingPalace === undefined) {
    throw new Error(`找不到值符星 "${zhiFu}" 落宫。`);
  }
  const zhiShiLandingPalace = diPanPalaces[hourZhi];
  if (zhiShiLandingPalace === undefined) {
    throw new Error(`找不到时支 "${hourZhi}" 对应的地盘宫位。`);
  }

  // ──────────────────────────────────────────────────────────────────────────
  // 步骤 6：基础格局标签
  // ──────────────────────────────────────────────────────────────────────────
  // 《烟波钓叟歌》：
  //   "星反吟兮门反吟，门迫宫兮事难行"
  //   "击刑之处防官非，十干入墓主事迟"
  //   "三奇得使最为良，符使同宫事必成"
  //
  // 检测以下标签：
  //   星伏吟/星反吟、门伏吟/门反吟、门迫、
  //   击刑、入墓、三奇得、符使同宫、三奇得使、马星
  const patternTags = getQimenPatternTags({
    zhiFu,
    zhiShi,
    zhiFuLandingPalace,
    zhiShiLandingPalace,
    jiuGongGe,
    hourGanForFind,
    horsePalace: horsePalace?.palace,
    horsePalaceName: horsePalace?.name,
  });

  // ──────────────────────────────────────────────────────────────────────────
  // 步骤 7：标签详情（面向用户的简要解读）
  // ──────────────────────────────────────────────────────────────────────────
  const patternDetails = buildPatternDetails(patternTags);

  // ──────────────────────────────────────────────────────────────────────────
  // 步骤 8：经典格局（advanced patterns）
  // ──────────────────────────────────────────────────────────────────────────
  // 《烟波钓叟歌》：
  //   "天遁地遁与人遁，龙遁虎遁与风遁，云遁鬼遁与神遁"   —— 九遁
  //   "三奇得使最为良，玉女守门喜非常"                     —— 三奇/玉女
  //   "十干入墓主事迟，击刑之处防官非"                    —— 入墓/击刑
  //   "门迫宫兮事难行"                                     —— 门迫
  //
  // 综合识别：九遁、三奇得使/升殿/入墓/会甲、符使同宫、
  // 天乙飞干格/伏干格、天辅时、玉女守门、门迫、门宫相生、击刑、入墓
  const dayStem = ganzhi.day.charAt(0);
  const classicPatternContext: PatternContext = {
    jiuGongGe,
    zhiFu,
    zhiShi,
    dayStem,
  };
  const classicPatternsRaw = getClassicPatterns(classicPatternContext);
  const classicPatterns = mapClassicPatterns(classicPatternsRaw);

  // ──────────────────────────────────────────────────────────────────────────
  // 步骤 9：天地盘干关系（每宫天盘干 vs 地盘干）
  // ──────────────────────────────────────────────────────────────────────────
  // 每个宫位输出天盘干与地盘干的主要关系：
  //   五行生克（克上/克下/生上/生下/比和）
  //   奇仪相合、入墓、击刑
  // 最多每宫输出一条主关系 + 边缘关系
  const stemRelationsRaw = getStemRelations(jiuGongGe);
  const stemRelations = mapStemRelations(stemRelationsRaw);

  // ──────────────────────────────────────────────────────────────────────────
  // 步骤 10：宫位洞察
  // ──────────────────────────────────────────────────────────────────────────
  // 综合门、神、星和模式标签，逐宫判定：
  //   有利（绿色）：吉门/吉神，适合行动
  //   关注（黄色）：值符所在，全局核心观察位
  //   风险（红色）：凶门/凶神/门迫/击刑/入墓，宜谨慎
  const palaceInsights = buildPalaceInsights({
    jiuGongGe,
    zhiFu,
    zhiShi,
    patternTags,
  });

  // ──────────────────────────────────────────────────────────────────────────
  // 步骤 11：方位建议
  // ──────────────────────────────────────────────────────────────────────────
  // 《烟波钓叟歌》："八门若遇开休生，诸事逢之总称情"
  //
  // 综合评分（门/神/星/三奇/空亡/经典格局）：
  //   吉方：Top 3 高分区位，含推荐用途
  //   避方：1 个最低分区位，含风险原因
  const directions = buildDirectionAdvice(jiuGongGe, voidBranches, classicPatternsRaw);

  // ──────────────────────────────────────────────────────────────────────────
  // 步骤 12：应期估算
  // ──────────────────────────────────────────────────────────────────────────
  // 《奇门遁甲大全》应期章：
  //   1. 用神落宫基线（内宫 1-3 速应，中宫 4-6 渐进，外宫 7-9 迟应）
  //   2. 值符值使落宫调整
  //   3. 庚格定应期（阳日看庚下、阴日看庚上，地支逢冲为应）
  //   4. 伏吟延迟 / 反吟加快 / 马星加快 / 空亡填实
  //   5. 经典格局影响（吉格加快 / 凶格延迟）
  const isFuyin = patternTags.some((t) => t.includes('伏吟'));
  const isFanyin = patternTags.some((t) => t.includes('反吟'));
  const hasVoid = voidBranches.length > 0;
  const hasHorse = !!horsePalace;
  const yingQi = estimateYingQi(jiuGongGe, zhiFuLandingPalace, {
    isFuyin,
    isFanyin,
    hasHorse,
    hasVoid,
    zhiFuLandingPalace,
    zhiShiLandingPalace,
    hourGanZhi: ganzhi.hour,
    classicPatterns: classicPatternsRaw,
    voidBranches,
  });

  // ──────────────────────────────────────────────────────────────────────────
  // 步骤 13：返回完整 QimenData
  // ──────────────────────────────────────────────────────────────────────────
  return {
    timeInfo: {
      solarTerm: jushuResult.jieQi || jieQi,
      epoch: jushuResult.yuan,
    },
    ganzhi,
    isYangDun: jushuResult.isYangDun,
    juShu: jushuResult.juShu,
    zhiFu,
    zhiShi,
    patternTags,
    patternDetails,
    palaceInsights,
    voidBranches,
    voidPalaces,
    horseStar: horsePalace ? { ...horsePalace, sourceBranch: hourZhi } : undefined,
    specialConditions,
    jiuGongGe,
    classicPatterns,
    stemRelations,
    directions,
    yingQi,
    timestamp,
  };
}

// ============================================================================
// 导出内部工具（供外部模块或测试使用）
// ============================================================================

export { getHorseBranch, resolveQimenBranchPalace };

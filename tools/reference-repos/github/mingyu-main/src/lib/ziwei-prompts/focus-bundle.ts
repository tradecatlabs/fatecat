import type { AnalysisPayloadV1 } from '../../types/analysis';
import { formatPalaceName } from './labels';
import {
  buildScopeFocusPalaces,
  dedupePalaces,
  getBodyPalace,
  getOppositePalace,
  getPalaceByIndex,
  getPalaceByName,
  getSurroundedPalaces,
} from './palace-helpers';
import type { PromptContext } from './types';

export function buildFocusTaskBundle(payload: AnalysisPayloadV1, reportContext: PromptContext) {
  const activePalace = getPalaceByIndex(payload, payload.active_scope.palace_index);
  const bodyPalace = getBodyPalace(payload);
  const mingPalace = getPalaceByName(payload, '命宫');
  const spousePalace = getPalaceByName(payload, '夫妻');
  const childrenPalace = getPalaceByName(payload, '子女');
  const wealthPalace = getPalaceByName(payload, '财帛');
  const travelPalace = getPalaceByName(payload, '迁移');
  const careerPalace = getPalaceByName(payload, '官禄');
  const housePalace = getPalaceByName(payload, '田宅');
  const fortunePalace = getPalaceByName(payload, '福德');
  const parentPalace = getPalaceByName(payload, '父母');
  const siblingPalace = getPalaceByName(payload, '兄弟');
  const healthPalace = getPalaceByName(payload, '疾厄');

  switch (`${reportContext.selected_topic}:${reportContext.report_type}`) {
    case 'destiny:destiny-overview':
      return {
        focusSummary: '概括命盘底色、核心驱动力、主要优势与人生主线。',
        focusPalaces: dedupePalaces([
          mingPalace,
          bodyPalace,
          fortunePalace,
          careerPalace,
          wealthPalace,
          travelPalace,
        ]),
        outputFocus: [
          '先判断整张命盘的底色与主导力量。',
          '再提炼最值得优先关注的 1 到 3 条人生主轴。',
          '每个结论都要能对应到具体宫位、主星、四化或运限触发。',
        ],
        avoid: ['保持命局综述视角，围绕主线组织内容。'],
      };
    case 'destiny:palace': {
      const selectedPalace = reportContext.palace_name
        ? getPalaceByName(payload, reportContext.palace_name)
        : null;
      return {
        focusSummary: `只解读${formatPalaceName(
          selectedPalace?.name ?? reportContext.palace_name ?? '当前宫位',
        )}本身，以及它的对宫与三方四正如何共同作用。`,
        focusPalaces: dedupePalaces([
          selectedPalace,
          getOppositePalace(payload, selectedPalace),
          ...getSurroundedPalaces(payload, selectedPalace),
        ]),
        outputFocus: [
          '先说明当前宫位的核心主题、主导星曜和关键标签。',
          '再结合对宫、三方四正说明支持、放大或牵制关系。',
          '建议只能围绕这一组宫位结构，不要跳去别的专题。',
        ],
        avoid: ['围绕当前宫位及其关联结构给出结论与建议。'],
      };
    }
    case 'destiny:scope':
      return {
        focusSummary: `聚焦${payload.active_scope.label}对本命主线的实际触发，判断这一阶段的重点变化与优先级。`,
        focusPalaces: dedupePalaces([
          activePalace,
          ...buildScopeFocusPalaces(payload),
          mingPalace,
          fortunePalace,
          careerPalace,
          travelPalace,
        ]).slice(0, 6),
        outputFocus: [
          '先判断这一阶段最强的触发点。',
          '说明它如何影响本命主线和原有格局。',
          '把结论落到阶段机会、阻力与行动优先级。',
        ],
        avoid: ['聚焦当前阶段触发，围绕阶段变化与优先级作答。'],
      };
    case 'relationship:relationship':
      return {
        focusSummary: '只解读婚姻感情、亲密关系、相处模式与当前阶段触发。',
        focusPalaces: dedupePalaces([
          spousePalace,
          mingPalace,
          fortunePalace,
          childrenPalace,
          travelPalace,
          activePalace,
        ]),
        outputFocus: [
          '优先判断关系模式、推进阻力与情绪互动。',
          '说明哪些结论来自夫妻宫、命宫、福德宫、子女宫或当前运限触发。',
          '建议要贴合当前阶段，不要空泛劝说。',
        ],
        avoid: ['围绕关系议题作答，并保持证据对应。'],
      };
    case 'relationship-push:relationship-push':
      return {
        focusSummary:
          '只解读这段关系当前更适合推进、放慢、稳定经营还是重新评估，以及相关证据与节奏建议。',
        focusPalaces: dedupePalaces([
          spousePalace,
          mingPalace,
          fortunePalace,
          childrenPalace,
          travelPalace,
          activePalace,
        ]),
        outputFocus: [
          '优先判断当前关系节奏、投入价值与推进阻力。',
          '说明哪些结论来自夫妻宫、命宫、福德宫、子女宫、迁移宫或当前运限触发。',
          '建议要落到推进、观察、边界或止损的判断标准，不要空泛劝说。',
        ],
        avoid: ['围绕关系推进决策作答，区分关系底色与当前阶段触发。'],
      };
    case 'relationship-decision:relationship-decision':
      return {
        focusSummary:
          '只解读这段关系当前更适合继续投入、放慢观察、重建边界还是及时止损，以及相关证据与判断标准。',
        focusPalaces: dedupePalaces([
          spousePalace,
          mingPalace,
          fortunePalace,
          childrenPalace,
          travelPalace,
          activePalace,
        ]),
        outputFocus: [
          '优先判断关系是否值得继续投入，以及当前最大的消耗点和止损信号。',
          '说明哪些结论来自夫妻宫、命宫、福德宫、子女宫、迁移宫或当前运限触发。',
          '建议要落到继续条件、观察重点、边界管理和止损判断标准，不要空泛劝说。',
        ],
        avoid: ['围绕关系去留决策作答，区分关系底色与当前阶段触发。'],
      };
    case 'children:children':
      return {
        focusSummary:
          '只解读子女缘分、亲子互动、养育压力、教育陪伴重点，以及数量和性别判断的证据边界。',
        focusPalaces: dedupePalaces([
          childrenPalace,
          spousePalace,
          mingPalace,
          fortunePalace,
          housePalace,
          healthPalace,
          activePalace,
        ]),
        outputFocus: [
          '优先判断子女缘分、亲子互动和养育压力。',
          '说明哪些结论来自子女宫、夫妻宫、命宫、福德宫、田宅宫或当前运限触发。',
          '涉及子女数量、性别或生育细节时只能给倾向、条件和待确认点，不要绝对化。',
        ],
        avoid: ['围绕子女亲缘议题作答，区分可确认主线与证据不足处。'],
      };
    case 'career-wealth:career-wealth':
      return {
        focusSummary: '只解读事业路径、财运抓手、资源配置与执行节奏。',
        focusPalaces: dedupePalaces([
          careerPalace,
          wealthPalace,
          mingPalace,
          fortunePalace,
          housePalace,
          travelPalace,
          activePalace,
        ]),
        outputFocus: [
          '区分事业发展、赚钱方式和资源落点。',
          '说明当前运限在哪些宫位形成机会或阻力。',
          '建议要体现先后顺序和风险控制。',
        ],
        avoid: ['围绕事业与财务议题作答，财务判断用趋势与条件表述。'],
      };
    case 'job-change:job-change':
      return {
        focusSummary:
          '只解读当前是否适合换工作、转方向、试探机会或继续积累，以及相关资源、风险与节奏判断。',
        focusPalaces: dedupePalaces([
          careerPalace,
          wealthPalace,
          travelPalace,
          mingPalace,
          fortunePalace,
          housePalace,
          activePalace,
        ]),
        outputFocus: [
          '先判断当前更适合留任、试探、跳槽、转方向还是暂缓。',
          '说明哪些结论来自官禄宫、财帛宫、迁移宫、命宫、福德宫、田宅宫或当前运限触发。',
          '建议要落到平台、收入、成长、代价和行动先后顺序。',
        ],
        avoid: ['围绕工作变动作答，区分长期职业底色与当前阶段窗口。'],
      };
    case 'startup-partnership:startup-partnership':
      return {
        focusSummary:
          '只解读当前是否适合创业、单干、找人合作、先试水还是继续积累，以及相关资源、风险与行动顺序。',
        focusPalaces: dedupePalaces([
          careerPalace,
          wealthPalace,
          siblingPalace,
          travelPalace,
          mingPalace,
          fortunePalace,
          activePalace,
        ]),
        outputFocus: [
          '先判断当前更适合单干、合作、试水、继续积累还是暂缓。',
          '说明哪些结论来自官禄宫、财帛宫、兄弟宫、迁移宫、命宫、福德宫或当前运限触发。',
          '建议要落到方向选择、资源来源、合作分工、现金流压力和行动先后顺序。',
        ],
        avoid: ['围绕创业合作决策作答，区分长期职业底色与当前阶段窗口。'],
      };
    case 'investment-partnership:investment-partnership':
      return {
        focusSummary:
          '只解读当前是否适合投资、独立布局、合作求财、继续观望或先守现金流，以及相关收益模式、风险与行动顺序。',
        focusPalaces: dedupePalaces([
          wealthPalace,
          careerPalace,
          fortunePalace,
          siblingPalace,
          travelPalace,
          mingPalace,
          activePalace,
        ]),
        outputFocus: [
          '先判断当前更适合独立投资、合作求财、继续观望还是先守财。',
          '说明哪些结论来自财帛宫、官禄宫、福德宫、兄弟宫、迁移宫、命宫或当前运限触发。',
          '建议要落到收益模式、资金压力、合作分工、风险边界和行动顺序。',
        ],
        avoid: ['围绕投资合作决策作答，财务判断用趋势、条件与边界表述。'],
      };
    case 'recent:recent':
      return {
        focusSummary: '只解读当前阶段主线、近期推进节奏、风险提醒与下一步动作优先级。',
        focusPalaces: dedupePalaces([
          activePalace,
          mingPalace,
          bodyPalace,
          careerPalace,
          wealthPalace,
          travelPalace,
          fortunePalace,
        ]),
        outputFocus: [
          '先判断当前阶段最强触发点与近期主线。',
          '区分适合主动推进的事项、应该暂缓的风险和节奏变化点。',
          '建议要落到接下来一段时间的行动顺序与取舍。',
        ],
        avoid: ['围绕近期趋势作答，区分原局底色与当前运限触发，不要扩写长期总论。'],
      };
    case 'family:family':
      return {
        focusSummary: '只解读父母、兄弟姐妹、伴侣、子女与原生家庭相关的现实关系结构。',
        focusPalaces: dedupePalaces([
          parentPalace,
          siblingPalace,
          spousePalace,
          childrenPalace,
          housePalace,
          fortunePalace,
          mingPalace,
          activePalace,
        ]),
        outputFocus: [
          '区分父母、兄弟姐妹、伴侣、子女各自的关系模式与责任压力。',
          '说明哪些支持、牵制或边界议题来自父母宫、兄弟宫、田宅宫、福德宫与当前运限触发。',
          '建议要落到边界、沟通、分工或照护安排，不要空断家庭事件。',
        ],
        avoid: ['围绕家庭与六亲议题作答，用现实关系结构和阶段压力组织结论。'],
      };
    case 'home-move:home-move':
      return {
        focusSummary:
          '只解读当前是否适合搬家、换城市、买房置业或调整居住安排，以及相关稳定性、成本与风险判断。',
        focusPalaces: dedupePalaces([
          housePalace,
          travelPalace,
          wealthPalace,
          parentPalace,
          fortunePalace,
          mingPalace,
          activePalace,
        ]),
        outputFocus: [
          '先判断当前更适合搬家、换城市、买房置业、租住调整还是继续观望。',
          '说明哪些结论来自田宅宫、迁移宫、财帛宫、父母宫、福德宫、命宫或当前运限触发。',
          '建议要落到稳定性、资金压力、家庭牵动、判断条件和行动顺序。',
        ],
        avoid: ['围绕搬家置业决策作答，区分长期居住底色与当前阶段窗口。'],
      };
    case 'settle-relocate:settle-relocate':
      return {
        focusSummary:
          '只解读当前是否适合长期定居、换城市发展、两地过渡或暂缓决定，以及相关稳定性、机会、成本与行动顺序。',
        focusPalaces: dedupePalaces([
          housePalace,
          travelPalace,
          careerPalace,
          wealthPalace,
          fortunePalace,
          parentPalace,
          mingPalace,
          activePalace,
        ]),
        outputFocus: [
          '先判断当前更适合留在当前城市、换城发展、两地过渡还是暂缓决定。',
          '说明哪些结论来自田宅宫、迁移宫、官禄宫、财帛宫、福德宫、父母宫、命宫或当前运限触发。',
          '建议要落到稳定性、事业机会、家庭牵动、成本压力、判断条件和行动顺序。',
        ],
        avoid: ['围绕定居换城决策作答，区分长期居住底色与当前阶段窗口。'],
      };
    case 'social:social':
      return {
        focusSummary: '只解读社交风格、合作关系、贵人阻力与现实人际策略。',
        focusPalaces: dedupePalaces([
          siblingPalace,
          travelPalace,
          fortunePalace,
          mingPalace,
          careerPalace,
          wealthPalace,
          activePalace,
        ]),
        outputFocus: [
          '先区分合作优势、贵人来源、沟通短板和关系消耗。',
          '说明哪些结论来自兄弟宫、迁移宫、福德宫、命宫、官禄宫或当前运限触发。',
          '建议要落到合作分工、圈层筛选、表达方式与边界管理。',
        ],
        avoid: ['围绕人际合作议题作答，不扩写无关的婚恋或家庭专题。'],
      };
    case 'emotion:emotion':
      return {
        focusSummary: '只解读情绪触发点、内耗模式、安全感来源与现实修复路径。',
        focusPalaces: dedupePalaces([
          fortunePalace,
          healthPalace,
          mingPalace,
          bodyPalace,
          housePalace,
          parentPalace,
          activePalace,
        ]),
        outputFocus: [
          '先区分情绪触发点、安全感来源、压力累积和恢复方式。',
          '说明哪些结论来自福德宫、疾厄宫、命宫、身宫、田宅宫或当前运限触发。',
          '建议只给节奏、边界、作息和修复方式，不做绝对化结论。',
        ],
        avoid: ['围绕情绪调节议题作答，用趋势提醒和可执行建议组织内容。'],
      };
    case 'health:health':
      return {
        focusSummary: '只解读健康隐患、身心压力、生活习惯影响与当前阶段的养护重点。',
        focusPalaces: dedupePalaces([
          healthPalace,
          fortunePalace,
          mingPalace,
          bodyPalace,
          travelPalace,
          parentPalace,
          activePalace,
        ]),
        outputFocus: [
          '先区分身体消耗、情绪压力、作息失衡和阶段性风险方向。',
          '说明哪些结论来自疾厄宫、福德宫、命宫、身宫或当前运限触发。',
          '建议只给养护、排查和生活管理方向，不做医学诊断或绝对判断。',
        ],
        avoid: ['围绕健康养护议题作答，只给趋势提醒和可执行建议，不替代医学判断。'],
      };
    case 'study:study':
      return {
        focusSummary: '只解读学习能力、专注表现、考试进修节奏与提升路径。',
        focusPalaces: dedupePalaces([
          mingPalace,
          bodyPalace,
          fortunePalace,
          careerPalace,
          parentPalace,
          travelPalace,
          activePalace,
        ]),
        outputFocus: [
          '先判断理解力、专注力、持续性和考试发挥的主要特点。',
          '说明哪些结论来自命宫、福德宫、官禄宫、父母宫或当前运限触发。',
          '建议要落到学习方式、节奏管理、选科进修或阶段突破口。',
        ],
        avoid: ['围绕学业成长议题作答，区分天赋倾向、现实环境和当前阶段节奏。'],
      };
    case 'study-advance:study-advance':
      return {
        focusSummary:
          '只解读当前是否适合考证、读研进修、跨领域学习或暂缓投入，以及相关节奏、代价与提升路径。',
        focusPalaces: dedupePalaces([
          mingPalace,
          bodyPalace,
          fortunePalace,
          careerPalace,
          parentPalace,
          travelPalace,
          activePalace,
        ]),
        outputFocus: [
          '先判断当前更适合考证、读研进修、跨领域学习还是暂缓投入。',
          '说明哪些结论来自命宫、福德宫、官禄宫、父母宫、迁移宫或当前运限触发。',
          '建议要落到投入产出、执行节奏、现实压力和下一步优先级。',
        ],
        avoid: ['围绕考证进修决策作答，区分长期学习底色与当前阶段窗口。'],
      };
    case 'exam-landing:exam-landing':
      return {
        focusSummary:
          '只解读这次考试、面试或申请更适合冲刺、稳住发挥、优化目标还是调整预期，以及相关机会、风险与准备节奏。',
        focusPalaces: dedupePalaces([
          mingPalace,
          fortunePalace,
          careerPalace,
          parentPalace,
          travelPalace,
          healthPalace,
          activePalace,
        ]),
        outputFocus: [
          '先判断当前更适合全力冲刺、稳住发挥、优化目标还是调整预期。',
          '说明哪些结论来自命宫、福德宫、官禄宫、父母宫、迁移宫、疾厄宫或当前运限触发。',
          '建议要落到上岸机会、失误风险、准备节奏、目标匹配度和下一步优先级。',
        ],
        avoid: ['围绕考试上岸决策作答，区分长期学习底色与当前阶段窗口。'],
      };
    case 'reconciliation-decision:reconciliation-decision':
      return {
        focusSummary:
          '只解读这段旧关系当前是否还有复合空间，更适合争取、观察、先立边界还是及时放下，以及相关证据与判断标准。',
        focusPalaces: dedupePalaces([
          spousePalace,
          mingPalace,
          fortunePalace,
          travelPalace,
          childrenPalace,
          activePalace,
        ]),
        outputFocus: [
          '优先判断旧关系是否还有复合空间，以及当前最大的现实阻力和风险信号。',
          '说明哪些结论来自夫妻宫、命宫、福德宫、迁移宫、子女宫或当前运限触发。',
          '建议要落到复合条件、观察重点、边界管理和放下判断标准，不要空泛劝说。',
        ],
        avoid: ['围绕复合判断作答，区分旧缘底色与当前阶段触发。'],
      };
    case 'growth:growth':
      return {
        focusSummary: '只解读性格矛盾、长期成长课题、反复受阻模式与现实突破口。',
        focusPalaces: dedupePalaces([
          mingPalace,
          bodyPalace,
          fortunePalace,
          careerPalace,
          housePalace,
          travelPalace,
          activePalace,
        ]),
        outputFocus: [
          '先概括最需要整合的性格矛盾与长期课题。',
          '说明哪些结论来自命宫、身宫、福德宫、官禄宫、田宅宫或当前运限触发。',
          '建议要落到习惯、节奏、边界和行动优先级，不讲空泛成长口号。',
        ],
        avoid: ['围绕成长课题作答，区分原局底色与当前阶段触发。'],
      };
    case 'talent:talent':
      return {
        focusSummary: '只解读核心天赋、能力优势、适配场景与长期放大路径。',
        focusPalaces: dedupePalaces([
          mingPalace,
          bodyPalace,
          careerPalace,
          wealthPalace,
          fortunePalace,
          travelPalace,
          activePalace,
        ]),
        outputFocus: [
          '先区分学习吸收、表达输出、组织执行、资源整合等不同优势。',
          '说明哪些结论来自命宫、身宫、官禄宫、财帛宫、福德宫或当前运限触发。',
          '建议要落到适合深耕的方向、表现方式和长期投入顺序。',
        ],
        avoid: ['围绕天赋优势作答，不把职业、情绪或关系议题平均铺开。'],
      };
    case 'life:life':
      return {
        focusSummary: '聚焦人生主线、阶段重点、长期方向与短期动作的衔接。',
        focusPalaces: dedupePalaces([
          mingPalace,
          bodyPalace,
          fortunePalace,
          careerPalace,
          wealthPalace,
          travelPalace,
          activePalace,
        ]),
        outputFocus: [
          '先概括主线，再区分长期与短期重点。',
          '如果当前有运限触发，要说明它如何改变节奏。',
          '建议必须能够落到当前阶段的行动次序。',
        ],
        avoid: ['围绕人生主线作答，并体现当前运限对节奏的影响。'],
      };
    case 'chat:chat':
      return {
        focusSummary: '围绕【问题】抽取直接相关的宫位与运限证据，给出判断与建议。',
        focusPalaces: dedupePalaces([
          mingPalace,
          bodyPalace,
          fortunePalace,
          careerPalace,
          wealthPalace,
          spousePalace,
          travelPalace,
          activePalace,
        ]).slice(0, 8),
        outputFocus: [
          '先直接回答问题，再补充关键依据。',
          '优先使用宫位、主星、四化、运限命中、证据摘要来支撑结论。',
          '建议要具体可执行，避免空泛表述。',
        ],
        avoid: ['不平均铺陈全盘，只取与【问题】直接相关的证据。'],
      };
    default:
      return {
        focusSummary: '围绕【问题】，结合盘面与运限给出判断与建议。',
        focusPalaces: dedupePalaces([
          mingPalace,
          bodyPalace,
          careerPalace,
          wealthPalace,
          spousePalace,
          activePalace,
        ]).slice(0, 6),
        outputFocus: ['先回答【问题】，再说明盘面依据。', '给出可操作建议，并区分短期与中期。'],
        avoid: ['不扩写无关专题，证据不足处明确保守表达。'],
      };
  }
}

/**
 * 盲派命理数据处理模块
 * 
 * 根据日柱天干地支从 mangpai.json 获取对应的口诀和称号
 */

import * as fs from 'fs';
import * as path from 'path';

export interface MangpaiEntry {
    index: number;
    type: string;      // 如 "甲子日"
    称号: string;       // 如 "天德贵人"
    口诀: string;       // 如 "甲子开元侬先来，水生木旺有文才..."
}

// 懒加载盲派数据
let mangpaiCache: MangpaiEntry[] | null = null;

function loadMangpaiData(): MangpaiEntry[] {
    if (mangpaiCache) return mangpaiCache;

    const filePath = path.join(process.cwd(), 'public', 'mangpai', 'mangpai.json');
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    mangpaiCache = JSON.parse(fileContent) as MangpaiEntry[];
    return mangpaiCache;
}

/**
 * 根据日柱获取盲派口诀
 * @param dayPillar 日柱天干地支，如 "甲子"
 * @returns 匹配的盲派条目，未找到返回 null
 */
export function getMangpaiByDayPillar(dayPillar: string): MangpaiEntry | null {
    // 尝试匹配 "甲子日" 格式
    const dayType = dayPillar.endsWith('日') ? dayPillar : `${dayPillar}日`;

    const mangpaiList = loadMangpaiData();
    const entry = mangpaiList.find(item => item.type === dayType);
    return entry || null;
}

/**
 * 生成盲派分析的系统提示词
 * @param dayPillar 日柱天干地支
 * @param basicChartInfo 基础命盘信息文本（姓名、性别、生日等）
 * @returns 盲派分析专用提示词
 */
export function generateMangpaiPrompt(dayPillar: string, basicChartInfo: string, extraContext?: string): string {
    const mangpai = getMangpaiByDayPillar(dayPillar);
    const extraSection = extraContext?.trim() ? `\n\n${extraContext.trim()}\n` : '';

    if (!mangpai) {
        // 如果没有找到对应的盲派数据，返回基础信息
        return `
--- 用户已选择以下命盘作为对话参考（盲派分析模式）---
${basicChartInfo}
请基于盲派命理理论为用户提供分析和建议。
${extraSection}
--- 命盘信息结束 ---
`;
    }

    return `
--- 用户已选择以下命盘作为对话参考（盲派分析模式）---
${basicChartInfo}

【盲派口诀】
日柱：${mangpai.type}
称号：${mangpai.称号}
口诀：${mangpai.口诀}

请严格基于以上盲派口诀和命理理论为用户进行分析。在分析时：
1. 首先解读该日柱的称号含义（${mangpai.称号}）
2. 逐句解析口诀内容，结合命主实际情况进行分析
3. 根据口诀中的喜忌指引，给出具体的趋吉避凶建议
4. 若用户询问特定运势，结合口诀中的关键字进行针对性解读

${extraSection}
--- 命盘信息结束 ---
`;
}

/**
 * 从八字数据中提取日柱
 * @param chartData 八字命盘数据
 * @returns 日柱天干地支，如 "甲子"
 */
export function extractDayPillar(chartData: { fourPillars?: { day?: { stem?: string; branch?: string } } }): string | null {
    const day = chartData?.fourPillars?.day;
    if (day?.stem && day?.branch) {
        return `${day.stem}${day.branch}`;
    }
    return null;
}

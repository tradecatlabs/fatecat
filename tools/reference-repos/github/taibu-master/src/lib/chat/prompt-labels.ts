/**
 * 提示词层级标签映射
 *
 * 用于 AI 设置页面和聊天提示词预览面板的统一显示。
 */

import { AI_PERSONALITY_META } from '@/lib/ai/personality-meta';

/** 层级显示条目（兼容完整诊断和简化版本） */
type LayerEntry = {
    id: string;
    priority?: string;
    included: boolean;
    tokens: number;
    truncated: boolean;
    reason?: string;
};

/** 静态层级 ID → 中文标签 */
export const PROMPT_LAYER_LABELS: Record<string, string> = {
    base_rules: '通用准则',
    personality_role: '专业分析师',
    chart_context: '命盘',
    expression_style: '表达风格',
    user_profile: '用户身份',
    custom_instructions: '自定义指令',
    mangpai_data: '盲派口诀',
    dream_bazi: '解梦·命盘信息',
    dream_fortune: '解梦·今日运势',
    visualization_dimensions: '可视化维度',
    visualization_dayun_display: '大运展示',
    visualization_chart_style: '图表风格',
    visualization_output_contract: '可视化输出',
    visualization_previous_charts: '历史图表',
    visualization_group: '可视化设置',
};

/** 需要合并显示的可视化层级前缀 */
const VISUALIZATION_PREFIX = 'visualization_';

/**
 * 解析层级 ID 为中文标签
 */
export function formatPromptLayerLabel(
    layerId: string,
    resolveName?: (layerId: string) => string | undefined,
): string {
    // personality_role:bazi+ziwei → 显示具体人格名
    if (layerId.startsWith('personality_role:')) {
        const tag = layerId.slice('personality_role:'.length);
        const names = tag.split('+').map((p) => {
            const meta = AI_PERSONALITY_META[p as keyof typeof AI_PERSONALITY_META];
            return meta?.name || p;
        }).join(' + ');
        return names || '专业分析师';
    }
    const staticLabel = PROMPT_LAYER_LABELS[layerId];
    if (staticLabel) return staticLabel;

    if (resolveName) {
        const resolved = resolveName(layerId);
        if (resolved) return resolved;
    }

    if (layerId.startsWith('mention_')) return '提及·数据';
    if (layerId.startsWith('kb_')) return '知识库';

    return layerId;
}

/**
 * 将多个 visualization_ 层合并为一个 "可视化设置" 条目，减少预览面板杂乱。
 * 其他层级保持原样。
 */
export function groupPromptLayers(
    layers: LayerEntry[],
): LayerEntry[] {
    const vizLayers: LayerEntry[] = [];
    const otherLayers: LayerEntry[] = [];

    for (const layer of layers) {
        if (layer.id.startsWith(VISUALIZATION_PREFIX)) {
            vizLayers.push(layer);
        } else {
            otherLayers.push(layer);
        }
    }

    if (vizLayers.length === 0) return layers;

    const includedViz = vizLayers.filter((l) => l.included);
    const merged: LayerEntry = {
        id: 'visualization_group',
        priority: 'P1',
        included: includedViz.length > 0,
        tokens: includedViz.reduce((sum, l) => sum + l.tokens, 0),
        truncated: includedViz.some((l) => l.truncated),
    };

    // 插入到第一个 visualization 层级原来所在的位置
    const result: LayerEntry[] = [];
    let vizInserted = false;
    for (let i = 0; i < layers.length; i++) {
        if (layers[i].id.startsWith(VISUALIZATION_PREFIX)) {
            if (!vizInserted) {
                result.push(merged);
                vizInserted = true;
            }
            // skip individual viz layers
        } else {
            result.push(layers[i]);
        }
    }
    // 防御性：如果 firstVizIndex 逻辑失败，确保插入
    if (!vizInserted) {
        result.push(merged);
    }

    return result;
}

/**
 * @mention 格式化工具
 *
 * 将消息中的 @{...} 格式转换为可读的 @名称 格式
 */

const mentionTokenRegex = /@\{(\{[\s\S]*?\}|[^{}]+)\}/g;

/**
 * 格式化消息中的 @mention 为可读格式
 */
export function formatMentionsForDisplay(content: string): string {
    return content.replace(mentionTokenRegex, (full, raw) => {
        try {
            const parsed = JSON.parse(raw) as { name?: string };
            if (parsed?.name) return `@${parsed.name}`;
        } catch {
            // 忽略解析错误
        }
        try {
            const parsed = JSON.parse(`{${raw}}`) as { name?: string };
            if (parsed?.name) return `@${parsed.name}`;
        } catch {
            // 忽略解析错误
        }
        return full;
    });
}

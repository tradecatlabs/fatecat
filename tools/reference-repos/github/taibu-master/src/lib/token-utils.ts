export function countTokens(text: string): number {
    if (!text) return 0;
    const chineseChars = (text.match(/[\u4e00-\u9fff]/g) || []).length;
    const otherChars = text.length - chineseChars;
    return Math.ceil(chineseChars / 1.5 + otherChars / 4);
}

export function truncateToTokens(text: string, maxTokens: number): string {
    const currentTokens = countTokens(text);
    if (currentTokens <= maxTokens) return text;
    const ratio = maxTokens / currentTokens;
    const targetLength = Math.floor(text.length * ratio * 0.9);
    return text.slice(0, targetLength) + '...（内容已截断）';
}

export function countMessageTokens(messages: Array<{ content?: string }>): number {
    if (!messages || messages.length === 0) return 0;
    let total = 0;
    for (const msg of messages) {
        if (!msg?.content) continue;
        total += countTokens(String(msg.content));
    }
    return total;
}

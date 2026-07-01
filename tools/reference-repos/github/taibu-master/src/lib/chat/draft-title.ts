function findSentenceBoundary(text: string): number {
    for (let index = 0; index < text.length; index += 1) {
        const char = text[index];
        if (char === '。' || char === '！' || char === '？') {
            return index;
        }
        if (char === '!' || char === '?') {
            const nextChar = text[index + 1] ?? '';
            if (!nextChar || /\s/u.test(nextChar)) {
                return index;
            }
        }
        if (char === '.') {
            const nextChar = text[index + 1] ?? '';
            if (!nextChar || /\s/u.test(nextChar)) {
                return index;
            }
        }
    }
    return -1;
}

export function buildDraftTitle(text: string): string {
    const trimmed = (text || '').trim();
    if (!trimmed) return '新对话';

    const firstLine = trimmed.split(/[\r\n]+/u)[0] ?? trimmed;
    const normalized = firstLine.replace(/\s+/g, ' ').trim();
    const boundaryIndex = findSentenceBoundary(normalized);
    if (boundaryIndex < 0) {
        return normalized;
    }
    return normalized.slice(0, boundaryIndex).trim() || normalized;
}

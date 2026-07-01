export function isValidBirthTimeString(value: unknown): value is string {
    if (typeof value !== 'string') {
        return false;
    }

    const trimmed = value.trim();
    if (!/^\d{2}:\d{2}$/.test(trimmed)) {
        return false;
    }

    const [hour, minute] = trimmed.split(':').map(Number);
    return (
        Number.isInteger(hour)
        && hour >= 0
        && hour <= 23
        && Number.isInteger(minute)
        && minute >= 0
        && minute <= 59
    );
}

export function parseBirthTimeString(value: string): { hour: number; minute: number } | null {
    if (!isValidBirthTimeString(value)) {
        return null;
    }

    const [hour, minute] = value.split(':').map(Number);
    return { hour, minute };
}

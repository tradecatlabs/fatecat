export async function withRetry<T>(
    fn: () => Promise<T>,
    retries = 3,
    delay = 500
): Promise<T> {
    let lastError: unknown;
    for (let i = 0; i < retries; i++) {
        try {
            return await fn();
        } catch (err) {
            lastError = err;
            if (i < retries - 1) {
                await new Promise(r => setTimeout(r, delay * (i + 1)));
            }
        }
    }
    throw lastError;
}

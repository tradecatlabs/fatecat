export function createMockUIMessageResult(options?: {
    text?: string;
    reasoning?: string;
}) {
    const text = options?.text ?? 'analysis';
    const reasoning = options?.reasoning ?? 'reason';

    return {
        toUIMessageStream(params?: {
            onFinish?: (event: {
                responseMessage: { parts: Array<Record<string, unknown>> };
                finishReason?: string;
                isAborted: boolean;
                isContinuation: boolean;
                messages: Array<{ parts: Array<Record<string, unknown>> }>;
            }) => PromiseLike<void> | void;
        }) {
            const stream = new ReadableStream<Record<string, unknown>>({
                start(controller) {
                    if (reasoning) {
                        controller.enqueue({ type: 'reasoning-start', id: 'reasoning-1' });
                        controller.enqueue({ type: 'reasoning-delta', id: 'reasoning-1', delta: reasoning });
                        controller.enqueue({ type: 'reasoning-end', id: 'reasoning-1' });
                    }
                    if (text) {
                        controller.enqueue({ type: 'text-start', id: 'text-1' });
                        controller.enqueue({ type: 'text-delta', id: 'text-1', delta: text });
                        controller.enqueue({ type: 'text-end', id: 'text-1' });
                    }
                    controller.close();
                },
            });

            queueMicrotask(() => {
                void params?.onFinish?.({
                    responseMessage: {
                        parts: [
                            ...(reasoning ? [{ type: 'reasoning', text: reasoning, state: 'done' }] : []),
                            ...(text ? [{ type: 'text', text, state: 'done' }] : []),
                        ],
                    },
                    finishReason: 'stop',
                    isAborted: false,
                    isContinuation: false,
                    messages: [],
                });
            });

            return stream;
        },
    };
}

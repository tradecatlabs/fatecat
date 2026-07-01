declare module 'https://deno.land/x/postgresjs@v3.4.5/mod.js' {
    type PostgresQueryFn = <T = Record<string, unknown>>(
        strings: TemplateStringsArray,
        ...values: unknown[]
    ) => Promise<T[]>;

    type PostgresClient = PostgresQueryFn & {
        unsafe: (query: string) => Promise<unknown>;
        end: () => Promise<void>;
    };

    type PostgresFactory = (url: string, options?: Record<string, unknown>) => PostgresClient;

    const postgres: PostgresFactory;
    export default postgres;
}

declare const Deno: {
    env: {
        get(key: string): string | undefined;
    };
    serve(handler: (req: Request) => Response | Promise<Response>): void;
};

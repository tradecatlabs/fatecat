export type PaginationOptions = {
    defaultPage?: number;
    defaultPageSize?: number;
    minPage?: number;
    minPageSize?: number;
    maxPageSize?: number;
};

export function parsePagination(
    searchParams: URLSearchParams,
    options: PaginationOptions = {}
): { page: number; pageSize: number; from: number; to: number } {
    const defaultPage = options.defaultPage ?? 1;
    const defaultPageSize = options.defaultPageSize ?? 20;
    const minPage = options.minPage ?? 1;
    const minPageSize = options.minPageSize ?? 1;
    const maxPageSize = options.maxPageSize ?? 200;

    const rawPage = searchParams.get('page');
    const rawPageSize = searchParams.get('pageSize');

    const parsedPage = rawPage ? Number(rawPage) : NaN;
    const parsedPageSize = rawPageSize ? Number(rawPageSize) : NaN;

    const page = Number.isFinite(parsedPage) && parsedPage >= minPage ? Math.floor(parsedPage) : defaultPage;
    const unclampedSize = Number.isFinite(parsedPageSize) ? Math.floor(parsedPageSize) : defaultPageSize;
    const pageSize = Math.min(maxPageSize, Math.max(minPageSize, unclampedSize));

    const from = (page - 1) * pageSize;
    const to = from + pageSize - 1;

    return { page, pageSize, from, to };
}

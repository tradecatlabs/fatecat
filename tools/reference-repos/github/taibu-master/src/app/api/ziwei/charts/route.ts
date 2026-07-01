import { createChartGetHandler, createChartPostHandler, validateRequiredBirthTime } from '@/lib/api/chart-crud';

const config = {
    tableName: 'ziwei_charts',
    validateCreatePayload: validateRequiredBirthTime,
} as const;

export const GET = createChartGetHandler(config);
export const POST = createChartPostHandler(config);

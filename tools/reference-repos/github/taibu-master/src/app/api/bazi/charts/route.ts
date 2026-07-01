import { createChartGetHandler, createChartPostHandler, createRequiredBirthTimeValidator } from '@/lib/api/chart-crud';

const config = {
    tableName: 'bazi_charts',
    validateCreatePayload: createRequiredBirthTimeValidator('八字命盘必须提供有效的出生时辰'),
} as const;

export const GET = createChartGetHandler(config);
export const POST = createChartPostHandler(config);

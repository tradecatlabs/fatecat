import { createChartUpdateHandler, prepareBaziChartUpdatePayload } from '@/lib/api/chart-crud';

export const POST = createChartUpdateHandler({
    tableName: 'bazi_charts',
    prepareUpdatePayload: prepareBaziChartUpdatePayload,
});

import type { DataSourceType } from '@/lib/data-sources/types';
import { DATA_SUBCATEGORY_MAP } from '@/components/chat/mention/mention-data-catalog';

export function getVisibleDataSubcategories(enabledTypes: readonly DataSourceType[]): string[] {
    const enabled = new Set(enabledTypes);
    return Object.keys(DATA_SUBCATEGORY_MAP).filter((subcategory) =>
        (DATA_SUBCATEGORY_MAP[subcategory] || []).some((type) => enabled.has(type))
    );
}

export function getVisibleDataTypesForSubcategory(
    subcategory: string,
    enabledTypes: readonly DataSourceType[]
): DataSourceType[] {
    const enabled = new Set(enabledTypes);
    return (DATA_SUBCATEGORY_MAP[subcategory] || []).filter((type) => enabled.has(type));
}

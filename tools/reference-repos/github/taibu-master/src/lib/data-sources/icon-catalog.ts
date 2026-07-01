import type { NavIcon } from '@/lib/navigation/registry';
import { getNavItemById } from '@/lib/navigation/registry';
import type { DataSourceType } from '@/lib/data-sources/types';
import { getDataSourceNavId } from '@/lib/data-sources/catalog';

export function getDataSourceNavIcon(type: DataSourceType): NavIcon | undefined {
    return getNavItemById(getDataSourceNavId(type))?.icon;
}

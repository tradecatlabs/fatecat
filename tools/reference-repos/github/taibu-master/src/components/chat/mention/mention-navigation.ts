export type MentionNavigationLevel = 'category' | 'subcategory' | 'type' | 'item' | 'search';

export interface MentionNavigationState {
    level: MentionNavigationLevel;
    selectedCategory?: 'data' | 'knowledge';
    selectedSubcategory?: string;
    selectedType?: string;
    activeIndex: number;
}

interface MentionNavigationOptions {
    defaultCategory?: 'knowledge' | 'data';
    knowledgeBaseLocked?: boolean;
}

export function getInitialMentionNavigationState({
    defaultCategory,
    knowledgeBaseLocked = false,
}: MentionNavigationOptions): MentionNavigationState {
    if (knowledgeBaseLocked) {
        return { level: 'subcategory', selectedCategory: 'data', activeIndex: 0 };
    }

    if (defaultCategory === 'knowledge') {
        return { level: 'item', selectedCategory: 'knowledge', activeIndex: 0 };
    }

    if (defaultCategory === 'data') {
        return { level: 'subcategory', selectedCategory: 'data', activeIndex: 0 };
    }

    return { level: 'category', activeIndex: 0 };
}

export function getBackNavigationState(
    state: MentionNavigationState,
    { knowledgeBaseLocked = false }: Pick<MentionNavigationOptions, 'knowledgeBaseLocked'> = {}
): MentionNavigationState | null {
    if (state.level === 'item' && state.selectedCategory === 'data' && state.selectedSubcategory) {
        if (state.selectedType) {
            return { level: 'type', selectedCategory: 'data', selectedSubcategory: state.selectedSubcategory, activeIndex: 0 };
        }

        return { level: 'subcategory', selectedCategory: 'data', activeIndex: 0 };
    }

    if (state.level === 'type') {
        return { level: 'subcategory', selectedCategory: 'data', activeIndex: 0 };
    }

    if (state.level === 'subcategory') {
        return knowledgeBaseLocked ? null : { level: 'category', activeIndex: 0 };
    }

    if (state.level === 'item' && state.selectedCategory === 'knowledge') {
        return knowledgeBaseLocked ? null : { level: 'category', activeIndex: 0 };
    }

    return state;
}

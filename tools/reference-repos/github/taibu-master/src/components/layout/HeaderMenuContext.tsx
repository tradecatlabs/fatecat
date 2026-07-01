/**
 * Header 菜单上下文
 *
 * 允许子页面向 Header 的三点菜单注入自定义菜单项
 */
'use client';

import { createContext, useContext, useState, useCallback, type ReactNode } from 'react';

export interface HeaderMenuItem {
    id: string;
    label: string;
    icon?: ReactNode;
    onClick: () => void;
    disabled?: boolean;
}

interface HeaderMenuContextType {
    menuItems: HeaderMenuItem[];
    setMenuItems: (items: HeaderMenuItem[]) => void;
    clearMenuItems: () => void;
}

const HeaderMenuContext = createContext<HeaderMenuContextType | null>(null);

export function HeaderMenuProvider({ children }: { children: ReactNode }) {
    const [menuItems, setMenuItemsState] = useState<HeaderMenuItem[]>([]);

    const setMenuItems = useCallback((items: HeaderMenuItem[]) => {
        setMenuItemsState(items);
    }, []);

    const clearMenuItems = useCallback(() => {
        setMenuItemsState([]);
    }, []);

    return (
        <HeaderMenuContext.Provider value={{ menuItems, setMenuItems, clearMenuItems }}>
            {children}
        </HeaderMenuContext.Provider>
    );
}

export function useHeaderMenu() {
    const context = useContext(HeaderMenuContext);
    if (!context) {
        throw new Error('useHeaderMenu must be used within HeaderMenuProvider');
    }
    return context;
}

export function useHeaderMenuSafe() {
    return useContext(HeaderMenuContext);
}

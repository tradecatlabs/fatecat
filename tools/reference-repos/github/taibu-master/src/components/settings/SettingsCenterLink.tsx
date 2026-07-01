'use client';

import type { MouseEvent, MouseEventHandler, ReactNode } from 'react';
import Link from 'next/link';
import { getSettingsCenterRouteTarget, openSettingsCenter, type SettingsCenterTab } from '@/lib/settings-center';

interface SettingsCenterLinkProps {
  tab: SettingsCenterTab;
  className?: string;
  children: ReactNode;
  title?: string;
  onClick?: MouseEventHandler<HTMLAnchorElement>;
}

function isModifiedEvent(event: MouseEvent<HTMLAnchorElement>) {
  return event.metaKey || event.altKey || event.ctrlKey || event.shiftKey;
}

export function SettingsCenterLink({
  tab,
  className,
  children,
  title,
  onClick,
}: SettingsCenterLinkProps) {
  return (
    <Link
      href={getSettingsCenterRouteTarget(tab)}
      className={className}
      title={title}
      onClick={(event) => {
        onClick?.(event);
        if (event.defaultPrevented) return;
        if (isModifiedEvent(event)) return;

        event.preventDefault();
        openSettingsCenter(tab);
      }}
    >
      {children}
    </Link>
  );
}

'use client';

import Link from 'next/link';
import { Lock } from 'lucide-react';

interface SettingsLoginRequiredProps {
  title?: string;
  description?: string;
}

export function SettingsLoginRequired({
  title = '请先登录',
  description = '登录后即可使用个性化设置、命盘管理和知识库等个人能力。',
}: SettingsLoginRequiredProps) {
  return (
    <div className="rounded-lg border border-border bg-background p-5">
      <div className="mb-3 flex h-9 w-9 items-center justify-center rounded-md bg-background-secondary text-foreground/70">
        <Lock className="h-4 w-4" />
      </div>
      <h2 className="text-sm font-semibold text-foreground">{title}</h2>
      <p className="mt-1 text-sm text-foreground-secondary">{description}</p>
      <Link
        href="/"
        className="mt-4 inline-flex items-center rounded-md border border-border bg-transparent px-3 py-2 text-sm font-medium text-foreground transition-colors duration-150 hover:bg-background-secondary active:bg-background-tertiary"
      >
        返回首页
      </Link>
    </div>
  );
}

'use client';

import { CustomProviderPanel } from '@/components/chat/CustomProviderPanel';

export default function BYOKPanel() {
  return (
    <CustomProviderPanel
      embedded
      title="BYOK"
      description="仅当前标签页生效，不会保存到服务器，关闭页面后自动失效，不消耗本站积分"
      showByokBadge={false}
    />
  );
}

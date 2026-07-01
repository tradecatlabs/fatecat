import { FeatureGate } from '@/components/layout/FeatureGate';

export default function ChatLayout({ children }: { children: React.ReactNode }) {
    return <FeatureGate featureId="chat">{children}</FeatureGate>;
}

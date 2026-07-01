import { FeatureGate } from '@/components/layout/FeatureGate';

export default function RecordsLayout({ children }: { children: React.ReactNode }) {
    return <FeatureGate featureId="records">{children}</FeatureGate>;
}

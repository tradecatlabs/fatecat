import type { ZiweiStarJSON } from 'taibu-core/ziwei';
import { getBrightnessColor, getMutagenColor } from '@/lib/divination/display-helpers';

type StarBadgeStar = ZiweiStarJSON & {
    type: 'major' | 'minor' | 'auxiliary';
};

interface StarBadgeProps {
    star: StarBadgeStar;
    size?: 'sm' | 'md';
}

const MINOR_MALEFIC_STARS = new Set(['擎羊', '陀罗', '火星', '铃星', '地空', '地劫']);

export function StarBadge({ star, size = 'sm' }: StarBadgeProps) {
    const isMajor = star.type === 'major';
    const isMinor = star.type === 'minor';
    const isAuxiliary = star.type === 'auxiliary';
    const isMinorMalefic = isMinor && MINOR_MALEFIC_STARS.has(star.星名);
    const textSize = size === 'sm' ? 'text-[10px]' : 'text-xs';
    const statusSize = size === 'sm' ? 'text-[9px]' : 'text-[10px]';

    // 竖排显示星名，不使用外框
    const textColor = isMinorMalefic
        ? 'text-rose-600 dark:text-rose-400'
        : isMajor
            ? 'text-red-500'
            : isMinor
                ? 'text-purple-500'
                : isAuxiliary
                    ? 'text-blue-500'
                    : 'text-foreground-secondary';

    // 亮度颜色标记
    const brightnessStyle = star.亮度
        ? { color: getBrightnessColor(star.亮度) }
        : undefined;

    // 四化颜色标记
    const mutagenColor = getMutagenColor(star.四化);
    const hasMutagen = star.四化 && mutagenColor !== 'transparent';
    const mutagenMarkers = [
        star.离心自化 ? { label: `↓${star.离心自化}`, color: getMutagenColor(star.离心自化) } : null,
        star.向心自化 ? { label: `↑${star.向心自化}`, color: getMutagenColor(star.向心自化) } : null,
    ].filter(Boolean) as Array<{ label: string; color: string }>;

    const nameChars = Array.from(star.星名);

    return (
        <span className={`inline-flex flex-col items-center ${textSize} leading-tight`}>
            <span className={`flex flex-col items-center font-medium ${textColor}`}>
                {nameChars.map((char, idx) => (
                    <span key={idx}>{char}</span>
                ))}
            </span>
            {star.亮度 && (
                <span className={statusSize} style={brightnessStyle}>
                    {star.亮度}
                </span>
            )}
            {hasMutagen && (
                <span className={statusSize} style={{ color: mutagenColor }}>
                    {star.四化}
                </span>
            )}
            {mutagenMarkers.map((marker, idx) => (
                <span
                    key={`${marker.label}-${idx}`}
                    className={statusSize}
                    style={marker.color !== 'transparent' ? { color: marker.color } : undefined}
                >
                    {marker.label}
                </span>
            ))}
        </span>
    );
}

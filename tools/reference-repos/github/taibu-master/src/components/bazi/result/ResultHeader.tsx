import Link from 'next/link';
import { Edit3, Save, Check, Share2, Copy } from 'lucide-react';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';

export function ResultHeader({
    chartId,
    saving,
    saved,
    saveDisabled = false,
    saveLabel = '保存',
    copied,
    jsonCopied,
    showJsonCopy = false,
    onEdit,
    onSave,
    onCopy,
    onCopyJson,
    onShare,
}: {
    chartId: string | null;
    saving: boolean;
    saved: boolean;
    saveDisabled?: boolean;
    saveLabel?: string;
    copied: boolean;
    jsonCopied?: boolean;
    showJsonCopy?: boolean;
    onEdit: () => void;
    onSave: () => void;
    onCopy: () => void;
    onCopyJson?: () => void;
    onShare: () => void;
}) {
    void chartId;
    return (
        <div className="hidden md:flex items-center justify-between mb-6">
            <Link
                href="/bazi"
                className="text-sm font-medium text-foreground/40 hover:text-foreground hover:bg-background-secondary px-2 py-1 rounded-md transition-colors"
            >
                返回
            </Link>
            <div className="flex items-center gap-2">
                <button
                    onClick={onEdit}
                    disabled={saving}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm font-medium border border-border hover:bg-background-secondary transition-colors disabled:opacity-50"
                >
                    <Edit3 className="w-3.5 h-3.5" />
                    修改
                </button>
                <button
                    onClick={onSave}
                    disabled={saving || saved || saveDisabled}
                    className={`
                        inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm font-medium transition-colors
                        ${saved
                            ? 'text-[#0f7b6c] bg-[#0f7b6c]/5 border border-[#0f7b6c]/10'
                            : 'bg-[#2383e2] text-white hover:bg-[#2383e2]/90 disabled:opacity-50'
                        }
                    `}
                >
                    {saved ? (
                        <><Check className="w-3.5 h-3.5" />已保存</>
                    ) : saving ? (
                        <><SoundWaveLoader variant="inline" />保存中</>
                    ) : (
                        <><Save className="w-3.5 h-3.5" />{saveLabel}</>
                    )}
                </button>
                <button
                    onClick={onCopy}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm font-medium border border-border hover:bg-background-secondary transition-colors"
                >
                    {copied ? <Check className="w-3.5 h-3.5 text-[#0f7b6c]" /> : <Copy className="w-3.5 h-3.5" />}
                    {copied ? '已复制' : '复制'}
                </button>
                {showJsonCopy && onCopyJson && (
                    <button
                        onClick={onCopyJson}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm font-medium border border-border hover:bg-background-secondary transition-colors"
                    >
                        {jsonCopied ? <Check className="w-3.5 h-3.5 text-[#0f7b6c]" /> : <Copy className="w-3.5 h-3.5" />}
                        {jsonCopied ? 'JSON 已复制' : '复制 JSON'}
                    </button>
                )}
                <button
                    onClick={onShare}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm font-medium border border-border hover:bg-background-secondary transition-colors"
                >
                    <Share2 className="w-3.5 h-3.5" />
                    分享
                </button>
            </div>
        </div>
    );
}

import { AlertCircle, Check } from 'lucide-react';

export function StatusBanner({ error, success }: { error: string; success: string }) {
    return (
        <>
            {error && (
                <div className="p-3 rounded-lg bg-red-500/10 text-red-500 text-sm flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 flex-shrink-0" />
                    {error}
                </div>
            )}
            {success && (
                <div className="p-3 rounded-lg bg-green-500/10 text-green-500 text-sm flex items-center gap-2">
                    <Check className="w-4 h-4 flex-shrink-0" />
                    {success}
                </div>
            )}
        </>
    );
}

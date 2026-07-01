import { useMemo, useState } from 'react';
import { shareText } from '@/utils/share-text';

export interface PromptCopyShare {
  copyState: string;
  shareState: string;
  handleCopy: () => Promise<void>;
  handleShare: () => Promise<void>;
}

export function usePromptCopyShare(promptText: string): PromptCopyShare {
  const [copyResult, setCopyResult] = useState<'idle' | 'copied' | 'failed'>('idle');
  const [shareResult, setShareResult] = useState<'idle' | 'shared' | 'failed' | 'unsupported'>(
    'idle',
  );

  const copyState = useMemo(() => {
    if (!promptText) return '暂无内容';
    if (copyResult === 'copied') return '已复制';
    if (copyResult === 'failed') return '复制失败';
    return '复制';
  }, [copyResult, promptText]);

  const shareState = useMemo(() => {
    if (!promptText) return '暂无内容';
    if (shareResult === 'shared') return '已调起系统分享';
    if (shareResult === 'unsupported') return '当前设备不支持系统分享';
    if (shareResult === 'failed') return '分享失败';
    return '分享';
  }, [shareResult, promptText]);

  async function handleCopy() {
    if (!promptText) {
      setCopyResult('failed');
      return;
    }

    try {
      await navigator.clipboard.writeText(promptText);
      setCopyResult('copied');
    } catch {
      setCopyResult('failed');
    }
  }

  async function handleShare() {
    if (!promptText) {
      setShareResult('failed');
      return;
    }

    try {
      const ok = await shareText(promptText);
      setShareResult(ok ? 'shared' : 'unsupported');
    } catch {
      setShareResult('failed');
    }
  }

  return { copyState, shareState, handleCopy, handleShare };
}

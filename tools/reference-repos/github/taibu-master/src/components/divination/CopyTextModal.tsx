'use client';

import { ConfirmDialog } from '@/components/ui/ConfirmDialog';
import { TextDetailLevelPicker } from '@/components/divination/TextDetailLevelPicker';
import type { ChartTextDetailLevel } from '@/lib/divination/detail-level';

export function CopyTextModal({
  isOpen,
  title = '复制文本',
  value,
  onChange,
  onClose,
  onConfirm,
}: {
  isOpen: boolean;
  title?: string;
  value: ChartTextDetailLevel;
  onChange: (value: ChartTextDetailLevel) => void;
  onClose: () => void;
  onConfirm: (value: ChartTextDetailLevel) => void | Promise<void>;
}) {
  return (
    <ConfirmDialog
      isOpen={isOpen}
      onClose={onClose}
      onConfirm={onClose}
      title={title}
      description="选择复制级别后立即复制，点空白处关闭。"
      showActions={false}
      variant="default"
    >
      <div className="flex justify-center">
        <TextDetailLevelPicker
          value={value}
          onChange={onChange}
          onSelect={onConfirm}
          label={null}
          className="justify-center"
        />
      </div>
    </ConfirmDialog>
  );
}

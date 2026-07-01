/**
 * 验证码输入组件
 *
 * 'use client' 标记说明：
 * - 使用 React hooks (useRef, useEffect)
 * - 有键盘导航和粘贴交互功能
 */
'use client';

import { useRef, useEffect, KeyboardEvent, ClipboardEvent } from 'react';

interface VerificationCodeInputProps {
    value: string;
    onChange: (value: string) => void;
    onComplete?: (value: string) => void;
    length?: number;
    disabled?: boolean;
}

export function VerificationCodeInput({
    value,
    onChange,
    onComplete,
    length = 6,
    disabled = false,
}: VerificationCodeInputProps) {
    const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

    // 当值填满时自动触发完成回调
    useEffect(() => {
        if (value.length === length && onComplete) {
            onComplete(value);
        }
    }, [value, length, onComplete]);

    const handleChange = (index: number, char: string) => {
        // 只允许数字
        const digit = char.replace(/\D/g, '').slice(0, 1);
        if (!digit && char !== '') return;

        const newValue = value.split('');
        newValue[index] = digit;
        const result = newValue.join('').slice(0, length);
        onChange(result);

        // 自动跳转到下一个输入框
        if (digit && index < length - 1) {
            inputRefs.current[index + 1]?.focus();
        }
    };

    const handleKeyDown = (index: number, e: KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Backspace') {
            if (!value[index] && index > 0) {
                // 当前格为空，删除上一格并聚焦
                const newValue = value.split('');
                newValue[index - 1] = '';
                onChange(newValue.join(''));
                inputRefs.current[index - 1]?.focus();
            } else {
                // 删除当前格
                const newValue = value.split('');
                newValue[index] = '';
                onChange(newValue.join(''));
            }
            e.preventDefault();
        } else if (e.key === 'ArrowLeft' && index > 0) {
            inputRefs.current[index - 1]?.focus();
        } else if (e.key === 'ArrowRight' && index < length - 1) {
            inputRefs.current[index + 1]?.focus();
        }
    };

    const handlePaste = (e: ClipboardEvent<HTMLInputElement>) => {
        e.preventDefault();
        const pastedData = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, length);
        if (pastedData) {
            onChange(pastedData);
            // 聚焦到最后一个填入的位置或最后一格
            const focusIndex = Math.min(pastedData.length, length - 1);
            inputRefs.current[focusIndex]?.focus();
        }
    };

    const handleFocus = (index: number) => {
        // 聚焦时选中内容
        inputRefs.current[index]?.select();
    };

    return (
        <div className="flex gap-2 justify-center">
            {Array.from({ length }).map((_, index) => (
                <input
                    key={index}
                    ref={(el) => { inputRefs.current[index] = el; }}
                    type="text"
                    inputMode="numeric"
                    maxLength={1}
                    value={value[index] || ''}
                    onChange={(e) => handleChange(index, e.target.value)}
                    onKeyDown={(e) => handleKeyDown(index, e)}
                    onPaste={handlePaste}
                    onFocus={() => handleFocus(index)}
                    disabled={disabled}
                    className="w-10 h-12 text-center text-xl font-mono rounded-lg bg-background-secondary border border-border focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20 transition-all disabled:opacity-50"
                />
            ))}
        </div>
    );
}

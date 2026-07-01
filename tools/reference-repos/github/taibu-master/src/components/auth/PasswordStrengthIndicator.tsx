/**
 * 密码强度指示器组件
 * 
 * 显示密码强度等级和具体要求
 */
'use client';

import { useMemo } from 'react';
import { Check, X } from 'lucide-react';

interface PasswordStrengthResult {
    isValid: boolean;
    score: number; // 0-4
    checks: {
        minLength: boolean;
        hasLowercase: boolean;
        hasUppercase: boolean;
        hasNumber: boolean;
    };
}

export function validatePasswordStrength(password: string): PasswordStrengthResult {
    const checks = {
        minLength: password.length >= 8,
        hasLowercase: /[a-z]/.test(password),
        hasUppercase: /[A-Z]/.test(password),
        hasNumber: /\d/.test(password),
    };

    const score = Object.values(checks).filter(Boolean).length;
    const isValid = checks.minLength && checks.hasLowercase && checks.hasUppercase && checks.hasNumber;

    return { isValid, score, checks };
}

interface PasswordStrengthIndicatorProps {
    password: string;
}

export function PasswordStrengthIndicator({ password }: PasswordStrengthIndicatorProps) {
    const { score, checks } = useMemo(() => validatePasswordStrength(password), [password]);

    if (!password) return null;

    const strengthLabels = ['弱', '弱', '中', '强', '极强'];
    const strengthColors = [
        'bg-red-500',
        'bg-red-500',
        'bg-orange-500',
        'bg-yellow-500',
        'bg-green-500',
    ];

    const requirements = [
        { key: 'minLength', label: '至少8个字符', met: checks.minLength },
        { key: 'hasLowercase', label: '包含小写字母', met: checks.hasLowercase },
        { key: 'hasUppercase', label: '包含大写字母', met: checks.hasUppercase },
        { key: 'hasNumber', label: '包含数字', met: checks.hasNumber },
    ];

    return (
        <div className="mt-2 space-y-2">
            {/* 强度条 */}
            <div className="flex items-center gap-2">
                <div className="flex-1 flex gap-1">
                    {[0, 1, 2, 3].map((i) => (
                        <div
                            key={i}
                            className={`h-1 flex-1 rounded-full transition-colors ${i < score ? strengthColors[score] : 'bg-border'
                                }`}
                        />
                    ))}
                </div>
                <span className={`text-xs font-medium ${score <= 1 ? 'text-red-500' :
                        score === 2 ? 'text-orange-500' :
                            score === 3 ? 'text-yellow-500' :
                                'text-green-500'
                    }`}>
                    {strengthLabels[score]}
                </span>
            </div>

            {/* 要求列表 */}
            <div className="grid grid-cols-2 gap-1 text-xs">
                {requirements.map((req) => (
                    <div
                        key={req.key}
                        className={`flex items-center gap-1 ${req.met ? 'text-green-500' : 'text-foreground-secondary'
                            }`}
                    >
                        {req.met ? (
                            <Check className="w-3 h-3" />
                        ) : (
                            <X className="w-3 h-3" />
                        )}
                        <span>{req.label}</span>
                    </div>
                ))}
            </div>
        </div>
    );
}

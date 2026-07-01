/**
 * 登录表单字段组件
 *
 * 'use client' 标记说明：
 * - 使用交互状态控制密码可见性
 */
'use client';

import { Mail, Lock, Eye, EyeOff } from 'lucide-react';

type LoginMethod = 'password' | 'otp';

interface LoginFormProps {
    loginMethod: LoginMethod;
    onLoginMethodChange: (method: LoginMethod) => void;
    emailPrefix: string;
    onEmailPrefixChange: (value: string) => void;
    emailSuffix: string;
    onEmailSuffixChange: (value: string) => void;
    emailSuffixes: string[];
    password: string;
    onPasswordChange: (value: string) => void;
    showPassword: boolean;
    onToggleShowPassword: () => void;
    onForgotPassword: () => void;
}

export function LoginForm({
    loginMethod,
    onLoginMethodChange,
    emailPrefix,
    onEmailPrefixChange,
    emailSuffix,
    onEmailSuffixChange,
    emailSuffixes,
    password,
    onPasswordChange,
    showPassword,
    onToggleShowPassword,
    onForgotPassword,
}: LoginFormProps) {
    return (
        <>
            {/* 登录方式切换 */}
            <div className="flex gap-2 p-1 bg-background-secondary rounded-xl">
                <button
                    type="button"
                    onClick={() => onLoginMethodChange('password')}
                    className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-colors ${loginMethod === 'password'
                        ? 'bg-background text-foreground shadow-sm'
                        : 'text-foreground-secondary hover:text-foreground'
                    }`}
                >
                    密码登录
                </button>
                <button
                    type="button"
                    onClick={() => onLoginMethodChange('otp')}
                    className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-colors ${loginMethod === 'otp'
                        ? 'bg-background text-foreground shadow-sm'
                        : 'text-foreground-secondary hover:text-foreground'
                    }`}
                >
                    验证码登录
                </button>
            </div>

            {/* 邮箱 */}
            <EmailField
                emailPrefix={emailPrefix}
                onEmailPrefixChange={onEmailPrefixChange}
                emailSuffix={emailSuffix}
                onEmailSuffixChange={onEmailSuffixChange}
                emailSuffixes={emailSuffixes}
            />

            {/* 密码（仅密码登录） */}
            {loginMethod === 'password' && (
                <>
                    <div className="space-y-2">
                        <label className="text-sm font-medium text-foreground-secondary">密码</label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-foreground-secondary" />
                            <input
                                type={showPassword ? 'text' : 'password'}
                                value={password}
                                onChange={(e) => onPasswordChange(e.target.value)}
                                placeholder="输入密码"
                                required
                                minLength={6}
                                className="w-full pl-10 pr-10 py-3 rounded-xl bg-background-secondary border border-border focus:border-accent focus:outline-none transition-colors"
                            />
                            <button
                                type="button"
                                onClick={onToggleShowPassword}
                                className="absolute right-3 top-1/2 -translate-y-1/2 text-foreground-secondary hover:text-foreground transition-colors"
                            >
                                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                            </button>
                        </div>
                    </div>
                    <div className="text-right">
                        <button
                            type="button"
                            onClick={onForgotPassword}
                            className="text-sm text-accent hover:underline"
                        >
                            忘记密码？
                        </button>
                    </div>
                </>
            )}
        </>
    );
}

/** 共享邮箱输入字段 */
export function EmailField({
    emailPrefix,
    onEmailPrefixChange,
    emailSuffix,
    onEmailSuffixChange,
    emailSuffixes,
}: {
    emailPrefix: string;
    onEmailPrefixChange: (value: string) => void;
    emailSuffix: string;
    onEmailSuffixChange: (value: string) => void;
    emailSuffixes: string[];
}) {
    return (
        <div className="space-y-2">
            <label className="text-sm font-medium text-foreground-secondary">邮箱</label>
            <div className="flex gap-2">
                <div className="relative flex-1">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-foreground-secondary" />
                    <input
                        type="text"
                        value={emailPrefix}
                        onChange={(e) => onEmailPrefixChange(e.target.value)}
                        placeholder="邮箱前缀"
                        required
                        className="w-full pl-10 pr-4 py-3 rounded-xl bg-background-secondary border border-border focus:border-accent focus:outline-none transition-colors"
                    />
                </div>
                <select
                    value={emailSuffix}
                    onChange={(e) => onEmailSuffixChange(e.target.value)}
                    className="px-3 py-3 rounded-xl bg-background-secondary border border-border focus:border-accent focus:outline-none transition-colors text-sm"
                >
                    {emailSuffixes.map(suffix => (
                        <option key={suffix} value={suffix}>{suffix}</option>
                    ))}
                </select>
            </div>
        </div>
    );
}

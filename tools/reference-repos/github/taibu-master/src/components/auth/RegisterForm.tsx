/**
 * 注册表单字段组件
 *
 * 'use client' 标记说明：
 * - 使用交互状态控制密码可见性
 */
'use client';

import { Lock, User, Eye, EyeOff } from 'lucide-react';
import { PasswordStrengthIndicator } from '@/components/auth/PasswordStrengthIndicator';
import { VerificationCodeInput } from '@/components/auth/VerificationCodeInput';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { EmailField } from '@/components/auth/LoginForm';

interface RegisterFormProps {
    nickname: string;
    onNicknameChange: (value: string) => void;
    emailPrefix: string;
    onEmailPrefixChange: (value: string) => void;
    emailSuffix: string;
    onEmailSuffixChange: (value: string) => void;
    emailSuffixes: string[];
    password: string;
    onPasswordChange: (value: string) => void;
    confirmPassword: string;
    onConfirmPasswordChange: (value: string) => void;
    showPassword: boolean;
    onToggleShowPassword: () => void;
    showConfirmPassword: boolean;
    onToggleShowConfirmPassword: () => void;
    verificationCode: string;
    onVerificationCodeChange: (value: string) => void;
    onSendCode: () => void;
    sendingCode: boolean;
    countdown: number;
    loading: boolean;
}

export function RegisterForm({
    nickname,
    onNicknameChange,
    emailPrefix,
    onEmailPrefixChange,
    emailSuffix,
    onEmailSuffixChange,
    emailSuffixes,
    password,
    onPasswordChange,
    confirmPassword,
    onConfirmPasswordChange,
    showPassword,
    onToggleShowPassword,
    showConfirmPassword,
    onToggleShowConfirmPassword,
    verificationCode,
    onVerificationCodeChange,
    onSendCode,
    sendingCode,
    countdown,
    loading,
}: RegisterFormProps) {
    return (
        <>
            {/* 昵称 */}
            <div className="space-y-2">
                <label className="text-sm font-medium text-foreground-secondary">昵称</label>
                <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-foreground-secondary" />
                    <input
                        type="text"
                        value={nickname}
                        onChange={(e) => onNicknameChange(e.target.value)}
                        placeholder="输入您的昵称"
                        className="w-full pl-10 pr-4 py-3 rounded-xl bg-background-secondary border border-border focus:border-accent focus:outline-none transition-colors"
                    />
                </div>
            </div>

            {/* 邮箱 */}
            <EmailField
                emailPrefix={emailPrefix}
                onEmailPrefixChange={onEmailPrefixChange}
                emailSuffix={emailSuffix}
                onEmailSuffixChange={onEmailSuffixChange}
                emailSuffixes={emailSuffixes}
            />

            {/* 密码 */}
            <div className="space-y-2">
                <label className="text-sm font-medium text-foreground-secondary">密码</label>
                <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-foreground-secondary" />
                    <input
                        type={showPassword ? 'text' : 'password'}
                        value={password}
                        onChange={(e) => onPasswordChange(e.target.value)}
                        placeholder="设置密码"
                        required
                        minLength={8}
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
                <PasswordStrengthIndicator password={password} />
            </div>

            {/* 确认密码 */}
            <div className="space-y-2">
                <label className="text-sm font-medium text-foreground-secondary">确认密码</label>
                <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-foreground-secondary" />
                    <input
                        type={showConfirmPassword ? 'text' : 'password'}
                        value={confirmPassword}
                        onChange={(e) => onConfirmPasswordChange(e.target.value)}
                        placeholder="再次输入密码"
                        required
                        minLength={8}
                        className={`w-full pl-10 pr-10 py-3 rounded-xl bg-background-secondary border focus:outline-none transition-colors ${confirmPassword && password !== confirmPassword
                            ? 'border-red-500 focus:border-red-500'
                            : 'border-border focus:border-accent'
                        }`}
                    />
                    <button
                        type="button"
                        onClick={onToggleShowConfirmPassword}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-foreground-secondary hover:text-foreground transition-colors"
                    >
                        {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                </div>
                {confirmPassword && password !== confirmPassword && (
                    <p className="text-xs text-red-500">两次输入的密码不一致</p>
                )}
            </div>

            {/* 验证码 */}
            <div className="space-y-3">
                <div className="flex items-center justify-between">
                    <label className="text-sm font-medium text-foreground-secondary">邮箱验证码</label>
                    <button
                        type="button"
                        onClick={onSendCode}
                        disabled={sendingCode || countdown > 0}
                        className="px-3 py-1.5 rounded-lg bg-accent/10 text-accent hover:bg-accent/20 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
                    >
                        {sendingCode ? (
                            <SoundWaveLoader variant="inline" />
                        ) : countdown > 0 ? (
                            `${countdown}s 后重发`
                        ) : (
                            '发送验证码'
                        )}
                    </button>
                </div>
                <VerificationCodeInput
                    value={verificationCode}
                    onChange={onVerificationCodeChange}
                    length={6}
                    disabled={loading}
                />
            </div>
        </>
    );
}

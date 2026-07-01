'use client';

import { useState, useEffect } from 'react';
import { Eye, EyeOff, Lock, Mail, RefreshCw } from 'lucide-react';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { sendOTP, verifyOTP } from '@/lib/auth';
import { supabase } from '@/lib/auth';
import { PasswordStrengthIndicator, validatePasswordStrength } from '@/components/auth/PasswordStrengthIndicator';
import { VerificationCodeInput } from '@/components/auth/VerificationCodeInput';

type PasswordChangeStep = 'idle' | 'send-code' | 'verify' | 'set-password';

export function PasswordSection({
    email,
}: {
    email: string;
}) {
    const [step, setStep] = useState<PasswordChangeStep>('idle');
    const [verificationCode, setVerificationCode] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [showNewPassword, setShowNewPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [countdown, setCountdown] = useState(0);

    // 倒计时效果
    useEffect(() => {
        if (countdown > 0) {
            const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
            return () => clearTimeout(timer);
        }
    }, [countdown]);

    // 重置状态
    const resetForm = () => {
        setStep('idle');
        setVerificationCode('');
        setNewPassword('');
        setConfirmPassword('');
        setShowNewPassword(false);
        setShowConfirmPassword(false);
        setError('');
        setSuccess('');
    };

    // 发送验证码
    const handleSendCode = async () => {
        if (!email) {
            setError('无法获取邮箱地址');
            return;
        }

        setError('');
        setLoading(true);

        try {
            const result = await sendOTP(email, 'recovery');
            if (result.success) {
                setCountdown(60);
                setStep('verify');
                setSuccess('验证码已发送到您的邮箱');
            } else {
                setError(result.error?.message || '发送失败');
            }
        } catch {
            setError('发送失败，请重试');
        } finally {
            setLoading(false);
        }
    };

    // 验证验证码
    const handleVerifyCode = async () => {
        if (!verificationCode || verificationCode.length !== 6) {
            setError('请输入完整的6位验证码');
            return;
        }

        setError('');
        setLoading(true);

        try {
            const result = await verifyOTP(email, verificationCode, 'recovery');
            if (result.success) {
                setStep('set-password');
                setSuccess('验证成功，请设置新密码');
            } else {
                setError(result.error?.message || '验证失败');
            }
        } catch {
            setError('验证失败，请重试');
        } finally {
            setLoading(false);
        }
    };

    // 重新发送验证码
    const handleResendCode = async () => {
        if (countdown > 0) return;
        await handleSendCode();
    };

    // 修改密码
    const handleChangePassword = async () => {
        const { isValid } = validatePasswordStrength(newPassword);
        if (!isValid) {
            setError('密码不符合强度要求');
            return;
        }

        if (newPassword !== confirmPassword) {
            setError('两次输入的密码不一致');
            return;
        }

        setError('');
        setLoading(true);

        try {
            const { error: updateError } = await supabase.auth.updateUser({
                password: newPassword
            });

            if (updateError) {
                setError('密码修改失败：' + updateError.message);
            } else {
                setSuccess('密码修改成功！');
                setTimeout(() => {
                    resetForm();
                    setSuccess('');
                }, 2000);
            }
        } catch {
            setError('密码修改失败，请重试');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-2">

            {/* 初始状态 - 显示修改密码按钮 */}
            {step === 'idle' && (
                <button
                    onClick={() => setStep('send-code')}
                    className="w-full px-4 py-3 rounded-xl bg-background-secondary border border-border text-left flex items-center gap-3 hover:border-accent transition-colors"
                >
                    <Lock className="w-5 h-5 text-foreground-secondary" />
                    <span>修改密码</span>
                </button>
            )}

            {/* 发送验证码步骤 */}
            {step === 'send-code' && (
                <div className="space-y-4 p-4 rounded-xl bg-background-secondary border border-border">
                    <p className="text-sm text-foreground-secondary">
                        为了安全，修改密码需要先验证您的身份
                    </p>

                    {/* 显示邮箱 */}
                    <div className="relative">
                        <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-foreground-secondary" />
                        <input
                            type="email"
                            value={email}
                            disabled
                            className="w-full pl-10 pr-4 py-3 rounded-lg bg-background border border-border text-foreground-secondary"
                        />
                    </div>

                    {error && (
                        <p className="text-sm text-red-500">{error}</p>
                    )}

                    <div className="flex gap-2">
                        <button
                            onClick={resetForm}
                            className="flex-1 py-2.5 rounded-lg border border-border hover:border-foreground-secondary transition-colors"
                        >
                            取消
                        </button>
                        <button
                            onClick={handleSendCode}
                            disabled={loading}
                            className="flex-1 py-2.5 rounded-lg bg-accent text-white font-medium hover:bg-accent/90 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                        >
                            {loading && <SoundWaveLoader variant="inline" />}
                            发送验证码
                        </button>
                    </div>
                </div>
            )}

            {/* 验证码验证步骤 */}
            {step === 'verify' && (
                <div className="space-y-4 p-4 rounded-xl bg-background-secondary border border-border">
                    <p className="text-sm text-foreground-secondary text-center">
                        验证码已发送至 <span className="font-medium text-foreground">{email}</span>
                    </p>

                    <VerificationCodeInput
                        value={verificationCode}
                        onChange={setVerificationCode}
                        onComplete={handleVerifyCode}
                        length={6}
                        disabled={loading}
                    />

                    {/* 重新发送 */}
                    <button
                        onClick={handleResendCode}
                        disabled={countdown > 0 || loading}
                        className="w-full flex items-center justify-center gap-2 text-sm text-accent hover:underline disabled:text-foreground-secondary disabled:no-underline disabled:cursor-not-allowed"
                    >
                        <RefreshCw className="w-4 h-4" />
                        {countdown > 0 ? `${countdown}秒后可重新发送` : '重新发送验证码'}
                    </button>

                    {success && (
                        <p className="text-sm text-green-500 text-center">{success}</p>
                    )}
                    {error && (
                        <p className="text-sm text-red-500 text-center">{error}</p>
                    )}

                    <div className="flex gap-2">
                        <button
                            onClick={resetForm}
                            className="flex-1 py-2.5 rounded-lg border border-border hover:border-foreground-secondary transition-colors"
                        >
                            取消
                        </button>
                        <button
                            onClick={handleVerifyCode}
                            disabled={loading || verificationCode.length !== 6}
                            className="flex-1 py-2.5 rounded-lg bg-accent text-white font-medium hover:bg-accent/90 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                        >
                            {loading && <SoundWaveLoader variant="inline" />}
                            验证
                        </button>
                    </div>
                </div>
            )}

            {/* 设置新密码步骤 */}
            {step === 'set-password' && (
                <div className="space-y-4 p-4 rounded-xl bg-background-secondary border border-border">
                    <p className="text-sm text-foreground-secondary">
                        身份验证成功，请设置新密码
                    </p>

                    {/* 新密码 */}
                    <div className="space-y-2">
                        <label className="text-xs text-foreground-secondary">新密码</label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-foreground-secondary" />
                            <input
                                type={showNewPassword ? 'text' : 'password'}
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                placeholder="设置新密码"
                                className="w-full pl-10 pr-10 py-3 rounded-lg bg-background border border-border focus:border-accent focus:outline-none transition-colors"
                            />
                            <button
                                type="button"
                                onClick={() => setShowNewPassword(!showNewPassword)}
                                className="absolute right-3 top-1/2 -translate-y-1/2 text-foreground-secondary hover:text-foreground transition-colors"
                            >
                                {showNewPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                            </button>
                        </div>
                        <PasswordStrengthIndicator password={newPassword} />
                    </div>

                    {/* 确认密码 */}
                    <div className="space-y-2">
                        <label className="text-xs text-foreground-secondary">确认新密码</label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-foreground-secondary" />
                            <input
                                type={showConfirmPassword ? 'text' : 'password'}
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                placeholder="再次输入新密码"
                                className={`w-full pl-10 pr-10 py-3 rounded-lg bg-background border focus:outline-none transition-colors ${confirmPassword && newPassword !== confirmPassword
                                    ? 'border-red-500 focus:border-red-500'
                                    : 'border-border focus:border-accent'
                                    }`}
                            />
                            <button
                                type="button"
                                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                                className="absolute right-3 top-1/2 -translate-y-1/2 text-foreground-secondary hover:text-foreground transition-colors"
                            >
                                {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                            </button>
                        </div>
                        {confirmPassword && newPassword !== confirmPassword && (
                            <p className="text-xs text-red-500">两次输入的密码不一致</p>
                        )}
                    </div>

                    {success && (
                        <p className="text-sm text-green-500 text-center">{success}</p>
                    )}
                    {error && (
                        <p className="text-sm text-red-500 text-center">{error}</p>
                    )}

                    <div className="flex gap-2">
                        <button
                            onClick={resetForm}
                            className="flex-1 py-2.5 rounded-lg border border-border hover:border-foreground-secondary transition-colors"
                        >
                            取消
                        </button>
                        <button
                            onClick={handleChangePassword}
                            disabled={loading || !newPassword || !confirmPassword}
                            className="flex-1 py-2.5 rounded-lg bg-accent text-white font-medium hover:bg-accent/90 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                        >
                            {loading && <SoundWaveLoader variant="inline" />}
                            确认修改
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

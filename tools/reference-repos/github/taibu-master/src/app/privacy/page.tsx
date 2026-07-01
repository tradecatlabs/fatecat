/**
 * 隐私政策页面
 *
 * 阐述太卜如何收集、使用、保护用户个人信息
 */
'use client';

import Link from 'next/link';
import { ArrowLeft, Shield, Eye, Lock, Database, Mail } from 'lucide-react';
import { getSettingsCenterRouteTarget } from '@/lib/settings-center';

export default function PrivacyPage() {
    return (
        <div className="min-h-screen bg-background">
            <div className="max-w-3xl mx-auto px-4 py-8 relative z-10 animate-fade-in">
                {/* 头部 */}
                <div className="hidden md:flex items-center gap-4 mb-10">
                    <Link
                        href={getSettingsCenterRouteTarget('help')}
                        className="p-2.5 rounded-xl bg-background-secondary/50 border border-border/50 hover:bg-background-secondary hover:shadow-md transition-all text-foreground-secondary hover:text-foreground backdrop-blur-sm"
                    >
                        <ArrowLeft className="w-5 h-5" />
                    </Link>
                    <div>
                        <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-foreground to-foreground/70">隐私政策</h1>
                        <p className="text-sm text-foreground-secondary mt-1">了解我们如何保护您的个人信息</p>
                    </div>
                </div>

                {/* 移动端头部 */}
                <div className="md:hidden mb-8">
                    <Link
                        href={getSettingsCenterRouteTarget('help')}
                        className="inline-flex items-center gap-2 text-sm text-foreground-secondary hover:text-foreground mb-4"
                    >
                        <ArrowLeft className="w-4 h-4" />
                        返回帮助中心
                    </Link>
                    <h1 className="text-2xl font-bold">隐私政策</h1>
                    <p className="text-sm text-foreground-secondary mt-1">了解我们如何保护您的个人信息</p>
                </div>

                {/* 内容区域 */}
                <div className="space-y-8">
                    {/* 简介 */}
                    <section className="bg-gradient-to-br from-background to-background-secondary/50 rounded-2xl border border-border/50 p-6 shadow-sm">
                        <div className="flex items-start gap-4">
                            <div className="p-3 rounded-xl bg-blue-500/10 text-blue-500">
                                <Shield className="w-6 h-6" />
                            </div>
                            <div>
                                <h2 className="text-lg font-bold mb-2">您的隐私对我们至关重要</h2>
                                <p className="text-sm text-foreground-secondary leading-relaxed">
                                    太卜（以下简称&quot;我们&quot;）非常重视用户的隐私保护。本隐私政策阐述了我们如何收集、使用、存储和保护您的个人信息。我们承诺按照相关法律法规的要求，为用户提供安全可靠的服务。
                                </p>
                            </div>
                        </div>
                    </section>

                    {/* 信息收集 */}
                    <section>
                        <h2 className="flex items-center gap-2 text-lg font-bold mb-4 ml-1">
                            <div className="p-1.5 rounded-lg bg-green-500/10 text-green-500">
                                <Database className="w-5 h-5" />
                            </div>
                            信息收集
                        </h2>
                        <div className="bg-background rounded-2xl border border-border/50 p-6 space-y-4">
                            <p className="text-sm text-foreground-secondary leading-relaxed">
                                我们可能会收集以下类型的个人信息：
                            </p>
                            <ul className="space-y-3 text-sm text-foreground-secondary">
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span><strong className="text-foreground">账户信息</strong>：包括邮箱地址、昵称、头像等注册信息</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span><strong className="text-foreground">出生信息</strong>：用于命理分析，包括出生日期、出生时间、出生地点等</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span><strong className="text-foreground">使用数据</strong>：包括使用记录、对话历史、查询历史等</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span><strong className="text-foreground">设备信息</strong>：包括设备类型、操作系统、浏览器类型等</span>
                                </li>
                            </ul>
                        </div>
                    </section>

                    {/* 信息使用 */}
                    <section>
                        <h2 className="flex items-center gap-2 text-lg font-bold mb-4 ml-1">
                            <div className="p-1.5 rounded-lg bg-purple-500/10 text-purple-500">
                                <Eye className="w-5 h-5" />
                            </div>
                            信息使用
                        </h2>
                        <div className="bg-background rounded-2xl border border-border/50 p-6 space-y-4">
                            <p className="text-sm text-foreground-secondary leading-relaxed">
                                我们收集的信息将用于以下目的：
                            </p>
                            <ul className="space-y-3 text-sm text-foreground-secondary">
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>提供、运营和维护我们的服务</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>生成个性化的命理分析报告和建议</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>改进我们的服务质量和用户体验</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>向您发送服务通知、更新信息和营销内容</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>处理您的账户安全和防止欺诈行为</span>
                                </li>
                            </ul>
                        </div>
                    </section>

                    {/* 信息保护 */}
                    <section>
                        <h2 className="flex items-center gap-2 text-lg font-bold mb-4 ml-1">
                            <div className="p-1.5 rounded-lg bg-red-500/10 text-red-500">
                                <Lock className="w-5 h-5" />
                            </div>
                            信息保护
                        </h2>
                        <div className="bg-background rounded-2xl border border-border/50 p-6 space-y-4">
                            <p className="text-sm text-foreground-secondary leading-relaxed">
                                我们采用多种安全措施来保护您的个人信息：
                            </p>
                            <ul className="space-y-3 text-sm text-foreground-secondary">
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>使用 SSL/TLS 加密技术保护数据传输</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>实施严格的访问控制和权限管理</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>定期进行安全审计和漏洞检测</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>存储用户敏感信息时使用加密处理</span>
                                </li>
                            </ul>
                        </div>
                    </section>

                    {/* 信息共享 */}
                    <section>
                        <h2 className="flex items-center gap-2 text-lg font-bold mb-4 ml-1">
                            <div className="p-1.5 rounded-lg bg-orange-500/10 text-orange-500">
                                <Mail className="w-5 h-5" />
                            </div>
                            信息共享
                        </h2>
                        <div className="bg-background rounded-2xl border border-border/50 p-6 space-y-4">
                            <p className="text-sm text-foreground-secondary leading-relaxed">
                                我们不会出售、交易或以其他方式转让您的个人信息给第三方，以下情况除外：
                            </p>
                            <ul className="space-y-3 text-sm text-foreground-secondary">
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>经您同意后，与服务提供商共享必要信息</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>遵守法律法规或政府机构的合法要求</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>保护我们或用户的权利、财产或安全</span>
                                </li>
                            </ul>
                        </div>
                    </section>

                    {/* 用户权利 */}
                    <section>
                        <h2 className="text-lg font-bold mb-4 ml-1">用户权利</h2>
                        <div className="bg-background rounded-2xl border border-border/50 p-6 space-y-4">
                            <p className="text-sm text-foreground-secondary leading-relaxed">
                                根据适用的数据保护法律，您享有以下权利：
                            </p>
                            <ul className="space-y-3 text-sm text-foreground-secondary">
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>访问您的个人信息和使用记录</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>更正不准确或不完整的个人信息</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>删除您的个人信息和账户</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>撤回您对信息处理的同意</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>导出您的个人数据</span>
                                </li>
                            </ul>
                        </div>
                    </section>

                    {/* 政策更新 */}
                    <section>
                        <h2 className="text-lg font-bold mb-4 ml-1">政策更新</h2>
                        <div className="bg-background rounded-2xl border border-border/50 p-6">
                            <p className="text-sm text-foreground-secondary leading-relaxed">
                                我们可能会不时更新本隐私政策。更新后的政策将在本页面上公布，并标明最新修订日期。我们鼓励您定期查阅本页面，以了解我们如何保护您的信息。如有重大变更，我们将通过电子邮件或网站公告的方式通知您。
                            </p>
                        </div>
                    </section>

                    {/* 联系我们 */}
                    <section>
                        <h2 className="text-lg font-bold mb-4 ml-1">联系我们</h2>
                        <div className="bg-gradient-to-br from-background to-background-secondary/50 rounded-2xl border border-border/50 p-6">
                            <p className="text-sm text-foreground-secondary leading-relaxed mb-4">
                                如果您对本隐私政策有任何疑问、意见或建议，欢迎随时联系我们。
                            </p>
                            <div className="flex items-center gap-3 px-5 py-3 rounded-xl bg-background border border-border/50 shadow-sm text-sm font-medium text-foreground">
                                <Mail className="w-4 h-4 text-accent" />
                                <span>support@mingai.fun</span>
                            </div>
                        </div>
                    </section>

                    {/* 生效日期 */}
                    <div className="text-center text-sm text-foreground-secondary pt-4">
                        <p>本隐私政策最后更新于 2026 年 2 月 13 日</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

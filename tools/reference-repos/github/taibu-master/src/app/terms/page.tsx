/**
 * 服务条款页面
 *
 * 阐述太卜服务的使用条款和条件
 */
'use client';

import Link from 'next/link';
import { ArrowLeft, FileText, Users, AlertCircle, CreditCard, Gavel } from 'lucide-react';
import { getSettingsCenterRouteTarget } from '@/lib/settings-center';

export default function TermsPage() {
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
                        <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-foreground to-foreground/70">服务条款</h1>
                        <p className="text-sm text-foreground-secondary mt-1">使用太卜服务前请仔细阅读</p>
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
                    <h1 className="text-2xl font-bold">服务条款</h1>
                    <p className="text-sm text-foreground-secondary mt-1">使用太卜服务前请仔细阅读</p>
                </div>

                {/* 内容区域 */}
                <div className="space-y-8">
                    {/* 简介 */}
                    <section className="bg-gradient-to-br from-background to-background-secondary/50 rounded-2xl border border-border/50 p-6 shadow-sm">
                        <div className="flex items-start gap-4">
                            <div className="p-3 rounded-xl bg-purple-500/10 text-purple-500">
                                <FileText className="w-6 h-6" />
                            </div>
                            <div>
                                <h2 className="text-lg font-bold mb-2">服务条款概述</h2>
                                <p className="text-sm text-foreground-secondary leading-relaxed">
                                    欢迎使用太卜（以下简称&quot;本服务&quot;）。本服务条款是您与太卜之间的法律协议，规定了使用本服务的条款和条件。在使用本服务前，请仔细阅读以下条款。您使用本服务即表示您同意接受本服务条款的约束。
                                </p>
                            </div>
                        </div>
                    </section>

                    {/* 服务说明 */}
                    <section>
                        <h2 className="flex items-center gap-2 text-lg font-bold mb-4 ml-1">
                            <div className="p-1.5 rounded-lg bg-blue-500/10 text-blue-500">
                                <FileText className="w-5 h-5" />
                            </div>
                            服务说明
                        </h2>
                        <div className="bg-background rounded-2xl border border-border/50 p-6 space-y-4">
                            <p className="text-sm text-foreground-secondary leading-relaxed">
                                太卜提供以下命理相关服务：
                            </p>
                            <ul className="space-y-3 text-sm text-foreground-secondary">
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>八字命理排盘与分析</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>紫微斗数命盘分析</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>塔罗占卜与六爻占卜</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>AI 智能对话与命理咨询</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>每日/每月运势预测</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>面相、手相分析</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>MBTI 人格测试与分析</span>
                                </li>
                            </ul>
                            <p className="text-sm text-foreground-secondary leading-relaxed pt-2">
                                我们保留随时修改、暂停或终止任何服务的权利，并将通过适当的方式通知用户。
                            </p>
                        </div>
                    </section>

                    {/* 用户资格 */}
                    <section>
                        <h2 className="flex items-center gap-2 text-lg font-bold mb-4 ml-1">
                            <div className="p-1.5 rounded-lg bg-green-500/10 text-green-500">
                                <Users className="w-5 h-5" />
                            </div>
                            用户资格
                        </h2>
                        <div className="bg-background rounded-2xl border border-border/50 p-6 space-y-4">
                            <p className="text-sm text-foreground-secondary leading-relaxed">
                                使用本服务，您必须：
                            </p>
                            <ul className="space-y-3 text-sm text-foreground-secondary">
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>年满 18 周岁，或已获得监护人的同意</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>具有签订法律协议的完全行为能力</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>同意本服务条款和隐私政策</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>提供真实、准确的注册信息</span>
                                </li>
                            </ul>
                        </div>
                    </section>

                    {/* 用户义务 */}
                    <section>
                        <h2 className="flex items-center gap-2 text-lg font-bold mb-4 ml-1">
                            <div className="p-1.5 rounded-lg bg-red-500/10 text-red-500">
                                <AlertCircle className="w-5 h-5" />
                            </div>
                            用户义务
                        </h2>
                        <div className="bg-background rounded-2xl border border-border/50 p-6 space-y-4">
                            <p className="text-sm text-foreground-secondary leading-relaxed">
                                您在使用本服务时，不得：
                            </p>
                            <ul className="space-y-3 text-sm text-foreground-secondary">
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>违反任何适用的法律法规</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>侵犯他人知识产权、隐私权或其他合法权益</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>上传或传播病毒、木马或其他恶意代码</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>试图未经授权访问本服务或相关系统</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>进行任何可能损害、干扰本服务正常运作的行为</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>将本服务用于任何商业目的（除非获得明确授权）</span>
                                </li>
                            </ul>
                        </div>
                    </section>

                    {/* 免责声明 */}
                    <section>
                        <h2 className="flex items-center gap-2 text-lg font-bold mb-4 ml-1">
                            <div className="p-1.5 rounded-lg bg-orange-500/10 text-orange-500">
                                <Gavel className="w-5 h-5" />
                            </div>
                            免责声明
                        </h2>
                        <div className="bg-background rounded-2xl border border-border/50 p-6 space-y-4">
                            <p className="text-sm text-foreground-secondary leading-relaxed">
                                本服务按&quot;现状&quot;提供，我们不做任何明示或暗示的保证：
                            </p>
                            <ul className="space-y-3 text-sm text-foreground-secondary">
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>本服务的内容、分析和建议仅供参考，不构成任何决策依据</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>命理分析结果仅供参考，不能替代专业的人生建议</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>我们不保证服务完全不中断或无错误</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 flex-shrink-0" />
                                    <span>对于因使用本服务造成的任何直接或间接损失，我们不承担责任</span>
                                </li>
                            </ul>
                            <p className="text-sm text-foreground-secondary leading-relaxed pt-2">
                                用户应理性看待命理分析结果，将其作为参考而非决策的唯一依据。
                            </p>
                        </div>
                    </section>

                    {/* 知识产权 */}
                    <section>
                        <h2 className="text-lg font-bold mb-4 ml-1">知识产权</h2>
                        <div className="bg-background rounded-2xl border border-border/50 p-6">
                            <p className="text-sm text-foreground-secondary leading-relaxed">
                                本服务及其内容（包括但不限于文字、图片、图标、设计、代码）的知识产权归太卜所有或已获得合法授权。未经我们书面许可，您不得复制、修改、传播、公开展示或使用本服务的任何内容。我们尊重他人的知识产权，如果您认为您的作品被侵权，请联系我们进行处理。
                            </p>
                        </div>
                    </section>

                    {/* 终止服务 */}
                    <section>
                        <h2 className="text-lg font-bold mb-4 ml-1">终止服务</h2>
                        <div className="bg-background rounded-2xl border border-border/50 p-6">
                            <p className="text-sm text-foreground-secondary leading-relaxed">
                                我们保留在任何时候终止或暂停您对本服务的访问权限的权利，无需事先通知。如果您违反本服务条款，我们可能会立即终止您的账户。对于已付费的会员服务，终止后我们不会退还剩余费用。您也可以随时通过账户设置删除您的账户。
                            </p>
                        </div>
                    </section>

                    {/* 条款更新 */}
                    <section>
                        <h2 className="text-lg font-bold mb-4 ml-1">条款更新</h2>
                        <div className="bg-background rounded-2xl border border-border/50 p-6">
                            <p className="text-sm text-foreground-secondary leading-relaxed">
                                我们可能会不时更新本服务条款。更新后的条款将在本页面上公布，并标明最新修订日期。我们鼓励您定期查阅本页面，以了解最新的服务条款。如有重大变更，我们将通过电子邮件或网站公告的方式通知您。继续使用本服务即表示您接受更新后的条款。
                            </p>
                        </div>
                    </section>

                    {/* 联系我们 */}
                    <section>
                        <h2 className="text-lg font-bold mb-4 ml-1">联系我们</h2>
                        <div className="bg-gradient-to-br from-background to-background-secondary/50 rounded-2xl border border-border/50 p-6">
                            <p className="text-sm text-foreground-secondary leading-relaxed mb-4">
                                如果您对本服务条款有任何疑问，欢迎随时联系我们。
                            </p>
                            <div className="flex items-center gap-3 px-5 py-3 rounded-xl bg-background border border-border/50 shadow-sm text-sm font-medium text-foreground">
                                <CreditCard className="w-4 h-4 text-accent" />
                                <span>support@mingai.fun</span>
                            </div>
                        </div>
                    </section>

                    {/* 生效日期 */}
                    <div className="text-center text-sm text-foreground-secondary pt-4">
                        <p>本服务条款最后更新于 2026 年 2 月 13 日</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

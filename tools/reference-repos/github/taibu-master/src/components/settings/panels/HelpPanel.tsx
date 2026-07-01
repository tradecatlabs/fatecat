'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ChevronDown, Github, Mail } from 'lucide-react';

interface FAQItem {
  question: string;
  answer: string;
}

const FAQ_LIST: FAQItem[] = [
  {
    question: 'AI 服务是否免费？',
    answer: 'AI 服务目前基于公益站提供，用户可以免费使用，但会存在次数限制或模型不可访问等情况。如果公益站关闭，AI 服务可能会受到影响，我们会尽力寻找替代方案。',
  },
  {
    question: 'AI 对话次数有多少？',
    answer: '每日 10 次对话次数，可在订阅中每天签到获取。后续会根据使用情况和反馈继续调整。',
  },
  {
    question: 'AI 分析结果为什么有时不够准确？',
    answer: 'AI 分析基于大量数据和算法，但仍可能存在误差。建议结合自身情况和专业命理师建议综合参考。',
  },
  {
    question: '为什么我的日运/月运功能缺少了？',
    answer: '如果没有设置默认命盘，日运/月运将无法使用个性化命盘分析。请先在“我的命盘”中设置默认命盘。',
  },
  {
    question: '为什么真太阳时和出生时间不一致？',
    answer: '真太阳时会根据出生地经度进行校正，因此可能与填写的出生时间不同。真太阳时计算依赖高德地图 API，额度不足时也可能出现误差。',
  },
  {
    question: '紫微斗数和八字有什么区别？',
    answer: '八字命理基于天干地支推算命运，侧重五行生克；紫微斗数则以紫微星系与十二宫位分析人生不同领域。两者各有特色，可互相参照。',
  },
];

export default function HelpPanel() {
  const [expandedFAQ, setExpandedFAQ] = useState<number | null>(null);
  const projectRepoUrl = 'https://github.com/hhszzzz/taibu';

  return (
    <div className="space-y-8">
      <section className="space-y-3">
        <h2 className="px-1 text-xs font-semibold uppercase tracking-wider text-foreground/50">常见问题</h2>
        <div className="overflow-hidden rounded-md border border-border bg-background divide-y divide-border/60">
          {FAQ_LIST.map((faq, index) => {
            const expanded = expandedFAQ === index;
            return (
              <div key={faq.question}>
                <button
                  type="button"
                  onClick={() => setExpandedFAQ(expanded ? null : index)}
                  className="flex w-full items-center gap-3 px-4 py-4 text-left transition-colors duration-150 hover:bg-[#efedea] dark:hover:bg-background-secondary"
                >
                  <ChevronDown className={`h-4 w-4 text-foreground/30 transition-transform duration-150 ${expanded ? 'rotate-0' : '-rotate-90'}`} />
                  <span className={`text-sm font-medium ${expanded ? 'text-accent' : 'text-foreground'}`}>
                    {faq.question}
                  </span>
                </button>

                <div className={`${expanded ? 'block' : 'hidden'} px-11 pb-4 text-sm leading-relaxed text-foreground-secondary`}>
                  {faq.answer}
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <section className="space-y-3">
        <h2 className="px-1 text-xs font-semibold uppercase tracking-wider text-foreground/50">联系我们</h2>
        <div className="flex flex-col items-start justify-between gap-4 rounded-md border border-border bg-background p-4">
          <div className="space-y-1">
            <h3 className="text-sm font-medium text-foreground">需要更多帮助？</h3>
            <p className="text-sm text-foreground-secondary">如果你没有找到需要的答案，可以通过邮件或 GitHub 仓库联系我们。</p>
          </div>
          <div className="flex w-full flex-col gap-3 sm:flex-row">
            <div className="inline-flex items-center gap-2 rounded-md border border-border bg-background-secondary px-3 py-2 text-sm text-foreground">
              <Mail className="h-4 w-4 text-accent" />
              <span>support@mingai.fun</span>
            </div>
            <a
              href={projectRepoUrl}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 rounded-md border border-border bg-background-secondary px-3 py-2 text-sm text-foreground transition-colors hover:bg-background-secondary/70"
            >
              <Github className="h-4 w-4 text-accent" />
              <span>github.com/hhszzzz/taibu</span>
            </a>
          </div>
        </div>
      </section>

      <footer className="border-t border-border/60 pt-4">
        <div className="flex items-center justify-center gap-6 text-xs text-foreground/40">
          <Link href="/privacy" className="hover:text-foreground hover:underline underline-offset-4">隐私政策</Link>
          <span className="h-1 w-1 rounded-full bg-background-secondary" />
          <Link href="/terms" className="hover:text-foreground hover:underline underline-offset-4">服务条款</Link>
        </div>
      </footer>
    </div>
  );
}

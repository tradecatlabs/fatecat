/**
 * 用户 MCP 服务页面
 *
 * 需要 useState + 浏览器 clipboard API
 */
'use client';

import { useState } from 'react';
import { AlertTriangle, Check, Copy, LockKeyhole } from 'lucide-react';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { useSessionSafe } from '@/components/providers/ClientProviders';
import { SettingsLoginRequired } from '@/components/settings/SettingsLoginRequired';
import { useFeatureToggles } from '@/lib/hooks/useFeatureToggles';
import {
  MCP_OAUTH_URL,
  MCP_PUBLIC_TOOLS,
  buildMcpOAuthConfig,
  buildMcpStdioNpxConfig,
} from '@/lib/mcp-service-config';

type McpConnectionMode = 'stdio' | 'oauth';

const STDIO_REQUIREMENTS = [
  '本机已安装 Node.js',
  '客户端支持 MCP stdio 连接方式',
];

function CodeBlock({
  title,
  description,
  snippet,
  snippetId,
  copiedSnippet,
  onCopy,
}: {
  title: string;
  description?: string;
  snippet: string;
  snippetId: string;
  copiedSnippet: string | null;
  onCopy: (snippetId: string, content: string) => Promise<void>;
}) {
  return (
    <div className="space-y-2">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-sm font-medium text-foreground">{title}</div>
          {description ? <p className="mt-1 text-xs text-foreground-secondary">{description}</p> : null}
        </div>
        <button
          type="button"
          onClick={() => onCopy(snippetId, snippet)}
          className="inline-flex items-center gap-1 rounded-lg border border-border px-2 py-1 text-xs hover:bg-background-secondary"
        >
          {copiedSnippet === snippetId ? <Check className="h-3 w-3 text-green-500" /> : <Copy className="h-3 w-3" />}
          复制
        </button>
      </div>
      <pre className="overflow-x-auto rounded-xl bg-background-secondary p-3 text-xs leading-6">{snippet}</pre>
    </div>
  );
}

export default function McpServicePanel() {
  const { user, loading: sessionLoading } = useSessionSafe();
  const { loaded: featureLoaded, isFeatureEnabled } = useFeatureToggles();
  const [mode, setMode] = useState<McpConnectionMode>('stdio');
  const [copiedSnippet, setCopiedSnippet] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const oauthEnabled = !featureLoaded || isFeatureEnabled('mcp-service');
  const resolvedMode: McpConnectionMode = !oauthEnabled && mode === 'oauth' ? 'stdio' : mode;
  const oauthTabClassName = resolvedMode === 'oauth'
    ? (
      oauthEnabled
        ? 'border-accent bg-accent/10 text-accent'
        : 'border-border bg-background-secondary/70 text-foreground/45 dark:text-foreground/50'
    )
    : (
      oauthEnabled
        ? 'border-border hover:bg-background-secondary'
        : 'border-border bg-background-secondary/70 text-foreground/45 dark:text-foreground/50'
    );

  const handleCopySnippet = async (snippetId: string, content: string) => {
    try {
      await navigator.clipboard.writeText(content);
      setError(null);
      setCopiedSnippet(snippetId);
      window.setTimeout(() => {
        setCopiedSnippet((current) => (current === snippetId ? null : current));
      }, 2000);
    } catch {
      setError('复制失败，请手动复制。');
    }
  };

  if (sessionLoading) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-8">
        <SoundWaveLoader variant="block" />
      </div>
    );
  }

  if (!user) {
    return <SettingsLoginRequired title="请先登录后使用 MCP 服务" />;
  }

  return (
    <div className="mx-auto max-w-4xl animate-fade-in">
      {error ? (
        <div className="mb-4 flex items-center gap-2 rounded-xl bg-red-500/10 p-3 text-sm text-red-500">
          <AlertTriangle className="h-4 w-4 flex-shrink-0" />
          {error}
        </div>
      ) : null}

      <div className="mb-4 rounded-2xl bg-background">
        <div className="mb-3 flex items-center gap-2">
          <h2 className="font-semibold text-foreground">可用工具</h2>
          <span className="rounded-full bg-background-secondary px-2 py-0.5 text-xs text-foreground-secondary">
            {MCP_PUBLIC_TOOLS.length} 个
          </span>
        </div>
        <div className="overflow-hidden rounded-xl border border-border">
          <table className="w-full text-sm">
            <thead className="bg-background-secondary/50 text-left text-foreground-secondary">
              <tr className="border-b border-border">
                <th className="px-4 py-3 font-medium">工具</th>
                <th className="px-4 py-3 font-medium">说明</th>
              </tr>
            </thead>
            <tbody>
              {MCP_PUBLIC_TOOLS.map((tool, index) => (
                <tr
                  key={tool.id}
                  className={index === MCP_PUBLIC_TOOLS.length - 1 ? '' : 'border-b border-border/70'}
                >
                  <td className="px-4 py-3 align-top">
                    <code className="rounded bg-background-secondary px-1.5 py-0.5 text-xs">{tool.id}</code>
                  </td>
                  <td className="px-4 py-3 text-foreground-secondary">{tool.label}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="mb-4 rounded-2xl border border-border bg-background p-5">
        <div className="mb-4 flex gap-2">
          <button
            type="button"
            onClick={() => setMode('stdio')}
            className={`flex-1 rounded-lg border px-4 py-2 text-sm font-medium transition-colors ${
              resolvedMode === 'stdio'
                ? 'border-accent bg-accent/10 text-accent'
                : 'border-border hover:bg-background-secondary'
            }`}
          >
            Stdio 本地接入
          </button>
          <button
            type="button"
            onClick={() => setMode('oauth')}
            disabled={!oauthEnabled}
            className={`flex-1 rounded-lg border px-4 py-2 text-sm font-medium transition-colors disabled:cursor-not-allowed ${oauthTabClassName}`}
          >
            <span className="flex items-center justify-center gap-2">
              {!oauthEnabled ? <LockKeyhole className="h-4 w-4" /> : null}
              <span>OAuth 远程接入</span>
            </span>
          </button>
        </div>

        {resolvedMode === 'stdio' ? (
          <div className="space-y-5">
            <div className="space-y-3">
              <h2 className="font-semibold text-foreground">快速开始</h2>
              <p className="text-sm text-foreground-secondary">在 MCP 客户端配置中加入：</p>
              <CodeBlock
                title="客户端配置"
                snippet={buildMcpStdioNpxConfig()}
                snippetId="stdio-npx"
                copiedSnippet={copiedSnippet}
                onCopy={handleCopySnippet}
              />
            </div>

            <div className="space-y-2 text-sm text-foreground-secondary">
              <p>要求：</p>
              <ul className="space-y-2">
                {STDIO_REQUIREMENTS.map((item) => (
                  <li key={item} className="flex items-start gap-2">
                    <span className="mt-1 h-1.5 w-1.5 rounded-full bg-accent" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between rounded-xl border border-border bg-background-secondary/30 p-4">
              <div>
                <div className="text-sm font-medium text-foreground">OAuth 远程接入</div>
              </div>
              <span className={`rounded-full px-3 py-1 text-xs font-medium ${
                oauthEnabled
                  ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400'
                  : 'bg-background-secondary text-foreground-secondary'
              }`}>
                {oauthEnabled ? '已启用' : '已禁用'}
              </span>
            </div>

            {oauthEnabled ? (
              <>
                <div className="rounded-xl border border-border bg-background-secondary/30 p-4 text-sm text-foreground-secondary">
                  <div className="flex flex-wrap items-center gap-2">
                    <span>远程入口：</span>
                    <code className="rounded bg-background px-1.5 py-0.5">{MCP_OAUTH_URL}</code>
                  </div>
                  <p className="mt-2">常见 type 可写为 <code className="rounded bg-background px-1 py-0.5">streamable-http</code>。</p>
                </div>

                <CodeBlock
                  title="远程客户端配置"
                  description="如果你的客户端支持远程 MCP，可使用这段最小配置。"
                  snippet={buildMcpOAuthConfig()}
                  snippetId="oauth-config"
                  copiedSnippet={copiedSnippet}
                  onCopy={handleCopySnippet}
                />
              </>
            ) : (
              <div className="rounded-xl border border-border bg-background-secondary/40 p-4 text-sm text-foreground-secondary">
                管理员当前已关闭 OAuth 接入；如需使用太卜 MCP，请切换到上方的 Stdio 本地接入方式。
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

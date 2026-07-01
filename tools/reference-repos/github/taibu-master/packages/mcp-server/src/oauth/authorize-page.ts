/**
 * MCP OAuth 授权页面 HTML 模板
 */

import { listToolDefinitions } from 'taibu-core/mcp';

// 工具名到中文显示名的映射
const TOOL_DISPLAY_NAMES: Record<string, string> = {
  astrology: '西方占星',
  bazi: '八字排盘',
  bazi_pillars_resolve: '四柱反推',
  bazi_dayun: '大运计算',
  ziwei: '紫微斗数',
  ziwei_horoscope: '紫微运限',
  ziwei_flying_star: '紫微飞星',
  liuyao: '六爻分析',
  meihua: '梅花易数',
  tarot: '塔罗占卜',
  taiyi: '太乙九星观测',
  almanac: '每日运势',
  qimen: '奇门遁甲',
  daliuren: '大六壬',
  xiaoliuren: '小六壬',
};

function getToolChips(): { count: number; html: string } {
  const chips = listToolDefinitions().map((tool) => {
    const name = tool.name;
    const label = TOOL_DISPLAY_NAMES[name] || name;
    return `<span class="tool-chip"><span class="tool-dot"></span>${escapeHtml(label)}</span>`;
  });
  return { count: chips.length, html: chips.join('\n        ') };
}

export function renderAuthorizePage(params: {
  clientName?: string;
  scopes: string[];
  error?: string;
  // 隐藏字段（回传给 POST /oauth/login）
  clientId: string;
  redirectUri: string;
  codeChallenge: string;
  codeChallengeMethod: string;
  state?: string;
  scope?: string;
  resource?: string;
}): string {
  const displayName = params.clientName || params.clientId;

  const errorBlock = params.error
    ? `<div class="error"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="7" stroke="#dc2626" stroke-width="1.5"/><path d="M8 4.5v4M8 10.5v.5" stroke="#dc2626" stroke-width="1.5" stroke-linecap="round"/></svg><span>${escapeHtml(params.error)}</span></div>`
    : '';

  const siteUrl = process.env.TAIBU_SITE_URL || 'https://www.mingai.fun';
  const logoUrl = `${siteUrl}/Logo.svg`;
  const tools = getToolChips();

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>授权登录 - 太卜</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;700&family=Noto+Sans+SC:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    *{margin:0;padding:0;box-sizing:border-box}

    body{
      font-family:"Noto Sans SC","PingFang SC","Helvetica Neue",sans-serif;
      background:#f8f6f1;
      color:#1a1a1a;
      min-height:100vh;
      display:flex;flex-direction:column;align-items:center;justify-content:center;
      padding:2rem 1rem;
      position:relative;overflow:hidden;
    }

    /* ── 背景装饰 ── */
    body::before{
      content:"";position:fixed;inset:0;pointer-events:none;
      background:
        radial-gradient(ellipse 80% 60% at 30% -10%,rgba(212,175,55,.07),transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 110%,rgba(212,175,55,.05),transparent 50%);
    }
    .bg-ornament{
      position:fixed;pointer-events:none;opacity:.04;
      font-size:18rem;color:#D4AF37;
      font-family:"Noto Serif SC",serif;font-weight:700;
      line-height:1;user-select:none;
    }
    .bg-ornament.tl{top:-2rem;left:-2rem}
    .bg-ornament.br{bottom:-3rem;right:-1rem}

    /* ── 页面容器 ── */
    .page{
      width:100%;max-width:400px;
      position:relative;z-index:1;
    }

    /* ── Logo + 品牌 ── */
    .brand{text-align:center;margin-bottom:1.75rem}
    .brand-logo{
      width:52px;height:52px;border-radius:14px;
      object-fit:contain;
      filter:drop-shadow(0 2px 8px rgba(212,175,55,.15));
    }
    .brand-name{
      font-family:"Noto Serif SC",serif;
      font-size:1.2rem;font-weight:700;
      color:#2a2a2a;margin-top:.625rem;
      letter-spacing:.05em;
    }
    .brand-name span{color:#D4AF37}

    /* ── 客户端请求条 ── */
    .client-bar{
      display:flex;align-items:center;gap:.5rem;
      background:rgba(212,175,55,.06);
      border:1px solid rgba(212,175,55,.15);
      border-radius:.625rem;
      padding:.5rem .75rem;margin-bottom:.875rem;
    }
    .client-icon{
      width:24px;height:24px;border-radius:6px;flex-shrink:0;
      background:linear-gradient(135deg,#D4AF37 0%,#c9a22e 100%);
      display:flex;align-items:center;justify-content:center;
    }
    .client-icon svg{width:14px;height:14px}
    .client-text{font-size:.78rem;color:#666;line-height:1.35}
    .client-name{color:#1a1a1a;font-weight:500}

    /* ── 登录卡片 ── */
    .card{
      background:#fff;
      border:1px solid rgba(0,0,0,.06);
      border-radius:1rem;
      padding:1.75rem;
      box-shadow:
        0 1px 2px rgba(0,0,0,.04),
        0 4px 16px rgba(0,0,0,.04),
        0 12px 40px rgba(212,175,55,.04);
      position:relative;
    }
    .card::before{
      content:"";position:absolute;top:-1px;left:2rem;right:2rem;height:2px;
      background:linear-gradient(90deg,transparent,#D4AF37,transparent);
      border-radius:1px;
    }

    .card-title{
      font-size:.95rem;font-weight:500;color:#1a1a1a;
      text-align:center;margin-bottom:1.25rem;
    }

    /* ── Error ── */
    .error{
      display:flex;align-items:center;gap:.5rem;
      background:#fef2f2;border:1px solid #fecaca;
      border-radius:.5rem;padding:.5rem .75rem;margin-bottom:1rem;
      color:#b91c1c;font-size:.8rem;
    }
    .error svg{flex-shrink:0}

    /* ── Form ── */
    .field{margin-bottom:.875rem}
    .field-label{
      display:block;font-size:.75rem;font-weight:400;
      color:#888;margin-bottom:.3rem;
    }
    .field-input{
      width:100%;padding:.625rem .75rem;
      border:1px solid #e5e5e5;border-radius:.5rem;
      background:#fafaf9;color:#1a1a1a;
      font-size:.85rem;font-family:inherit;outline:none;
      transition:border-color .2s,box-shadow .2s;
    }
    .field-input:focus{
      border-color:#D4AF37;
      box-shadow:0 0 0 3px rgba(212,175,55,.1);
      background:#fff;
    }
    .field-input::placeholder{color:#bbb}

    .actions{display:flex;gap:.625rem;margin-top:1.25rem}
    .btn{
      flex:1;padding:.65rem;border-radius:.5rem;border:none;
      font-size:.85rem;font-weight:500;font-family:inherit;
      cursor:pointer;transition:all .2s;
    }
    .btn-primary{
      background:linear-gradient(135deg,#D4AF37 0%,#c19b2a 100%);
      color:#fff;
      box-shadow:0 2px 8px rgba(212,175,55,.25);
    }
    .btn-primary:hover{
      box-shadow:0 4px 14px rgba(212,175,55,.35);
      transform:translateY(-1px);
    }
    .btn-secondary{
      background:#f5f5f4;color:#888;border:1px solid #e5e5e5;
    }
    .btn-secondary:hover{background:#ececea;color:#666}

    /* ── 分隔线 ── */
    .divider{
      display:flex;align-items:center;gap:.75rem;
      margin:1.5rem 0 1.125rem;color:#ccc;font-size:.7rem;
    }
    .divider::before,.divider::after{
      content:"";flex:1;height:1px;background:#e8e8e5;
    }

    /* ── 工具展示 ── */
    .tools{
      margin-top:1.5rem;
      background:#fff;
      border:1px solid rgba(0,0,0,.05);
      border-radius:.875rem;
      padding:1rem 1.125rem;
      box-shadow:0 1px 4px rgba(0,0,0,.02);
    }
    .tools-header{
      display:flex;align-items:center;justify-content:space-between;
      margin-bottom:.75rem;
    }
    .tools-title{font-size:.75rem;font-weight:500;color:#999;letter-spacing:.04em}
    .tools-badge{
      font-size:.6rem;color:#D4AF37;
      background:rgba(212,175,55,.08);
      padding:.15rem .45rem;border-radius:3px;
      font-weight:500;
    }
    .tools-list{display:flex;flex-wrap:wrap;gap:.375rem}
    .tool-chip{
      display:inline-flex;align-items:center;gap:.3rem;
      padding:.3rem .6rem;border-radius:2rem;
      background:#fafaf9;border:1px solid #eee;
      font-size:.7rem;color:#555;
      transition:all .2s;
    }
    .tool-chip:hover{
      border-color:rgba(212,175,55,.3);
      background:rgba(212,175,55,.04);
      color:#8b7320;
    }
    .tool-dot{
      width:5px;height:5px;border-radius:50%;
      background:#D4AF37;opacity:.6;
    }

    /* ── Footer ── */
    .footer{
      text-align:center;margin-top:1.25rem;
      font-size:.75rem;color:#aaa;line-height:1.8;
    }
    .footer a{
      color:#b8962e;text-decoration:none;
      border-bottom:1px solid transparent;
      transition:border-color .2s;
    }
    .footer a:hover{border-bottom-color:#b8962e}
    .sep{margin:0 .35rem;opacity:.35}

    /* ── Responsive ── */
    @media(max-width:420px){
      .card{padding:1.25rem}
      .tools{padding:.75rem}
      .tools-list{gap:.25rem}
    }
  </style>
</head>
<body>
  <div class="bg-ornament tl">命</div>
  <div class="bg-ornament br">理</div>

  <div class="page">
    <div class="brand">
      <img class="brand-logo" src="${escapeAttr(logoUrl)}" alt="太卜" onerror="this.style.display='none'" />
      <div class="brand-name"><span>太</span>卜 MCP</div>
    </div>

    <div class="client-bar">
      <div class="client-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
      </div>
      <div class="client-text">
        <span class="client-name">${escapeHtml(displayName)}</span> 请求访问你的太卜账户
      </div>
    </div>

    <div class="card">
      <div class="card-title">登录以授权访问</div>

      ${errorBlock}

      <form method="POST" action="/oauth/login">
        <input type="hidden" name="client_id" value="${escapeAttr(params.clientId)}" />
        <input type="hidden" name="redirect_uri" value="${escapeAttr(params.redirectUri)}" />
        <input type="hidden" name="code_challenge" value="${escapeAttr(params.codeChallenge)}" />
        <input type="hidden" name="code_challenge_method" value="${escapeAttr(params.codeChallengeMethod)}" />
        ${params.state ? `<input type="hidden" name="state" value="${escapeAttr(params.state)}" />` : ''}
        ${params.scope ? `<input type="hidden" name="scope" value="${escapeAttr(params.scope)}" />` : ''}
        ${params.resource ? `<input type="hidden" name="resource" value="${escapeAttr(params.resource)}" />` : ''}

        <div class="field">
          <label class="field-label" for="email">邮箱地址</label>
          <input class="field-input" type="email" id="email" name="email" required autocomplete="email" placeholder="you@example.com" />
        </div>

        <div class="field">
          <label class="field-label" for="password">密码</label>
          <input class="field-input" type="password" id="password" name="password" required autocomplete="current-password" placeholder="输入密码" />
        </div>

        <div class="actions">
          <button type="button" class="btn btn-secondary" onclick="window.close()">取消</button>
          <button type="submit" class="btn btn-primary">授权登录</button>
        </div>
      </form>
    </div>

    <div class="tools">
      <div class="tools-header">
        <span class="tools-title">授权后可使用的命理工具</span>
        <span class="tools-badge">${tools.count} 项</span>
      </div>
      <div class="tools-list">
        ${tools.html}
      </div>
    </div>

    <div class="footer">
      还没有账号？<a href="${escapeAttr(siteUrl)}" target="_blank" rel="noopener">前往注册</a>
      <span class="sep">·</span>
      <a href="${escapeAttr(siteUrl)}" target="_blank" rel="noopener">了解更多</a>
    </div>
  </div>
</body>
</html>`;
}

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function escapeAttr(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

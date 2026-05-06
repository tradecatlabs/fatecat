"""
用户报告生成器 - 生成Markdown格式的命理排盘报告
依赖: bazi_calculator.py 的计算结果
"""

import re
from datetime import datetime
from typing import Any

from branding import build_brand_footer_text, build_disclaimer_text, load_branding
from prediction_systems import REPORT_SYSTEM_LABELS, report_system_allowed_text


def public_birth_place(value: str | None) -> str:
    """返回可展示的出生地区。

    用户前端只允许展示北京类地区；其他真实地区名只参与经纬度解析和后端记录。
    """
    text = (value or "").strip()
    if not text:
        return ""
    if "北京" in text:
        return text
    return "已填写（非北京地区已隐藏）"


def _normalize_present_text(text: str) -> str:
    """统一清理“呈现层”文案中的提示词。

    说明：
    - 仅影响 TXT 呈现，不影响计算与字段完整性。
    - 用户要求：不显示“（展开）”等提示词。
    """
    if not text:
        return text
    return (
        text.replace("（依据，展开）", "（依据）")
        .replace("（全展开）", "")
        .replace("（全量）", "")
        .replace("（展开）", "")
    )


def _tbl_escape(v: object) -> str:
    s = "" if v is None else str(v)
    # Markdown 表格分隔符保护
    return s.replace("|", "｜")


def _render_table(headers: list[str], rows: list[list[object]]) -> list[str]:
    """渲染 Markdown 表格（不减少信息，只压缩呈现）。"""
    if not headers:
        return []
    out: list[str] = []
    out.append("| " + " | ".join(_tbl_escape(h) for h in headers) + " |")
    out.append("| " + " | ".join([":--"] * len(headers)) + " |")
    for r in rows:
        cells = r if isinstance(r, list) else [r]
        cells = list(cells) + [""] * (len(headers) - len(cells))
        out.append("| " + " | ".join(_tbl_escape(c) for c in cells[: len(headers)]) + " |")
    out.append("")
    return out


def _compact_inline_text(s: str) -> str:
    """将多行文本压成单行，便于表格呈现（不丢信息，仅改变换行）。"""
    if not s:
        return ""
    return " ".join(x.strip() for x in str(s).splitlines() if x.strip())


# 默认综合八字不计算紫微/天文等扩展；独立体系按 report_system 打开所需计算。
DEFAULT_HIDE: dict[str, bool] = {
    "extensions": True,
    "huangli": True,
    "zeri": True,
    "divination": True,
    "fengshui": True,
    "astro": True,
    "calendar": True,
    "number_divination": True,
    "yijing": True,
    "name_marriage": True,
    "system": True,
    "health": True,
}


def generate_report(result: dict[str, Any], hide: dict[str, bool] | None = None) -> str:
    """生成Markdown格式报告（主干部分）。

    注意：hide 仅影响 TXT 呈现，不影响上游计算与数据完整性。
    """
    lines = []
    hide = hide or {}
    inp = result.get("input", {})
    name = inp.get("name", "命主")
    hide_non_bazi_basic = hide.get("non_bazi_basic", False)

    lines.append(f"# 命理排盘报告：{name or '命主'}")
    lines.append("")
    lines.append("## 第一卷：先天命格（静态分析）")
    lines.append("")

    # 基本信息
    lines.append("## 基本资料（含真太阳时、节气）")
    lines.append("")
    bi = result.get("birthInfo", {})
    meta = result.get("meta", {})
    jq = result.get("jieqiDetail", {})
    sl = result.get("siling", {})

    # 农历日期
    lunar_str = bi.get("lunar") or bi.get("lunarCn") or bi.get("lunarDate", "")
    if not lunar_str:
        # 尝试从其他字段构建
        lunar_str = f"{bi.get('lunarYear', '')}年{bi.get('lunarMonth', '')}月{bi.get('lunarDay', '')}日"

    gender_cn = meta.get("genderCn") or inp.get("gender", "")
    true_solar_time = meta.get("trueSolarTime") or result.get("trueSolarTime", "")

    # 不在这里输出“阳历/农历/性别”的合并行，统一放到“基本信息（展开）”中逐条输出

    # 出生节气
    prev_jq = jq.get("prevJieQi", {})
    next_jq = jq.get("nextJieQi", {})
    lng = inp.get("longitude", "")
    lat = inp.get("latitude", "")
    lnglat = f"{lng}° / {lat}°" if (lng or lat) else ""

    vi = result.get("voidInfo", {})
    day_void = vi.get("day", {})
    void_str = day_void.get("kong", "") if isinstance(day_void, dict) else str(day_void)

    sp = result.get("specialPalaces", {})
    ty = sp.get("taiYuan", {})
    tx = sp.get("taiXi", {})
    mg = sp.get("mingGong", {})
    sg = sp.get("shenGong", {})
    zi_time = result.get("ziTimeAnalysis", {})

    mgua = result.get("mingGua", {})
    lines.append("")

    # 基本信息展开（避免表格中信息被认为“缩写”）
    lines.append("### 基本资料")
    lines.append("")
    rows = []
    rows.append(["姓名", name or "-"])
    if inp.get("birthDate", ""):
        rows.append(["出生日期", inp.get("birthDate", "")])
    if inp.get("birthTime", ""):
        rows.append(["出生时间", inp.get("birthTime", "")])
    if lunar_str:
        rows.append(["农历", lunar_str])
    # 性别字段可能是“乾造(男)/坤造(女)”这种合并口径，拆开输出
    g_txt = (gender_cn or inp.get("gender", "") or "").strip()
    m = re.match(r"^(乾造|坤造)\((男|女)\)$", g_txt)
    if m:
        rows.append(["造", m.group(1)])
        rows.append(["性别", m.group(2)])
    else:
        rows.append(["性别", g_txt])
    if inp.get("birthPlace", ""):
        rows.append(["出生地区", inp.get("birthPlace", "")])
    if lnglat:
        if lng != "":
            rows.append(["经度", f"{lng}°"])
        if lat != "":
            rows.append(["纬度", f"{lat}°"])
    if true_solar_time:
        rows.append(["真太阳时", true_solar_time])
    if (not hide_non_bazi_basic) and bi.get("zodiac", ""):
        rows.append(["生肖", bi.get("zodiac", "")])
    if (not hide_non_bazi_basic) and bi.get("constellation", ""):
        rows.append(["星座", bi.get("constellation", "")])
    xx = bi.get("xingXiu", bi.get("xiu", bi.get("xingxiu", bi.get("star", "-"))))
    if (not hide_non_bazi_basic) and xx and xx != "-":
        rows.append(["星宿", xx])
    if prev_jq:
        rows.append(
            ["前节气", f"{prev_jq.get('name', '')} {prev_jq.get('date', '')} 已过{prev_jq.get('daysAfter', '')}天"]
        )
    if next_jq:
        rows.append(
            ["后节气", f"{next_jq.get('name', '')} {next_jq.get('date', '')} 还有{next_jq.get('daysBefore', '')}天"]
        )
    if sl.get("current", ""):
        rows.append(["人元司令", f"{sl.get('current', '')}用事"])
    if void_str:
        rows.append(["空亡", void_str])
    if ty.get("pillar", ""):
        rows.append(["胎元", f"{ty.get('pillar', '')} {ty.get('nayin', '')}".strip()])
    if tx.get("pillar", ""):
        rows.append(["胎息", f"{tx.get('pillar', '')} {tx.get('nayin', '')}".strip()])
    if mg.get("pillar", ""):
        rows.append(["命宫", f"{mg.get('pillar', '')} {mg.get('nayin', '')}".strip()])
    if sg.get("pillar", ""):
        rows.append(["身宫", f"{sg.get('pillar', '')} {sg.get('nayin', '')}".strip()])
    if zi_time and isinstance(zi_time, dict):
        zt = []
        if zi_time.get("timeZhi", ""):
            zt.append(f"时支{zi_time.get('timeZhi', '')}")
        if "zwzShift" in zi_time:
            zt.append(f"早晚子规则触发{'是' if zi_time.get('zwzShift') else '否'}")
        if zi_time.get("dayPillarNormal", ""):
            zt.append(f"日柱常规{zi_time.get('dayPillarNormal', '')}")
        if zi_time.get("dayPillarZwz", ""):
            zt.append(f"日柱早晚子{zi_time.get('dayPillarZwz', '')}")
        if zi_time.get("rule", ""):
            zt.append(f"规则{zi_time.get('rule', '')}")
        if zt:
            rows.append(["子时判定", "；".join(zt)])
    if (not hide_non_bazi_basic) and mgua.get("guaName", ""):
        rows.append(["命卦", f"{mgua.get('guaName', '')} {mgua.get('group', '')}".strip()])
    lines.extend(_render_table(["项目", "内容"], rows))

    # 空亡信息明细：已在“四柱信息表”中给出（旬/空亡），这里默认不再重复输出
    # 如需单独展开，可通过 hide["void_detail"]=False 打开。
    if not hide.get("void_detail", True):
        if isinstance(vi, dict) and vi:
            name_map = {"year": "年柱", "month": "月柱", "day": "日柱", "hour": "时柱"}
            order = ["year", "month", "day", "hour"]
            has_any = any(
                isinstance(vi.get(k), dict) and (vi.get(k).get("xun") or vi.get(k).get("kong")) for k in order
            )
            if has_any:
                lines.append("### 空亡信息（依据）")
                lines.append("")
                for k in order:
                    item = vi.get(k, {})
                    if not isinstance(item, dict):
                        continue
                    xun = item.get("xun", "")
                    kong = item.get("kong", "")
                    if xun or kong:
                        lines.append(f"* {name_map.get(k, k)}：")
                        if xun:
                            lines.append(f"  - 旬：{xun}")
                        if kong:
                            lines.append(f"  - 空亡：{kong}")
                lines.append("")

    # 八字排盘详情
    lines.append("## 八字排盘详情")
    lines.append("")
    fp = result.get("fourPillars", {})
    tg = result.get("tenGods", {})
    hs = result.get("hiddenStems", {})
    tw = result.get("twelveGrowth", {})
    dm = result.get("dayMaster", {})

    def _split_csv(val):
        if val is None:
            return []
        if isinstance(val, list):
            return [str(x).strip() for x in val if str(x).strip()]
        s = str(val).replace("，", ",")
        return [x.strip() for x in s.split(",") if x.strip()]

    gz_extra = result.get("ganzhiExtra", {}) or {}
    he_detail_all = gz_extra.get("heDetail", {}) if isinstance(gz_extra, dict) else {}

    # 四柱信息：改为表格呈现（不减少信息，只压缩排版）
    def _fmt_hidden(hidden_list: list[str], gods: list[str], score: dict) -> str:
        parts: list[str] = []
        for i_h, h in enumerate(hidden_list):
            g = gods[i_h] if i_h < len(gods) else ""
            w = score.get(h) if isinstance(score, dict) else None
            seg = h
            if g:
                seg += f"({g})"
            if w is not None:
                seg += f":{w}"
            parts.append(seg)
        return "、".join([x for x in parts if x])

    def _fmt_void(xun: str, kong: str) -> str:
        segs: list[str] = []
        if xun:
            segs.append(f"旬{xun}")
        if kong:
            segs.append(f"空亡{kong}")
        return "；".join(segs)

    pillar_order = [("year", "年柱"), ("month", "月柱"), ("day", "日柱"), ("hour", "时柱")]
    col_headers = ["项目"] + [t for _, t in pillar_order]
    table_rows: list[list[object]] = []

    row_keys = [
        ("干支", "ganZhi"),
        ("天干", "stem"),
        ("十神（天干）", "stemGod"),
        ("地支", "branch"),
        ("十神（地支）", "branchGods"),
        ("藏干（含十神/强度）", "hiddenDetail"),
        ("星运", "growth"),
        ("自坐", "selfSitting"),
        ("空亡", "void"),
        ("纳音", "nayin"),
    ]
    row_vals: dict[str, list[str]] = {k: [""] * 4 for _, k in row_keys}

    for idx, (k, _) in enumerate(pillar_order):
        p_fp = fp.get(k, {}) if isinstance(fp, dict) else {}
        p_tg = tg.get(k, {}) if isinstance(tg, dict) else {}
        p_hidden = hs.get(k, []) if isinstance(hs, dict) else []
        p_void = vi.get(k, {}) if isinstance(vi, dict) else {}
        p_growth = tw.get(k, {}) if isinstance(tw, dict) else {}

        gan_zhi = p_fp.get("fullName") or f"{p_fp.get('stem', '')}{p_fp.get('branch', '')}"
        stem = p_fp.get("stem", "")
        branch = p_fp.get("branch", "")
        nayin = p_fp.get("nayin", "")

        stem_god = p_tg.get("stem", "") if isinstance(p_tg, dict) else ""
        branch_gods = _split_csv(p_tg.get("branch", "")) if isinstance(p_tg, dict) else []

        hidden_list = _split_csv(p_hidden)
        he_item = he_detail_all.get(k, {}) if isinstance(he_detail_all, dict) else {}
        zhi_hidden_score = he_item.get("zhiHiddenScore", {}) if isinstance(he_item, dict) else {}

        growth = (
            p_growth if isinstance(p_growth, str) else (p_growth.get("state", "") if isinstance(p_growth, dict) else "")
        )
        xun = p_void.get("xun", "") if isinstance(p_void, dict) else ""
        kong = p_void.get("kong", "") if isinstance(p_void, dict) else ""

        self_sitting = ""
        if k == "day":
            self_sitting = dm.get("sitting", dm.get("selfSitting", "")) if isinstance(dm, dict) else ""

        row_vals["ganZhi"][idx] = gan_zhi
        row_vals["stem"][idx] = stem
        row_vals["stemGod"][idx] = stem_god
        row_vals["branch"][idx] = branch
        row_vals["branchGods"][idx] = "、".join(branch_gods)
        row_vals["hiddenDetail"][idx] = _fmt_hidden(hidden_list, branch_gods, zhi_hidden_score)
        row_vals["growth"][idx] = growth
        row_vals["selfSitting"][idx] = self_sitting
        row_vals["void"][idx] = _fmt_void(xun, kong)
        row_vals["nayin"][idx] = nayin

    for label, keyname in row_keys:
        table_rows.append([label] + row_vals[keyname])
    lines.extend(_render_table(col_headers, table_rows))

    # 五行分数（表格化）
    wx_score = result.get("wuxingScores", {})
    if wx_score:
        lines.append("### 五行分数")
        lines.append("")
        fe = wx_score.get("fiveElementScore", {})
        if fe:
            lines.extend(_render_table(["五行", "分数"], [[k, v] for k, v in fe.items()]))
        gs = wx_score.get("ganScore", {})
        if gs:
            lines.append("### 天干分数")
            lines.append("")
            lines.extend(_render_table(["天干", "分数"], [[k, v] for k, v in gs.items()]))
        detail = wx_score.get("statusDetail", [])
        if detail:
            seq = "、".join([str(x) for x in detail if str(x).strip()])
            if seq:
                lines.append(f"日主状态序列：{seq}")
        summary = wx_score.get("statusSummary", "")
        if summary:
            parts = [x.strip() for x in str(summary).replace("／", "/").split("/") if x.strip()]
            if parts:
                lines.append("长生概要：")
                lines.extend(_render_table(["项目", "内容"], [[str(i + 1), x] for i, x in enumerate(parts)]))
            else:
                lines.append(f"长生概要：{summary}")
        lines.append("")

    # 温湿度与拱神（表格化）
    climate = result.get("climateScores", {})
    if climate and not climate.get("error"):
        lines.append("### 温湿度与拱神")
        lines.append("")
        crows: list[list[object]] = []
        if climate.get("temperatureScore", "") != "":
            crows.append(["湿度分数", climate.get("temperatureScore", "")])
        if climate.get("hint", ""):
            crows.append(["说明", climate.get("hint", "")])
        gongs = climate.get("gongs", []) or []
        if gongs:
            crows.append(["拱神", "、".join([str(x) for x in gongs if str(x).strip()])])
        empties = climate.get("empties", []) or []
        if empties:
            crows.append(["空亡提示", "、".join([str(x) for x in empties if str(x).strip()])])
        if crows:
            lines.extend(_render_table(["项目", "内容"], crows))

    # 干支合克与入库
    gz_extra = result.get("ganzhiExtra", {})
    if gz_extra:
        lines.append("### 干支合克与入库")
        lines.append("")

        def _fmt_score(d: dict) -> str:
            if not isinstance(d, dict) or not d:
                return ""
            return "、".join([f"{k}:{v}" for k, v in d.items() if str(k).strip()])

        name_map = {"year": "年", "month": "月", "day": "日", "hour": "时"}
        order = ["year", "month", "day", "hour"]

        # 1) 干支相合
        he_detail = gz_extra.get("heDetail", {})
        if he_detail:
            rows: list[list[object]] = []
            for k in order:
                item = he_detail.get(k, {})
                label = f"{name_map.get(k, k)}柱"
                if not isinstance(item, dict):
                    rows.append([label, "", "", str(item), "", ""])
                    continue
                if item.get("error"):
                    rows.append([label, "", "", f"error: {item.get('error')}", "", ""])
                    continue
                rows.append(
                    [
                        label,
                        item.get("ganZhi", ""),
                        item.get("heGan", ""),
                        item.get("hitItem", "") or "-",
                        "相合" if item.get("hit") is True else "不相合",
                        _fmt_score(item.get("zhiHiddenScore", {})),
                    ]
                )
            lines.append("#### 干支相合（依据）")
            lines.append("")
            lines.extend(_render_table(["柱", "干支", "合干", "命中", "结论", "支藏干强度"], rows))
        else:
            if gz_extra.get("he"):
                raise RuntimeError("干支相合数据缺失: ganzhiExtra.heDetail 缺失但 he 非空")

        # 2) 天干相克
        ke_detail = gz_extra.get("keDetail", [])
        if ke_detail:
            rows: list[list[object]] = []
            for i, item in enumerate(ke_detail, 1):
                txt = item.get("text", "") if isinstance(item, dict) else str(item)
                for kk, vv in name_map.items():
                    txt = txt.replace(f"{kk}干", f"{vv}柱天干")
                rows.append([i, txt])
            if rows:
                lines.append("#### 天干相克（依据）")
                lines.append("")
                lines.extend(_render_table(["序号", "关系"], rows))
        else:
            ke = gz_extra.get("ke", [])
            if ke:
                raise RuntimeError("天干相克数据缺失: ganzhiExtra.keDetail 缺失但 ke 非空")

        # 3) 地支入库
        ku_detail = gz_extra.get("kuDetail", {})
        if ku_detail:
            rows: list[list[object]] = []
            for k in order:
                item = ku_detail.get(k, {})
                label = f"{name_map.get(k, k)}柱"
                if not isinstance(item, dict):
                    rows.append([label, "", str(item), "", "", "", "", "", "", ""])
                    continue
                if item.get("error"):
                    rows.append([label, "", f"error: {item.get('error')}", "", "", "", "", "", "", ""])
                    continue
                zhi = item.get("zhi", "")
                is_ku = item.get("isKu") is True
                ku_elem = item.get("kuElement", "") or ""
                weakest = item.get("weakestGan", "") or ""
                weakest_score = item.get("weakestScore", "")
                hit_item = item.get("hitItem", "") or "-"
                verdict = "入库" if item.get("hit") is True else "不入库"
                hiddens = item.get("hidden", []) if isinstance(item.get("hidden", []), list) else []
                rows.append(
                    [
                        label,
                        zhi,
                        "是" if is_ku else "否",
                        f"{ku_elem}库" if ku_elem else "",
                        weakest,
                        weakest_score,
                        hit_item,
                        verdict,
                        "、".join([str(x) for x in hiddens if str(x).strip()]),
                        _fmt_score(item.get("zhiHiddenScore", {})),
                    ]
                )
            lines.append("#### 地支入库（依据）")
            lines.append("")
            lines.extend(
                _render_table(
                    ["柱", "地支", "四库", "库类", "最弱藏干", "最弱分数", "命中", "结论", "本柱藏干", "支藏干强度"],
                    rows,
                )
            )
        else:
            if gz_extra.get("ku"):
                raise RuntimeError("地支入库数据缺失: ganzhiExtra.kuDetail 缺失但 ku 非空")

        lines.append("")

    # 地支六合 / 三会 / 三合 / 冲刑害破
    zhi_rel = result.get("branchRelations", {})
    if zhi_rel and not zhi_rel.get("error"):
        lines.append("### 地支关系")
        lines.append("")
        liu_he_detail = zhi_rel.get("liuHeDetail", [])
        san_hui_detail = zhi_rel.get("sanHuiDetail", [])
        san_he_detail = zhi_rel.get("sanHeDetail", [])
        conf_detail = zhi_rel.get("conflictsDetail", [])

        def _expand_relation_text(text: str) -> list[str]:
            """
            将 bazi_calculator 输出的关系 text（经常带“（半）/六合(金)/刑(名字)/三会：... => ...”）
            拆成“全展开”多行结构，避免一行塞多个信息。
            """
            if not text:
                return []
            t = str(text).strip()
            out: list[str] = []

            # 1) 半/全 标记
            completeness = ""
            if t.endswith("（半）"):
                completeness = "半"
                t = t[:-3]
            elif t.endswith("（全）"):
                completeness = "全"
                t = t[:-3]

            # 2) 三会/三合：带 “=>”
            if t.startswith("三会：") or t.startswith("三合："):
                out.append("  - 关系（展开）：")
                out.append(f"    - 原文：{t}")
                head, _, tail = t.partition("=>")
                if head:
                    out.append(f"    - 组成：{head.strip()}")
                if tail:
                    out.append(f"    - 结论：{tail.strip()}")
                if completeness:
                    out.append(f"    - 完整度：{completeness}")
                return out

            # 3) 六合：末尾可能带 “(金)” 这种元素标记
            m = re.search(r"六合\(([^)]+)\)\s*$", t)
            liuhe_elem = ""
            if m:
                liuhe_elem = m.group(1).strip()
                t = t[: m.start()].rstrip()

            # 4) 刑：末尾可能带 “刑(子卯刑)” 这类
            m = re.search(r"刑\(([^)]+)\)\s*$", t)
            xing_name = ""
            if m:
                xing_name = m.group(1).strip()
                t = t[: m.start()].rstrip()

            # 5) 尝试抽取“年/月/日/时支X … 月支Y”这类柱位与地支信息
            pairs = re.findall(r"([年月日时])支([子丑寅卯辰巳午未申酉戌亥])", t)
            rel = ""
            # 关系关键字（优先“六合”，其次“合/会/冲/害/破”等）
            for k in ["六合", "三会", "三合", "合", "会", "冲", "害", "破"]:
                if k in t:
                    rel = k
                    break

            out.append("  - 关系（展开）：")
            out.append(f"    - 原文：{t}")
            if rel:
                out.append(f"    - 关系：{rel}")
            if liuhe_elem:
                out.append(f"    - 六合五行：{liuhe_elem}")
            if xing_name:
                out.append(f"    - 刑类：{xing_name}")
            if pairs:
                out.append("    - 柱位地支（展开）：")
                for pos, zhi in pairs:
                    out.append(f"      - {pos}支：{zhi}")
            if completeness:
                out.append(f"    - 完整度：{completeness}")
            return out

        if liu_he_detail:
            lines.append("* 六合（依据）：")
            for item in liu_he_detail:
                if isinstance(item, dict) and item.get("text"):
                    for x in _expand_relation_text(item.get("text")):
                        lines.append(x)
        elif zhi_rel.get("liuHe"):
            raise RuntimeError("地支关系数据缺失: branchRelations.liuHeDetail 缺失但 liuHe 非空")

        if san_hui_detail:
            lines.append("* 三会（依据）：")
            for item in san_hui_detail:
                if isinstance(item, dict) and item.get("text"):
                    for x in _expand_relation_text(item.get("text")):
                        lines.append(x)
        elif zhi_rel.get("sanHui"):
            raise RuntimeError("地支关系数据缺失: branchRelations.sanHuiDetail 缺失但 sanHui 非空")

        if san_he_detail:
            lines.append("* 三合（依据）：")
            for item in san_he_detail:
                if isinstance(item, dict) and item.get("text"):
                    for x in _expand_relation_text(item.get("text")):
                        lines.append(x)
        elif zhi_rel.get("sanHe"):
            raise RuntimeError("地支关系数据缺失: branchRelations.sanHeDetail 缺失但 sanHe 非空")

        if conf_detail:
            lines.append("* 刑冲害破（依据）：")
            for item in conf_detail:
                if isinstance(item, dict) and item.get("text"):
                    for x in _expand_relation_text(item.get("text")):
                        lines.append(x)
        elif zhi_rel.get("conflicts"):
            raise RuntimeError("地支关系数据缺失: branchRelations.conflictsDetail 缺失但 conflicts 非空")
        lines.append("")

    # 神煞（默认输出合并后的全量列表；禁止回退到简表口径）
    full_sp = result.get("spiritsFull", {})
    full_by = full_sp.get("byPillar", {})
    lines.append("## 神煞断语")
    lines.append("")
    if not isinstance(full_by, dict):
        raise RuntimeError("神煞数据缺失: spiritsFull.byPillar 不是 dict")
    srows: list[list[object]] = []
    for pillar, pname in [("year", "年柱"), ("month", "月柱"), ("day", "日柱"), ("hour", "时柱")]:
        slist = full_by.get(pillar, [])
        if not slist:
            continue
        srows.append([pname, "、".join([str(x) for x in slist if str(x).strip()])])
    if srows:
        lines.extend(_render_table(["柱", "神煞（合并去重）"], srows))
    descs = full_sp.get("descriptions", {})
    if descs:
        lines.append("")
        lines.append("**神煞释义**")
        for k, v in descs.items():
            lines.append(f"- {k}：{v}")

    # 兼容字段：spirits / spiritsExplain（不丢字段；与 spiritsFull 可能重复）
    sp = result.get("spirits", {})
    sp_by = sp.get("byPillar", {}) if isinstance(sp, dict) else {}
    if isinstance(sp_by, dict) and sp_by:
        lines.append("")
        lines.append("### 简表神煞（字段展开）")
        lines.append("")
        rows = []
        for pillar, pname in [("year", "年柱"), ("month", "月柱"), ("day", "日柱"), ("hour", "时柱")]:
            slist = sp_by.get(pillar, [])
            if not slist:
                continue
            rows.append([pname, "、".join([str(x) for x in slist if str(x).strip()])])
        if rows:
            lines.extend(_render_table(["柱", "神煞"], rows))
    sp_ex = result.get("spiritsExplain", {})
    if isinstance(sp_ex, dict) and sp_ex:
        lines.append("")
        lines.append("**简表神煞释义（字段展开）**")
        for k, v in sp_ex.items():
            lines.append(f"- {k}：{v}")
    lines.append("")

    return _normalize_present_text("\n".join(lines))


def generate_daymaster_section(result: dict[str, Any]) -> str:
    """生成日主概览（属性/阴阳/旺衰/格局参考）"""
    lines = []
    dm = result.get("dayMaster", {})
    wx_state = result.get("wuxingState", {})
    geju = result.get("geju", {})
    sizi_sum = result.get("siziSummary", {}) or {}
    if dm or wx_state or geju:
        lines.append("## 日主概览")
        lines.append("")
        if dm:
            lines.append("* 日主属性（展开）：")
            if dm.get("stem", ""):
                lines.append(f"  - 天干：{dm.get('stem', '')}")
            elem = dm.get("elementCn", dm.get("element", ""))
            if elem:
                lines.append(f"  - 五行：{elem}")
            lines.append(f"* 阴阳参考：{dm.get('yinYang', '')}")
            if dm.get("strength"):
                lines.append(f"* 旺衰参考：{dm.get('strength')}")
        if wx_state:
            desc = wx_state.get("description", "")
            if desc:
                lines.append(f"* 五行状态：{desc}")
            summary = wx_state.get("statusSummary", "")
            if summary:
                lines.append(f"* 旺衰概要：{summary}")
        if geju:
            main = geju.get("main", "")
            pats = geju.get("patterns", [])
            if main or pats:
                if main:
                    lines.append(f"* 格局参考：{main}")
                # 备选格局展开
                others = [p for p in pats if p and p != main]
                if others:
                    lines.append("* 备选格局：")
                    for p in others:
                        lines.append(f"  - {p}")
        # 外部断语（bazi-1 sizi.summarys）：属于“干支性情”文本资源，不做自写推断
        if isinstance(sizi_sum, dict) and sizi_sum.get("text"):
            lines.append("* 四柱断语：")
            if sizi_sum.get("key", ""):
                lines.append(f"  - 键：{sizi_sum.get('key', '')}")
            text = str(sizi_sum.get("text", "")).strip()
            if text:
                # 保留原文（按行拆分）
                lines.append("  - 原文：")
                for ln in text.splitlines():
                    t = ln.strip()
                    if t:
                        lines.append(f"    - {t}")
        lines.append("")
    return "\n".join(lines)


def generate_wuxing_section(result: dict[str, Any]) -> str:
    """生成五行分析部分"""
    lines = []
    lines.append("## 五行喜忌（调候与平衡）")
    lines.append("")

    dm = result.get("dayMaster", {})
    # 日主属性与强弱（单一口径，取 weakStrong 优先，其次 dayMaster.strength）
    strength = dm.get("strength", "")
    wx_strength = result.get("wuxingScores", {}).get("weakStrong")
    final_strength = wx_strength or strength
    lines.append("日主属性（展开）：")
    if dm.get("stem", ""):
        lines.append(f"* 天干：{dm.get('stem', '')}")
    elem = dm.get("elementCn", dm.get("element", ""))
    if elem:
        lines.append(f"* 五行：{elem}")
    if final_strength:
        lines.append(f"强弱判断：{final_strength}")
    lines.append("")

    # 五行统计
    fe = result.get("fiveElements", {})
    lines.append("### 五行比例")
    lines.append("")
    ratio_rows: list[list[object]] = []
    for wx in ["木", "火", "土", "金", "水"]:
        val = fe.get(wx, {})
        if isinstance(val, dict):
            pct = val.get("percentage", 0)
            cnt = val.get("count", 0)
        else:
            pct = val
            cnt = "-"
        ratio_rows.append([wx, f"{pct}%", cnt])
    lines.extend(_render_table(["五行", "比例", "个数"], ratio_rows))

    # 五行分数 / 天干分数（含藏干、月支加权）
    wx_score = result.get("wuxingScores", {})
    if wx_score:
        fes = wx_score.get("fiveElementScore", {})
        gan_sc = wx_score.get("ganScore", {})
        if fes or gan_sc:
            lines.append("### 五行分数")
            lines.append("")
        if fes:
            rows = [[k, v] for k, v in fes.items()]
            lines.append("口径：含藏干")
            lines.append("")
            lines.extend(_render_table(["五行", "分数"], rows))
        if gan_sc:
            rows = [[k, v] for k, v in gan_sc.items()]
            lines.append("### 天干分数")
            lines.append("")
            lines.extend(_render_table(["天干", "分数"], rows))
        # 避免重复展示，与上方“强弱判断”保持一致
        if wx_score.get("statusDetail"):
            seq = "、".join([str(x) for x in wx_score.get("statusDetail") if str(x).strip()])
            if seq:
                lines.append(f"日主状态序列：{seq}")
        if wx_score.get("statusSummary"):
            summary = wx_score.get("statusSummary")
            parts = [x.strip() for x in str(summary).replace("／", "/").split("/") if x.strip()]
            if parts:
                lines.append("长生概要：")
                lines.extend(_render_table(["项目", "内容"], [[str(i + 1), x] for i, x in enumerate(parts)]))
            else:
                lines.append(f"长生概要：{summary}")
        lines.append("")

    # 五行状态
    ws = result.get("wuxingState", {})
    desc = ws.get("description", "")
    if desc:
        lines.append(f"五行状态：{desc}")
        lines.append("")

    return "\n".join(lines)


def generate_bone_section(result: dict[str, Any]) -> str:
    """生成称骨算命部分"""
    lines = []
    bw = result.get("boneWeight", {})
    if bw:
        lines.append("## 袁天罡称骨")
        lines.append("")
        lines.append("* 称骨（展开）：")
        if bw.get("weight", "") != "":
            lines.append(f"  - 数值：{bw.get('weight', '')}两")
        if bw.get("weightCn", ""):
            lines.append(f"  - 中文：{bw.get('weightCn', '')}")
        lines.append(f"* 评语：{bw.get('text', '')}")
        comp = bw.get("components", {})
        if comp:
            lines.append("* 权重构成：")
            year = comp.get("year", {})
            month = comp.get("month", {})
            day = comp.get("day", {})
            hour = comp.get("hour", {})
            lines.append(f"  - 年柱 {year.get('ganZhi', '')}：{year.get('weight', '')}两")
            lines.append(f"  - 月份 {month.get('month', '')}月：{month.get('weight', '')}两")
            lines.append(f"  - 出生日 {day.get('day', '')}日：{day.get('weight', '')}两")
            lines.append(f"  - 时辰 {hour.get('zhi', '')}时：{hour.get('weight', '')}两")
        lines.append("")
    return "\n".join(lines)


def generate_fortune_section(result: dict[str, Any], recent_years: int | None = None) -> str:
    """生成运势分析部分

    recent_years:
      - None: 全量输出（历史/未来全部）
      - N: 仅输出近 N 年（按北京时间当前年开始）
    """
    lines = []
    lines.append("## 运势分析")
    lines.append("")

    # 大运建议（外部口径）：直接引用 yongShen.basis 中的“大运：...”段落
    ys = result.get("yongShen", {}) or {}
    basis = ys.get("basis", "") if isinstance(ys, dict) else ""
    if basis and "大运：" in basis:
        m = re.search(r"大运：(.+?)(?:备注：|$)", str(basis))
        seg = m.group(1).strip() if m else ""
        if seg:
            lines.append("* 大运建议：")
            lines.append(f"  - 原文：{seg}")
            lines.append("")

    # 交运信息
    jy = result.get("jiaoYun", {})
    mf = result.get("majorFortune", {})

    if jy:
        desc = jy.get("description", "")
        start_date = jy.get("startDate", "")
        if start_date:
            lines.append("起运（展开）：")
            if desc:
                lines.append(f"* 描述：{desc}")
            lines.append(f"* 日期：{start_date}")
        else:
            lines.append("起运（展开）：")
            if desc:
                lines.append(f"* 描述：{desc}")
        lines.append(f"交运：逢{jy.get('jiaoJieQi', '')}节后交大运")
        vi = result.get("voidInfo", {}).get("day", {})
        if isinstance(vi, dict):
            lines.append("空亡（展开）：")
            if vi.get("kong", ""):
                lines.append(f"* 空亡：{vi.get('kong', '')}")
            lines.append("* 依据：日柱")
        sl = result.get("siling", {})
        if sl:
            lines.append(f"司令：{sl.get('current', '')}")
        lines.append("")

    # 大运（表格化呈现：压缩排版，不减少字段）
    if mf:
        lines.append("### 大运分析")
        lines.append("")
        pillars = mf.get("pillars", [])
        msp_map = {str(dy.get("startYear")): dy for dy in result.get("majorFortuneSpirits", []) if isinstance(dy, dict)}
        rows: list[list[object]] = []
        for f in pillars:
            if not isinstance(f, dict):
                continue
            age = f.get("age", "")
            year = f.get("startYear", "")
            gz = f.get("fullName", "") or f.get("ganZhi", "")
            tg = f.get("shiShen", "") or ""
            ny = f.get("nayin", "") or ""

            msp = msp_map.get(str(year), {})
            wxc_txt = ""
            sp_txt = ""
            if isinstance(msp, dict):
                wxc = msp.get("wuxingContribution", {}) or {}
                if isinstance(wxc, dict) and wxc:
                    wxc_txt = "、".join([f"{k}:{v}" for k, v in wxc.items() if str(k).strip()])
                sp = msp.get("spirits", []) or []
                if sp:
                    sp_txt = "、".join([str(x) for x in sp if str(x).strip()])

            rows.append([f"{age}岁" if str(age) != "" else "", year, gz, tg, ny, wxc_txt, sp_txt])
        lines.extend(_render_table(["起始年龄", "起始年份", "干支", "十神", "纳音", "五行贡献", "神煞"], rows))

    # 流年
    af = result.get("annualFortune", [])
    if af:
        years_all = [x for x in af if isinstance(x, dict) and str(x.get("year", "")).strip()]
        years_sorted = sorted(years_all, key=lambda x: int(x.get("year")))

        selected = years_sorted
        if recent_years is not None:
            # 以北京时间当前年为起点优先挑选；若命中不足则退化为“取最靠前 N 条”
            now_year = datetime.now().year
            target_years = {str(now_year + i) for i in range(max(0, int(recent_years)))}
            picked = [x for x in years_sorted if str(x.get("year")) in target_years]
            selected = picked if len(picked) >= 1 else years_sorted[: int(recent_years)]

        lines.append(f"### 近期流年指引（近{recent_years}年）" if recent_years else "### 流年")
        lines.append("")
        asp_map = {
            str(y.get("year")): (y.get("spirits", []) or [])
            for y in result.get("annualSpirits", [])
            if isinstance(y, dict)
        }
        rows: list[list[object]] = []
        for f in selected:
            if not isinstance(f, dict):
                continue
            year = f.get("year", "")
            gz = f.get("fullName", "") or f.get("ganZhi", "")
            tg = f.get("shiShen", "") or ""
            ny = f.get("nayin", "") or ""
            sp = asp_map.get(str(year), [])
            sp_txt = "、".join([str(x) for x in sp if str(x).strip()]) if sp else ""
            rows.append([year, gz, tg, ny, sp_txt])
        lines.extend(_render_table(["年份", "干支", "十神", "纳音", "神煞"], rows))

    return "\n".join(lines)


def generate_relations_section(result: dict[str, Any]) -> str:
    """生成干支关系部分"""
    lines = []
    gr = result.get("ganzhiRelations", {})
    if gr:
        lines.append("## 干支关系")
        lines.append("")

        tg = gr.get("tianGan", gr.get("stems", {}))
        dz = gr.get("diZhi", gr.get("branches", {}))

        def _expand_tg_text(text: str) -> list[str]:
            t = (text or "").strip()
            if not t:
                return []
            out: list[str] = []
            # 形如：年月甲己合化土 / 年日甲庚冲
            m = re.match(
                r"^([年月日时])([年月日时])([甲乙丙丁戊己庚辛壬癸])([甲乙丙丁戊己庚辛壬癸])合化([木火土金水])$", t
            )
            if m:
                out.append("  - 关系（展开）：")
                out.append("    - 柱位（展开）：")
                out.append(f"      - {m.group(1)}")
                out.append(f"      - {m.group(2)}")
                out.append("    - 天干（展开）：")
                out.append(f"      - {m.group(3)}")
                out.append(f"      - {m.group(4)}")
                out.append("    - 关系：合化")
                out.append(f"    - 化气：{m.group(5)}")
                return out
            m = re.match(r"^([年月日时])([年月日时])([甲乙丙丁戊己庚辛壬癸])([甲乙丙丁戊己庚辛壬癸])冲$", t)
            if m:
                out.append("  - 关系（展开）：")
                out.append("    - 柱位（展开）：")
                out.append(f"      - {m.group(1)}")
                out.append(f"      - {m.group(2)}")
                out.append("    - 天干（展开）：")
                out.append(f"      - {m.group(3)}")
                out.append(f"      - {m.group(4)}")
                out.append("    - 关系：冲")
                return out
            # 兜底：保留原文（不做错误解释）
            out.append("  - 关系（展开）：")
            out.append(f"    - 原文：{t}")
            return out

        def _expand_dz_text(text: str) -> list[str]:
            t = (text or "").strip()
            if not t:
                return []
            out: list[str] = []
            # 六合：年月子丑合土
            m = re.match(
                r"^([年月日时])([年月日时])([子丑寅卯辰巳午未申酉戌亥])([子丑寅卯辰巳午未申酉戌亥])合([木火土金水])$", t
            )
            if m:
                out.append("  - 关系（展开）：")
                out.append("    - 柱位（展开）：")
                out.append(f"      - {m.group(1)}")
                out.append(f"      - {m.group(2)}")
                out.append("    - 地支（展开）：")
                out.append(f"      - {m.group(3)}")
                out.append(f"      - {m.group(4)}")
                out.append("    - 关系：合")
                out.append(f"    - 合化五行：{m.group(5)}")
                return out
            # 六冲：年月子午冲
            m = re.match(r"^([年月日时])([年月日时])([子丑寅卯辰巳午未申酉戌亥])([子丑寅卯辰巳午未申酉戌亥])冲$", t)
            if m:
                out.append("  - 关系（展开）：")
                out.append("    - 柱位（展开）：")
                out.append(f"      - {m.group(1)}")
                out.append(f"      - {m.group(2)}")
                out.append("    - 地支（展开）：")
                out.append(f"      - {m.group(3)}")
                out.append(f"      - {m.group(4)}")
                out.append("    - 关系：冲")
                return out
            # 三合/半合：申子辰三合水局 / 申子半合水
            m = re.match(r"^([子丑寅卯辰巳午未申酉戌亥]+)(三合)([木火土金水])局$", t)
            if m:
                out.append("  - 关系（展开）：")
                out.append(f"    - 地支：{m.group(1)}")
                out.append("    - 关系：三合")
                out.append(f"    - 五行：{m.group(3)}")
                out.append("    - 结论：成局")
                return out
            m = re.match(r"^([子丑寅卯辰巳午未申酉戌亥]+)半合([木火土金水])$", t)
            if m:
                out.append("  - 关系（展开）：")
                out.append(f"    - 地支：{m.group(1)}")
                out.append("    - 关系：半合")
                out.append(f"    - 五行：{m.group(2)}")
                return out
            # 刑：子卯刑(无礼之刑)
            m = re.match(r"^([子丑寅卯辰巳午未申酉戌亥]+)刑\(([^)]+)\)$", t)
            if m:
                out.append("  - 关系（展开）：")
                out.append(f"    - 地支：{m.group(1)}")
                out.append("    - 关系：刑")
                out.append(f"    - 刑类：{m.group(2)}")
                return out
            # 害/破：年月子未害 / 年日子酉破
            m = re.match(r"^([年月日时])([年月日时])([子丑寅卯辰巳午未申酉戌亥])([子丑寅卯辰巳午未申酉戌亥])害$", t)
            if m:
                out.append("  - 关系（展开）：")
                out.append("    - 柱位（展开）：")
                out.append(f"      - {m.group(1)}")
                out.append(f"      - {m.group(2)}")
                out.append("    - 地支（展开）：")
                out.append(f"      - {m.group(3)}")
                out.append(f"      - {m.group(4)}")
                out.append("    - 关系：害")
                return out
            m = re.match(r"^([年月日时])([年月日时])([子丑寅卯辰巳午未申酉戌亥])([子丑寅卯辰巳午未申酉戌亥])破$", t)
            if m:
                out.append("  - 关系（展开）：")
                out.append("    - 柱位（展开）：")
                out.append(f"      - {m.group(1)}")
                out.append(f"      - {m.group(2)}")
                out.append("    - 地支（展开）：")
                out.append(f"      - {m.group(3)}")
                out.append(f"      - {m.group(4)}")
                out.append("    - 关系：破")
                return out

            out.append("  - 关系（展开）：")
            out.append(f"    - 原文：{t}")
            return out

        if tg:
            lines.append("* 天干关系（展开）：")
            items = tg if isinstance(tg, list) else []
            if isinstance(tg, dict):
                for v in tg.values():
                    if isinstance(v, list):
                        items.extend(v)
                    elif v:
                        items.append(v)
            for item in items:
                for x in _expand_tg_text(str(item)):
                    lines.append(x)

        if dz:
            lines.append("* 地支关系（展开）：")
            items = dz if isinstance(dz, list) else []
            if isinstance(dz, dict):
                for v in dz.values():
                    if isinstance(v, list):
                        items.extend(v)
                    elif v:
                        items.append(v)
            for item in items:
                for x in _expand_dz_text(str(item)):
                    lines.append(x)

        lines.append("")

    return "\n".join(lines)


def generate_bingyao_section(result: dict[str, Any]) -> str:
    """五行停匀/寒湿燥热与调候依据（不做自写结论，仅输出外部口径结果）。"""
    cs = result.get("climateScores", {})
    ys = result.get("yongShen", {})
    if not cs and not ys:
        return ""
    lines: list[str] = []
    lines.append("## 五行停匀与寒湿燥热（调候依据）")
    lines.append("")
    rows: list[list[object]] = []
    if cs:
        rows.append(["温湿度分数", cs.get("temperatureScore", "")])
        if cs.get("hint"):
            rows.append(["口径说明", cs.get("hint")])
        g = cs.get("gongs") or []
        if g:
            rows.append(["拱神", "，".join([str(x) for x in g if x])])
        e = cs.get("empties") or []
        if e:
            rows.append(["空亡命中", "，".join([str(x) for x in e if x])])
    th = ys.get("tiaoHou", {}) if isinstance(ys, dict) else {}
    if th:
        xi = th.get("xi") or []
        ji = th.get("ji") or []
        if xi:
            rows.append(["调候喜用", "，".join([str(x) for x in xi if x])])
        if ji:
            rows.append(["调候忌神", "，".join([str(x) for x in ji if x])])
    if rows:
        lines.extend(_render_table(["项目", "内容"], rows))
    return "\n".join(lines)


def generate_ganzhi_imagery_section(result: dict[str, Any]) -> str:
    """干支取象/纳音（bazi-1 字典原文）。"""
    gi = result.get("ganzhiImagery", {})
    fp = result.get("fourPillars", {})
    if not isinstance(gi, dict) or not gi:
        return ""
    pos_cn = {"year": "年柱", "month": "月柱", "day": "日柱", "hour": "时柱"}
    lines: list[str] = []
    lines.append("## 干支取象（原文）")
    lines.append("")
    rows: list[list[object]] = []
    for pos in ["year", "month", "day", "hour"]:
        item = gi.get(pos, {}) if isinstance(gi.get(pos, {}), dict) else {}
        stem = item.get("stem", "")
        zhi = item.get("branch", "")
        stem_img = _compact_inline_text(item.get("stemImagery", ""))
        zhi_img = _compact_inline_text(item.get("branchImagery", ""))
        nayin = ""
        if isinstance(fp, dict):
            nayin = (fp.get(pos, {}) or {}).get("nayin", "") if isinstance(fp.get(pos, {}), dict) else ""
        rows.append([pos_cn.get(pos, pos), stem, stem_img, zhi, zhi_img, nayin])
    lines.extend(_render_table(["柱位", "天干", "天干取象", "地支", "地支取象", "纳音"], rows))
    return "\n".join(lines)


def generate_ziwei_horoscope_section(result: dict[str, Any]) -> str:
    """紫微运限四化（iztro horoscope 原生输出）。"""
    hz = result.get("ziweiHoroscope", {})
    if not isinstance(hz, dict) or not hz:
        return ""
    lines: list[str] = []
    lines.append("## 紫微运限四化（大限/流年/流月/流日/流时）")
    lines.append("")
    rows = []
    if hz.get("solarDate"):
        rows.append(["运限阳历", hz.get("solarDate")])
    if hz.get("lunarDate"):
        rows.append(["运限农历", hz.get("lunarDate")])
    age = hz.get("age")
    if isinstance(age, dict) and age:
        # 避免把 dict 直接 str() 输出导致出现英文键
        if age.get("nominalAge") is not None:
            rows.append(["当前年龄（虚岁）", age.get("nominalAge")])
        if age.get("name"):
            rows.append(["运限类型", age.get("name")])
        hs = age.get("heavenlyStem", "")
        eb = age.get("earthlyBranch", "")
        if hs or eb:
            rows.append(["运限干支", f"{hs}{eb}"])
        if age.get("index") is not None:
            rows.append(["序号", age.get("index")])
        pn = age.get("palaceNames") or []
        if isinstance(pn, list) and pn:
            rows.append(["十二宫顺序", "、".join([str(x) for x in pn if str(x).strip()])])
        mu = age.get("mutagen") or []
        if isinstance(mu, list) and mu:
            rows.append(["生年四化", "、".join([str(x) for x in mu if str(x).strip()])])
    elif age is not None and age != "":
        rows.append(["当前年龄", age])
    if rows:
        lines.extend(_render_table(["项目", "内容"], rows))

    def _mutagen_map(arr: object) -> str:
        if not isinstance(arr, list) or len(arr) != 4:
            return "，".join([str(x) for x in (arr or []) if x]) if isinstance(arr, list) else ""
        lu, quan, ke, ji = arr
        return f"禄：{lu}；权：{quan}；科：{ke}；忌：{ji}"

    for scope_key, scope_cn in [
        ("decadal", "大限"),
        ("yearly", "流年"),
        ("monthly", "流月"),
        ("daily", "流日"),
        ("hourly", "流时"),
    ]:
        scope = hz.get(scope_key, {})
        if not isinstance(scope, dict) or not scope:
            continue
        lines.append(f"### {scope_cn}")
        lines.append("")
        head_rows = []
        if scope.get("heavenlyStem") or scope.get("earthlyBranch"):
            head_rows.append(["干支", f"{scope.get('heavenlyStem', '')}{scope.get('earthlyBranch', '')}"])
        if scope.get("mutagen") is not None:
            head_rows.append(["四化", _mutagen_map(scope.get("mutagen"))])
        if head_rows:
            lines.extend(_render_table(["项目", "内容"], head_rows))

        palace_names = scope.get("palaceNames") or []
        stars = scope.get("stars") or []
        if isinstance(palace_names, list) and isinstance(stars, list) and palace_names and stars:
            star_rows = []
            for i, pn in enumerate(palace_names):
                block = stars[i] if i < len(stars) else []
                if isinstance(block, list):
                    names = []
                    for s in block:
                        if isinstance(s, dict):
                            names.append(s.get("name", ""))
                        else:
                            names.append(str(s))
                    star_rows.append([pn, "，".join([x for x in names if x])])
                else:
                    star_rows.append([pn, str(block)])
            lines.extend(_render_table(["宫位", "流耀"], star_rows))
        lines.append("")
    return "\n".join(lines)


def _report_name(result: dict[str, Any]) -> str:
    inp = result.get("input", {})
    name = inp.get("name", "命主") if isinstance(inp, dict) else "命主"
    return str(name or "命主")


def _wrap_report(parts: list[str]) -> str:
    branding = load_branding()
    normalized = _normalize_present_text("\n".join(parts))
    disclaimer_section = f"{build_disclaimer_text()}\n\n"
    sponsor_section = "\n".join(
        [
            f"## {branding['reportFooterTitle']}",
            "",
            build_brand_footer_text(compact=False),
        ]
    )
    return f"{disclaimer_section}{sponsor_section}\n\n{normalized}"


def _normalize_report_system(report_system: str | None) -> str:
    normalized = (report_system or "bazi").strip().lower().replace("-", "_")
    aliases = {
        "standard": "bazi",
        "pure_bazi": "bazi",
        "ba_zi": "bazi",
        "八字": "bazi",
        "正宗八字": "bazi",
        "综合八字": "bazi",
        "ziweidoushu": "ziwei",
        "zi_wei": "ziwei",
        "紫微": "ziwei",
        "紫微斗数": "ziwei",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in REPORT_SYSTEM_LABELS:
        allowed = report_system_allowed_text()
        raise ValueError(f"未知报告体系: {report_system}；允许值: {allowed}")
    return normalized


def normalize_report_system(report_system: str | None) -> str:
    """公开的报告体系归一化入口。"""
    return _normalize_report_system(report_system)


def build_report_hide(report_system: str | None = "bazi", hide: dict[str, bool] | None = None) -> dict[str, bool]:
    """按报告体系构造计算/呈现开关。

    默认综合八字不需要紫微扩展；只有 `ziwei` 独立体系开启扩展计算。
    """
    system = _normalize_report_system(report_system)
    merged = dict(DEFAULT_HIDE)
    if hide:
        merged.update({k: bool(v) for k, v in hide.items()})
    merged["extensions"] = system != "ziwei"
    return merged


def generate_bazi_standard_report(result: dict[str, Any], hide: dict[str, bool] | None = None) -> str:
    """生成综合八字标准报告：八字主线 + 称骨民俗辅助，不混入紫微或建除。"""
    HIDE = build_report_hide("bazi", hide=hide)
    HIDE["non_bazi_basic"] = True

    RECENT_YEARS = None
    parts: list[str] = [
        generate_report(result, hide=HIDE),
        generate_daymaster_section(result),
        generate_wuxing_section(result),
        generate_bingyao_section(result),
        generate_ganzhi_imagery_section(result),
        generate_geju_section(result),
        generate_jieqi_section(result),
        generate_relations_section(result),
        "",
        "## 第二卷：后天运路（动态趋势）",
        "",
        generate_fortune_section(result, recent_years=RECENT_YEARS),
        generate_monthly_section(result, recent_years=RECENT_YEARS),
        "",
        "## 第三卷：民俗与建议（生活应用）",
        "",
        generate_bone_section(result),
    ]
    return _wrap_report(parts)


def generate_ziwei_report(result: dict[str, Any]) -> str:
    """生成紫微斗数独立报告。"""
    name = _report_name(result)
    parts = [
        f"# 紫微斗数报告：{name}",
        "",
        generate_ziwei_section(result),
        generate_ziwei_basic_section(result),
        generate_ziwei_horoscope_section(result),
    ]
    return _wrap_report(parts)


def generate_full_report(
    result: dict[str, Any],
    hide: dict[str, bool] | None = None,
    report_system: str | None = "bazi",
) -> str:
    """生成指定体系的标准报告。

    默认输出综合八字体系。紫微斗数作为独立体系通过 report_system 单独选择，
    不再与综合八字默认报告混排。
    """
    system = _normalize_report_system(report_system)
    if system == "bazi":
        return generate_bazi_standard_report(result, hide=hide)
    if system == "ziwei":
        return generate_ziwei_report(result)
    raise AssertionError(f"未处理的报告体系: {system}")


def generate_geju_section(result: dict[str, Any]) -> str:
    """生成格局用神部分"""
    lines = []
    gj = result.get("geju", {})
    ys = result.get("yongShen", {})

    if gj or ys:
        lines.append("## 命造格局（格局用神）")
        lines.append("")

        if gj:
            lines.append(f"* 主格局：{gj.get('main', '')}")
            patterns = gj.get("patterns", [])
            if len(patterns) > 1:
                lines.append("* 其他格局：")
                for p in patterns[1:]:
                    lines.append(f"  - {p}")

        if ys:
            th = ys.get("tiaoHou", {})
            xi = th.get("xi", [])
            ji = th.get("ji", [])
            if xi:
                lines.append("* 调候喜用：")
                for x in xi:
                    lines.append(f"  - {x}")
            if ji:
                lines.append("* 调候忌神：")
                for x in ji:
                    lines.append(f"  - {x}")
            note = ys.get("note", "")
            if note:
                lines.append(f"* 用神备注：{note}")
            basis = ys.get("basis", "") if isinstance(ys, dict) else ""
            if basis:
                lines.append("* 取用依据：")
                raw = ys.get("tiaohouRaw", "")
                if raw:
                    lines.append(f"  - 调候编码：{raw}")
                lines.append("  - 原文：")
                # 保留原文，不做“自写解释”
                for ln in str(basis).splitlines():
                    t = ln.strip()
                    if t:
                        lines.append(f"    - {t}")
        lines.append("")

    return "\n".join(lines)


def generate_monthly_section(result: dict[str, Any], recent_years: int | None = None) -> str:
    """生成流月小运部分

    recent_years:
      - None: 全量输出（所有年份的流月）
      - N: 仅输出近 N 年的 12 流月（按北京时间当前年开始）
    """
    lines = []
    mf = result.get("monthlyFortune", [])
    xy = result.get("xiaoYun", [])
    msp = result.get("monthlySpirits", [])

    if mf:
        now_year = datetime.now().year
        years_filter = None
        if recent_years is not None:
            years_filter = {str(now_year + i) for i in range(max(0, int(recent_years)))}

        lines.append(f"### 近期流月指引（近{recent_years}年）" if recent_years else "### 流月运势（全展开）")
        lines.append("")
        # 以 monthlySpirits 为事实来源展开（每条含 year/monthCn/ganZhi/spirits）
        if not msp:
            raise RuntimeError("流月神煞数据缺失: monthlySpirits 为空")
        rows: list[list[object]] = []
        for item in [x for x in msp if isinstance(x, dict)]:
            year = item.get("year", "")
            if years_filter is not None and str(year) not in years_filter:
                continue
            month_cn = item.get("monthCn", "") or ""
            gz = item.get("ganZhi", "") or ""
            sp = item.get("spirits", []) or []
            sp_txt = "、".join([str(x) for x in sp if str(x).strip()]) if sp else ""

            # 从 monthlyFortune 补齐十神/纳音（若能匹配到）
            ten_god = ""
            nayin = ""
            for m in mf:
                if not isinstance(m, dict):
                    continue
                if str(m.get("year")) == str(year) and str(m.get("ganZhi", "")) == str(gz):
                    ten_god = m.get("shiShen") or m.get("tenGod") or ""
                    nayin = m.get("naYin") or ""
                    break
            rows.append([year, f"{month_cn}月", gz, ten_god, nayin, sp_txt])

        lines.extend(_render_table(["年份", "月份", "干支", "十神", "纳音", "神煞"], rows))

    if xy:
        lines.append("### 小运")
        lines.append("")
        rows: list[list[object]] = []
        for item in [x for x in xy if isinstance(x, dict)]:
            age = item.get("age", "")
            year = item.get("year", "")
            gz = item.get("ganZhi", "")
            shi = item.get("shiShen", "") or ""
            ny = item.get("naYin", "") or ""
            sp = item.get("spirits", []) or []
            sp_txt = "、".join([str(x) for x in sp if str(x).strip()]) if sp else ""
            rows.append([f"{age}岁" if age != "" else "", year, gz, shi, ny, sp_txt])
        lines.extend(_render_table(["年龄", "年份", "干支", "十神", "纳音", "神煞"], rows))

    return "\n".join(lines)


def generate_jieqi_section(result: dict[str, Any]) -> str:
    """生成节气司令部分"""
    lines = []
    jq = result.get("jieqiDetail", {})
    sl = result.get("siling", {})

    if jq or sl:
        lines.append("## 节气司令")
        lines.append("")

        if jq:
            prev = jq.get("prevJieQi", {})
            next_ = jq.get("nextJieQi", {})
            if prev:
                lines.append("* 前节气（展开）：")
                if prev.get("name", ""):
                    lines.append(f"  - 名称：{prev.get('name', '')}")
                if prev.get("date", ""):
                    lines.append(f"  - 日期：{prev.get('date', '')}")
                if prev.get("daysAfter", "") != "":
                    lines.append(f"  - 已过：{prev.get('daysAfter', '')}天")
            if next_:
                lines.append("* 后节气（展开）：")
                if next_.get("name", ""):
                    lines.append(f"  - 名称：{next_.get('name', '')}")
                if next_.get("date", ""):
                    lines.append(f"  - 日期：{next_.get('date', '')}")
                if next_.get("daysBefore", "") != "":
                    lines.append(f"  - 还有：{next_.get('daysBefore', '')}天")

        if sl:
            lines.append(f"* 人元司令：{sl.get('current', '')}用事")
            detail = sl.get("detail", [])
            days_from = sl.get("daysFromJieqi", "")
            if detail:
                lines.append("* 司令分野（依据，展开）：")
                if days_from != "":
                    lines.append(f"  - 节后第：{days_from}天")
                for item in detail:
                    if not isinstance(item, dict):
                        continue
                    gan = item.get("gan", "")
                    days = item.get("days", "")
                    rng = item.get("range", "")
                    if gan:
                        lines.append(f"  - {gan}：")
                        if days != "":
                            lines.append(f"    - 天数：{days}天")
                        if rng:
                            lines.append(f"    - 范围：{rng}")
        lines.append("")

    return "\n".join(lines)


def generate_ziwei_section(result: dict[str, Any]) -> str:
    """生成紫微斗数部分"""
    lines = []
    zw = result.get("ziweiChart", {})
    pa = result.get("palaceAnalysis", [])

    if zw and zw.get("source"):
        lines.append("## 紫微斗数")
        lines.append("")
        lines.append(f"* 命局：{result.get('starInfluence', '')}")
        lines.append("* 星曜展示口径：星名（亮度/四化），缺失则留空")

        if pa:
            lines.append("")
            lines.append("### 十二宫")
            lines.append("")
            for p in pa:
                name = p.get("name", "")
                display_name = name if name.endswith("宫") else f"{name}宫"

                def _fmt_star(s: object) -> str:
                    if not isinstance(s, dict):
                        return str(s)
                    n = s.get("name", "")
                    br = s.get("brightness", "")
                    mu = s.get("mutagen", "")
                    meta = "/".join([x for x in [br, mu] if x])
                    return f"{n}（{meta}）" if meta else n

                majors = [_fmt_star(s) for s in (p.get("majorStars", []) or []) if s]
                minors = [_fmt_star(s) for s in (p.get("minorStars", []) or []) if s]
                adjs = [_fmt_star(s) for s in (p.get("adjectiveStars", []) or []) if s]
                stars = majors + minors + adjs
                if not stars:
                    lines.append(f"* {display_name}：-")
                    continue
                lines.append(f"* {display_name}：")
                for s in stars:
                    if s:
                        lines.append(f"  - {s}")
        lines.append("")

    return "\n".join(lines)


def generate_ziwei_basic_section(result: dict[str, Any]) -> str:
    """紫微基础信息"""
    lines = []
    zb = result.get("ziweiBasic", {})
    if zb:
        lines.append("## 紫微基础")
        lines.append("")
        mg = zb.get("mingGong", {})
        if mg:
            lines.append("* 命宫（展开）：")
            if mg.get("gong", ""):
                lines.append(f"  - 宫位：{mg.get('gong', '')}")
            if mg.get("dizhi", ""):
                lines.append(f"  - 地支：{mg.get('dizhi', '')}")
        tp = zb.get("twelvePalaces", [])
        if tp:
            lines.append("* 十二宫地支：")
            for p in tp:
                lines.append(f"  - {p.get('name', '')}：{p.get('dizhi', '')}")
        lines.append("")
    return "\n".join(lines)


def save_report(result: dict[str, Any], path: str) -> str:
    """保存报告到文件"""
    report = generate_full_report(result)
    if not path.endswith(".md"):
        path = path + ".md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(report)
    return path

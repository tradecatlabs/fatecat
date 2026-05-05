#!/usr/bin/env python3
"""
JSONL -> 文本报告转换小工具（最小改动版）
- 读取按分类的 JSONL（output_xxx.jsonl）
- 合并为单一 result dict
- 复用现有 report_generator 生成 Markdown 字符串
- 将内容写入 .txt（实为 Markdown 文本）
"""

import json
import sys
from pathlib import Path

sys.path.append("src")
from report_generator import generate_full_report  # noqa: E402


def load_jsonl(path: str) -> dict:
    """加载 JSONL，按行合并 data 字段"""
    merged = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            merged.update(obj.get("data", {}))
    return merged


def main(jsonl_path: str, out_path: str | None):
    """从 JSONL 生成报告文本；默认写入 output/txt 下"""
    in_path = Path(jsonl_path)
    if out_path is None:
        stem = in_path.stem
        out_path = Path("output/txt") / f"{stem}.txt"
    else:
        out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    data = load_jsonl(jsonl_path)
    raw = generate_full_report(data)
    report = _filter_txt(raw)
    out_path.write_text(report, encoding="utf-8")


def _filter_txt(md: str) -> str:
    """
    TXT 专用过滤器（保持原生内容）
    - 先前为防止模块泄露曾做过裁剪，现改为透明直通，避免任何截断
    - 需要隐藏的模块统一由 report_generator.HIDE 控制，避免双重过滤造成误判
    """
    return md


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python jsonl_to_txt.py <input.jsonl> [output.txt]")
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else None
    main(src, dst)

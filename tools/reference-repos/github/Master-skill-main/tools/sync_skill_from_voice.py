#!/usr/bin/env python3
"""
Sync SKILL.md PART B from voice.md (single source of truth).

SKILL.md contains voice.md content inlined as PART B. When voice.md changes,
SKILL.md must be regenerated to keep them in sync.

Usage:
    python3 tools/sync_skill_from_voice.py --all         # sync all masters
    python3 tools/sync_skill_from_voice.py --slug xuyun  # sync one master
    python3 tools/sync_skill_from_voice.py --verify      # check sync status only
"""

import argparse
import os
import re
import sys
from pathlib import Path

PREBUILT_DIR = Path(__file__).parent.parent / "prebuilt"

# Section markers in SKILL.md
PART_B_START = "## PART B — 说法风格"
PART_C_START = "## 运行规则"


def sync_one(slug: str, verify_only: bool = False) -> bool:
    """Sync one master's SKILL.md PART B from voice.md.

    Returns True if in sync (or successfully synced), False if mismatch found
    in verify mode.
    """
    master_dir = PREBUILT_DIR / slug
    voice_path = master_dir / "voice.md"
    skill_path = master_dir / "SKILL.md"

    if not voice_path.exists() or not skill_path.exists():
        print(f"[SKIP] {slug}: missing voice.md or SKILL.md")
        return False

    voice_content = voice_path.read_text(encoding="utf-8")
    skill_content = skill_path.read_text(encoding="utf-8")

    # Voice.md starts with a # Title line. Skip it.
    voice_lines = voice_content.split("\n")
    if voice_lines and voice_lines[0].startswith("# "):
        voice_body = "\n".join(voice_lines[1:]).lstrip("\n")
    else:
        voice_body = voice_content

    # Find PART B and 运行规则 boundaries
    b_idx = skill_content.find(PART_B_START)
    c_idx = skill_content.find(PART_C_START)

    if b_idx == -1 or c_idx == -1:
        print(f"[ERR] {slug}: cannot find PART B or 运行规则 markers")
        return False

    # Build new SKILL.md
    # Keep everything up to and including PART B header + blank line
    header = skill_content[:b_idx] + PART_B_START + "\n\n"
    # Insert voice.md body
    new_part_b = voice_body.rstrip() + "\n\n"
    # Append everything from 运行规则 onwards
    tail = skill_content[c_idx:]

    new_skill_content = header + new_part_b + tail

    if verify_only:
        if new_skill_content != skill_content:
            print(f"[OUT OF SYNC] {slug}")
            return False
        else:
            print(f"[OK] {slug}")
            return True

    if new_skill_content != skill_content:
        skill_path.write_text(new_skill_content, encoding="utf-8")
        print(f"[SYNCED] {slug}")
    else:
        print(f"[OK] {slug}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Sync SKILL.md PART B from voice.md")
    parser.add_argument("--slug", help="Sync one specific master")
    parser.add_argument("--all", action="store_true", help="Sync all masters")
    parser.add_argument("--verify", action="store_true", help="Only verify, don't modify")
    args = parser.parse_args()

    if args.slug:
        slugs = [args.slug]
    elif args.all or args.verify:
        slugs = sorted(
            d.name for d in PREBUILT_DIR.iterdir()
            if d.is_dir() and (d / "voice.md").exists()
        )
    else:
        parser.print_help()
        return 1

    all_ok = True
    for slug in slugs:
        if not sync_one(slug, verify_only=args.verify):
            all_ok = False

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())

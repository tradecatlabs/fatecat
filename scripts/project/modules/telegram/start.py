#!/usr/bin/env python3
"""FateCat Telegram 模块启动脚本"""

import subprocess
import sys
from pathlib import Path


def _run_subprocess(command: list[str]) -> int:
    completed = subprocess.run(command, check=False)
    return completed.returncode


def main() -> int:
    src_dir = Path(__file__).parent / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    from branding import build_branding_text

    print(build_branding_text(compact=False))
    print("")

    if len(sys.argv) < 2:
        print("用法:")
        print("  python start.py bot     # 启动 Telegram Bot")
        print("  python start.py api     # 启动 FastAPI 接口")
        print("  python start.py both    # 同时启动 Bot 和 API")
        return 2

    mode = sys.argv[1]

    if mode == "bot":
        print("🤖 启动 Telegram Bot...")
        return _run_subprocess([sys.executable, str(src_dir / "bot.py")])

    elif mode == "api":
        print("🚀 启动 FastAPI 接口...")
        return _run_subprocess([sys.executable, str(src_dir / "main.py")])

    elif mode == "both":
        print("🚀 同时启动 Bot 和 API...")
        import threading

        results = {"bot": 0, "api": 0}

        def run_bot():
            results["bot"] = _run_subprocess([sys.executable, str(src_dir / "bot.py")])

        def run_api():
            results["api"] = _run_subprocess([sys.executable, str(src_dir / "main.py")])

        bot_thread = threading.Thread(target=run_bot)
        api_thread = threading.Thread(target=run_api)

        bot_thread.start()
        api_thread.start()

        bot_thread.join()
        api_thread.join()
        return max(results.values())

    else:
        print(f"❌ 未知模式: {mode}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

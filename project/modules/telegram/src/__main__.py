"""
FateCat Telegram module entry point.

Usage:
    python -m modules.telegram.src bot   # Start Telegram Bot
    python -m modules.telegram.src api   # Start FastAPI server
    python -m modules.telegram.src both  # Start both
"""

import sys
from pathlib import Path

# Ensure src directory is in path
SRC_DIR = Path(__file__).parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        print("Available commands: bot, api, both")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "bot":
        from bot import main as bot_main

        bot_main()
    elif mode == "api":
        from main import main as api_main

        api_main()
    elif mode == "both":
        import threading

        from bot import main as bot_main
        from main import main as api_main

        bot_thread = threading.Thread(target=bot_main)
        api_thread = threading.Thread(target=api_main)

        bot_thread.start()
        api_thread.start()

        bot_thread.join()
        api_thread.join()
    else:
        print(f"Unknown mode: {mode}")
        print("Available commands: bot, api, both")
        sys.exit(1)


if __name__ == "__main__":
    main()

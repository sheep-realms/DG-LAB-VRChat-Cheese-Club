#!/usr/bin/env python3
"""芝士郊狼控制软件 - Cheese DGLAB Controller"""

import os
import sys

# Force matplotlib to use TkAgg backend before any matplotlib import
os.environ["MPLBACKEND"] = "TkAgg"
os.environ["QT_QPA_PLATFORM"] = "offscreen"
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def main():
    try:
        from app import App
        app = App()
        app.run()
    except ImportError as e:
        print(f"缺少依赖库: {e}")
        print("请运行: pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n已退出")


if __name__ == "__main__":
    main()

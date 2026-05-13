#!/usr/bin/env python3
"""芝士郊狼控制软件 - Cheese DGLAB Controller"""

import os
import sys

# Enable high DPI awareness before tkinter loads
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

# Force matplotlib to use TkAgg backend before any matplotlib import
os.environ["MPLBACKEND"] = "TkAgg"
os.environ["QT_QPA_PLATFORM"] = "offscreen"
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei UI', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
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

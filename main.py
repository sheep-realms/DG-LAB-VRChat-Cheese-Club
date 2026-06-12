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

# 加载自定义字体 (MiSans)
FONT_FAMILY_REGISTERED = "MiSans Normal"


def _get_font_dir():
    """获取字体目录路径。"""
    if getattr(sys, 'frozen', False):
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "fonts")


def _load_custom_font():
    """在 Windows 上注册 MiSans 字体供本进程使用（GDI 层面）。
    必须在 Tk 初始化之前调用，这样 Tk 创建字体时能通过 CreateFont 找到它。
    """
    if sys.platform != "win32":
        return
    font_path = os.path.join(_get_font_dir(), "MiSans-Normal.otf")
    if not os.path.exists(font_path):
        return
    try:
        import ctypes
        gdi32 = ctypes.windll.gdi32
        # FR_PRIVATE = 0x10 — 仅当前进程可见，进程退出自动移除，不污染系统
        gdi32.AddFontResourceExW(font_path, 0x10, 0)
    except Exception:
        pass

_load_custom_font()

# Force matplotlib to use TkAgg backend before any matplotlib import
os.environ["MPLBACKEND"] = "TkAgg"
os.environ["QT_QPA_PLATFORM"] = "offscreen"
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['MiSans Normal', 'MiSans', 'Microsoft YaHei UI', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def _kill_old_instances():
    """Kill any already-running instances of this EXE (avoid accumulating orphans)."""
    import subprocess, re
    my_pid = str(os.getpid())
    try:
        result = subprocess.run(
            ["tasklist", "/FI", 'IMAGENAME eq DG-LAB_VRChat_Controller*.exe', "/FO", "CSV"],
            capture_output=True, text=True, timeout=5,
        )
        for line in result.stdout.strip().split("\n")[1:]:
            pid_match = re.search(r'"(\d+)"', line)
            if pid_match:
                pid = pid_match.group(1)
                if pid == my_pid:
                    continue  # 补药自杀
                subprocess.run(["taskkill", "/F", "/PID", pid],
                             capture_output=True, timeout=3)
    except Exception:
        pass


def main():
    _kill_old_instances()
    try:
        from app import App
        app = App()
        app.run()
    except SystemExit:
        raise  # Let sys.exit() pass through

    except ImportError as e:
        print(f"缺少依赖库: {e}")
        print("请运行: pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n已退出")


if __name__ == "__main__":
    main()

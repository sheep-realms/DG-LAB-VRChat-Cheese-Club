import os
import re
import time
import threading
from pathlib import Path
from typing import Callable, Optional


SHOCK_PATTERN = re.compile(
    r"\[DGLABCheeseShocking\]LocalShocking调用[:：]\s*mode=(\w+),\s*seconds=(\d+),\s*hand=(\w+)"
)


class LogMonitor:
    def __init__(
        self,
        on_shock_event: Callable[[dict], None],
        on_log_line: Callable[[str], None],
        log_dir: str = "",
        poll_interval: float = 0.5,
        idle_check_interval: float = 5.0,
    ):
        self._on_shock = on_shock_event
        self._on_log_line = on_log_line
        self._poll_interval = poll_interval
        self._idle_check_interval = idle_check_interval

        if log_dir:
            self._log_dir = Path(log_dir)
        else:
            self._log_dir = Path.home() / "AppData" / "LocalLow" / "VRChat" / "VRChat"

        self._current_file: Optional[Path] = None
        self._file_position: int = 0
        self._last_activity_time: float = time.time()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def _find_latest_log(self) -> Optional[Path]:
        if not self._log_dir.exists():
            return None
        log_files = sorted(
            self._log_dir.glob("output_log_*.txt"),
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )
        return log_files[0] if log_files else None

    def _check_for_newer_file(self) -> Optional[Path]:
        latest = self._find_latest_log()
        if latest and self._current_file and latest != self._current_file:
            return latest
        return None

    def _read_new_lines(self) -> list[str]:
        if not self._current_file or not self._current_file.exists():
            return []
        lines = []
        try:
            with open(self._current_file, "rb") as f:
                f.seek(self._file_position)
                data = f.read()
                self._file_position = f.tell()
                if data:
                    text = data.decode("utf-8", errors="replace")
                    for line in text.splitlines():
                        lines.append(line)
        except OSError:
            pass
        return lines

    def _process_line(self, line: str):
        self._on_log_line(line)
        match = SHOCK_PATTERN.search(line)
        if match:
            event = {
                "mode": match.group(1),
                "seconds": int(match.group(2)),
                "hand": match.group(3),
            }
            self._on_shock(event)

    def _monitor_loop(self):
        while not self._stop_event.is_set():
            # Find initial file if not set
            if self._current_file is None or not self._current_file.exists():
                self._current_file = self._find_latest_log()
                if self._current_file:
                    # Start from end of file - ignore old content
                    try:
                        self._file_position = self._current_file.stat().st_size
                    except OSError:
                        self._file_position = 0
                    self._on_log_line(f"[日志] 开始监控: {self._current_file.name}")

            # Read new lines
            new_lines = self._read_new_lines()
            if new_lines:
                self._last_activity_time = time.time()
                for line in new_lines:
                    self._process_line(line)

            # Check for newer log file if idle
            elapsed = time.time() - self._last_activity_time
            if elapsed >= self._idle_check_interval:
                newer = self._check_for_newer_file()
                if newer:
                    self._on_log_line(f"[日志] 检测到新日志文件: {newer.name}")
                    self._current_file = newer
                    try:
                        self._file_position = newer.stat().st_size
                    except OSError:
                        self._file_position = 0
                    self._last_activity_time = time.time()

            self._stop_event.wait(self._poll_interval)

    def start(self):
        if self._running:
            return
        self._running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2)
            self._thread = None

    @property
    def current_file(self) -> Optional[Path]:
        return self._current_file

    @property
    def log_dir(self) -> Path:
        return self._log_dir

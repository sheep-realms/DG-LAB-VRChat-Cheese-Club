from gui.fonts import UI_XS, UI_S, UI_S_B, UI_M, UI_M_B, MONO_S
import tkinter as tk
from datetime import datetime


class ConsolePanel(tk.Frame):
    def __init__(self, master, theme: dict = None, **kwargs):
        self._theme = theme or {}
        super().__init__(master, bg=self._theme.get("bg_panel", "#111827"), **kwargs)
        self._max_lines = 300
        self._build()

    def _build(self):
        t = self._theme

        # Container with border
        container = tk.Frame(self, bg=t.get("bg_card", "#151d2b"),
                            highlightbackground=t.get("border_color", "#1e293b"),
                            highlightthickness=1)
        container.pack(fill="both", expand=True, padx=4, pady=4)

        # Header
        header = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        header.pack(fill="x", padx=12, pady=(12, 8))

        tk.Label(
            header, text="日志",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_primary", "#f1f5f9"),
            font=(UI_M_B), anchor="w",
        ).pack(side="left")

        # Action buttons
        btn_frame = tk.Frame(header, bg=t.get("bg_card", "#151d2b"))
        btn_frame.pack(side="right")

        self._show_debug = False
        self._debug_btn = tk.Button(
            btn_frame, text="Debug",
            bg=t.get("bg_input", "#0f1520"),
            fg=t.get("text_muted", "#475569"),
            activebackground=t.get("border_color", "#1e293b"),
            activeforeground=t.get("text_primary", "#f1f5f9"),
            font=(UI_XS), relief="flat", cursor="hand2",
            command=self._toggle_debug,
        )
        self._debug_btn.pack(side="left", padx=(0, 4))

        self._clear_btn = tk.Button(
            btn_frame, text="清空",
            bg=t.get("bg_input", "#0f1520"),
            fg=t.get("text_secondary", "#94a3b8"),
            activebackground=t.get("border_color", "#1e293b"),
            activeforeground=t.get("text_primary", "#f1f5f9"),
            font=(UI_XS), relief="flat", cursor="hand2",
            command=self._clear,
        )
        self._clear_btn.pack(side="left")

        # Console text area
        text_frame = tk.Frame(container, bg=t.get("console_bg", "#0c1017"))
        text_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self._text = tk.Text(
            text_frame,
            bg=t.get("console_bg", "#0c1017"),
            fg=t.get("console_text", "#94a3b8"),
            font=(MONO_S), relief="flat", wrap="word",
            insertbackground=t.get("text_primary", "#f1f5f9"),
            selectbackground=t.get("accent_blue", "#3b82f6"),
            state="disabled", height=8,
            highlightbackground=t.get("border_color", "#1e293b"),
            highlightthickness=1,
        )
        self._scrollbar = tk.Scrollbar(
            text_frame, command=self._text.yview,
            bg=t.get("bg_card", "#151d2b"),
            troughcolor=t.get("console_bg", "#0c1017"),
            highlightbackground=t.get("border_color", "#1e293b"),
        )
        self._text.configure(yscrollcommand=self._scrollbar.set)

        self._scrollbar.pack(side="right", fill="y", padx=(0, 0), pady=0)
        self._text.pack(side="left", fill="both", expand=True, padx=0, pady=0)

        self._apply_tags()

    def _apply_tags(self):
        t = self._theme
        self._text.tag_configure("timestamp", foreground=t.get("text_muted", "#475569"))
        self._text.tag_configure("info", foreground=t.get("console_info", "#60a5fa"))
        self._text.tag_configure("warning", foreground=t.get("console_warning", "#fbbf24"))
        self._text.tag_configure("error", foreground=t.get("console_error", "#f87171"))
        self._text.tag_configure("shock", foreground=t.get("accent_violet", "#a78bfa"))
        self._text.tag_configure("recv", foreground=t.get("console_success", "#34d399"))
        self._text.tag_configure("debug", foreground=t.get("text_muted", "#475569"))

    def apply_theme(self, theme: dict):
        self._theme = theme
        t = theme
        self.configure(bg=t.get("bg_panel", "#111827"))
        for w in self._get_all_widgets():
            try:
                bg = t.get("bg_card", "#151d2b")
                fg = t.get("text_primary", "#f1f5f9")
                if isinstance(w, tk.Text):
                    w.configure(bg=t.get("console_bg", "#0c1017"),
                                fg=t.get("console_text", "#94a3b8"),
                                insertbackground=fg,
                                selectbackground=t.get("accent_blue", "#3b82f6"),
                                highlightbackground=t.get("border_color", "#1e293b"))
                elif isinstance(w, tk.Button):
                    w.configure(bg=t.get("bg_input", "#0f1520"), fg=t.get("text_secondary", "#94a3b8"),
                                activebackground=t.get("border_color", "#1e293b"))
                elif isinstance(w, tk.Scrollbar):
                    w.configure(bg=t.get("bg_card", "#151d2b"),
                                troughcolor=t.get("console_bg", "#0c1017"))
                elif isinstance(w, tk.Frame):
                    w.configure(bg=bg)
                elif isinstance(w, tk.Label):
                    w.configure(bg=bg, fg=fg)
            except (tk.TclError, KeyError):
                pass
        self._apply_tags()

    def _get_all_widgets(self):
        widgets = []
        stack = [self]
        while stack:
            w = stack.pop()
            widgets.append(w)
            stack.extend(w.winfo_children())
        return widgets

    def append(self, text: str, tag: str = "info"):
        if tag == "debug" and not self._show_debug:
            return
        now = datetime.now().strftime("%H:%M:%S")
        self._text.configure(state="normal")
        self._text.insert("end", f"[{now}] ", "timestamp")
        self._text.insert("end", f"{text}\n", tag)
        line_count = int(self._text.index("end-1c").split(".")[0])
        if line_count > self._max_lines:
            self._text.delete("1.0", f"{line_count - self._max_lines}.0")
        self._text.see("end")
        self._text.configure(state="disabled")

    def _toggle_debug(self):
        self._show_debug = not self._show_debug
        t = self._theme
        if self._show_debug:
            self._debug_btn.configure(fg=t.get("accent_cyan", "#06b6d4"))
        else:
            self._debug_btn.configure(fg=t.get("text_muted", "#475569"))

    def _clear(self):
        self._text.configure(state="normal")
        self._text.delete("1.0", "end")
        self._text.configure(state="disabled")

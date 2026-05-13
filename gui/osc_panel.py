from gui.fonts import UI_XS, UI_S, UI_S_B, UI_M, UI_M_B, MONO_S
import tkinter as tk


class OSCPanel(tk.Frame):
    def __init__(self, master, theme: dict = None, on_osc_toggle=None, **kwargs):
        self._theme = theme or {}
        super().__init__(master, bg=self._theme.get("bg_panel", "#111827"), **kwargs)
        self._on_toggle = on_osc_toggle or (lambda connected: None)
        self._connected = False
        self._build()

    def _build(self):
        t = self._theme

        # Container with border
        container = tk.Frame(self, bg=t.get("bg_card", "#151d2b"),
                            highlightbackground=t.get("border_color", "#1e293b"),
                            highlightthickness=1)
        container.pack(fill="x", padx=4, pady=4)

        # Header
        header = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        header.pack(fill="x", padx=12, pady=(12, 8))

        tk.Label(
            header, text="VRChat OSC",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_primary", "#f1f5f9"),
            font=(UI_M_B), anchor="w",
        ).pack(side="left")

        # Status
        status_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        status_frame.pack(fill="x", padx=12, pady=(0, 8))

        self._status_dot = tk.Canvas(status_frame, width=10, height=10,
                                     bg=t.get("bg_card", "#151d2b"), highlightthickness=0)
        self._status_dot.pack(side="left", padx=(0, 8))
        self._draw_dot(t.get("status_offline", "#6b7280"))

        self._status_label = tk.Label(
            status_frame, text="未连接",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_secondary", "#94a3b8"),
            font=(UI_S),
        )
        self._status_label.pack(side="left")

        # Chatbox port
        port_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        port_frame.pack(fill="x", padx=12, pady=(0, 8))

        tk.Label(
            port_frame, text="Chatbox端口",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_dim", "#64748b"),
            font=(UI_S),
        ).pack(side="left")

        self._chatbox_port_var = tk.StringVar(value="9000")
        self._chatbox_port_entry = tk.Entry(
            port_frame, textvariable=self._chatbox_port_var,
            bg=t.get("bg_input", "#0f1520"),
            fg=t.get("text_primary", "#f1f5f9"),
            insertbackground=t.get("text_primary", "#f1f5f9"),
            font=(MONO_S), relief="flat", width=6,
            highlightbackground=t.get("border_color", "#1e293b"),
            highlightthickness=1,
        )
        self._chatbox_port_entry.pack(side="left", padx=(8, 0))

        # Avatar OSC port
        avt_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        avt_frame.pack(fill="x", padx=12, pady=(0, 8))

        tk.Label(
            avt_frame, text="Avatar端口",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_dim", "#64748b"),
            font=(UI_S),
        ).pack(side="left")

        self._avatar_port_var = tk.StringVar(value="9001")
        tk.Label(
            avt_frame, text="9001 (固定)",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_muted", "#475569"),
            font=(UI_S),
        ).pack(side="left", padx=(8, 0))

        # Mode selection (A/B)
        mode_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        mode_frame.pack(fill="x", padx=12, pady=(0, 8))

        # Channel A mode
        ch_a = tk.Frame(mode_frame, bg=t.get("bg_card", "#151d2b"))
        ch_a.pack(fill="x", pady=(0, 4))
        tk.Label(
            ch_a, text="A",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("accent_emerald", "#34d399"),
            font=(UI_S_B), width=2,
        ).pack(side="left")
        self._mode_a_var = tk.StringVar(value="distance")
        for txt, val in [("距离", "distance"), ("电击", "shock"), ("触感", "touch")]:
            tk.Radiobutton(
                ch_a, text=txt, variable=self._mode_a_var, value=val,
                bg=t.get("bg_card", "#151d2b"),
                fg=t.get("text_secondary", "#94a3b8"),
                selectcolor=t.get("bg_input", "#0f1520"),
                activebackground=t.get("bg_card", "#151d2b"),
                activeforeground=t.get("text_primary", "#f1f5f9"),
                font=(UI_XS), relief="flat",
            ).pack(side="left", padx=(4, 0))

        # Channel B mode
        ch_b = tk.Frame(mode_frame, bg=t.get("bg_card", "#151d2b"))
        ch_b.pack(fill="x")
        tk.Label(
            ch_b, text="B",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("accent_amber", "#fbbf24"),
            font=(UI_S_B), width=2,
        ).pack(side="left")
        self._mode_b_var = tk.StringVar(value="distance")
        for txt, val in [("距离", "distance"), ("电击", "shock"), ("触感", "touch")]:
            tk.Radiobutton(
                ch_b, text=txt, variable=self._mode_b_var, value=val,
                bg=t.get("bg_card", "#151d2b"),
                fg=t.get("text_secondary", "#94a3b8"),
                selectcolor=t.get("bg_input", "#0f1520"),
                activebackground=t.get("bg_card", "#151d2b"),
                activeforeground=t.get("text_primary", "#f1f5f9"),
                font=(UI_XS), relief="flat",
            ).pack(side="left", padx=(4, 0))

        # Buttons
        btn_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        btn_frame.pack(fill="x", padx=12, pady=(0, 12))

        self._connect_btn = tk.Button(
            btn_frame, text="连接",
            bg=t.get("bg_button_success", "#059669"),
            fg="#ffffff",
            activebackground=t.get("bg_button_success_hover", "#10b981"),
            font=(UI_S_B), relief="flat",
            cursor="hand2", command=self._on_connect_click, width=10,
        )
        self._connect_btn.pack(side="left", padx=(0, 8))

        self._disconnect_btn = tk.Button(
            btn_frame, text="关闭Chatbox",
            bg=t.get("bg_button_danger", "#dc2626"),
            fg="#ffffff",
            activebackground=t.get("bg_button_danger_hover", "#ef4444"),
            font=(UI_S), relief="flat",
            cursor="hand2", command=self._on_disconnect_click,
            state="disabled",
        )
        self._disconnect_btn.pack(side="left")

        # Received parameter display
        param_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        param_frame.pack(fill="x", padx=12, pady=(0, 12))

        tk.Label(
            param_frame, text="接收参数",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_dim", "#64748b"),
            font=(UI_XS),
        ).pack(anchor="w")

        self._param_label = tk.Label(
            param_frame, text="--",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("accent_cyan", "#06b6d4"),
            font=(MONO_S), anchor="w", justify="left",
            wraplength=260,
        )
        self._param_label.pack(anchor="w", pady=(4, 0))

    def _draw_dot(self, color: str):
        self._status_dot.delete("all")
        self._status_dot.create_oval(2, 2, 8, 8, fill=color, outline=color)

    def _on_connect_click(self):
        self._connect_btn.configure(state="disabled")
        self._disconnect_btn.configure(state="normal")
        self._connected = True
        self._status_label.configure(text="连接中...")
        self._draw_dot(self._theme.get("status_warning", "#f59e0b"))
        self._on_toggle(True)

    def _on_disconnect_click(self):
        self._connect_btn.configure(state="normal")
        self._disconnect_btn.configure(state="disabled")
        self._connected = False
        self._status_label.configure(text="未连接")
        self._draw_dot(self._theme.get("status_offline", "#6b7280"))
        self._param_label.configure(text="--")
        self._on_toggle(False)

    def set_status(self, status: str):
        t = self._theme
        status_map = {
            "connecting": (t.get("status_warning", "#f59e0b"), "连接中..."),
            "connected": (t.get("status_online", "#10b981"), "已连接"),
            "disconnected": (t.get("status_offline", "#6b7280"), "未连接"),
        }
        color, text = status_map.get(status, (t.get("status_offline", "#6b7280"), "未知"))
        self._draw_dot(color)
        self._status_label.configure(text=text)

        if status == "disconnected":
            self._connect_btn.configure(state="normal")
            self._disconnect_btn.configure(state="disabled")
            self._connected = False
        elif status in ("connected", "connecting"):
            self._connect_btn.configure(state="disabled")
            self._disconnect_btn.configure(state="normal")

    def update_params(self, params: dict):
        if not params:
            self._param_label.configure(text="--")
            return
        lines = [f"{k}: {v}" for k, v in params.items()]
        self._param_label.configure(text="\n".join(lines[:6]))

    def get_chatbox_port(self) -> int:
        try:
            val = int(self._chatbox_port_var.get().strip())
            return max(1, min(65535, val))
        except ValueError:
            return 9000

    def set_chatbox_port(self, port: int):
        port = max(1, min(65535, int(port)))
        self._chatbox_port_var.set(str(port))

    def get_avatar_port(self) -> int:
        return 9001

    def set_avatar_port(self, port: int):
        pass

    def get_mode_a(self) -> str:
        return self._mode_a_var.get()

    def set_mode_a(self, mode: str):
        self._mode_a_var.set(mode)

    def get_mode_b(self) -> str:
        return self._mode_b_var.get()

    def set_mode_b(self, mode: str):
        self._mode_b_var.set(mode)

    @property
    def is_connected(self) -> bool:
        return self._connected

    def apply_theme(self, theme: dict):
        self._theme = theme
        t = theme
        self.configure(bg=t.get("bg_panel", "#111827"))
        for w in self._get_all_widgets():
            try:
                bg = t.get("bg_card", "#151d2b")
                fg = t.get("text_primary", "#f1f5f9")
                if isinstance(w, tk.Canvas):
                    w.configure(bg=bg)
                elif isinstance(w, tk.Button):
                    txt = str(w.cget("text"))
                    if txt == "关闭Chatbox":
                        w.configure(bg=t.get("bg_button_danger", "#dc2626"), fg="#ffffff",
                                    activebackground=t.get("bg_button_danger_hover", "#ef4444"))
                    else:
                        w.configure(bg=t.get("bg_button_success", "#059669"), fg="#ffffff",
                                    activebackground=t.get("bg_button_success_hover", "#10b981"))
                elif isinstance(w, tk.Entry):
                    w.configure(bg=t.get("bg_input", "#0f1520"), fg=fg, insertbackground=fg,
                                highlightbackground=t.get("border_color", "#1e293b"))
                elif isinstance(w, tk.Frame):
                    w.configure(bg=bg)
                elif isinstance(w, tk.Label):
                    current_fg = str(w.cget("fg"))
                    if current_fg in ["#f1f5f9", "#e6edf3"]:
                        w.configure(bg=bg, fg=fg)
                    elif "34d399" in current_fg or "3fb950" in current_fg:
                        w.configure(bg=bg, fg=t.get("accent_emerald", "#34d399"))
                    elif "fbbf24" in current_fg or "d29922" in current_fg:
                        w.configure(bg=bg, fg=t.get("accent_amber", "#fbbf24"))
                    else:
                        w.configure(bg=bg, fg=t.get("text_dim", "#64748b"))
                elif isinstance(w, tk.Radiobutton):
                    w.configure(bg=bg, fg=t.get("text_secondary", "#94a3b8"),
                                selectcolor=t.get("bg_input", "#0f1520"),
                                activebackground=bg)
            except (tk.TclError, KeyError):
                pass

    def _get_all_widgets(self):
        widgets = []
        stack = [self]
        while stack:
            w = stack.pop()
            widgets.append(w)
            stack.extend(w.winfo_children())
        return widgets

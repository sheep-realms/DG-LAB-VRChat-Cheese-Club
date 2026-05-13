from gui.fonts import UI_XS, UI_S, UI_S_B, UI_M, UI_M_B, UI_L, MONO_S, MONO_M_B
import tkinter as tk
from waveform_library import get_names


class SettingsPanel(tk.Frame):
    def __init__(self, master, theme: dict = None, on_settings_change=None, on_theme_toggle=None, on_test_shock=None, **kwargs):
        self._theme = theme or {}
        super().__init__(master, bg=self._theme.get("bg_panel", "#111827"), **kwargs)
        self._on_change = on_settings_change or (lambda: None)
        self._on_theme_toggle = on_theme_toggle or (lambda: None)
        self._on_test_shock = on_test_shock or (lambda: None)
        self._build()

    def _build(self):
        t = self._theme

        # Main container
        container = tk.Frame(self, bg=t.get("bg_card", "#151d2b"),
                            highlightbackground=t.get("border_color", "#1e293b"),
                            highlightthickness=1)
        container.pack(fill="x", padx=4, pady=4)

        # Header
        header = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        header.pack(fill="x", padx=12, pady=(12, 8))

        tk.Label(
            header, text="电击设置",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_primary", "#f1f5f9"),
            font=(UI_M_B), anchor="w",
        ).pack(side="left")

        self._theme_btn = tk.Button(
            header, text="主题",
            bg=t.get("bg_button", "#2563eb"),
            fg="#ffffff",
            activebackground=t.get("bg_button_hover", "#3b82f6"),
            font=(UI_XS), relief="flat", cursor="hand2",
            command=self._on_theme_toggle, width=6,
        )
        self._theme_btn.pack(side="right")

        # Channel A limit
        a_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        a_frame.pack(fill="x", padx=12, pady=(0, 8))

        tk.Label(
            a_frame, text="A上限",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("accent_emerald", "#34d399"),
            font=(UI_S_B),
        ).pack(side="left")

        self._a_limit_var = tk.IntVar(value=200)
        self._a_limit_label = tk.Label(
            a_frame, text="200",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("accent_emerald", "#34d399"),
            font=(MONO_M_B), width=4,
        )
        self._a_limit_label.pack(side="right")

        self._a_limit_scale = tk.Scale(
            a_frame, from_=0, to=200, orient="horizontal",
            variable=self._a_limit_var, command=self._on_a_limit_change,
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_secondary", "#94a3b8"),
            troughcolor=t.get("bg_slider_trough", "#1e293b"),
            highlightthickness=0, sliderrelief="flat", length=180,
        )
        self._a_limit_scale.pack(side="right", padx=(8, 8))

        # Channel B limit
        b_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        b_frame.pack(fill="x", padx=12, pady=(0, 8))

        tk.Label(
            b_frame, text="B上限",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("accent_amber", "#fbbf24"),
            font=(UI_S_B),
        ).pack(side="left")

        self._b_limit_var = tk.IntVar(value=200)
        self._b_limit_label = tk.Label(
            b_frame, text="200",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("accent_amber", "#fbbf24"),
            font=(MONO_M_B), width=4,
        )
        self._b_limit_label.pack(side="right")

        self._b_limit_scale = tk.Scale(
            b_frame, from_=0, to=200, orient="horizontal",
            variable=self._b_limit_var, command=self._on_b_limit_change,
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_secondary", "#94a3b8"),
            troughcolor=t.get("bg_slider_trough", "#1e293b"),
            highlightthickness=0, sliderrelief="flat", length=180,
        )
        self._b_limit_scale.pack(side="right", padx=(8, 8))

        # Current strength display
        strength_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        strength_frame.pack(fill="x", padx=12, pady=(0, 12))

        tk.Label(
            strength_frame, text="当前强度",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_dim", "#64748b"),
            font=(UI_XS),
        ).pack(side="left")

        self._a_label = tk.Label(
            strength_frame, text="A: 0",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("accent_emerald", "#34d399"),
            font=(MONO_S),
        )
        self._a_label.pack(side="left", padx=(8, 16))

        self._b_label = tk.Label(
            strength_frame, text="B: 0",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("accent_amber", "#fbbf24"),
            font=(MONO_S),
        )
        self._b_label.pack(side="left")

        # Mode selection
        mode_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        mode_frame.pack(fill="x", padx=12, pady=(0, 12))

        tk.Label(
            mode_frame, text="模式",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_dim", "#64748b"),
            font=(UI_XS),
        ).pack(side="left")

        self._mode_var = tk.StringVar(value="instant")
        modes = [
            ("一键开火", "instant"),
            ("温柔加力", "gradual"),
            ("拉满", "max"),
        ]

        for text, value in modes:
            rb = tk.Radiobutton(
                mode_frame, text=text, variable=self._mode_var, value=value,
                bg=t.get("bg_card", "#151d2b"),
                fg=t.get("text_secondary", "#94a3b8"),
                selectcolor=t.get("bg_input", "#0f1520"),
                activebackground=t.get("bg_card", "#151d2b"),
                activeforeground=t.get("text_primary", "#f1f5f9"),
                font=(UI_S), relief="flat",
                command=self._on_change,
            )
            rb.pack(side="left", padx=(8, 0))

        # Waveform mode
        wf_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        wf_frame.pack(fill="x", padx=12, pady=(0, 12))

        tk.Label(
            wf_frame, text="波形",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_dim", "#64748b"),
            font=(UI_XS),
        ).pack(side="left")

        self._wf_var = tk.StringVar(value="library")
        wf_modes = [
            ("波形库", "library"),
            ("自定义", "custom"),
        ]

        for text, value in wf_modes:
            rb = tk.Radiobutton(
                wf_frame, text=text, variable=self._wf_var, value=value,
                bg=t.get("bg_card", "#151d2b"),
                fg=t.get("text_secondary", "#94a3b8"),
                selectcolor=t.get("bg_input", "#0f1520"),
                activebackground=t.get("bg_card", "#151d2b"),
                activeforeground=t.get("text_primary", "#f1f5f9"),
                font=(UI_S), relief="flat",
                command=self._on_wf_mode_change,
            )
            rb.pack(side="left", padx=(8, 0))

        # Custom waveform preset dropdown (hidden by default)
        self._wf_names = get_names()
        self._custom_wf_group = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))

        tk.Label(
            self._custom_wf_group, text="选择波形",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_dim", "#64748b"),
            font=(UI_XS),
        ).pack(anchor="w")

        self._custom_wf_var = tk.StringVar(value=self._wf_names[0] if self._wf_names else "")
        self._custom_wf_menu = tk.OptionMenu(
            self._custom_wf_group, self._custom_wf_var, *self._wf_names,
        )
        self._custom_wf_menu.configure(
            bg=t.get("bg_input", "#0f1520"),
            fg=t.get("text_primary", "#f1f5f9"),
            activebackground=t.get("bg_button_hover", "#3b82f6"),
            activeforeground=t.get("text_primary", "#f1f5f9"),
            highlightthickness=0, relief="flat",
            font=(UI_XS),
        )
        self._custom_wf_menu["menu"].configure(
            bg=t.get("bg_input", "#0f1520"),
            fg=t.get("text_primary", "#f1f5f9"),
            activebackground=t.get("bg_button_hover", "#3b82f6"),
            font=(UI_XS),
        )
        self._custom_wf_menu.pack(fill="x", pady=(4, 0))
        self._update_custom_wf_visibility()

        # Channel selection
        ch_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        ch_frame.pack(fill="x", padx=12, pady=(0, 12))

        tk.Label(
            ch_frame, text="通道",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_dim", "#64748b"),
            font=(UI_XS),
        ).pack(side="left")

        self._channel_var = tk.StringVar(value="A")
        channels = [("A", "A"), ("B", "B")]
        self._channel_rbs = []

        for text, value in channels:
            rb = tk.Radiobutton(
                ch_frame, text=text, variable=self._channel_var, value=value,
                bg=t.get("bg_card", "#151d2b"),
                fg=t.get("text_secondary", "#94a3b8"),
                selectcolor=t.get("bg_input", "#0f1520"),
                activebackground=t.get("bg_card", "#151d2b"),
                activeforeground=t.get("text_primary", "#f1f5f9"),
                font=(UI_S), relief="flat",
                command=self._on_change,
            )
            rb.pack(side="left", padx=(8, 0))
            self._channel_rbs.append(rb)

        self._dual_var = tk.BooleanVar(value=False)
        self._dual_check = tk.Checkbutton(
            ch_frame, text="双通道", variable=self._dual_var,
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_secondary", "#94a3b8"),
            selectcolor=t.get("bg_input", "#0f1520"),
            activebackground=t.get("bg_card", "#151d2b"),
            activeforeground=t.get("text_primary", "#f1f5f9"),
            font=(UI_S), relief="flat",
            command=self._on_dual_toggle,
        )
        self._dual_check.pack(side="left", padx=(16, 0))

        self._alternate_var = tk.BooleanVar(value=False)
        self._alternate_check = tk.Checkbutton(
            ch_frame, text="波形交替", variable=self._alternate_var,
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_secondary", "#94a3b8"),
            selectcolor=t.get("bg_input", "#0f1520"),
            activebackground=t.get("bg_card", "#151d2b"),
            activeforeground=t.get("text_primary", "#f1f5f9"),
            font=(UI_S), relief="flat",
            command=self._on_change,
        )
        self._alternate_check.pack(side="left", padx=(16, 0))

        # Test shock button
        btn_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        btn_frame.pack(fill="x", padx=12, pady=(0, 12))

        self._test_btn = tk.Button(
            btn_frame, text="测试电击 (3秒双通道)",
            bg=t.get("bg_button", "#2563eb"),
            fg="#ffffff",
            activebackground=t.get("bg_button_hover", "#3b82f6"),
            font=(UI_S_B), relief="flat", cursor="hand2",
            command=self._on_test_shock, height=1,
        )
        self._test_btn.pack(fill="x")

        # Chatbox customization
        chatbox_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        chatbox_frame.pack(fill="x", padx=12, pady=(0, 12))

        tk.Label(
            chatbox_frame, text="Chatbox自定义",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_dim", "#64748b"),
            font=(UI_XS),
        ).pack(anchor="w")

        self._chatbox_entry = tk.Entry(
            chatbox_frame,
            bg=t.get("bg_input", "#0f1520"),
            fg=t.get("text_primary", "#f1f5f9"),
            insertbackground=t.get("text_primary", "#f1f5f9"),
            font=(UI_S), relief="flat",
            highlightbackground=t.get("border_color", "#1e293b"),
            highlightthickness=1,
        )
        self._chatbox_entry.pack(fill="x", pady=(4, 0))

        # Chatbox line toggles
        lines_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        lines_frame.pack(fill="x", padx=12, pady=(0, 12))

        tk.Label(
            lines_frame, text="Chatbox显示行",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_dim", "#64748b"),
            font=(UI_XS),
        ).pack(anchor="w")

        toggles_frame = tk.Frame(lines_frame, bg=t.get("bg_card", "#151d2b"))
        toggles_frame.pack(fill="x", pady=(4, 0))

        self._chatbox_toggles = {}
        toggle_labels = ["全部", "标题行", "强度行", "剩余秒数", "波形名", "自定义"]
        for label in toggle_labels:
            var = tk.BooleanVar(value=(label == "全部"))
            cb = tk.Checkbutton(
                toggles_frame, text=label, variable=var,
                bg=t.get("bg_card", "#151d2b"),
                fg=t.get("text_secondary", "#94a3b8"),
                selectcolor=t.get("bg_input", "#0f1520"),
                activebackground=t.get("bg_card", "#151d2b"),
                activeforeground=t.get("text_primary", "#f1f5f9"),
                font=(UI_XS), relief="flat",
                command=self._on_change,
            )
            cb.pack(side="left", padx=(0, 8))
            self._chatbox_toggles[label] = var

        # Statistics
        stats_frame = tk.Frame(container, bg=t.get("bg_card", "#151d2b"))
        stats_frame.pack(fill="x", padx=12, pady=(0, 12))

        tk.Label(
            stats_frame, text="电击统计",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("text_dim", "#64748b"),
            font=(UI_XS),
        ).pack(anchor="w")

        self._stats_a_label = tk.Label(
            stats_frame, text="A: 0秒 | 强度x时间: 0",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("accent_emerald", "#34d399"),
            font=(MONO_S),
        )
        self._stats_a_label.pack(anchor="w", pady=(4, 0))

        self._stats_b_label = tk.Label(
            stats_frame, text="B: 0秒 | 强度x时间: 0",
            bg=t.get("bg_card", "#151d2b"),
            fg=t.get("accent_amber", "#fbbf24"),
            font=(MONO_S),
        )
        self._stats_b_label.pack(anchor="w")

    def _on_dual_toggle(self):
        dual = self._dual_var.get()
        state = "disabled" if dual else "normal"
        for rb in self._channel_rbs:
            rb.configure(state=state)
        self._on_change()

    def _on_wf_mode_change(self):
        self._update_custom_wf_visibility()
        self._on_change()

    def _update_custom_wf_visibility(self):
        if self._wf_var.get() == "custom":
            self._custom_wf_group.pack(fill="x", padx=12, pady=(0, 12))
        else:
            self._custom_wf_group.pack_forget()

    def _on_a_limit_change(self, value):
        self._a_limit_label.configure(text=str(int(float(value))))
        self._on_change()

    def _on_b_limit_change(self, value):
        self._b_limit_label.configure(text=str(int(float(value))))
        self._on_change()

    def get_a_limit(self) -> int:
        return self._a_limit_var.get()

    def set_a_limit(self, value: int):
        self._a_limit_var.set(value)
        self._a_limit_label.configure(text=str(value))

    def get_b_limit(self) -> int:
        return self._b_limit_var.get()

    def set_b_limit(self, value: int):
        self._b_limit_var.set(value)
        self._b_limit_label.configure(text=str(value))

    def get_mode(self) -> str:
        return self._mode_var.get()

    def set_mode(self, mode: str):
        self._mode_var.set(mode)

    def get_waveform_mode(self) -> str:
        return self._wf_var.get()

    def set_waveform_mode(self, mode: str):
        self._wf_var.set(mode)
        self._update_custom_wf_visibility()

    def get_channel(self) -> str:
        return self._channel_var.get()

    def set_channel(self, channel: str):
        self._channel_var.set(channel)

    def get_dual_channel(self) -> bool:
        return self._dual_var.get()

    def set_dual_channel(self, dual: bool):
        self._dual_var.set(dual)
        state = "disabled" if dual else "normal"
        for rb in self._channel_rbs:
            rb.configure(state=state)

    def get_alternate_waveform(self) -> bool:
        return self._alternate_var.get()

    def set_alternate_waveform(self, alternate: bool):
        self._alternate_var.set(alternate)

    def get_max_mode(self) -> bool:
        return self._mode_var.get() == "max"

    def set_max_mode(self, max_mode: bool):
        if max_mode:
            self._mode_var.set("max")

    def get_custom_waveform(self) -> str:
        return self._custom_wf_var.get()

    def set_custom_waveform(self, waveform: str):
        if waveform in self._wf_names:
            self._custom_wf_var.set(waveform)

    def set_chatbox_enabled(self, enabled: bool):
        if hasattr(self, '_chatbox_toggles') and "全部" in self._chatbox_toggles:
            self._chatbox_toggles["全部"].set(enabled)

    def get_chatbox_enabled(self) -> bool:
        if hasattr(self, '_chatbox_toggles') and "全部" in self._chatbox_toggles:
            return self._chatbox_toggles["全部"].get()
        return True

    def set_custom_chatbox(self, text: str):
        if hasattr(self, '_chatbox_entry'):
            self._chatbox_entry.delete(0, "end")
            self._chatbox_entry.insert(0, text)

    def get_custom_chatbox(self) -> str:
        if hasattr(self, '_chatbox_entry'):
            return self._chatbox_entry.get().strip()
        return ""

    def set_chatbox_toggles(self, toggles: dict):
        if hasattr(self, '_chatbox_toggles'):
            for key, value in toggles.items():
                if key in self._chatbox_toggles:
                    self._chatbox_toggles[key].set(value)

    def set_theme_button_text(self, theme_name: str):
        if hasattr(self, '_theme_btn'):
            self._theme_btn.configure(text=theme_name)

    def set_chatbox_enabled_callback(self, callback):
        self._chatbox_enabled_callback = callback

    def set_on_chatbox_enabled(self, callback):
        self._chatbox_enabled_callback = callback

    def get_chatbox_toggles(self) -> dict:
        return {k: v.get() for k, v in self._chatbox_toggles.items()}

    def update_stats(self, a_seconds, b_seconds, a_intensity_time, b_intensity_time):
        self._stats_a_label.configure(
            text=f"A: {a_seconds}秒 | 强度x时间: {int(a_intensity_time)}"
        )
        self._stats_b_label.configure(
            text=f"B: {b_seconds}秒 | 强度x时间: {int(b_intensity_time)}"
        )

    def set_strength(self, a: int, b: int):
        self._a_label.configure(text=f"A: {a}")
        self._b_label.configure(text=f"B: {b}")

    def update_strength(self, a: int, b: int):
        self.set_strength(a, b)

    def apply_theme(self, theme: dict):
        self._theme = theme
        t = theme
        self.configure(bg=t.get("bg_panel", "#111827"))
        for w in self._get_all_widgets():
            try:
                bg = t.get("bg_card", "#151d2b")
                fg = t.get("text_primary", "#f1f5f9")
                if isinstance(w, tk.Scale):
                    w.configure(bg=bg, fg=t.get("text_secondary", "#94a3b8"),
                                troughcolor=t.get("bg_slider_trough", "#1e293b"))
                elif isinstance(w, tk.Button):
                    txt = str(w.cget("text"))
                    if txt == "主题":
                        w.configure(bg=t.get("bg_button", "#2563eb"), fg="#ffffff",
                                    activebackground=t.get("bg_button_hover", "#3b82f6"))
                    else:
                        w.configure(bg=t.get("bg_button", "#2563eb"), fg="#ffffff",
                                    activebackground=t.get("bg_button_hover", "#3b82f6"))
                elif isinstance(w, tk.Entry):
                    w.configure(bg=t.get("bg_input", "#0f1520"), fg=fg, insertbackground=fg,
                                highlightbackground=t.get("border_color", "#1e293b"))
                elif isinstance(w, tk.Text):
                    w.configure(bg=t.get("bg_input", "#0f1520"), fg=fg, insertbackground=fg,
                                highlightbackground=t.get("border_color", "#1e293b"))
                elif isinstance(w, tk.Frame):
                    w.configure(bg=bg)
                elif isinstance(w, tk.Label):
                    current_fg = str(w.cget("fg"))
                    if current_fg in ["#f1f5f9", "#e6edf3"]:
                        w.configure(bg=bg, fg=fg)
                    else:
                        w.configure(bg=bg, fg=t.get("text_dim", "#64748b"))
                elif isinstance(w, tk.Radiobutton):
                    state = "disabled" if (hasattr(self, '_dual_var') and self._dual_var.get() and w in getattr(self, '_channel_rbs', [])) else "normal"
                    w.configure(bg=bg, fg=t.get("text_secondary", "#94a3b8"),
                                selectcolor=t.get("bg_input", "#0f1520"),
                                activebackground=bg, state=state)
                elif isinstance(w, tk.Checkbutton):
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

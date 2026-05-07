import tkinter as tk
import os


class ConnectionPanel(tk.Frame):
    QR_SIZE = 260  # pixels

    def __init__(self, master, theme: dict = None, on_connect=None, on_disconnect=None, **kwargs):
        self._theme = theme or {}
        super().__init__(master, bg=self._theme.get("bg_panel", "#1a1a2e"), **kwargs)
        self._on_connect = on_connect or (lambda: None)
        self._on_disconnect = on_disconnect or (lambda: None)
        self._qr_image = None
        self._qr_path = None
        self._build()

    def _build(self):
        t = self._theme

        header = tk.Frame(self, bg=t.get("bg_header", "#16213e"))
        header.pack(fill="x", padx=2, pady=(2, 0))
        tk.Label(
            header, text="📡 连接状态", bg=t.get("bg_header", "#16213e"),
            fg=t.get("text_primary", "#e0e0e0"),
            font=("Microsoft YaHei UI", 10, "bold"), anchor="w",
        ).pack(side="left", padx=8, pady=4)

        # Status
        status_frame = tk.Frame(self, bg=t.get("bg_panel", "#1a1a2e"))
        status_frame.pack(fill="x", padx=8, pady=4)

        self._status_dot = tk.Canvas(status_frame, width=12, height=12,
                                     bg=t.get("bg_panel", "#1a1a2e"), highlightthickness=0)
        self._status_dot.pack(side="left", padx=(0, 6))
        self._draw_dot(t.get("accent_red", "#ef5350"))

        self._status_label = tk.Label(
            status_frame, text="未启动", bg=t.get("bg_panel", "#1a1a2e"),
            fg=t.get("text_secondary", "#b0b0b0"),
            font=("Microsoft YaHei UI", 9),
        )
        self._status_label.pack(side="left")

        # Port input
        port_frame = tk.Frame(self, bg=t.get("bg_panel", "#1a1a2e"))
        port_frame.pack(fill="x", padx=8, pady=2)

        tk.Label(
            port_frame, text="端口:", bg=t.get("bg_panel", "#1a1a2e"),
            fg=t.get("text_dim", "#888888"),
            font=("Microsoft YaHei UI", 9),
        ).pack(side="left")

        self._port_var = tk.StringVar(value="9999")
        self._port_entry = tk.Entry(
            port_frame, textvariable=self._port_var,
            bg=t.get("bg_input", "#0a0a1a"), fg=t.get("text_primary", "#e0e0e0"),
            insertbackground=t.get("text_primary", "#e0e0e0"),
            font=("Consolas", 9), relief="flat", width=8,
        )
        self._port_entry.pack(side="left", padx=(4, 0))

        # Buttons
        btn_frame = tk.Frame(self, bg=t.get("bg_panel", "#1a1a2e"))
        btn_frame.pack(fill="x", padx=8, pady=4)

        self._start_btn = tk.Button(
            btn_frame, text="启动服务", bg=t.get("bg_button", "#0f3460"),
            fg=t.get("text_primary", "#e0e0e0"),
            activebackground=t.get("bg_button_hover", "#1a5276"),
            activeforeground=t.get("text_primary", "#ffffff"),
            font=("Microsoft YaHei UI", 9, "bold"), relief="flat",
            cursor="hand2", command=self._on_connect_click, width=8,
        )
        self._start_btn.pack(side="left", padx=(0, 4))

        self._stop_btn = tk.Button(
            btn_frame, text="停止", bg=t.get("bg_button_danger", "#4a1a1a"),
            fg=t.get("text_primary", "#e0e0e0"),
            activebackground=t.get("bg_button_danger_hover", "#6a2a2a"),
            activeforeground=t.get("text_primary", "#ffffff"),
            font=("Microsoft YaHei UI", 9), relief="flat",
            cursor="hand2", command=self._on_disconnect_click, width=8,
            state="disabled",
        )
        self._stop_btn.pack(side="left")

        # QR code area
        qr_frame = tk.Frame(self, bg=t.get("bg_panel", "#1a1a2e"))
        qr_frame.pack(fill="x", padx=8, pady=(4, 2))

        tk.Label(
            qr_frame, text="APP扫码配对", bg=t.get("bg_panel", "#1a1a2e"),
            fg=t.get("text_dim", "#888888"),
            font=("Microsoft YaHei UI", 9),
        ).pack()

        self._qr_canvas = tk.Canvas(
            qr_frame,
            width=self.QR_SIZE, height=self.QR_SIZE,
            bg=t.get("bg_input", "#0a0a1a"),
            highlightthickness=1, highlightbackground=t.get("text_muted", "#666666"),
            cursor="hand2",
        )
        self._qr_canvas.pack(pady=4)
        self._qr_canvas.create_text(
            self.QR_SIZE // 2, self.QR_SIZE // 2,
            text="启动服务后显示", fill=t.get("text_muted", "#666666"),
            font=("Microsoft YaHei UI", 9), tags="placeholder",
        )
        self._qr_canvas.bind("<Button-1>", self._on_qr_click)

        # Full-screen QR overlay (hidden by default)
        self._qr_overlay = None
        self._qr_enlarged = False
        self._qr_full_image = None

        # Client ID
        self._id_label = tk.Label(
            self, text="", bg=t.get("bg_panel", "#1a1a2e"),
            fg=t.get("text_muted", "#666666"),
            font=("Consolas", 8), wraplength=280,
        )
        self._id_label.pack(padx=8, pady=(0, 4))

    def _draw_dot(self, color: str):
        self._status_dot.delete("all")
        self._status_dot.create_oval(2, 2, 10, 10, fill=color, outline=color)

    def _on_connect_click(self):
        self._start_btn.configure(state="disabled")
        self._stop_btn.configure(state="normal")
        self._on_connect()

    def _on_disconnect_click(self):
        self._start_btn.configure(state="normal")
        self._stop_btn.configure(state="disabled")
        self._on_disconnect()

    def apply_theme(self, theme: dict):
        self._theme = theme
        t = theme
        self.configure(bg=t.get("bg_panel", "#1a1a2e"))
        for w in self._get_all_widgets():
            try:
                bg = t.get("bg_panel", "#1a1a2e")
                fg = t.get("text_primary", "#e0e0e0")
                if isinstance(w, tk.Canvas):
                    w.configure(bg=t.get("bg_input", "#0a0a1a"))
                elif isinstance(w, tk.Button):
                    txt = str(w.cget("text"))
                    if txt == "停止":
                        w.configure(bg=t.get("bg_button_danger", "#4a1a1a"), fg=fg,
                                    activebackground=t.get("bg_button_danger_hover", "#6a2a2a"))
                    else:
                        w.configure(bg=t.get("bg_button", "#0f3460"), fg=fg,
                                    activebackground=t.get("bg_button_hover", "#1a5276"))
                elif isinstance(w, tk.Entry):
                    w.configure(bg=t.get("bg_input", "#0a0a1a"), fg=fg, insertbackground=fg)
                elif isinstance(w, tk.Frame):
                    w.configure(bg=bg)
                elif isinstance(w, tk.Label):
                    w.configure(bg=bg, fg=t.get("text_muted", "#666666"))
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

    def set_status(self, status: str):
        t = self._theme
        status_map = {
            "connecting": (t.get("accent_orange", "#ffb74d"), "启动中..."),
            "connected": (t.get("accent_green", "#66bb6a"), "服务运行中"),
            "paired": (t.get("accent_blue", "#4fc3f7"), "已配对"),
            "disconnected": (t.get("accent_red", "#ef5350"), "未启动"),
        }
        color, text = status_map.get(status, (t.get("accent_red", "#ef5350"), "未知"))
        self._draw_dot(color)
        self._status_label.configure(text=text)

        if status == "disconnected":
            self._start_btn.configure(state="normal")
            self._stop_btn.configure(state="disabled")
            self._qr_canvas.delete("all")
            self._qr_canvas.create_text(
                self.QR_SIZE // 2, self.QR_SIZE // 2,
                text="启动服务后显示", fill=t.get("text_muted", "#666666"),
                font=("Microsoft YaHei UI", 9), tags="placeholder",
            )
            self._id_label.configure(text="")
        elif status in ("connected", "paired"):
            self._start_btn.configure(state="disabled")
            self._stop_btn.configure(state="normal")

    def set_qr(self, url_or_image, client_id: str = ""):
        if hasattr(url_or_image, "size"):
            from PIL import ImageTk
            self._qr_original = url_or_image
            img = url_or_image.resize((self.QR_SIZE, self.QR_SIZE))
            self._qr_image = ImageTk.PhotoImage(img)
            self._qr_canvas.delete("all")
            self._qr_canvas.create_image(
                self.QR_SIZE // 2, self.QR_SIZE // 2, image=self._qr_image, anchor="center",
            )
            try:
                self._qr_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dgcode.png"
                )
                url_or_image.save(self._qr_path)
            except Exception:
                pass
        elif isinstance(url_or_image, str) and url_or_image:
            try:
                import qrcode
                from PIL import ImageTk
                qr = qrcode.QRCode(
                    version=None,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=10, border=4,
                )
                qr.add_data(url_or_image)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
                self._qr_original = img

                # Save to PNG file like OMO
                self._qr_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dgcode.png"
                )
                img.save(self._qr_path)

                # Display on Canvas at fixed pixel size
                display_img = img.resize((self.QR_SIZE, self.QR_SIZE))
                self._qr_image = ImageTk.PhotoImage(display_img)
                self._qr_canvas.delete("all")
                self._qr_canvas.create_image(
                    self.QR_SIZE // 2, self.QR_SIZE // 2, image=self._qr_image, anchor="center",
                )
            except Exception as e:
                self._qr_canvas.delete("all")
                self._qr_canvas.create_text(
                    self.QR_SIZE // 2, self.QR_SIZE // 2,
                    text=str(e)[:50], fill="#ef5350",
                    font=("Consolas", 8), width=self.QR_SIZE - 20,
                )
        if client_id:
            self._id_label.configure(text=f"ID: {client_id[:20]}")

    def _on_qr_click(self, event=None):
        if not self._qr_image:
            return
        if self._qr_enlarged:
            self._shrink_qr()
        else:
            self._enlarge_qr()

    def _enlarge_qr(self):
        if self._qr_enlarged or not self._qr_image:
            return
        self._qr_enlarged = True
        # Find the root window
        root = self.winfo_toplevel()
        root.update_idletasks()
        w = root.winfo_width()
        h = root.winfo_height()

        self._qr_overlay = tk.Frame(root, bg="#000000")
        self._qr_overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self._qr_overlay.bind("<Button-1>", lambda e: self._shrink_qr())

        # Enlarge the QR image
        size = min(w, h) - 80
        from PIL import ImageTk
        img = self._qr_image._original if hasattr(self._qr_image, '_original') else None
        if img is None and self._qr_path and os.path.exists(self._qr_path):
            from PIL import Image
            img = Image.open(self._qr_path)
        if img:
            display = img.resize((size, size))
            self._qr_full_image = ImageTk.PhotoImage(display)
        else:
            self._qr_full_image = self._qr_image

        canvas = tk.Canvas(
            self._qr_overlay, width=size, height=size,
            bg="#000000", highlightthickness=0, cursor="hand2",
        )
        canvas.place(relx=0.5, rely=0.5, anchor="center")
        canvas.create_image(size // 2, size // 2, image=self._qr_full_image, anchor="center")
        canvas.bind("<Button-1>", lambda e: self._shrink_qr())

        hint = tk.Label(
            self._qr_overlay, text="点击任意位置关闭",
            bg="#000000", fg="#888888",
            font=("Microsoft YaHei UI", 12),
        )
        hint.place(relx=0.5, rely=0.9, anchor="center")

    def _shrink_qr(self):
        if not self._qr_enlarged:
            return
        self._qr_enlarged = False
        if self._qr_overlay:
            self._qr_overlay.destroy()
            self._qr_overlay = None
        self._qr_full_image = None

    def get_port(self) -> int:
        try:
            return int(self._port_var.get().strip())
        except ValueError:
            return 9999

    def set_port(self, port: int):
        self._port_var.set(str(port))

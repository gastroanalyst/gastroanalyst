"""Growth tracker tab — follower counter, milestones, checklist, schedule."""
import customtkinter as ctk
import config
import storage
from widgets import SURFACE, SURFACE2, BORDER, GREEN, GREEN2, AMBER, TEXT, TEXT_DIM, TEXT_MID, FONT


class GrowthTab(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=config.DATA_DIR.parent.__class__.__name__ and SURFACE, corner_radius=0, **kwargs)
        self.configure(fg_color="#08090A")
        self._checks: dict = storage.load_today_checklist()
        self._check_vars: dict = {}
        self._build()
        self.refresh()

    def _build(self):
        outer = ctk.CTkScrollableFrame(self, fg_color="#08090A", corner_radius=0)
        outer.pack(fill="both", expand=True, padx=16, pady=16)

        # Two-column grid
        left = ctk.CTkFrame(outer, fg_color="#08090A", corner_radius=0)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        right = ctk.CTkFrame(outer, fg_color="#08090A", corner_radius=0)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        outer.grid_columnconfigure(0, weight=1)
        outer.grid_columnconfigure(1, weight=1)

        # ── LEFT ────────────────────────────────────────────
        self._build_counter(left)
        self._build_milestones(left)

        # ── RIGHT ───────────────────────────────────────────
        self._build_checklist(right)
        self._build_schedule(right)

    # ── Counter ────────────────────────────────────────────
    def _build_counter(self, parent):
        card = self._card(parent, "◈  Takipçi Sayacı")

        row = ctk.CTkFrame(card, fg_color="transparent", corner_radius=0)
        row.pack(fill="x", pady=(0, 12))

        self.follower_entry = ctk.CTkEntry(
            row,
            width=160,
            height=42,
            fg_color=SURFACE2,
            border_color=BORDER,
            text_color=TEXT,
            font=ctk.CTkFont(family="Courier", size=20),
            placeholder_text="0",
            corner_radius=0,
        )
        self.follower_entry.pack(side="left")
        ctk.CTkButton(
            row,
            text="Kaydet",
            width=80,
            height=42,
            fg_color=GREEN2,
            hover_color=GREEN,
            text_color="#08090A",
            font=ctk.CTkFont(family=FONT, size=10, weight="bold"),
            corner_radius=0,
            command=self._save_followers,
        ).pack(side="left", padx=(8, 0))

        # Progress bar
        self.prog_canvas = ctk.CTkProgressBar(card, height=8, corner_radius=4,
                                               fg_color=SURFACE2, progress_color=GREEN)
        self.prog_canvas.set(0)
        self.prog_canvas.pack(fill="x", pady=(0, 6))

        meta = ctk.CTkFrame(card, fg_color="transparent", corner_radius=0)
        meta.pack(fill="x")
        self.pct_lbl = ctk.CTkLabel(meta, text="%0.0", font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
                                     text_color=GREEN)
        self.pct_lbl.pack(side="left")
        self.rem_lbl = ctk.CTkLabel(meta, text="100.000'e 100.000 kaldı",
                                     font=ctk.CTkFont(family=FONT, size=11), text_color=TEXT_DIM)
        self.rem_lbl.pack(side="right")

    # ── Milestones ─────────────────────────────────────────
    def _build_milestones(self, parent):
        card = self._card(parent, "◈  Yol Haritası")
        self.milestone_frame = ctk.CTkFrame(card, fg_color="transparent", corner_radius=0)
        self.milestone_frame.pack(fill="x")

    def _render_milestones(self):
        for w in self.milestone_frame.winfo_children():
            w.destroy()
        found_next = False
        for m in config.MILESTONES:
            reached = config.FOLLOWERS >= m
            row = ctk.CTkFrame(self.milestone_frame, fg_color="transparent", corner_radius=0)
            row.pack(fill="x", pady=3)
            if reached:
                dot_color, label_color, label_extra = GREEN, TEXT_DIM, " ✓"
                strike = True
            elif not found_next:
                dot_color, label_color, label_extra = AMBER, AMBER, " ← sonraki"
                found_next = True
                strike = False
            else:
                dot_color, label_color, label_extra = BORDER, TEXT_DIM, ""
                strike = False
            dot = ctk.CTkFrame(row, width=10, height=10, fg_color=dot_color, corner_radius=5)
            dot.pack(side="left", padx=(0, 10))
            label = f"{m//1000}K" if m >= 1000 else str(m)
            ctk.CTkLabel(
                row,
                text=f"{label} takipçi{label_extra}",
                font=ctk.CTkFont(family=FONT, size=12),
                text_color=label_color,
            ).pack(side="left")

    # ── Checklist ──────────────────────────────────────────
    def _build_checklist(self, parent):
        card = self._card(parent, "◈  Günlük Kontrol Listesi")
        for cid, label in config.DAILY_TASKS:
            var = ctk.BooleanVar(value=self._checks.get(cid, False))
            self._check_vars[cid] = var
            cb = ctk.CTkCheckBox(
                card,
                text=label,
                variable=var,
                font=ctk.CTkFont(family=FONT, size=12),
                text_color=TEXT_MID,
                fg_color=GREEN,
                hover_color=GREEN2,
                checkmark_color="#08090A",
                corner_radius=2,
                command=lambda c=cid, v=var: self._toggle_check(c, v),
            )
            cb.pack(anchor="w", pady=3)

    def _toggle_check(self, cid, var):
        self._checks[cid] = var.get()
        storage.save_checklist(self._checks)

    # ── Schedule ───────────────────────────────────────────
    def _build_schedule(self, parent):
        card = self._card(parent, "◈  Optimal Paylaşım Zamanları")
        for ctype, time, freq in config.SCHEDULE:
            row = ctk.CTkFrame(card, fg_color=SURFACE2, corner_radius=0)
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=ctype, font=ctk.CTkFont(family=FONT, size=11),
                          text_color=TEXT_MID).pack(side="left", padx=12, pady=8)
            right = ctk.CTkFrame(row, fg_color="transparent", corner_radius=0)
            right.pack(side="right", padx=12)
            ctk.CTkLabel(right, text=time, font=ctk.CTkFont(family="Courier", size=11),
                          text_color=GREEN).pack(anchor="e")
            ctk.CTkLabel(right, text=freq, font=ctk.CTkFont(family=FONT, size=9),
                          text_color=TEXT_DIM).pack(anchor="e")

    # ── Helpers ────────────────────────────────────────────
    def _card(self, parent, title: str) -> ctk.CTkFrame:
        card = ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=0)
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(family=FONT, size=9),
                      text_color=TEXT_DIM).pack(anchor="w", padx=16, pady=(14, 10))
        inner = ctk.CTkFrame(card, fg_color="transparent", corner_radius=0)
        inner.pack(fill="x", padx=16, pady=(0, 14))
        return inner

    def _save_followers(self):
        try:
            val = int(self.follower_entry.get().replace(".", "").replace(",", ""))
        except ValueError:
            return
        config.FOLLOWERS = val
        config.save_settings()
        self.refresh()

    def refresh(self):
        """Update progress indicators from config.FOLLOWERS."""
        f = config.FOLLOWERS
        pct = min(100.0, f / config.TARGET * 100)
        rem = max(0, config.TARGET - f)
        self.prog_canvas.set(pct / 100)
        self.pct_lbl.configure(text=f"%{pct:.1f}")
        self.rem_lbl.configure(text=f"100.000'e {rem:,} kaldı".replace(",", "."))
        if self.follower_entry.get() != str(f):
            self.follower_entry.delete(0, "end")
            self.follower_entry.insert(0, str(f))
        self._render_milestones()

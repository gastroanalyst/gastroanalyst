"""GastroAnalyst — AI Social Media Office (Desktop)
Entry point: python main.py
"""
import sys
import customtkinter as ctk

import config
import storage
import agents as ag
from widgets import (
    BG, SURFACE, SURFACE2, BORDER, GREEN, GREEN2, AMBER, TEXT, TEXT_DIM, TEXT_MID, FONT,
)
from tabs.growth import GrowthTab
from tabs.strategy import StrategyTab
from tabs.content import ContentTab
from tabs.viral import ViralTab
from tabs.engage import EngageTab
from tabs.history import HistoryTab

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


# ─────────────────────────────────────────────────────────────────
# Setup window
# ─────────────────────────────────────────────────────────────────
class SetupWindow(ctk.CTkToplevel):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success
        self.title("GastroAnalyst — Giriş")
        self.geometry("500x520")
        self.resizable(False, False)
        self.configure(fg_color=BG)
        self._build()
        self.grab_set()
        self.focus()

    def _build(self):
        # Top accent line
        ctk.CTkFrame(self, height=3, fg_color=GREEN, corner_radius=0).pack(fill="x")

        box = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=0)
        box.pack(fill="both", expand=True, padx=40, pady=40)

        ctk.CTkLabel(box, text="GastroAnalyst",
                      font=ctk.CTkFont(family="Georgia", size=28, weight="bold"),
                      text_color=GREEN).pack(anchor="w", padx=24, pady=(24, 0))
        ctk.CTkLabel(box, text="AI SOCIAL MEDIA OFFICE",
                      font=ctk.CTkFont(family=FONT, size=9),
                      text_color=TEXT_DIM).pack(anchor="w", padx=24)
        ctk.CTkLabel(
            box,
            text="İşlenmiş gıdaların bilimsel pozitif yönlerini anlatan marka.\n"
                 "7 AI ajan · Streaming · Timeout yok · 100K hedef.",
            font=ctk.CTkFont(family=FONT, size=12),
            text_color=TEXT_MID,
            justify="left",
        ).pack(anchor="w", padx=24, pady=(12, 24))

        # API Key
        ctk.CTkLabel(box, text="CLAUDE API ANAHTARI",
                      font=ctk.CTkFont(family=FONT, size=9), text_color=TEXT_DIM).pack(anchor="w", padx=24)
        self.api_entry = ctk.CTkEntry(
            box, placeholder_text="sk-ant-api03-…", show="•",
            fg_color=SURFACE2, border_color=BORDER, text_color=TEXT,
            font=ctk.CTkFont(family="Courier", size=12),
            height=40, corner_radius=0,
        )
        self.api_entry.pack(fill="x", padx=24, pady=(6, 16))

        # Handle + Followers
        row = ctk.CTkFrame(box, fg_color="transparent", corner_radius=0)
        row.pack(fill="x", padx=24)
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(row, text="INSTAGRAM HESABI",
                      font=ctk.CTkFont(family=FONT, size=9), text_color=TEXT_DIM).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(row, text="MEVCUT TAKİPÇİ",
                      font=ctk.CTkFont(family=FONT, size=9), text_color=TEXT_DIM).grid(row=0, column=1, sticky="w", padx=(12, 0))
        self.handle_entry = ctk.CTkEntry(
            row, placeholder_text="@gastroanalyst",
            fg_color=SURFACE2, border_color=BORDER, text_color=TEXT,
            font=ctk.CTkFont(family="Courier", size=12),
            height=38, corner_radius=0,
        )
        self.handle_entry.grid(row=1, column=0, sticky="ew", pady=(6, 0))
        self.followers_entry = ctk.CTkEntry(
            row, placeholder_text="0",
            fg_color=SURFACE2, border_color=BORDER, text_color=TEXT,
            font=ctk.CTkFont(family="Courier", size=12),
            height=38, corner_radius=0,
        )
        self.followers_entry.grid(row=1, column=1, sticky="ew", padx=(12, 0), pady=(6, 0))

        # Error label
        self.err_lbl = ctk.CTkLabel(box, text="", font=ctk.CTkFont(family=FONT, size=11),
                                     text_color="#E85B4A")
        self.err_lbl.pack(padx=24, pady=(12, 4))

        # Start button
        ctk.CTkButton(
            box, text="Sistemi Başlat →",
            fg_color=GREEN, hover_color=AMBER, text_color=BG,
            font=ctk.CTkFont(family=FONT, size=13, weight="bold"),
            height=46, corner_radius=0,
            command=self._start,
        ).pack(fill="x", padx=24, pady=(4, 16))

        ctk.CTkLabel(
            box,
            text="Tüm veriler yalnızca cihazında saklanır.",
            font=ctk.CTkFont(family=FONT, size=10),
            text_color=TEXT_DIM,
        ).pack(padx=24)

        # Pre-fill from saved settings
        if config.API_KEY:
            self.api_entry.insert(0, config.API_KEY)
        if config.IG_HANDLE:
            self.handle_entry.insert(0, config.IG_HANDLE)
        if config.FOLLOWERS:
            self.followers_entry.insert(0, str(config.FOLLOWERS))

    def _start(self):
        key = self.api_entry.get().strip()
        handle = self.handle_entry.get().strip() or "@gastroanalyst"
        try:
            followers = int(self.followers_entry.get().replace(".", "").replace(",", "") or "0")
        except ValueError:
            followers = 0

        if not key.startswith("sk-ant-"):
            self.err_lbl.configure(text="Geçerli API anahtarı gir (sk-ant- ile başlamalı)")
            return

        config.API_KEY = key
        config.IG_HANDLE = handle
        config.FOLLOWERS = followers
        config.save_settings()
        self.destroy()
        self.on_success()


# ─────────────────────────────────────────────────────────────────
# Main application window
# ─────────────────────────────────────────────────────────────────
class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GastroAnalyst — AI Social Media Office")
        self.geometry("1280x820")
        self.minsize(960, 640)
        self.configure(fg_color=BG)
        config.load_settings()
        self._setup_shown = False
        self._tabs: dict = {}
        self._build_header()
        self._build_tabs()
        # Show setup if no API key
        self.after(100, self._maybe_setup)

    # ── Header ────────────────────────────────────────────
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color=SURFACE, height=56, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Brand
        brand = ctk.CTkFrame(header, fg_color="transparent", corner_radius=0)
        brand.pack(side="left", padx=20)
        ctk.CTkLabel(brand, text="GastroAnalyst",
                      font=ctk.CTkFont(family="Georgia", size=18, weight="bold"),
                      text_color=GREEN).pack(anchor="w")
        ctk.CTkLabel(brand, text="AI OFFICE",
                      font=ctk.CTkFont(family=FONT, size=8), text_color=TEXT_DIM).pack(anchor="w")

        # Progress bar (center)
        prog_frame = ctk.CTkFrame(header, fg_color="transparent", corner_radius=0)
        prog_frame.pack(side="left", expand=True, padx=20, fill="x")
        meta = ctk.CTkFrame(prog_frame, fg_color="transparent", corner_radius=0)
        meta.pack(fill="x")
        self.h_count = ctk.CTkLabel(meta, text="0 / 100K",
                                     font=ctk.CTkFont(family="Courier", size=11), text_color=TEXT)
        self.h_count.pack(side="left")
        self.h_pct = ctk.CTkLabel(meta, text="%0.0",
                                   font=ctk.CTkFont(family="Courier", size=11), text_color=GREEN)
        self.h_pct.pack(side="right")
        self.h_bar = ctk.CTkProgressBar(prog_frame, height=4, corner_radius=2,
                                         fg_color=SURFACE2, progress_color=GREEN)
        self.h_bar.set(0)
        self.h_bar.pack(fill="x", pady=(4, 0))

        # Buttons
        btns = ctk.CTkFrame(header, fg_color="transparent", corner_radius=0)
        btns.pack(side="right", padx=20)
        self.gen_btn = ctk.CTkButton(
            btns, text="⚡  Tümünü Üret", width=140, height=34,
            fg_color=GREEN, hover_color=AMBER, text_color=BG,
            font=ctk.CTkFont(family=FONT, size=11, weight="bold"),
            corner_radius=0, command=self._generate_all,
        )
        self.gen_btn.pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            btns, text="Çıkış", width=60, height=34,
            fg_color="transparent", border_width=1, border_color=BORDER,
            text_color=TEXT_DIM, hover_color=SURFACE2,
            font=ctk.CTkFont(family=FONT, size=10), corner_radius=0,
            command=self._logout,
        ).pack(side="left")

    # ── Tabs ──────────────────────────────────────────────
    def _build_tabs(self):
        tabview = ctk.CTkTabview(
            self, fg_color=BG, corner_radius=0,
            segmented_button_fg_color=SURFACE,
            segmented_button_selected_color=GREEN,
            segmented_button_selected_hover_color=AMBER,
            segmented_button_unselected_color=SURFACE,
            segmented_button_unselected_hover_color=SURFACE2,
            text_color=TEXT_DIM,
            text_color_disabled=TEXT_DIM,
        )
        tabview.pack(fill="both", expand=True)

        tab_defs = [
            ("🎯  Büyüme",    GrowthTab),
            ("🧠  Strateji",  StrategyTab),
            ("📱  İçerik",    ContentTab),
            ("🔥  Viral",     ViralTab),
            ("💬  Etkileşim", EngageTab),
            ("📜  Geçmiş",    HistoryTab),
        ]
        for name, Cls in tab_defs:
            tabview.add(name)
            frame = Cls(tabview.tab(name))
            frame.pack(fill="both", expand=True)
            self._tabs[name] = frame

        self._tabview = tabview

    # ── Generate All ──────────────────────────────────────
    def _generate_all(self):
        self.gen_btn.configure(state="disabled", text="⏳  Üretiliyor…")
        results: dict = {}

        strategy_tab: StrategyTab = self._tabs["🧠  Strateji"]
        content_tab:  ContentTab  = self._tabs["📱  İçerik"]
        viral_tab:    ViralTab    = self._tabs["🔥  Viral"]
        engage_tab:   EngageTab   = self._tabs["💬  Etkileşim"]

        def finish():
            self.gen_btn.configure(state="normal", text="⚡  Tümünü Üret")
            # Collect all outputs
            for key, card in [
                ("growth_dir", strategy_tab.card_growth),
                ("researcher", strategy_tab.card_research),
                ("carousel",   content_tab.card_carousel),
                ("reels",      content_tab.card_reels),
                ("story",      content_tab.card_story),
                ("hooks",      viral_tab.card_hooks),
                ("engage",     engage_tab.card_engage),
            ]:
                t = card.get_text()
                if t:
                    results[key] = t
            storage.save_session(results, config.FOLLOWERS)
            history_tab: HistoryTab = self._tabs["📜  Geçmiş"]
            history_tab.refresh()

        def after_engage(_):
            finish()

        def after_viral(_):
            engage_tab.card_engage.run(callback=after_engage)

        def after_content():
            viral_tab.card_hooks.run(callback=after_viral)

        def after_strategy():
            content_tab.run_all(on_done=after_content)

        strategy_tab.run_all(on_done=after_strategy)

    # ── Header progress update ─────────────────────────────
    def _update_header_progress(self):
        f = config.FOLLOWERS
        pct = min(100.0, f / config.TARGET * 100)
        self.h_count.configure(text=f"{f:,} / 100K".replace(",", "."))
        self.h_pct.configure(text=f"%{pct:.1f}")
        self.h_bar.set(pct / 100)

    # ── Auth ──────────────────────────────────────────────
    def _maybe_setup(self):
        if not config.API_KEY:
            self._show_setup()
        else:
            self._update_header_progress()

    def _show_setup(self):
        SetupWindow(self, on_success=self._on_login)

    def _on_login(self):
        self._update_header_progress()
        growth_tab: GrowthTab = self._tabs["🎯  Büyüme"]
        growth_tab.refresh()

    def _logout(self):
        config.API_KEY = ""
        config.save_settings()
        self._show_setup()


# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

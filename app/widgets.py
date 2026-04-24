"""Reusable UI widgets."""
import tkinter as tk
import customtkinter as ctk
from agents import run_agent, AGENTS

# ── Palette ───────────────────────────────────────────────
BG       = "#08090A"
SURFACE  = "#0F1112"
SURFACE2 = "#161A1C"
BORDER   = "#252A2C"
GREEN    = "#A8C44A"
GREEN2   = "#7a9033"
AMBER    = "#E8B84B"
RED      = "#E85B4A"
TEXT     = "#EAE6DC"
TEXT_DIM = "#555C52"
TEXT_MID = "#9A9690"
FONT     = "Outfit"
MONO     = "Courier"

STATUS_MAP = {
    "idle":    ("Bekliyor",    TEXT_DIM),
    "working": ("Çalışıyor…", AMBER),
    "done":    ("Tamamlandı ✓", GREEN),
    "error":   ("Hata",        RED),
}


class AgentCard(ctk.CTkFrame):
    """A card widget that displays one AI agent's output with run/copy controls."""

    def __init__(self, parent, agent_key: str, **kwargs):
        super().__init__(parent, fg_color=SURFACE, corner_radius=0, **kwargs)
        self.agent_key = agent_key
        self.agent = AGENTS[agent_key]
        self._full_text = ""
        self._running = False
        self._build()

    def _build(self):
        accent = self.agent["accent"]

        # Top accent line
        ctk.CTkFrame(self, height=2, fg_color=accent, corner_radius=0).pack(fill="x")

        # Header
        header = ctk.CTkFrame(self, fg_color=SURFACE2, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(
            header,
            text=f"{self.agent['icon']}  {self.agent['name']}",
            font=ctk.CTkFont(family=FONT, size=12, weight="bold"),
            text_color=TEXT,
        ).pack(side="left", padx=14, pady=10)
        ctk.CTkLabel(
            header,
            text=self.agent["role"],
            font=ctk.CTkFont(family=FONT, size=9),
            text_color=TEXT_DIM,
        ).pack(side="left")
        self.status_lbl = ctk.CTkLabel(
            header,
            text="Bekliyor",
            font=ctk.CTkFont(family=FONT, size=9),
            text_color=TEXT_DIM,
        )
        self.status_lbl.pack(side="right", padx=14)

        # Output text
        self.output = ctk.CTkTextbox(
            self,
            height=220,
            fg_color=SURFACE,
            text_color=TEXT_MID,
            font=ctk.CTkFont(family=MONO, size=11),
            corner_radius=0,
            border_width=0,
            wrap="word",
            state="disabled",
        )
        self.output.pack(fill="both", expand=True, padx=14, pady=(12, 0))
        self._set_placeholder()

        # Footer
        footer = ctk.CTkFrame(self, fg_color=SURFACE2, corner_radius=0)
        footer.pack(fill="x", pady=(8, 0))
        self.run_btn = ctk.CTkButton(
            footer,
            text="▶  Çalıştır",
            width=100,
            height=28,
            fg_color=GREEN2,
            hover_color=GREEN,
            text_color="#08090A",
            font=ctk.CTkFont(family=FONT, size=10, weight="bold"),
            corner_radius=0,
            command=self.run,
        )
        self.run_btn.pack(side="left", padx=(14, 6), pady=8)
        ctk.CTkButton(
            footer,
            text="Kopyala",
            width=80,
            height=28,
            fg_color="transparent",
            border_width=1,
            border_color=BORDER,
            text_color=TEXT_DIM,
            hover_color=SURFACE,
            font=ctk.CTkFont(family=FONT, size=10),
            corner_radius=0,
            command=self._copy,
        ).pack(side="left", pady=8)

    def _set_placeholder(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", f"  {self.agent['name']} çıktısı burada görünecek…")
        self.output.configure(state="disabled")

    def set_status(self, state: str):
        label, color = STATUS_MAP.get(state, ("?", TEXT_DIM))
        self.status_lbl.configure(text=label, text_color=color)

    def run(self, callback=None):
        if self._running:
            return
        self._running = True
        self._full_text = ""
        self.run_btn.configure(state="disabled")
        self.set_status("working")
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")

        def on_token(text: str):
            self.after(0, lambda t=text: self._append(t))

        def on_done(full: str):
            self._full_text = full
            self._running = False
            self.after(0, lambda: self.run_btn.configure(state="normal"))
            self.after(0, lambda: self.set_status("done"))
            if callback:
                self.after(0, lambda: callback(full))

        def on_error(msg: str):
            self._running = False
            self.after(0, lambda: self._show_error(msg))
            self.after(0, lambda: self.run_btn.configure(state="normal"))

        run_agent(self.agent_key, on_token, on_done, on_error)

    def _append(self, text: str):
        self.output.configure(state="normal")
        self.output.insert("end", text)
        self.output.see("end")
        self.output.configure(state="disabled")

    def _show_error(self, msg: str):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", f"Hata: {msg}")
        self.output.configure(state="disabled")
        self.set_status("error")

    def _copy(self):
        text = self._full_text or self.output.get("1.0", "end").strip()
        if not text or "burada görünecek" in text:
            return
        self.clipboard_clear()
        self.clipboard_append(text)

    def get_text(self) -> str:
        return self._full_text

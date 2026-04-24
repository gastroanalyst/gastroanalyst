"""Viral tab — Hook Factory."""
import customtkinter as ctk
from widgets import AgentCard, GREEN, GREEN2, TEXT_DIM, FONT


class ViralTab(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="#08090A", corner_radius=0, **kwargs)
        self._build()

    def _build(self):
        bar = ctk.CTkFrame(self, fg_color="#08090A", corner_radius=0)
        bar.pack(fill="x", padx=16, pady=(14, 8))
        ctk.CTkLabel(bar, text="◈  VİRAL MOTOR",
                      font=ctk.CTkFont(family=FONT, size=9), text_color=TEXT_DIM).pack(side="left")
        ctk.CTkButton(
            bar, text="▶  Hook Üret", width=130, height=30,
            fg_color=GREEN2, hover_color=GREEN, text_color="#08090A",
            font=ctk.CTkFont(family=FONT, size=10, weight="bold"),
            corner_radius=0, command=lambda: self.card_hooks.run(),
        ).pack(side="right")

        self.card_hooks = AgentCard(self, "hooks")
        self.card_hooks.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def get_cards(self) -> list:
        return [self.card_hooks]

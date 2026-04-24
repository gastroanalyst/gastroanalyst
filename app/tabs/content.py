"""Content tab — Carousel, Reels, Story agents."""
import customtkinter as ctk
from widgets import AgentCard, GREEN, GREEN2, TEXT_DIM, FONT


class ContentTab(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="#08090A", corner_radius=0, **kwargs)
        self._build()

    def _build(self):
        bar = ctk.CTkFrame(self, fg_color="#08090A", corner_radius=0)
        bar.pack(fill="x", padx=16, pady=(14, 8))
        ctk.CTkLabel(bar, text="◈  İÇERİK FABRİKASI",
                      font=ctk.CTkFont(family=FONT, size=9), text_color=TEXT_DIM).pack(side="left")
        self.run_btn = ctk.CTkButton(
            bar, text="▶  İçerik Üret", width=140, height=30,
            fg_color=GREEN2, hover_color=GREEN, text_color="#08090A",
            font=ctk.CTkFont(family=FONT, size=10, weight="bold"),
            corner_radius=0, command=self.run_all,
        )
        self.run_btn.pack(side="right")

        # 3-column grid
        grid = ctk.CTkScrollableFrame(self, fg_color="#08090A", corner_radius=0)
        grid.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)
        grid.grid_columnconfigure(2, weight=1)

        self.card_carousel = AgentCard(grid, "carousel")
        self.card_carousel.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        self.card_reels = AgentCard(grid, "reels")
        self.card_reels.grid(row=0, column=1, sticky="nsew", padx=6)

        self.card_story = AgentCard(grid, "story")
        self.card_story.grid(row=0, column=2, sticky="nsew", padx=(6, 0))

    def run_all(self, on_done=None):
        self.run_btn.configure(state="disabled", text="⏳  Üretiliyor…")
        remaining = [0]
        cards = [self.card_carousel, self.card_reels, self.card_story]
        remaining[0] = len(cards)

        def on_card_done(_):
            remaining[0] -= 1
            if remaining[0] == 0:
                self.run_btn.configure(state="normal", text="▶  İçerik Üret")
                if on_done:
                    on_done()

        for card in cards:
            card.run(callback=on_card_done)

    def get_cards(self) -> list:
        return [self.card_carousel, self.card_reels, self.card_story]

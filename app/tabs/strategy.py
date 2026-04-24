"""Strategy tab — Growth Director + Researcher agents."""
import customtkinter as ctk
from widgets import AgentCard, SURFACE, SURFACE2, GREEN, GREEN2, AMBER, TEXT, TEXT_DIM, FONT


class StrategyTab(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="#08090A", corner_radius=0, **kwargs)
        self._build()

    def _build(self):
        # Action row
        bar = ctk.CTkFrame(self, fg_color="#08090A", corner_radius=0)
        bar.pack(fill="x", padx=16, pady=(14, 8))
        ctk.CTkLabel(bar, text="◈  STRATEJİ MODÜLÜ",
                      font=ctk.CTkFont(family=FONT, size=9), text_color=TEXT_DIM).pack(side="left")
        self.run_btn = ctk.CTkButton(
            bar, text="▶  Strateji Üret", width=140, height=30,
            fg_color=GREEN2, hover_color=GREEN, text_color="#08090A",
            font=ctk.CTkFont(family=FONT, size=10, weight="bold"),
            corner_radius=0, command=self.run_all,
        )
        self.run_btn.pack(side="right")

        # Cards
        grid = ctk.CTkFrame(self, fg_color="#08090A", corner_radius=0)
        grid.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        self.card_growth = AgentCard(grid, "growth_dir")
        self.card_growth.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        self.card_research = AgentCard(grid, "researcher")
        self.card_research.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

    def run_all(self, on_done=None):
        self.run_btn.configure(state="disabled", text="⏳  Üretiliyor…")

        def after_growth(_):
            def after_research(text):
                self.run_btn.configure(state="normal", text="▶  Strateji Üret")
                if on_done:
                    on_done()
            self.card_research.run(callback=after_research)

        self.card_growth.run(callback=after_growth)

    def get_cards(self) -> list:
        return [self.card_growth, self.card_research]

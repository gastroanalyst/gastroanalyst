"""History tab — past sessions."""
import customtkinter as ctk
import storage
from storage import AGENT_LABELS
from widgets import SURFACE, SURFACE2, GREEN, TEXT, TEXT_DIM, TEXT_MID, FONT


class HistoryTab(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="#08090A", corner_radius=0, **kwargs)
        self._build()
        self.refresh()

    def _build(self):
        bar = ctk.CTkFrame(self, fg_color="#08090A", corner_radius=0)
        bar.pack(fill="x", padx=16, pady=(14, 8))
        ctk.CTkLabel(bar, text="◈  İÇERİK GEÇMİŞİ",
                      font=ctk.CTkFont(family=FONT, size=9), text_color=TEXT_DIM).pack(side="left")
        ctk.CTkButton(
            bar, text="Geçmişi Temizle", width=140, height=28,
            fg_color="transparent", border_width=1, border_color="#252A2C",
            text_color=TEXT_DIM, hover_color=SURFACE2,
            font=ctk.CTkFont(family=FONT, size=10), corner_radius=0,
            command=self._clear,
        ).pack(side="right")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#08090A", corner_radius=0)
        self.scroll.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def refresh(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        history = storage.load_history()
        if not history:
            ctk.CTkLabel(
                self.scroll,
                text="Henüz üretim yapılmadı.\n⚡  \"Tümünü Üret\" ile başla.",
                font=ctk.CTkFont(family=FONT, size=13),
                text_color=TEXT_DIM,
            ).pack(pady=60)
            return

        for session in history:
            self._add_session(session)

    def _add_session(self, session: dict):
        frame = ctk.CTkFrame(self.scroll, fg_color=SURFACE, corner_radius=0)
        frame.pack(fill="x", pady=(0, 10))

        # Header row (always visible)
        header = ctk.CTkFrame(frame, fg_color=SURFACE2, corner_radius=0)
        header.pack(fill="x")
        f = session.get("followers", 0)
        agents_done = len(session.get("results", {}))
        ctk.CTkLabel(
            header,
            text=session.get("date", "?"),
            font=ctk.CTkFont(family="Courier", size=11),
            text_color=TEXT_MID,
        ).pack(side="left", padx=14, pady=10)
        ctk.CTkLabel(
            header,
            text=f"{f:,} takipçi · {agents_done} ajan".replace(",", "."),
            font=ctk.CTkFont(family=FONT, size=10),
            text_color=TEXT_DIM,
        ).pack(side="right", padx=14)

        # Collapsible body
        body = ctk.CTkFrame(frame, fg_color=SURFACE, corner_radius=0)
        expanded = [False]

        def toggle():
            if expanded[0]:
                body.pack_forget()
                expanded[0] = False
            else:
                body.pack(fill="x")
                expanded[0] = True

        header.bind("<Button-1>", lambda _: toggle())
        for child in header.winfo_children():
            child.bind("<Button-1>", lambda _: toggle())

        for key, text in session.get("results", {}).items():
            sec = ctk.CTkFrame(body, fg_color="transparent", corner_radius=0)
            sec.pack(fill="x", padx=14, pady=8)
            ctk.CTkLabel(sec, text=AGENT_LABELS.get(key, key),
                          font=ctk.CTkFont(family=FONT, size=9),
                          text_color=GREEN).pack(anchor="w")
            tb = ctk.CTkTextbox(sec, height=120, fg_color=SURFACE2, text_color=TEXT_MID,
                                 font=ctk.CTkFont(family="Courier", size=10),
                                 corner_radius=0, border_width=0, wrap="word", state="normal")
            tb.insert("end", text)
            tb.configure(state="disabled")
            tb.pack(fill="x", pady=(4, 0))

    def _clear(self):
        storage.HISTORY_FILE.unlink(missing_ok=True)
        self.refresh()

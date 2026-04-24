import json
from pathlib import Path

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
SETTINGS_FILE = DATA_DIR / "settings.json"

MODEL = "claude-sonnet-4-6"
TARGET = 100_000
MILESTONES = [500, 1_000, 2_500, 5_000, 10_000, 25_000, 50_000, 75_000, 100_000]

DAILY_TASKS = [
    ("c1", "🖼  Carousel paylaşıldı"),
    ("c2", "📱  3+ Story paylaşıldı"),
    ("c3", "💬  5+ Büyük hesaba yorum yapıldı"),
    ("c4", "#️⃣  Hashtag seti kullanıldı"),
    ("c5", "💼  LinkedIn cross-post yapıldı"),
    ("c6", "📩  DM'lere yanıt verildi"),
    ("c7", "🎬  Reels paylaşıldı (haftalık)"),
    ("c8", "🤝  İş birliği için DM atıldı"),
]

SCHEDULE = [
    ("🖼  Carousel",  "19:00 – 21:00", "Salı / Perşembe / Cts"),
    ("🎬  Reels",     "18:00 – 20:00", "Cuma / Cumartesi / Paz"),
    ("📱  Story",     "08:30 + 12:30", "Her gün (2 sefer)"),
    ("💼  LinkedIn",  "09:00 – 11:00", "Salı / Çarşamba"),
]

# Runtime state — mutated by setup screen
API_KEY: str = ""
IG_HANDLE: str = "@gastroanalyst"
FOLLOWERS: int = 0
RESEARCH_OUTPUT: str = ""  # shared between researcher → other agents


def save_settings() -> None:
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump({"api_key": API_KEY, "ig_handle": IG_HANDLE, "followers": FOLLOWERS}, f)


def load_settings() -> None:
    global API_KEY, IG_HANDLE, FOLLOWERS
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
        API_KEY = d.get("api_key", "")
        IG_HANDLE = d.get("ig_handle", "@gastroanalyst")
        FOLLOWERS = int(d.get("followers", 0))

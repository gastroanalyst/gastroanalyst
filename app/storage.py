import json
from datetime import datetime
from config import DATA_DIR

HISTORY_FILE = DATA_DIR / "history.json"
CHECKLIST_FILE = DATA_DIR / "checklist.json"

AGENT_LABELS = {
    "growth_dir": "Büyüme Direktörü",
    "researcher": "Trend Araştırmacı",
    "carousel":   "Carousel",
    "reels":      "Reels",
    "story":      "Story",
    "hooks":      "Hook Fabrikası",
    "engage":     "Etkileşim",
}


def save_session(results: dict, followers: int) -> None:
    history = load_history()
    history.insert(0, {
        "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "followers": followers,
        "results": results,
    })
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history[:7], f, ensure_ascii=False, indent=2)


def load_history() -> list:
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_checklist(checks: dict) -> None:
    all_checks = _load_all_checklists()
    all_checks[_today()] = checks
    with open(CHECKLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(all_checks, f, ensure_ascii=False)


def load_today_checklist() -> dict:
    return _load_all_checklists().get(_today(), {})


def _load_all_checklists() -> dict:
    if CHECKLIST_FILE.exists():
        with open(CHECKLIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _today() -> str:
    return datetime.now().strftime("%Y-%m-%d")

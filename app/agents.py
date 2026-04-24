"""Agent definitions and streaming runner."""
import threading
from datetime import datetime
import anthropic
import config


def _today() -> str:
    return datetime.now().strftime("%A, %d %B %Y")


def _research_ctx() -> str:
    if config.RESEARCH_OUTPUT and len(config.RESEARCH_OUTPUT) > 60:
        return f"\n\nAraştırmacı Ajan'ın konu önerisi:\n{config.RESEARCH_OUTPUT[:500]}"
    return ""


AGENTS: dict = {
    "growth_dir": {
        "name": "Büyüme Direktörü",
        "icon": "🎯",
        "role": "30-Gün Büyüme Planı",
        "accent": "#A8C44A",
        "max_tokens": 700,
        "system": (
            "Sen GastroAnalyst'in Büyüme Direktörü yapay zeka ajanısın. "
            "GastroAnalyst; Türkiye'de işlenmiş gıdaların bilimsel ve POZİTİF yönlerini anlatan "
            "Instagram+LinkedIn markasıdır. Rakip: @neyemeliyizzz (negatif anlatı). "
            "Hedef: 100.000 organik takipçi. Taktik, ölçülebilir, aksiyon odaklı. Türkçe."
        ),
        "get_prompt": lambda: (
            f"Bugün {_today()}. Hesap: {config.IG_HANDLE}. "
            f"Takipçi: {config.FOLLOWERS:,}. Hedef: 100.000.\n\n"
            "🎯 BU HAFTA 3 KRİTİK AKSİYON (spesifik, ölçülebilir, bugün başlanabilir)\n"
            "📈 BU AY MILESTONE: geçilmesi gereken sayı + 2 yöntem\n"
            "⚔️ 2 COUNTER-CONTENT FİKRİ (@neyemeliyizzz'e karşı pozitif bilimsel)\n"
            "🤝 3 KOLABORATİF HEDEF HESAP TİPİ ve nasıl yaklaşılacağı\n"
            "⏰ BUGÜNÜN #1 AKSİYONU (tek cümle)\n\n"
            "Her madde max 2-3 cümle. Kısa, net, uygulanabilir."
        ),
    },
    "researcher": {
        "name": "Trend Araştırmacı",
        "icon": "🔍",
        "role": "Viral Konu & Hashtag",
        "accent": "#4ABDE8",
        "max_tokens": 700,
        "system": (
            "Sen GastroAnalyst'in araştırmacı ajanısın. İşlenmiş gıda biliminde viral potansiyelli "
            "konuları, Instagram algoritmasını ve niche hashtag stratejisini bilirsin. Türkçe."
        ),
        "get_prompt": lambda: (
            f"Bugün {_today()}. Hesap: {config.IG_HANDLE} ({config.FOLLOWERS:,} takipçi).\n\n"
            "🔥 BUGÜNÜN VİRAL KONUSU (şaşırtıcı/yanlış bilinen işlenmiş gıda gerçeği + neden viral?)\n"
            "🎣 İLK SLAYT HOOK'U (scroll durduracak, max 8 kelime)\n"
            "🏷️ HASHTAG STRATEJİSİ:\n"
            "  MEGA 5 adet (>5M):\n"
            "  MİD 10 adet (100K-2M):\n"
            "  NİCHE 10 adet (<100K):\n"
            "  TÜRKÇE NİCHE 5 adet:\n"
            "⏰ İDEAL YAYINLAMA: gün + saat\n"
            "📊 TAHMİN: beklenen reach/save oranı ve neden"
        ),
    },
    "carousel": {
        "name": "Carousel Yazarı",
        "icon": "🖼",
        "role": "7 Slayt · Instagram",
        "accent": "#E8B84B",
        "max_tokens": 900,
        "system": (
            "Sen GastroAnalyst'in carousel yazarısın. Save/share oranı yüksek, "
            "7 slaytlık Instagram carousel'lar yazarsın. İlk slayt scroll durdurur, "
            "son slayt güçlü CTA içerir. Üslup: uzman ama samimi. Türkçe."
        ),
        "get_prompt": lambda: (
            f"Bugün {_today()}.{_research_ctx()}\n\n"
            "7 slaytlık tam Instagram carousel:\n\n"
            "📌 SLAYT 1 — HOOK\n"
            "Başlık: [MAX 6 KELIME, BÜYÜK HARF]\n"
            "Metin: [merak boşluğu, 2 cümle + 'Kaydır 👉']\n\n"
            "📌 SLAYT 2 — TEMEL BİLGİ\n"
            "Başlık + 3 cümle metin\n\n"
            "📌 SLAYT 3 — BİLİMSEL DERİNLİK\n"
            "Başlık + en ilginç bilimsel detay\n\n"
            "📌 SLAYT 4 — MİT-BUSTING\n"
            "Başlık + yanlışı çürüt, pozitif çerçevele\n\n"
            "📌 SLAYT 5 — GÜNLÜK HAYAT\n"
            "Başlık + okuyucu kendini görsün\n\n"
            "📌 SLAYT 6 — ŞAŞIRTICI VERİ\n"
            "Başlık + istatistik/araştırma bulgusu\n\n"
            "📌 SLAYT 7 — CTA\n"
            "'Kaydet 🔖 çünkü [neden]. [Soru]. Takip et 🎯'"
        ),
    },
    "reels": {
        "name": "Reels Senaristi",
        "icon": "🎬",
        "role": "45-60 Sn Video Script",
        "accent": "#E85B4A",
        "max_tokens": 700,
        "system": (
            "Sen GastroAnalyst'in reels senaristi ajanısın. "
            "45-60 saniyelik, izletme oranı yüksek video senaryoları yazarsın. "
            "İlk 3 saniye kritik. Hızlı tempo, net bilgi, güçlü CTA. Türkçe."
        ),
        "get_prompt": lambda: (
            f"Bugün {_today()}.{_research_ctx()}\n\n"
            "45-60 sn Reels senaryosu:\n\n"
            "🎬 HOOK (0-3 sn)\n"
            "Ekran metni: [kalın, max 5 kelime]\n"
            "Ses: [şok/merak cümlesi]\n\n"
            "📖 ORTA (4-40 sn)\n"
            "[6 kısa cümle, her biri yeni bilgi, hızlı tempo]\n\n"
            "🎯 CTA (41-55 sn)\n"
            "[Kaydet + takip et + soru]\n\n"
            "🎵 MÜZİK ÖNERİSİ: tempo + duygu\n"
            "🖼 GÖRSEL REHBERİ: kısa notlar her bölüm için\n"
            "📝 CAPTION: 3 cümle + 5 hashtag"
        ),
    },
    "story": {
        "name": "Story Yazarı",
        "icon": "📱",
        "role": "5 Story Serisi",
        "accent": "#B44AE8",
        "max_tokens": 600,
        "system": (
            "Sen GastroAnalyst'in story yazarısın. "
            "5 story'lik etkileşim yaratan seriler tasarlarsın. "
            "Her story: metin + sticker + CTA. Türkçe."
        ),
        "get_prompt": lambda: (
            f"Bugün {_today()}.{_research_ctx()}\n\n"
            "5 story'lik seri:\n\n"
            "📱 STORY 1 — KANCA\nMetin + Sticker önerisi\n\n"
            "📱 STORY 2 — BİLGİ\nMetin + Anket (2 seçenek)\n\n"
            "📱 STORY 3 — DERİNLEŞTİRME\nMetin + Link/Kaydır sticker\n\n"
            "📱 STORY 4 — ETKİLEŞİM\nSoru çıkartması metni\n\n"
            "📱 STORY 5 — CTA\nAna posta yönlendirme + takip çağrısı"
        ),
    },
    "hooks": {
        "name": "Hook Fabrikası",
        "icon": "🎣",
        "role": "10 Scroll-Stopping Hook",
        "accent": "#E8B84B",
        "max_tokens": 700,
        "system": (
            "Sen GastroAnalyst'in viral metin uzmanısın. "
            "Scroll durduran, farklı psikolojik tetikleyiciler kullanan "
            "hook cümleleri yazarsın. Türkçe."
        ),
        "get_prompt": lambda: (
            f"Bugün {_today()}.{_research_ctx()}\n\n"
            "10 farklı scroll-stopping hook (her biri farklı psikolojik tetikleyici):\n\n"
            "1. 🤯 ŞOK — beklentiyi kıran gerçek\n"
            "2. ❓ MERAK — cevabı merak ettiren soru\n"
            "3. 📊 İSTATİSTİK — çarpıcı sayı/oran\n"
            "4. ⚔️ KARŞI ANLATI — 'sana yanlış söylediler'\n"
            "5. 🔬 BİLİM — araştırma kancası\n"
            "6. 💡 VAAT — 'bunu okuyunca X değişecek'\n"
            "7. 🎯 NİCHE — 'gıda etiketi okuyanlara...'\n"
            "8. 🏆 OTORİTE — 'gıda mühendisi olarak...'\n"
            "9. ⚡ ACİLİYET — 'bunu bugün öğren'\n"
            "10. 🔄 KARŞI SEZGİ — mantığa aykırı ama doğru\n\n"
            "Format: Hook metni (max 10 kelime) | Kullanım yeri"
        ),
    },
    "engage": {
        "name": "Etkileşim Ajan",
        "icon": "💬",
        "role": "Marka Yorum Bankası",
        "accent": "#A8C44A",
        "max_tokens": 700,
        "system": (
            "Sen GastroAnalyst'in etkileşim ajanısın. Büyük gıda markalarına "
            "uzman bakışlı, konuşma başlatan, reklam görünmeyen yorumlar yazarsın. "
            "Max 2 cümle. GastroAnalyst'i mention etme. Türkçe."
        ),
        "get_prompt": lambda: (
            f"Bugün {_today()}.\n\n"
            "7 marka için yorum önerileri:\n"
            "Markalar: Ülker, Eti, Pınar, Torku, Nestlé TR, Unilever TR, Tat\n\n"
            "Her marka:\n"
            "🏢 MARKA\n"
            "💬 Yorum A: [bilgi katan, uzman bakış]\n"
            "💬 Yorum B: [soru soran, konuşma başlatan]\n\n"
            "Kurallar: max 2 cümle, uzman görünüm, reklam değil."
        ),
    },
}

# Execution order for "Generate All"
ALL_ORDER = ["growth_dir", "researcher", "hooks", "carousel", "reels", "story", "engage"]


def run_agent(
    key: str,
    on_token,
    on_done,
    on_error,
) -> None:
    """Run an agent in a background thread with streaming."""
    agent = AGENTS[key]

    def _worker():
        try:
            client = anthropic.Anthropic(api_key=config.API_KEY)
            prompt = agent["get_prompt"]()
            with client.messages.stream(
                model=config.MODEL,
                max_tokens=agent["max_tokens"],
                system=[{"type": "text", "text": agent["system"],
                         "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": prompt}],
            ) as stream:
                full_text = ""
                for text in stream.text_stream:
                    full_text += text
                    on_token(text)
            # Store researcher output for context sharing
            if key == "researcher":
                config.RESEARCH_OUTPUT = full_text
            on_done(full_text)
        except Exception as exc:
            on_error(str(exc))

    threading.Thread(target=_worker, daemon=True).start()

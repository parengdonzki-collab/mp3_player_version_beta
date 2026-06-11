import requests


class LyricsService:

    # -------------------------
    # PROVIDERS
    # -------------------------

    @staticmethod
    def provider_lyrics_ovh(artist, title):
        url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
        res = requests.get(url, timeout=10)

        if res.status_code == 200:
            return res.json().get("lyrics")
        return None


    @staticmethod
    def provider_lyrics_fallback_api(artist, title):
        # Example placeholder (you can replace with real API)
        url = f"https://some-lyrics-api.com/search?artist={artist}&title={title}"
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                return data.get("lyrics")
        except:
            pass
        return None


    @staticmethod
    def provider_genius_like(artist, title):
        # placeholder for Genius-style API integration
        url = f"https://api.example.com/lyrics?artist={artist}&title={title}"
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                return res.json().get("lyrics")
        except:
            pass
        return None


    # -------------------------
    # ENGINE
    # -------------------------

    @staticmethod
    def get_lyrics(artist, title):

        providers = [
            LyricsService.provider_lyrics_ovh,
            LyricsService.provider_lyrics_fallback_api,
            LyricsService.provider_genius_like
        ]

        for provider in providers:
            try:
                result = provider(artist, title)
                if result:
                    return result
            except Exception:
                continue

        return "No lyrics found from any provider."
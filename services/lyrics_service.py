import os
import requests
print("Lyrics Service loading")

# =====================================================
# LRC SERVICE
# =====================================================

class LRCService:

    @staticmethod
    def find_lrc(song_path):
        """
        Looks for:
            song.mp3
            song.lrc
        """

        if not song_path:
            return None

        base, _ = os.path.splitext(song_path)
        lrc_path = base + ".lrc"

        if os.path.exists(lrc_path):
            return lrc_path

        return None

    @staticmethod
    def load_lrc(lrc_path):

        try:
            with open(lrc_path, "r", encoding="utf-8") as f:
                return f.read()

        except Exception as e:
            return f"Error loading LRC: {e}"


# =====================================================
# CACHE SERVICE
# =====================================================

class CacheService:

    CACHE_DIR = "cache/lyrics"

    @staticmethod
    def ensure_cache_dir():
        os.makedirs(CacheService.CACHE_DIR, exist_ok=True)

    @staticmethod
    def build_cache_path(artist, title):

        filename = f"{artist} - {title}.txt"

        # Windows-safe filename
        invalid = r'<>:"/\|?*'

        for char in invalid:
            filename = filename.replace(char, "_")

        return os.path.join(CacheService.CACHE_DIR, filename)

    @staticmethod
    def load_cache(artist, title):

        CacheService.ensure_cache_dir()

        path = CacheService.build_cache_path(artist, title)

        if os.path.exists(path):

            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()

            except Exception:
                return None

        return None

    @staticmethod
    def save_cache(artist, title, lyrics):

        CacheService.ensure_cache_dir()

        path = CacheService.build_cache_path(artist, title)

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(lyrics)

        except Exception:
            pass


# =====================================================
# LYRICS SERVICE
# =====================================================

class LyricsService:
    
    # -------------------------------------------------
    # PROVIDER 1 - lyrics.ovh
    # -------------------------------------------------

    @staticmethod
    def provider_lyrics_ovh(artist, title):

        try:
            url = f"https://api.lyrics.ovh/v1/{artist}/{title}"

            res = requests.get(url, timeout=10)

            if res.status_code == 200:

                data = res.json()

                return data.get("lyrics")

        except requests.exceptions.Timeout:
            print("Lyrics request timed out.")

        except requests.exceptions.RequestException as e:
            print("Network error:", e)

        except Exception as e:
            print("Provider error:", e)

        return None

    # -------------------------------------------------
    # ENGINE
    # -------------------------------------------------

    @staticmethod
    def get_lyrics(artist, title, song_path=None):
        print("getting lyrics")
        # =============================================
        # 1. CHECK LOCAL LRC
        # =============================================

        if song_path:

            lrc_path = LRCService.find_lrc(song_path)

            if lrc_path:

                print("FOUND LRC:", lrc_path)

                return LRCService.load_lrc(lrc_path)

        # =============================================
        # 2. CHECK CACHE
        # =============================================

        cached = CacheService.load_cache(artist, title)

        if cached:

            print("LOADED FROM CACHE")

            return cached

        # =============================================
        # 3. API PROVIDERS
        # =============================================

        providers = [
            LyricsService.provider_lyrics_ovh
        ]

        for provider in providers:

            try:
                result = provider(artist, title)

                if result:

                    print("LYRICS FOUND FROM PROVIDER")

                    # save cache
                    CacheService.save_cache(
                        artist,
                        title,
                        result
                    )

                    return result

            except Exception as e:
                print("Provider failed:", e)

        # =============================================
        # 4. FAIL
        # =============================================

        return "No lyrics found."



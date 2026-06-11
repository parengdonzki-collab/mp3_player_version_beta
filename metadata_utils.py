from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


# ==========================================
# GET SONG METADATA
# ==========================================

def get_song_metadata(mp3_path):

    try:

        audio = MP3(
            mp3_path,
            ID3=EasyID3
        )

        title = audio.get(
            "title",
            ["Unknown"]
        )[0]

        artist = audio.get(
            "artist",
            ["Unknown"]
        )[0]

        return {
            "title": title.strip(),
            "artist": artist.strip()
        }

    except Exception as e:

        print("Metadata error:", e)

        return {
            "title": "Unknown",
            "artist": "Unknown"
        }
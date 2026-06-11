from mutagen import File
from mutagen.easyid3 import EasyID3

import os
import re

class Song:

    def __init__(self, title, path, artist="Unknown Artist", album="Unknown Album", duration="00:00"):

        self.path = path
        self.filename = os.path.basename(path)

        self.extension = os.path.splitext(self.path)[1].lower()
        self.filesize = os.path.getsize(self.path)

        self.title = os.path.splitext(title)[0]
        self.artist = artist
        self.album = album
        self.duration = duration

        # optional overlays only
        self.album_art_data = None
        self.lyrics = None
        self._lyrics_loaded = False
        self._lyrics_loading = False
        
        # safety flag (optional)
        self.metadata_loaded = False
        self.title = title
        self.path = path

        self.format = "Unknown"
        self.bitrate = "0"
        self.sample_rate = "0"

        self.load_metadata()
    # ----------------------------
    # SAFE COMPATIBILITY STUBS
    # ----------------------------

    def load_metadata(self):
        from mutagen.mp3 import MP3


        try:
            audio = MP3(self.path)

            self.format = "MP3"
            self.bitrate = str(int(audio.info.bitrate / 1000))
            self.sample_rate = str(audio.info.sample_rate)

        except Exception:
            self.format = "Unknown"
            self.bitrate = "0"
            self.sample_rate = "0"

    def load_lyrics(self):

        print("LAZY LOADING LYRICS FOR:", self.title)

        # already loaded
        if self._lyrics_loaded:
            return self.lyrics

        # already in memory
        if self.lyrics:
            self._lyrics_loaded = True
            return self.lyrics

        # placeholder (future API / file / DB)
        lyrics = None

        if lyrics:
            self.lyrics = lyrics
        else:
            self.lyrics = "No lyrics found."

        self._lyrics_loaded = True
        return self.lyrics

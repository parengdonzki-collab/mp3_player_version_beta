from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import os


class Song:

    def __init__(self, title, path):

        self.path = path

        self.filename = os.path.basename(path)

        # FALLBACK TITLE
        self.title = title

        self.artist = "Unknown Artist"
        self.album = "Unknown Album"

        self.duration = 0

        # ALBUM ART
        self.album_art_data = None

        self.load_metadata()

    def load_metadata(self):

        try:

            audio = MP3(
                self.path,
                ID3=ID3
            )

            self.duration = int(
                audio.info.length
            )

            # =================================================
            # TEXT METADATA
            # =================================================

            if audio.tags:

                if audio.tags.get("TIT2"):
                    self.title = str(
                        audio.tags.get("TIT2")
                    )

                if audio.tags.get("TPE1"):
                    self.artist = str(
                        audio.tags.get("TPE1")
                    )

                if audio.tags.get("TALB"):
                    self.album = str(
                        audio.tags.get("TALB")
                    )

                # =============================================
                # ALBUM ART
                # =============================================

                for tag in audio.tags.values():

                    if tag.FrameID == "APIC":

                        self.album_art_data = tag.data
                        break

        except Exception as e:

            print("Metadata Error:", e)
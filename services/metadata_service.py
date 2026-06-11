from mutagen import File
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
class MetadataService:

    def try_enrich(self, song):

        try:

            audio = File(song.path)

            if audio and hasattr(audio, "info"):

                total = int(audio.info.length)

                song.duration = (
                    f"{total//60:02}:{total%60:02}"
                )

            if audio.tags:

                # TITLE
                if "TIT2" in audio.tags:
                    song.title = str(
                        audio.tags["TIT2"]
                    )

                # ARTIST
                if "TPE1" in audio.tags:
                    song.artist = str(
                        audio.tags["TPE1"]
                    )

                # ALBUM
                if "TALB" in audio.tags:
                    song.album = str(
                        audio.tags["TALB"]
                    )

                # ALBUM ART
                for tag in audio.tags.values():

                    if tag.FrameID == "APIC":

                        song.album_art_data = tag.data
                        break
            

        except Exception as e:

            print("METADATA ERROR:")
            print(e)
       # =====================================================
    # UPDATE METADATA
    # =====================================================

    def update(self,song,title, artist, album="None" ):
       
       
        path = song.path if hasattr(song, "path") else song


        audio = EasyID3(path)

        audio["title"] = title
        audio["artist"] = artist
        audio["album"] = album
        
        if album:
            audio["album"] = album
        
        audio.save()

        # UPDATE MEMORY OBJECT

        song.title = title
        song.artist = artist
        
        if album:
            song.album = album
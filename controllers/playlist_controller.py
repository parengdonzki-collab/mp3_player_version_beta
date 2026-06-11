from tkinter import filedialog
import os
from models.song import Song
#from services.metadata_service import MetadataService

class PlaylistController:

    def __init__(self, view, songs, playlist, playlist_service, player):
        self.view = view
        self.songs = songs
        self.playlist = playlist
        self.playlist_service = playlist_service
        self.player = player
    # =====================================================
    # SAVE PLAYLIST
    # =====================================================

    def save_playlist(self):


        songs_data = []

        for song in self.songs:

            songs_data.append({
                "title": song.title,
                "path": song.path,
                "artist": song.artist,
                "album": song.album if hasattr(song, "album") else "",
                "duration": song.duration if hasattr(song, "duration") else 0
            })

        self.playlist_service.save_playlist( songs_data)
     # =====================================================
    # LOAD PLAYLIST
    # =====================================================

    def load_playlist(self):

        filepath = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json")]
        )

        if not filepath:
            print("No file selected")
            return

        data = self.playlist_service.load_playlist(filepath)

        self.songs.clear()
        self.playlist.songs.clear()
        self.view.clear_playlist_view()

        # ✅ FIX: support list OR dict
        songs_list = data["songs"] if isinstance(data, dict) else data

        for song_data in songs_list:

            path = song_data["path"]

            if os.path.exists(path):
                self.player.add_song(path)
    #===========================================
    # AUTO LOAD PLAYLIST
    # =====================================================
    def auto_load_playlist(self):

        filepath = os.path.join(
            self.playlist_service.playlist_folder,
            "sakto.json"
        )

        print("AUTOLOAD PATH:", filepath)

        if not os.path.exists(filepath):
            print("No saved playlist found")
            return

        data = self.playlist_service.load_playlist(filepath)

        print("LOADED DATA:", data)

        self.songs.clear()
        self.playlist.songs.clear()
        

        # ✅ handle both formats safely
        if isinstance(data, dict):
            songs_list = data.get("songs", [])
        else:
            songs_list = data

        for song_data in songs_list:

        

            path = song_data.get("path")

            if not path or not os.path.exists(path):
                continue

            # 🚀 FAST LOAD
            song = Song(
                song_data.get("title", os.path.basename(path)),
                path
            )

            song.artist = song_data.get("artist", "Unknown Artist")
            song.album = song_data.get("album", "")
            song.duration = song_data.get("duration", "00:00")

            # ❌ DO NOT CALL:
            self.player.metadata_service.try_enrich(song)

            self.playlist.add_song(song)
    

            self.view.add_song_to_playlist(
                song.title,
                song.artist,
                song.duration
            )
        # ✅ IMPORTANT: update UI counters
        self.view.update_song_count()

        # ✅ AUTO PLAY FIRST SONG
        items = self.view.playlist_box.get_children()

        if items:
            first = items[0]

            self.view.playlist_box.selection_set(first)
            self.view.playlist_box.focus(first)
            
            current_song = self.songs[0]
            self.player.update_song_ui(current_song)
            self.playlist.current_index = 0
            if self.songs:
                self.player.play_song()           
    

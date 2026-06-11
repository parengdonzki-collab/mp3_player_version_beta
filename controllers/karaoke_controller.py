from models import song
from services.lyrics_service import LyricsService
import customtkinter as ctk

class KaraokeController:

    def __init__(self, view, songs, playlist):
        self.view = view
        self.songs = songs
        self.playlist = playlist
        self.current_song = None

    # =====================================================
    # LOAD LYRICS
    # =====================================================

    def load_lyrics(self, song):
        print(f"🎤 Fetching lyrics for: {song.title} by {song.artist}")

        if (
            not hasattr(self, "lyrics_window")
            or not self.lyrics_window.winfo_exists()
        ):
            self.open_lyrics_window()

        self.lyrics_box.delete("1.0", "end")
        self.lyrics_box.insert("1.0", "Loading lyrics...")

        try:
            print("Song path:", song.path)
            # FIXED: Correctly pass the song file path to fetch local .lrc files
            lyrics = LyricsService.get_lyrics(song.artist, song.title, song.path)

            self.lyrics_box.delete("1.0", "end")

            if not lyrics:
                self.lyrics_box.insert("1.0", "No lyrics found")
                return

            lyrics = LyricsService.get_lyrics(
                song.artist,
                song.title,
                song.path
            )

            self.lyrics_box.delete("1.0", "end")
            self.lyrics_box.insert("1.0", lyrics)

        except Exception as e:
            self.lyrics_box.delete("1.0", "end")
            self.lyrics_box.insert("1.0", f"Failed to load lyrics.\n\n{e}")    

    # =====================================================
    # SYNC ENGINE HOOK
    # =====================================================

    def update_active_song(self, song):
        """Updates internal track reference and refreshes open panels instantly"""
        self.current_song = song
        
        # Automatically update lyrics window on track skip / auto-play if it's open
        if hasattr(self, "lyrics_window") and self.lyrics_window.winfo_exists():
            self.load_lyrics(song)
    
    # =====================================================
    # OPEN LYRICS WINDOW
    # =====================================================

    def open_lyrics_window(self):
        if (
            hasattr(self, "lyrics_window")
            and self.lyrics_window.winfo_exists()
        ):
            self.lyrics_window.focus()
            return

        self.lyrics_window = ctk.CTkToplevel(self.view.root)
        self.lyrics_window.transient(self.view.root)
        self.lyrics_window.grab_set()
        self.lyrics_window.focus_force()

        self.lyrics_window.attributes("-topmost", True)
        self.lyrics_window.after(
            100,
            lambda: self.lyrics_window.attributes("-topmost", False)
        )
        self.lyrics_window.title("Lyrics")
        self.lyrics_window.geometry("600x400")

        self.lyrics_box = ctk.CTkTextbox(self.lyrics_window, font=("Arial", 18))
        self.lyrics_box.pack(fill="both", expand=True, padx=10, pady=10)
        self.lyrics_box.insert("1.0", "Lyrics will appear here...")

    def open_lyrics(self):
        """Triggered directly by clicking the menu item button"""
        print("🔍 Open Lyrics requested via menu context...")

        # FIX: If self.current_song is None, actively pull the active track from the playlist object
        if not self.current_song and hasattr(self.playlist, 'songs') and self.playlist.songs:
            if self.playlist.current_index is not None and self.playlist.current_index < len(self.playlist.songs):
                self.current_song = self.playlist.songs[self.playlist.current_index]
                print(f"🎵 Restored tracking reference to active playlist track: {self.current_song.title}")

        # If it's still empty because no song is loaded in the player at all
        if not self.current_song:
            print("❌ Cancelled window launch: No active track loaded in player system context.")
            
            # Open a blank window fallback so the user doesn't get left with nothing appearing
            self.open_lyrics_window()
            self.lyrics_box.delete("1.0", "end")
            self.lyrics_box.insert("1.0", "Please select and play an MP3 track first before loading lyrics.")
            return
        
        # If the window isn't currently open on screen, build it
        if (
            not hasattr(self, "lyrics_window")
            or not self.lyrics_window.winfo_exists()
        ):
            self.open_lyrics_window()

        # Safely fetch local LRC files or API feeds
        self.load_lyrics(self.current_song)


    def open_karaoke_mode(self):
        """Alternative visualization mode pane"""
        if (
            hasattr(self, "lyrics_window")
            and self.lyrics_window.winfo_exists()
        ):
            self.lyrics_window.destroy()

        selected = self.view.playlist_box.selection()
        if not selected:
            print("❌ Selection empty: Click a track inside the list grid layout first.")
            return

        # Safely calculate the index from selection array or string item id
        selected_id = selected[0] if isinstance(selected, (list, tuple)) else selected
        all_items = list(self.view.playlist_box.get_children())
        
        if selected_id not in all_items:
            print("❌ Internal mismatch: Selection identifier not found inside UI children array.")
            return
            
        index = all_items.index(selected_id)

        song = self.songs[index]
        self.current_song = song
        
        print(f"🎤 Opening Karaoke Mode viewport layout for: {song.title}")
        lyrics = LyricsService.get_lyrics(song.artist, song.title, song.path)

        karaoke_window = ctk.CTkToplevel(self.view.root)
        karaoke_window.title(f"Karaoke - {song.title}")
        karaoke_window.geometry("900x700")

        lyrics_box = ctk.CTkTextbox(
            karaoke_window,
            font=("Segoe UI", 28, "bold"),
            wrap="word"
        )
        lyrics_box.pack(fill="both", expand=True, padx=20, pady=20)

        lyrics_box.insert("1.0", lyrics)
        lyrics_box.configure(state="disabled")

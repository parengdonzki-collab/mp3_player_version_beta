import customtkinter as ctk
import pygame
from services.lyrics_engine import LyricsEngine



class FullKaraokeController:

    def __init__(self, view, songs, playlist):

        self.lyrics_engine = LyricsEngine()
        self.view = view
        self.songs = songs
        self.playlist = playlist

        self.karaoke_window = None

        self.prev_label = None
        self.current_label = None
        self.next_label = None

    # =====================================================
    # OPEN KARAOKE MODE
    # =====================================================

    def open_karaoke_mode(self):

        print("KARAOKE MODE OPENED")

        if self.karaoke_window and self.karaoke_window.winfo_exists():
            self.karaoke_window.focus()
            return

        self.karaoke_window = ctk.CTkToplevel(self.view.root)
        self.karaoke_window.title("Karaoke Mode")
        self.karaoke_window.attributes("-fullscreen", True)
        self.karaoke_window.configure(fg_color="black")

        self.karaoke_window.bind(
            "<Escape>",
            lambda e: self.close_karaoke_mode()
        )

        main_frame = ctk.CTkFrame(
            self.karaoke_window,
            fg_color="black"
        )
        main_frame.pack(expand=True, fill="both")

        # PREVIOUS LINE
        self.prev_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=("Arial", 28),
            text_color="gray"
        )
        self.prev_label.pack(pady=(80, 20))

        # CURRENT LINE
        self.current_label = ctk.CTkLabel(
            main_frame,
            text="No Lyrics Loaded",
            font=("Arial", 48, "bold"),
            text_color="white",
            wraplength=1400,
            justify="center"
        )
        self.current_label.pack(expand=True)

        # NEXT LINE
        self.next_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=("Arial", 28),
            text_color="gray"
        )
        self.next_label.pack(pady=(20, 80))

        self.update_karaoke()

    # =====================================================
    # SET ACTIVE SONG (IMPORTANT FIX)
    # =====================================================

    def set_active_song(self, song):

        print("ACTIVE SONG:", song.title)

        self.active_song = song

        self.lyrics_engine.set_lyrics(lyrics)

        print("LYRICS LOADED:", len(lyrics))

    # =====================================================
    # UPDATE LOOP (SYNCED TO MUSIC)
    # =====================================================

    def update_karaoke(self):

        if not self.karaoke_window or not self.karaoke_window.winfo_exists():
            return

        if not self.lyrics_engine.lyrics:
            self.current_label.configure(text="No Lyrics Loaded")
            self.karaoke_window.after(200, self.update_karaoke)
            return

        current_time = pygame.mixer.music.get_pos() / 1000

        previous_line, current_line, next_line = self.lyrics_engine.get_current_lines(
            current_time
        )

        self.update_karaoke_display(
            previous_line,
            current_line,
            next_line
        )

        self.karaoke_window.after(100, self.update_karaoke)

    # =====================================================
    # UPDATE DISPLAY
    # =====================================================

    def update_karaoke_display(
        self,
        previous_line="",
        current_line="",
        next_line=""
    ):

        if not self.karaoke_window or not self.karaoke_window.winfo_exists():
            return

        self.prev_label.configure(text=previous_line)
        self.current_label.configure(text=current_line)
        self.next_label.configure(text=next_line)

    # =====================================================
    # CLOSE
    # =====================================================

    def close_karaoke_mode(self):

        if self.karaoke_window and self.karaoke_window.winfo_exists():
            self.karaoke_window.destroy()

        self.karaoke_window = None
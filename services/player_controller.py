from tkinter import filedialog
from models import song
from services.lyrics_resolver import LyricsResolver
from controllers.playlist_controller import PlaylistController

from services.metadata_service import MetadataService
from controllers.metadata_controller import MetadataController
import pygame
from services.playlist_service import PlaylistService
from models.playlist_model import PlaylistModel
from services.audio_service import AudioService
from models.song import Song
from controllers.karaoke_controller import KaraokeController
from controllers.full_karaoke_controller import FullKaraokeController 
import os
import random
from tkinterdnd2 import DND_FILES
from services.mic_service import MicService
from mutagen import File


class PlayerController:

    def __init__(self, view):

        self.view = view

        self.dragging_slider = False

        self.playlist = PlaylistModel()
        self.playlist.current_index = 0

        self.audio = AudioService()
        self.playlist_service = PlaylistService()
        self.mic_service = MicService()

        self.audio.set_volume(0.5)

        self.shuffle_enabled = False
        self.repeat_enabled = False

        self.closing = False
        self.paused = False

        self.playlist.songs = []
        self.karaoke = KaraokeController(
                                            self.view,
                                            self.playlist.songs,
                                            self.playlist
                                        )
        self.playlist_controller = PlaylistController(
                                                        self.view,
                                                        self.playlist.songs,
                                                        self.playlist,
                                                        self.playlist_service
                                        )
        self.full_karaoke = FullKaraokeController(
                    self.view,
                    self.playlist.songs,
                    self.playlist
                    )
        self.metadata_service = MetadataService()

        self.metadata_controller = MetadataController(
            self.view,
            self.playlist.songs,
            self.karaoke,
            self.metadata_service,
            self
        )
        self.current_song_length = 0
        self.seek_offset = 0

        self.connect_events()

        self.view.set_close_callback(
            self.close_app
        )

        # AUTO LOAD PLAYLIST
        self.playlist_controller.auto_load_playlist()

        self.check_music_end()
        self.update_progress()

    # =====================================================
    # EVENTS
    # =====================================================

    def connect_events(self):

        # MENU
        self.view.open_mp3_option.configure(
            command=self.load_songs
        )

        self.view.save_playlist_option.configure(
            command=self.playlist_controller.save_playlist
        )

        self.view.load_playlist_option.configure(
            command=self.playlist_controller.load_playlist
        )

        self.view.exit_option.configure(
            command=self.close_app
        )

        self.view.open_lyrics_option.configure(
            command=self.open_lyrics_window
        )
        self.view.edit_metadata_option.configure(
            command=self.metadata_controller.open_metadata_editor
            )
        self.view.karaoke_option.configure(
                command=self.full_karaoke.open_karaoke_mode
            )

        # PLAYER CONTROLS
        self.view.play_button.configure(
            command=self.play_song
        )

        self.view.stop_button.configure(
            command=self.stop_song
        )

        self.view.pause_button.configure(
            command=self.pause_song
        )

        self.view.next_button.configure(
            command=self.next_song
        )

        self.view.prev_button.configure(
            command=self.prev_song
        )

        # SHUFFLE / REPEAT
        self.view.shuffle_button.configure(
            command=self.toggle_shuffle
        )

        self.view.repeat_button.configure(
            command=self.toggle_repeat
        )
        self.view.mic_button.configure(
            command=self.toggle_mic
        )

        # PLAYLIST
        self.view.playlist_box.bind(
            "<Double-Button-1>",
            self.play_song
        )

        self.view.remove_song_button.configure(
            command=self.remove_song
        )

        self.view.clear_playlist_button.configure(
            command=self.clear_playlist
        )

        # SEEK BAR
        self.view.progress_slider.bind(
            "<Button-1>",
            self.start_drag
        )

        self.view.progress_slider.bind(
            "<ButtonRelease-1>",
            self.seek_song
        )

        # VOLUME
        self.view.volume_slider.configure(
            command=self.change_volume
        )

        # DRAG AND DROP
        self.view.playlist_box.drop_target_register(
            DND_FILES
        )

        self.view.playlist_box.dnd_bind(
            "<<Drop>>",
            self.on_drop
        )

        # SEARCH
        self.view.search_entry.bind(
            "<KeyRelease>",
            self.search_song
        )

        # KEYBOARD SHORTCUTS
        self.view.root.bind(
            "<space>",
            lambda e: self.pause_song()
        )

        self.view.root.bind(
            "<Control-o>",
            lambda e: self.load_songs()
        )

        self.view.root.bind(
            "<Delete>",
            lambda e: self.remove_song()
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search_song(self, event=None):

        query = self.view.search_entry.get().lower()

        self.view.playlist_box.selection_remove(
            self.view.playlist_box.selection()
        )

        for item in self.view.playlist_box.get_children():

            values = self.view.playlist_box.item(
                item,
                "values"
            )

            title = str(values[0]).lower()
            artist = str(values[1]).lower()

            if (
                query in title
                or query in artist
            ):

                self.view.playlist_box.selection_set(
                    item
                )

                self.view.playlist_box.focus(
                    item
                )

                self.view.playlist_box.see(
                    item
                )

                break

    # =====================================================
    # SHUFFLE
    # =====================================================

    def toggle_shuffle(self):

        self.shuffle_enabled = (
            not self.shuffle_enabled
        )

        if self.shuffle_enabled:

            self.view.shuffle_button.configure(
                fg_color="green"
            )

        

        else:

            self.view.shuffle_button.configure(
                fg_color="#1f6aa5"
            )



    # =====================================================
    # REPEAT
    # =====================================================

    def toggle_repeat(self):

        self.repeat_enabled = (
            not self.repeat_enabled
        )

        if self.repeat_enabled:

            self.view.repeat_button.configure(
                fg_color="green"
            )


        else:

            self.view.repeat_button.configure(
                fg_color="#1f6aa5"
            )

            

    # =====================================================
    # DRAG AND DROP
    # =====================================================
    def on_drop(self, event):

        files = self.view.root.tk.splitlist(
            event.data
        )

        added = False

        for path in files:

            if self.add_song(path):
                added = True

        if added:
            self.playlist_controller.save_playlist()
            

    # =====================================================
    # LOAD SONGS
    # =====================================================

    def load_songs(self):
            

        paths = filedialog.askopenfilenames(
            filetypes=[
                (
                    "Audio Files",
                    "*.mp3 *.wav *.ogg *.flac"
                )
            ]
        )

        if not paths:
            return

        added = False

        for path in paths:

            if self.add_song(path):
                added = True

        if added:
            self.playlist_controller.save_playlist()


    # =====================================================
    # PLAY SONG
    # =====================================================

    def play_song(self, event=None):

        song, item, index = self.get_selected_song()

        if not song:
            return
        
        index = self.view.playlist_box.index(
            item
        )

        self.playlist.current_index = index

        song = self.playlist.songs[index]

        self.start_song(song)
    # =====================================================
    # NEXT SONG
    # =====================================================

    def next_song(self):

        self.play_next_song()

    # =====================================================
    # PLAY NEXT LOGIC
    # =====================================================

    def play_next_song(self):

        if not self.playlist.songs:
            return

        # REPEAT
        if self.repeat_enabled:

            song = self.playlist.songs[
                self.playlist.current_index
            ]

        # SHUFFLE
        elif self.shuffle_enabled:

            self.playlist.current_index = (
                random.randint(
                    0,
                    len(self.playlist.songs) - 1
                )
            )

            song = self.playlist.songs[
                self.playlist.current_index
            ]

        # NORMAL
        else:

            self.playlist.current_index += 1

            if (
                self.playlist.current_index
                >= len(self.playlist.songs)
            ):

                self.playlist.current_index = 0

            song = self.playlist.songs[
                self.playlist.current_index
            ]

        self.start_song(song)
    # =====================================================
    # PREVIOUS SONG
    # =====================================================

    def prev_song(self):

        if not self.playlist.songs:
            return

        self.playlist.current_index -= 1

        if self.playlist.current_index < 0:

            self.playlist.current_index = (
                len(self.playlist.songs) - 1
            )

        song = self.playlist.songs[
            self.playlist.current_index
        ]

        self.start_song(song)
    # =====================================================
    # UPDATE SONG UI
    # =====================================================

    def update_song_ui(self, song):

        self.view.update_album_art(
            song.album_art_data
        )

        self.view.song_title_label.configure(
            text=song.title
        )

        self.view.artist_label.configure(
            text=song.artist
        )

    # =====================================================
    # HIGHLIGHT CURRENT SONG
    # =====================================================

    def highlight_current_song(self):

        items = self.view.playlist_box.get_children()

        if not items:
            return

        if self.playlist.current_index >= len(items):
            return

        item = items[self.playlist.current_index]

        self.view.playlist_box.selection_remove(
            self.view.playlist_box.selection()
        )

        self.view.playlist_box.selection_set(item)

        self.view.playlist_box.focus(item)

        self.view.playlist_box.see(item)
   
    # =====================================================
    # STOP
    # =====================================================

    def stop_song(self, event=None):

        self.audio.stop()

        self.paused = False

        self.current_song_length = 0

        self.seek_offset = 0

        self.view.progress_slider.set(0)

        self.view.time_label.configure(
            text="00:00 / 00:00"
        )

    # =====================================================
    # PAUSE
    # =====================================================

    def pause_song(self):

        if not pygame.mixer.music.get_busy() and not self.paused:
            return

        if not self.paused:

            self.audio.pause()

            self.paused = True

        else:

            self.audio.resume()

            self.paused = False

    # =====================================================
    # SEEK
    # =====================================================

    def start_drag(self, event=None):

        self.dragging_slider = True

    def seek_song(self, event=None):

        if self.current_song_length <= 0:
            return

        if not self.playlist.songs:
            return

        progress = self.view.progress_slider.get()

        seek_time = (
            progress / 100
        ) * self.current_song_length

        self.seek_offset = seek_time

        current_song = self.playlist.songs[
            self.playlist.current_index
        ]

        pygame.mixer.music.load(
            current_song.path
        )

        pygame.mixer.music.play(
            start=seek_time
        )

        self.dragging_slider = False

        self.paused = False

    # =====================================================
    # VOLUME
    # =====================================================

    def change_volume(self, value):

        volume = float(value) / 100

        self.audio.set_volume(volume)

    # =====================================================
    # PROGRESS
    # =====================================================

    def update_progress(self):

        if self.closing:
            return

        if pygame.mixer.music.get_busy():

            current_time = (
                pygame.mixer.music.get_pos() / 1000
            ) + self.seek_offset

            total_time = (
                self.current_song_length
            )

            if (
                total_time > 0
                and not self.dragging_slider
            ):

                progress = (
                    current_time / total_time
                ) * 100

                self.view.progress_slider.set(
                    progress
                )

                current = self.format_time(
                    current_time
                )

                total = self.format_time(
                    total_time
                )

                self.view.time_label.configure(
                    text=f"{current} / {total}"
                )

        self.view.root.after(
            1000,
            self.update_progress
        )

    # =====================================================
    # CHECK SONG END
    # =====================================================

    def check_music_end(self):

        if self.closing:
            return

        if (
            not pygame.mixer.music.get_busy()
            and not self.paused
            and self.current_song_length > 0
            and not self.dragging_slider
        ):

            self.play_next_song()

        self.view.root.after(
            1000,
            self.check_music_end
        )

    # =====================================================
    # TIME FORMAT
    # =====================================================

    def format_time(self, seconds):

        minutes = int(seconds // 60)

        seconds = int(seconds % 60)

        return f"{minutes:02}:{seconds:02}"

    # =====================================================
    # REMOVE SONG
    # =====================================================

    def remove_song(self):

        song, item, index = self.get_selected_song()

        if not song:
            return

        
        del self.playlist.songs[index]

    

        self.view.playlist_box.delete(item)

        self.playlist_controller.save_playlist()

    # =====================================================
    # CLEAR PLAYLIST
    # =====================================================

    def clear_playlist(self):

        self.audio.stop()

        self.playlist.songs.clear()

    
        self.playlist.current_index = 0

        self.view.clear_playlist()

        self.playlist_controller.save_playlist()

    
        

    
        
    # =====================================================
    # MIC
    # =====================================================

    def toggle_mic(self):

        if self.mic_service.enabled:

            self.mic_service.stop_monitoring()

            self.view.mic_button.configure(
                text="🎤 Mic"
            )

        
        else:

            self.mic_service.start_monitoring()

            self.view.mic_button.configure(
                text="🎤 Mic ON"
            )

    def add_song(self, path):

        supported_formats = (
            ".mp3",
            ".wav",
            ".ogg",
            ".flac"
        )

        if not path.lower().endswith(
            supported_formats
        ):
            return False

        if any(
            s.path == path
            for s in self.playlist.songs
        ):
            return False

        song = Song(
            os.path.basename(path),
            path
        )

        self.playlist.add_song(song)

        self.view.add_song_to_playlist(
            song.title,
            song.artist,
            song.duration
        )

        return True
    def get_selected_song(self):

        selected = self.view.playlist_box.selection()

        if not selected:
            return None, None, None

        item = selected[0]

        index = self.view.playlist_box.index(item)

        song = self.playlist.songs[index]

        return song, item, index    
    def start_song(self, song):
        
        self.seek_offset = 0

        self.audio.play(song)

        self.paused = False

        self.current_song_length = (
            self.audio.get_song_length(song)
        )

        self.update_song_ui(song)

        # LOAD LRC LYRICS
    

        lyrics = song.load_lyrics()
        

    
        print("SONG LYRICS:")
        print(song.lyrics)
        self.full_karaoke.lyrics_engine.set_lyrics(lyrics)

        # SET ACTIVE SONG
        self.full_karaoke.active_song = song

        self.highlight_current_song()
    def open_lyrics_window(self):
        self.karaoke.open_lyrics_window() 
    def load_lyrics(self, song):
        self.karaoke.load_lyrics(song)       
    # =====================================================
    # CLOSE APP
    # =====================================================

    def close_app(self):

        if self.closing:
            return

        self.closing = True

        
        self.audio.quit()
        
        self.mic_service.stop_monitoring()

        self.view.root.after(
            0,
            self.view.root.destroy
        )
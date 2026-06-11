from tkinter import filedialog

from views.radio_view import RadioView
from services.radio_service import RadioService
from controllers.radio_controller import RadioController



from controllers.playlist_controller import PlaylistController
from controllers.metadata_controller import MetadataController
from controllers.karaoke_controller import KaraokeController
from controllers.full_karaoke_controller import FullKaraokeController
from services.bridge import connect_audio_to_visualizer
from services.metadata_service import MetadataService
from services.lyrics_service import LyricsService
from services.playlist_service import PlaylistService
from services.audio_service import AudioService
from services.mic_service import MicService

from models.playlist_model import PlaylistModel
from models.song import Song
from views.eq_panel import EQPanel
from tkinterdnd2 import DND_FILES
import subprocess
import sys
from karaoke_app import KaraokeApp
import pygame
import os
import random
import time
class PlayerController:
    def __init__(self, view, audio_service, visualizer):
        # inside __init__, after other controllers:
        self.radio_service = RadioService()
        self.view = view
        self.audio_service = audio_service
        self.visualizer = visualizer
        self.dragging_slider = False

        self.playlist = PlaylistModel()
        self.playlist.current_index = 0

        self.audio = audio_service

        self.playlist_service = PlaylistService()

        self.metadata_service = MetadataService()
        self.lyrics_service = LyricsService()

        self.mic_service = MicService()

        self.audio.set_volume(0.5)

        self.shuffle_enabled = False
        self.repeat_enabled = False

        self.closing = False
        self.paused = False
        self.karaoke_mode = False
        
        # Karaoke isolation flags
        self.karaoke_mode = False
        self.pause_all_logic = False
        
        self.current_song_length = 0
        
        
        # =====================================================
        # SONG STORAGE
        # =====================================================

        self.playlist.songs = []

        # =====================================================
        # CONTROLLERS
        # =====================================================

        self.karaoke = KaraokeController(
            self.view,
            self.playlist.songs,
            self.playlist
        )

        self.full_karaoke = FullKaraokeController(
            self.view,
            self.playlist.songs,
            self.playlist
        )

        self.playlist_controller = PlaylistController(
            self.view,
            self.playlist.songs,
            self.playlist,
            self.playlist_service,
            self
        )

        self.metadata_controller = MetadataController(
            self.view,
            self.playlist.songs,
            self.karaoke,
            self.metadata_service,
            self
        )

        # =====================================================
        # SETUP
        # =====================================================

        self.connect_events()
        self._connect_eq() 

        self.view.set_close_callback(
            self.close_app
        )
        
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
            command=self.on_open_lyrics_clicked
        )

        self.view.edit_metadata_option.configure(
            command=self.metadata_controller.open_metadata_editor
        )

        self.view.karaoke_option.configure(
            command=self.launch_karaoke
        )
                
        self.view.launch_visual_option.configure(
            command=self.open_radio   # or add a new menu item
        )
   

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

                # Change this line inside connect_events:
        self.view.playlist_box.bind(
            "<Double-1>",
            lambda e: self.play_song()
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

        # SHORTCUTS

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
        

    def _connect_eq(self):
        eq = self.audio.eq

        self.view.eq_panel.bass_slider.configure(
                command=lambda v: eq.set_bass(float(v))
            )
        self.view.eq_panel.mid_slider.configure(
                command=lambda v: eq.set_mid(float(v))
            )
        self.view.eq_panel.treble_slider.configure(
                command=lambda v: eq.set_treble(float(v))
            )
        self.view.eq_panel.reset_button.configure(
                command=self._reset_eq
            )

    def _reset_eq(self):
       self.audio.eq.set_bass(1.0)
       self.audio.eq.set_mid(1.0)
       self.audio.eq.set_treble(1.0)
       self.view.eq_panel.bass_slider.set(1.0)
       self.view.eq_panel.mid_slider.set(1.0)
       self.view.eq_panel.treble_slider.set(1.0)

    # =====================================================
    # SONG LOADING
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
        
    
   

    def add_song(self, path):

        try:

            supported_formats = (
                ".mp3",
                ".wav",
                ".ogg",
                ".flac"
            )

            if not path.lower().endswith(supported_formats):
                return False

            if any(s.path == path for s in self.playlist.songs):
                return False

            song = Song(
                    os.path.basename(path),
                    path
            )

            self.metadata_service.try_enrich(song)

            self.playlist.add_song(song)

            self.view.add_song_to_playlist(
                song.title,
                song.artist,
                song.duration
            )
           
            return True

        except Exception as e:

            print("ADD SONG ERROR:")
            print(e)

        return False
        # =====================================================
    # PLAYBACK
    # =====================================================

    def play_song(self, event=None):
        
        
        if not self.playlist.songs:
            return

        # 1. Safely parse the current selection from the Treeview grid
        
        selected_items = self.view.playlist_box.selection()
        if selected_items:
            selected_id = selected_items[0] if isinstance(selected_items, (list, tuple)) else selected_items
            all_items = self.view.playlist_box.get_children()
            if selected_id in all_items:
                self.playlist.current_index = all_items.index(selected_id)
        else:
            if self.playlist.current_index is None:
                self.playlist.current_index = 0

        if self.playlist.current_index >= len(self.playlist.songs):
            self.playlist.current_index = 0
        
        
      
        current_song = self.playlist.songs[self.playlist.current_index]
        
        self.audio.play(current_song)
        
        self.karaoke.update_active_song(current_song)
        
    
        
            # FIXED: Removed self.visualizer_manager.launch() from here!
        
        self.current_song_length = self.audio.get_song_length(current_song)
        self.is_paused = False
        
        
        self.update_status("playing", current_song.title)
        # 2. Configure state parameters


        
        self.update_song_ui(current_song)

        self.paused = False
        
        
        self.is_paused = False
               
        
        

    def start_song(self, song):

        
        self.seek_offset = 0

        self.audio.play(song)
        
        self.karaoke.update_active_song(song)
        print("CURRENT SONG SET:", self.karaoke.current_song.title)

        self.paused = False
    
        self.current_song_length = (
            self.audio.get_song_length(song)
        )

        self.update_song_ui(song)

        self.full_karaoke.lyrics_engine.set_lyrics(
            song.lyrics
        )

        self.full_karaoke.active_song = song

        self.highlight_current_song()
        
        self.update_status("playing", song.title)
        
        self.check_music_end()

    def stop_song(self, event=None):

        self.audio.stop()
        
        self.update_status("STOPPED")

        self.paused = False

        self.current_song_length = 0

        self.seek_offset = 0

        self.view.progress_slider.set(0)

        self.view.time_label.configure(
            text="00:00 / 00:00"
        )

    def pause_song(self):
        if not pygame.mixer.music.get_busy() and not self.is_paused:
            return

        if not self.is_paused:
            self.audio.pause()
            self.pause_start_time = time.time()
            self.is_paused = True
            self.update_status("paused", self.karaoke.current_song.title)

        else:
            self.audio.resume()
            self.paused_time_total += time.time() - self.pause_start_time
            self.is_paused = False
            self.update_status("playing", self.karaoke.current_song.title)        
    def next_song(self):

        self.play_next_song()

    def play_next_song(self):

        if not self.playlist.songs:
            return

        if self.repeat_enabled:

            song = self.playlist.songs[
                self.playlist.current_index
            ]

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
        print("AUTO NEXT:", self.playlist.current_index)

        self.start_song(song)

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
    # UI
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
        audio_info = (
        f"{song.format} • "
        f"{song.bitrate}kbps • "
        f"{song.sample_rate}Hz"
    )

        self.view.update_audio_info(audio_info)

   
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
    def on_open_lyrics_clicked(self):
        print("clicked")
        song = self.karaoke.current_song

        if not song:
            return

    

        print("loading Lyrics")
        self.karaoke.open_lyrics()  # 👈 open window

        self.karaoke.load_lyrics(song)  # 👈 push lyrics into karaoke UI
    # =====================================================
    # SEARCH
    # =====================================================
    def open_radio(self):
        radio_view = RadioView(self.view.root)
        radio_ctrl = RadioController(radio_view, self.radio_service)

        radio_view.search_button.configure(
            command=lambda: radio_ctrl.search(radio_view.search_entry.get())
        )
        radio_view.play_button.configure(
            command=lambda: radio_ctrl.play_station(
                *radio_view.get_selected_url_and_name()
            )
        )
        radio_view.stop_button.configure(command=radio_ctrl.stop)
        radio_view.station_list.bind(
            "<Double-1>",
            lambda e: radio_ctrl.play_station(
                *radio_view.get_selected_url_and_name()
            )
        )

        # load top stations immediately on open
        radio_ctrl.search("")
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
    # REMOVE / CLEAR
    # =====================================================

    def remove_song(self):

        index = self.view.get_selected_index()
        if index is None:
            return

        if index < 0 or index >= len(self.playlist.songs):
            return

        # remove from model
        self.playlist.songs.pop(index)

        # remove from UI
        self.view.playlist_box.delete(*self.view.playlist_box.get_children())

        # rebuild UI from model (SAFE + SIMPLE)
        for song in self.playlist.songs:
            self.view.add_song_to_playlist(
                song.title,
                song.artist,
                song.duration
            )

        # fix index drift
        if self.playlist.current_index >= len(self.playlist.songs):
            self.playlist.current_index = max(0, len(self.playlist.songs) - 1)
                

    def clear_playlist(self):

        self.audio.stop()

        self.playlist.songs.clear()

        self.playlist.current_index = 0

        self.view.clear_playlist_view()

        

    # =====================================================
    # SHUFFLE / REPEAT
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
    # SEEK
    # =====================================================

    def start_drag(self, event=None):

        self.dragging_slider = True

    def seek_song(self, event=None):
        if not self.playlist.songs:
            return

        if self.current_song_length <= 0:
            return

        progress = self.view.progress_slider.get()
        seek_time = (progress / 100) * self.current_song_length

        self.audio.seek(seek_time)
        self.dragging_slider = False    
      # =====================================================
    # PROGRESS
    # =====================================================
    def update_progress(self):
        if self.closing:
            return

        total_time = self.current_song_length

        if total_time > 0 and not self.dragging_slider:

            current_time = self.audio.get_position_ms() / 1000.0

            progress = (current_time / total_time) * 100
            progress = max(0, min(100, progress))

            self.view.progress_slider.set(progress)

            self.view.time_label.configure(
                text=f"{self.format_time(current_time)} / {self.format_time(total_time)}"
            )

        self.view.root.after(200, self.update_progress)  
    def check_music_end(self):
        if self.closing:
            return

        if self.playlist.songs and self.current_song_length > 0:

            pos = self.audio.get_position_ms()

            if pos >= 0:
                current_time = pos / 1000.0

                if current_time >= self.current_song_length:
                    print("🎵 Track finished! Next song...")
                    self.play_next_song()
                    

        self.view.root.after(500, self.check_music_end)      
    # =====================================================
    # UTILITIES
    # =====================================================

    def format_time(self, seconds):

        minutes = int(seconds // 60)

        seconds = int(seconds % 60)

        return f"{minutes:02}:{seconds:02}"

    def change_volume(self, value):

        volume = float(value) / 100

        self.audio.set_volume(volume)

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

    def get_selected_song(self):

        selected = self.view.playlist_box.selection()

        if not selected:
            return None, None, None

        item = selected[0]

        index = self.view.playlist_box.index(item)

        song = self.playlist.songs[index]

        return song, item, index

    # =====================================================
    # LYRICS
    # =====================================================
    
    def open_lyrics_window(self):

        self.karaoke.open_lyrics()

    def load_lyrics(self, song):

        self.karaoke.load_lyrics(song)


    def launch_karaoke(self):
        self.current_song_length = 0
        pygame.mixer.music.stop()

        self.audio.stop()

        subprocess.Popen(
            [sys.executable, "karaoke_app.py"]
        )
  
    def update_status(self, state, song_title=""):
        state = state.lower()  # 🔥 normalize everything

        if state == "playing":
            self.view.status_label.configure(text=f"Now Playing: {song_title}")

        elif state == "paused":
            self.view.status_label.configure(text=f"Paused: {song_title}")

        elif state == "stopped":
            self.view.status_label.configure(text="Stopped")

        else:
            self.view.status_label.configure(text="Ready")

    # =====================================================
    # CLOSE
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
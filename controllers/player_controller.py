from tkinter import filedialog
import pygame
from services.playlist_service import PlaylistService
from models.playlist_model import PlaylistModel
from services.audio_service import AudioService
from models.song import Song
import os
import random


class PlayerController:

    def __init__(self, view):

        self.view = view

        self.dragging_slider = False

        self.playlist = PlaylistModel()
        self.playlist.current_index = 0

        self.audio = AudioService()
        self.playlist_service = PlaylistService()

        self.audio.set_volume(0.5)

        self.shuffle_enabled = False
        self.repeat_enabled = False

        self.closing = False
        self.paused = False

        self.songs = []

        self.current_song_length = 0
        self.seek_offset = 0

        self.connect_events()

        self.view.set_close_callback(
            self.close_app
        )

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
            command=self.save_playlist
        )

        self.view.load_playlist_option.configure(
            command=self.load_playlist
        )

        self.view.exit_option.configure(
            command=self.close_app
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

    # =====================================================
    # SHUFFLE
    # =====================================================

    def toggle_shuffle(self):

        self.shuffle_enabled = not self.shuffle_enabled

        if self.shuffle_enabled:

            self.view.shuffle_button.configure(
                fg_color="green"
            )

            print("Shuffle ON")

        else:

            self.view.shuffle_button.configure(
                fg_color="#1f6aa5"
            )

            print("Shuffle OFF")

    # =====================================================
    # REPEAT
    # =====================================================

    def toggle_repeat(self):

        self.repeat_enabled = not self.repeat_enabled

        if self.repeat_enabled:

            self.view.repeat_button.configure(
                fg_color="green"
            )

            print("Repeat ON")

        else:

            self.view.repeat_button.configure(
                fg_color="#1f6aa5"
            )

            print("Repeat OFF")

    # =====================================================
    # LOAD SONGS
    # =====================================================

    def load_songs(self):

        paths = filedialog.askopenfilenames(
            filetypes=[("MP3 Files", "*.mp3")]
        )

        if not paths:
            return

        for path in paths:

            song = Song(
                os.path.basename(path),
                path
            )

            self.songs.append(song)

            self.playlist.add_song(song)

            self.view.add_song_to_playlist(
                song.title,
                song.artist,
                song.duration
            )

        self.save_playlist()

    # =====================================================
    # PLAY SONG
    # =====================================================

    def play_song(self, event=None):

        selected = self.view.playlist_box.selection()

        if not selected:
            return

        item = selected[0]

        index = self.view.playlist_box.index(item)

        self.playlist.current_index = index

        song = self.songs[index]

        self.seek_offset = 0

        self.audio.play(song)

        self.current_song_length = self.audio.get_song_length(song)

        # UPDATE UI
        self.update_song_ui(song)

        # HIGHLIGHT
        self.highlight_current_song()

    # =====================================================
    # NEXT SONG
    # =====================================================

    def next_song(self):

        self.play_next_song()

    # =====================================================
    # PLAY NEXT LOGIC
    # =====================================================

    def play_next_song(self):

        if not self.songs:
            return

        # REPEAT
        if self.repeat_enabled:

            song = self.songs[
                self.playlist.current_index
            ]

        # SHUFFLE
        elif self.shuffle_enabled:

            self.playlist.current_index = random.randint(
                0,
                len(self.songs) - 1
            )

            song = self.songs[
                self.playlist.current_index
            ]

        # NORMAL
        else:

            self.playlist.current_index += 1

            if self.playlist.current_index >= len(self.songs):

                self.playlist.current_index = 0

            song = self.songs[
                self.playlist.current_index
            ]

        self.seek_offset = 0

        self.audio.play(song)

        self.current_song_length = self.audio.get_song_length(song)

        self.update_song_ui(song)

        self.highlight_current_song()

    # =====================================================
    # PREVIOUS SONG
    # =====================================================

    def prev_song(self):

        if not self.songs:
            return

        self.playlist.current_index -= 1

        if self.playlist.current_index < 0:

            self.playlist.current_index = (
                len(self.songs) - 1
            )

        song = self.songs[
            self.playlist.current_index
        ]

        self.seek_offset = 0

        self.audio.play(song)

        self.current_song_length = self.audio.get_song_length(song)

        self.update_song_ui(song)

        self.highlight_current_song()

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

        item = self.view.playlist_box.get_children()[
            self.playlist.current_index
        ]

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

        self.current_song_length = 0

        self.seek_offset = 0

        self.view.progress_slider.set(0)

        self.view.time_label.configure(
            text="00:00 / 00:00"
        )

        self.view.song_title_label.configure(
            text="No Song"
        )

        self.view.artist_label.configure(
            text="Unknown Artist"
        )

        self.view.update_album_art(None)

    # =====================================================
    # PAUSE
    # =====================================================

    def pause_song(self):

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

        progress = self.view.progress_slider.get()

        seek_time = (
            progress / 100
        ) * self.current_song_length

        self.seek_offset = seek_time

        pygame.mixer.music.play(
            start=seek_time
        )

        pygame.mixer.music.set_pos(
            seek_time
        )

        self.dragging_slider = False

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

            total_time = self.current_song_length

            if total_time > 0 and not self.dragging_slider:

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

        selected = self.view.playlist_box.selection()

        if not selected:
            return

        item = selected[0]

        index = self.view.playlist_box.index(item)

        del self.songs[index]

        del self.playlist.songs[index]

        self.view.playlist_box.delete(item)

        self.save_playlist()

    # =====================================================
    # CLEAR PLAYLIST
    # =====================================================

    def clear_playlist(self):

        self.audio.stop()

        self.songs.clear()

        self.playlist.songs.clear()

        self.playlist.current_index = 0

        self.view.clear_playlist()

        self.view.progress_slider.set(0)

        self.view.time_label.configure(
            text="00:00 / 00:00"
        )

        self.view.song_title_label.configure(
            text="No Song"
        )

        self.view.artist_label.configure(
            text="Unknown Artist"
        )

        self.view.update_album_art(None)

        self.save_playlist()

        print("Playlist cleared!")

    # =====================================================
    # SAVE PLAYLIST
    # =====================================================

    def save_playlist(self):

        songs_data = []

        for song in self.songs:

            songs_data.append({
                "title": song.title,
                "path": song.path
            })

        self.playlist_service.save_playlist(
            "my_playlist",
            songs_data
        )

        print("Playlist saved!")

    # =====================================================
    # LOAD PLAYLIST
    # =====================================================

    def load_playlist(self):

        filepath = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json")]
        )

        if not filepath:
            return

        data = self.playlist_service.load_playlist(
            filepath
        )

        self.songs.clear()

        self.playlist.songs.clear()

        self.view.clear_playlist()

        for song_data in data["songs"]:

            path = song_data["path"]

            if os.path.exists(path):

                song = Song(
                    song_data["title"],
                    path
                )

                self.songs.append(song)

                self.playlist.add_song(song)

                self.view.add_song_to_playlist(
                    song.title,
                    song.artist,
                    song.duration
                )

        print("Playlist loaded!")

        self.save_playlist()

    # =====================================================
    # AUTO LOAD PLAYLIST
    # =====================================================

    def auto_load_playlist(self):

        filepath = os.path.join(
            self.playlist_service.playlist_folder,
            "my_playlist.json"
        )

        if not os.path.exists(filepath):
            return

        data = self.playlist_service.load_playlist(
            filepath
        )

        self.songs.clear()

        self.view.clear_playlist()

        for song_data in data["songs"]:

            path = song_data["path"]

            if os.path.exists(path):

                song = Song(
                    song_data["title"],
                    path
                )

                self.songs.append(song)

                self.playlist.add_song(song)

                self.view.add_song_to_playlist(
                    song.title,
                    song.artist,
                    song.duration
                )

        print("Auto playlist loaded!")

    # =====================================================
    # CLOSE APP
    # =====================================================

    def close_app(self):

        if self.closing:
            return

        self.closing = True

        print("Shutting down...")

        self.audio.quit()

        self.view.root.after(
            0,
            self.view.root.destroy
        )
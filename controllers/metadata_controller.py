import customtkinter as ctk
from mutagen.easyid3 import EasyID3


class MetadataController:

    def __init__(
        self,
        view,
        songs,
        karaoke,
        metadata_service,
        player_controller
    ):
        self.view = view
        self.songs = songs
        self.karaoke = karaoke
        self.metadata_service = metadata_service
        self.player_controller = player_controller

    def open_metadata_editor(self):

        selected = self.view.playlist_box.selection()

        if not selected:
            return

        index = self.view.playlist_box.index(
            selected[0]
        )

        song = self.songs[index]

        window = ctk.CTkToplevel(
            self.view.root
        )
        window.transient(self.view.root)
        window.grab_set()
        window.focus_force()

        window.attributes("-topmost", True)
        window.after(
            100,
            lambda: window.attributes("-topmost", False)
        )
        window.title("Edit Metadata")
        window.geometry("400x250")

        # TITLE

        title_label = ctk.CTkLabel(
            window,
            text="Title"
        )

        title_label.pack(
            pady=(15, 5)
        )

        title_entry = ctk.CTkEntry(
            window,
            width=300
        )

        title_entry.pack()

        title_entry.insert(
            0,
            song.title
        )

        # ARTIST

        artist_label = ctk.CTkLabel(
            window,
            text="Artist"
        )

        artist_label.pack(
            pady=(15, 5)
        )

        artist_entry = ctk.CTkEntry(
            window,
            width=300
        )

        artist_entry.pack()

        artist_entry.insert(
            0,
            song.artist
        )

        # SAVE

        def save_metadata():

            new_title = title_entry.get().strip()
            new_artist = artist_entry.get().strip()

            # SERVICE
            self.metadata_service.update(
                song,
                new_title,
                new_artist
            )

            # UPDATE MODEL
            song.title = new_title
            song.artist = new_artist

            # UPDATE PLAYLIST UI
            item = selected[0]

            self.view.playlist_box.item(
                item,
                values=(
                    song.title,
                    song.artist,
                    song.duration
                )
            )

            # UPDATE NOW PLAYING UI
            self.player_controller.update_song_ui(song)

            # RELOAD LYRICS
            self.karaoke.load_lyrics(song)

            window.destroy()

        # BUTTON

        save_button = ctk.CTkButton(
            window,
            text="Save",
            command=save_metadata
        )

        save_button.pack(
            pady=20
        )
    
 
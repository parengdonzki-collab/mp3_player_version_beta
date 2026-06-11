import json
import os
from tkinter import filedialog

class PlaylistService:

    def __init__(self):

        BASE_DIR = os.path.dirname(
            os.path.dirname(__file__)
        )

        self.playlist_folder = os.path.join(BASE_DIR, "playlists")
        self.lyrics_folder = os.path.join(BASE_DIR, "lyrics")

        os.makedirs(self.playlist_folder, exist_ok=True)
        os.makedirs(self.lyrics_folder, exist_ok=True)

    # =========================
    # SAVE
    # =========================

    def save_playlist(self, songs):

        filepath = filedialog.asksaveasfilename(
            initialdir=self.playlist_folder,
            defaultextension=".json",
            filetypes=[
                ("JSON Files", "*.json"),
                ("All Files", "*.*")
            ]
        )

        if not filepath:
            return

        data = {"songs": songs}

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Saved:", filepath)

    # =========================
    # LOAD
    # =========================

    def load_playlist(self, filepath):

        if not filepath:
            return {"songs": []}

        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
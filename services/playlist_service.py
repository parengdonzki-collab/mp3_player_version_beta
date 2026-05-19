import json
import os


class PlaylistService:

    def __init__(self):

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))

        self.playlist_folder = os.path.join(
            BASE_DIR,
            "playlists"
        )

        os.makedirs(self.playlist_folder, exist_ok=True)

    def save_playlist(self, filename, songs):

        filepath = os.path.join(
            self.playlist_folder,
            f"{filename}.json"
        )

        data = {
            "songs": songs
        }

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Saved:", filepath)

    def load_playlist(self, filepath):

        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
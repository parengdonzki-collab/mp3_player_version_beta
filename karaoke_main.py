from karaoke_app import KaraokeApp


def open_karaoke(self):

    current_song = self.player_controller.current_song

    app = KaraokeApp(
        song_path=current_song.path,
        artist=current_song.artist,
        title=current_song.title
    )

    app.run()
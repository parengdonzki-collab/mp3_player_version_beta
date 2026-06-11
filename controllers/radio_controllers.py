import pygame
import threading

class RadioController:
    def __init__(self, view, radio_service):
        self.view = view
        self.radio_service = radio_service
        self.current_station = None

    def search(self, query=""):
        self.view.set_status("Searching...")
        threading.Thread(
            target=self._search_thread,
            args=(query,),
            daemon=True
        ).start()

    def _search_thread(self, query):
        stations = self.radio_service.search_stations(query)
        self.view.root.after(0, lambda: self._populate(stations))

    def _populate(self, stations):
        self.view.clear_stations()
        for s in stations:
            self.view.add_station(
                s.get("name", "Unknown"),
                s.get("country", ""),
                s.get("url_resolved", "")
            )
        self.view.set_status(f"{len(stations)} stations found")

    def play_station(self, url, name):
        if not url:
            return
        self.view.set_status(f"Connecting to {name}...")
        threading.Thread(
            target=self._play_thread,
            args=(url, name),
            daemon=True
        ).start()

    def _play_thread(self, url, name):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(url)
            pygame.mixer.music.play()
            self.view.root.after(
                0, lambda: self.view.set_status(f"▶ Now Playing: {name}")
            )
        except Exception as e:
            self.view.root.after(
                0, lambda: self.view.set_status(f"Error: {e}")
            )

    def stop(self):
        pygame.mixer.music.stop()
        self.view.set_status("Stopped")
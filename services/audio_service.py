import pygame
import sounddevice as sd
import numpy as np
from mutagen.mp3 import MP3
from pydub import AudioSegment
from services.eq_service import EQService

class AudioService:

    CHUNK = 1024
    RATE = 44100

    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=self.RATE)

        self.current_song_path = None
        self.is_playing = False
        self.is_paused = False
        self._seek_offset_ms = 0

        # Decoded PCM of the current song for the visualizer
        self._pcm: np.ndarray | None = None
        self._pcm_rate: int = self.RATE
        self.eq = EQService(rate=self.RATE)  
    # =====================================================
    # VISUALIZER AUDIO — reads from decoded PCM, not mic
    # =====================================================
    def get_audio(self) -> np.ndarray:
        if self._pcm is None or not self.is_playing:
            return np.zeros(self.CHUNK)

        pos_ms = self.get_position_ms()
        sample_idx = int((pos_ms / 1000.0) * self._pcm_rate)
        chunk = self._pcm[sample_idx: sample_idx + self.CHUNK]

        if len(chunk) < self.CHUNK:
            return np.zeros(self.CHUNK)
        return self.eq.process(chunk)  
        return chunk

    # =====================================================
    # PLAY
    # =====================================================
    def play(self, song):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(song.path)
        pygame.mixer.music.play()
        self.current_song_path = song.path
        self.is_playing = True
        self.is_paused = False
        self._seek_offset_ms = 0
        self._load_pcm(song.path)   # decode MP3 into memory for visualizer

    def _load_pcm(self, path: str):
        """Decode MP3 → mono float32 PCM for get_audio()."""
        seg = AudioSegment.from_file(path)
        seg = seg.set_channels(1).set_frame_rate(self.RATE)
        samples = np.array(seg.get_array_of_samples(), dtype=np.float32)
        samples /= 32768.0
        self._pcm = samples
        self._pcm_rate = self.RATE

    # =====================================================
    # PAUSE / RESUME
    # =====================================================
    def pause(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True

    def resume(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False

    # =====================================================
    # STOP
    # =====================================================
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self._seek_offset_ms = 0

    # =====================================================
    # SEEK
    # =====================================================
    def seek(self, seconds: float):
        if not self.current_song_path:
            return
        pygame.mixer.music.load(self.current_song_path)
        pygame.mixer.music.play(start=seconds)
        self._seek_offset_ms = int(seconds * 1000)

    # =====================================================
    # POSITION
    # =====================================================
    def get_position_ms(self) -> int:
        pos = pygame.mixer.music.get_pos()
        if pos < 0:
            return self._seek_offset_ms
        return self._seek_offset_ms + pos

    # =====================================================
    # LENGTH
    # =====================================================
    def get_song_length(self, song) -> float:
        return MP3(song.path).info.length

    # =====================================================
    # VOLUME
    # =====================================================
    def set_volume(self, volume: float):
        pygame.mixer.music.set_volume(volume)

    # =====================================================
    # CLEANUP
    # =====================================================
    def quit(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
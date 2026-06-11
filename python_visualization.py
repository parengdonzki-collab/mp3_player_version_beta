import numpy as np
import socket
import threading
import time
from pydub import AudioSegment
from scipy.ndimage import uniform_filter1d


class AudioVisualizer:

    def __init__(self, port=6000):

        self.BANDS = 20
        self.CHUNK = 2048

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", port))

        print("Connected to Java visualizer")

        self.audio = None
        self.running = False

    # =========================
    # LOAD AUDIO
    # =========================
    def load_song(self, path):

        audio = AudioSegment.from_file(path)
        audio = audio.set_channels(1)

        samples = np.array(audio.get_array_of_samples()).astype(np.float32)

        # normalize
        samples /= np.max(np.abs(samples) + 1e-9)

        self.audio = samples
        self.sample_rate = audio.frame_rate

        print("Loaded:", path)

    # =========================
    # START
    # =========================
    def start(self):

        if self.audio is None:
            return

        self.running = True
        threading.Thread(target=self._run, daemon=True).start()

    # =========================
    # FFT PROCESS
    # =========================
    def _compute_bands(self, chunk):

        fft = np.abs(np.fft.rfft(chunk))

        # log scaling (important for music feel)
        fft = np.log1p(fft)

        step = len(fft) // self.BANDS
        bands = []

        for i in range(self.BANDS):
            start = i * step
            end = start + step
            val = np.mean(fft[start:end]) if end < len(fft) else 0
            bands.append(val)

        # normalize
        bands = np.array(bands)
        bands = bands / (np.max(bands) + 1e-9)

        # smoothing (VERY IMPORTANT)
        bands = uniform_filter1d(bands, size=3)

        return bands

    # =========================
    # SEND TO JAVA
    # =========================
    def _send(self, bands):

        msg = ",".join(f"{b:.3f}" for b in bands) + "\n"
        self.sock.sendall(msg.encode())

    # =========================
    # MAIN LOOP
    # =========================
    def _run(self):

        print("Visualizer running...")

        pos = 0

        while self.running and pos + self.CHUNK < len(self.audio):

            chunk = self.audio[pos:pos + self.CHUNK]

            bands = self._compute_bands(chunk)
            self._send(bands)

            pos += self.CHUNK

            time.sleep(0.03)  # smooth 30 FPS
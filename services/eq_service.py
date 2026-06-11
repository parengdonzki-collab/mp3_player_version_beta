import numpy as np
from scipy.signal import butter, sosfilt

class EQService:
    def __init__(self, rate=44100):
        self.rate = rate
        self.bass = 1.0      # 0.0 - 2.0
        self.mid = 1.0
        self.treble = 1.0

    def set_bass(self, value): self.bass = value
    def set_mid(self, value): self.mid = value
    def set_treble(self, value): self.treble = value

    def _bandpass(self, data, low, high):
        sos = butter(4, [low, high], btype='band', fs=self.rate, output='sos')
        return sosfilt(sos, data)

    def _lowpass(self, data, cutoff):
        sos = butter(4, cutoff, btype='low', fs=self.rate, output='sos')
        return sosfilt(sos, data)

    def _highpass(self, data, cutoff):
        sos = butter(4, cutoff, btype='high', fs=self.rate, output='sos')
        return sosfilt(sos, data)

    def process(self, audio: np.ndarray) -> np.ndarray:
        bass_band   = self._lowpass(audio, 300)       * self.bass
        mid_band    = self._bandpass(audio, 300, 4000) * self.mid
        treble_band = self._highpass(audio, 4000)      * self.treble
        mixed = bass_band + mid_band + treble_band
        # prevent clipping
        peak = np.max(np.abs(mixed))
        if peak > 1.0:
            mixed /= peak
        return mixed
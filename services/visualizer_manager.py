import numpy as np

class SpectrumProcessor:
    def __init__(self, bands=40):
        self.bands = bands

    def process(self, audio):
        audio = np.nan_to_num(audio)

        fft = np.abs(np.fft.rfft(audio))
        fft = fft[:len(fft)//2]

        if len(fft) < self.bands:
            return np.zeros(self.bands)

        size = max(1, len(fft) // self.bands)

        bands = [
            np.mean(fft[i * size:(i + 1) * size])
            for i in range(self.bands)
        ]

        bands = np.array(bands)

        max_val = np.max(bands)
        if max_val > 0:
            bands /= max_val

        return bands
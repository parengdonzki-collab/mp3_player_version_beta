import numpy as np

class SpectrumProcessor:
    def __init__(self, bands=40, smoothing=0.7):
        self.bands = bands
        self.smoothing = smoothing
        self._prev = np.zeros(bands)  # for smoothing

    def process(self, audio):
       
           
      import numpy as np

class SpectrumProcessor:
    def __init__(self, bands=40, smoothing=0.7):
        self.bands = bands
        self.smoothing = smoothing
        self._prev = np.zeros(bands)

    def process(self, audio):
        audio = np.nan_to_num(audio)
        audio = audio - np.mean(audio)  # remove DC bias

        fft = np.abs(np.fft.rfft(audio))
        fft = fft[1:]  # skip bin 0

        if len(fft) < self.bands:
            return np.zeros(self.bands)

        size = max(1, len(fft) // self.bands)
        bands = np.array([
            np.mean(fft[i * size:(i + 1) * size])
            for i in range(self.bands)
        ])

        # log scale
        bands = np.log1p(bands)

        # ← frequency weighting: ramp up higher bands
        weights = np.linspace(0.1, 3.0, self.bands)
        bands = bands * weights

        max_val = np.max(bands)
        if max_val > 0:
            bands /= max_val

        self._prev = self.smoothing * self._prev + (1 - self.smoothing) * bands
        return self._prev
import numpy as np
import tkinter as tk

class AudioVisualizer:
    def __init__(self, audio_service, processor, canvas: tk.Canvas, width=900, height=200):
        self.audio_service = audio_service
        self.processor = processor
        self.canvas = canvas
        self.width = width
        self.height = height

    def start(self):
        self._update()

    def _bar_color(self, value: float) -> str:
        r = min(255, int(255 * value))
        g = min(255, int(255 * (1 - value * 0.6)))
        return f"#{r:02x}{g:02x}50"

    def _update(self):
        audio = self.audio_service.get_audio()
        spectrum = self.processor.process(audio)

        self.canvas.delete("bar")

        n = len(spectrum)
        bw = self.width / n

        for i, value in enumerate(spectrum):
            bh = max(2, int(value * self.height * 0.95))
            x0 = i * bw
            x1 = x0 + bw - 2
            y0 = self.height - bh
            y1 = self.height
            color = self._bar_color(value)
            self.canvas.create_rectangle(x0, y0, x1, y1,
                                         fill=color, outline="",
                                         tags="bar")

        self.canvas.after(16, self._update)
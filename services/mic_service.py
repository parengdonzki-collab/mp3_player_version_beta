# services/mic_service.py

import sounddevice as sd

class MicService:

    def __init__(self):
        self.stream = None
        self.enabled = False

    def start_monitoring(self):

        if self.enabled:
            return

        self.stream = sd.Stream(
            samplerate=44100,
            channels=1,
            dtype='float32'
        )

        self.stream.start()
        self.enabled = True

    def stop_monitoring(self):

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        self.enabled = False
import subprocess
import os
import time


class VisualizerManager:

    def __init__(self, audio_visualizer):
        self.audio_visualizer = audio_visualizer
        self.process = None

    def launch(self):

        if self.process is not None:
            print("Visualizer already running")
            return

        jar_path = os.path.join(
            os.getcwd(),
            "EqualizerServer.jar"
        )

        self.process = subprocess.Popen([
            "java",
            "--module-path",
            r"C:\javafx-sdk-25\lib",
            "--add-modules",
            "javafx.controls,javafx.graphics",
            "-jar",
            jar_path
        ])

        print("Java visualizer launched")

        # Give Java time to open its socket
        time.sleep(2)

        self.audio_visualizer.start()
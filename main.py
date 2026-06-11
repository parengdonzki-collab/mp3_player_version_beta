from views.main_view import MainView
from controllers.player_controller import PlayerController

from services.audio_service import AudioService
from services.visualizer import AudioVisualizer
from services.spectrum_processor import SpectrumProcessor
import tkinter as tk

def main():
    
    view = MainView()
    audio_service = AudioService()
    processor = SpectrumProcessor(bands=10)

    # Add as row 2 in main_frame's grid
    viz_canvas = tk.Canvas(view.viz_placeholder, width=200, height=200, bg="#0a0a0a", highlightthickness=0)
    viz_canvas.pack(fill="both", expand=True)

    visualizer = AudioVisualizer(
        audio_service=audio_service,
        processor=processor,
        canvas=viz_canvas,
        width=200,
        height=200
    )

    controller = PlayerController(view, audio_service, visualizer)
    visualizer.start()
    view.run()
if __name__ == "__main__":
    main()
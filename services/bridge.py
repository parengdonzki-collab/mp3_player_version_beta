import numpy as np
import librosa
import threading
import time

def connect_audio_to_visualizer(audio_service, visualizer, path):
    # Force standard 44100Hz tracking constraints
    
    print("Loading audio...")
    start_time = time.time()

    audio, sr = librosa.load(path, sr=44100, mono=True)
    print(f"Loaded in {time.time() - start_time:.2f} sec")
    
    chunk_size = visualizer.CHUNK

    def loop():
        print("🔗 Librosa audio tracking bridge online.")
        while visualizer.running:
            pos_ms = audio_service.get_position_ms()

            # Wait if the player service hasn't started or is loading
            if pos_ms < 0:
                time.sleep(0.01)
                continue

            # Calculate index position over time
            start = int((pos_ms / 1000.0) * sr)
            end = start + chunk_size

            # If track finishes or bounds exceed, break or wrap safely
            if start >= len(audio):
                time.sleep(0.1)
                continue

            samples = audio[start:end]

            # Zero-pad remaining frames if the chunk cuts off near the track's end
            if len(samples) < chunk_size:
                samples = np.pad(
                    samples,
                    (0, chunk_size - len(samples)),
                    mode='constant'
                )

            # Ensure data types match expected 32-bit floating-point arrays
            float_samples = samples.astype(np.float32)

            # Assign directly to left and right stereo channels
            visualizer.audio_buffer_l = float_samples
            visualizer.audio_buffer_r = float_samples

            # Sleep ~22ms to maintain synchronization with a 45 FPS send rate
            time.sleep(0.022)

    threading.Thread(target=loop, daemon=True).start()

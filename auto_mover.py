import os
import shutil

DOWNLOADS = r"C:\Users\NEC\Downloads"

BASE_DIR = r"C:\Users\NEC\Music\KaraokeApp"

SONGS = os.path.join(BASE_DIR, "Songs")
KARAOKE = os.path.join(BASE_DIR, "Karaoke")
LYRICS = os.path.join(BASE_DIR, "Lyrics")

# create folders automatically
os.makedirs(SONGS, exist_ok=True)
os.makedirs(KARAOKE, exist_ok=True)
os.makedirs(LYRICS, exist_ok=True)

for file in os.listdir(DOWNLOADS):

    source = os.path.join(DOWNLOADS, file)

    filename = file.lower()

    # ==========================================
    # MP3 FILES
    # ==========================================
    if filename.endswith(".mp3"):

        if (
            "karaoke" in filename
            or "instrumental" in filename
            or "minus one" in filename
        ):
            destination = os.path.join(KARAOKE, file)

        else:
            destination = os.path.join(SONGS, file)

        shutil.move(source, destination)
        print(f"Moved MP3: {file}")

    # ==========================================
    # LRC FILES
    # ==========================================
    elif filename.endswith(".lrc"):

        destination = os.path.join(LYRICS, file)

        shutil.move(source, destination)
        print(f"Moved LRC: {file}")
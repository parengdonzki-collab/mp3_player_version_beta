import os
import re
import vlc
import customtkinter as ctk

from tkinter import filedialog

from metadata_utils import get_song_metadata


# =====================================================
# VLC DLL FIX (WINDOWS)
# =====================================================

os.add_dll_directory(
    r"C:\Program Files\VideoLAN\VLC"
)


# =====================================================
# LRC PARSER
# =====================================================

def parse_lrc(raw_lyrics):

    parsed = []

    offset = 0

    pattern = r"\[(\d+):(\d+(?:\.\d+)?)\](.*)"

    for line in raw_lyrics.splitlines():

        # -----------------------------------------
        # OFFSET
        # -----------------------------------------

        if line.startswith("[offset:"):

            try:

                offset = int(
                    line.split(":")[1]
                    .replace("]", "")
                )

            except:

                offset = 0

            continue

        # -----------------------------------------
        # TIMESTAMP
        # -----------------------------------------

        matches = re.findall(pattern, line)

        for match in matches:

            minutes = int(match[0])

            seconds = float(match[1])

            lyric = match[2].strip()

            timestamp = (
                minutes * 60
                + seconds
                + (offset / 1000)
            )

            parsed.append(
                (timestamp, lyric)
            )

    parsed.sort(
        key=lambda x: x[0]
    )

    return parsed


# =====================================================
# LOAD LYRICS
# =====================================================

def load_lyrics(song_path):

    base = os.path.splitext(song_path)[0]

    lrc_path = base + ".lrc"

    txt_path = base + ".txt"

    # -----------------------------------------
    # LRC
    # -----------------------------------------

    if os.path.exists(lrc_path):

        with open(
            lrc_path,
            "r",
            encoding="utf-8"
        ) as f:

            return parse_lrc(f.read())

    # -----------------------------------------
    # TXT FALLBACK
    # -----------------------------------------

    if os.path.exists(txt_path):

        with open(
            txt_path,
            "r",
            encoding="utf-8"
        ) as f:

            lines = f.read().splitlines()

        fake = []

        for i, line in enumerate(lines):

            if line.strip():

                fake.append(
                    (
                        i * 3.0,
                        line
                    )
                )

        return fake

    return []


# =====================================================
# KARAOKE APP
# =====================================================

class KaraokeApp:

    def __init__(self):

        # =================================================
        # WINDOW
        # =================================================
        
        self.root = ctk.CTk()
        
        self.root.geometry("1200x700")

        self.root.title("LibreKanta Karaoke")

        self.root.configure(
            fg_color="black"
        )

        # =================================================
        # CURRENT LYRIC
        # =================================================

        self.lyric_label = ctk.CTkLabel(
            self.root,
            text="Open a song...",
            font=("Segoe UI", 42, "bold"),
            wraplength=1000,
            text_color="white",
            justify="center"
        )

        self.lyric_label.pack(
            expand=True
        )

        # =================================================
        # NEXT LYRIC
        # =================================================

        self.next_label = ctk.CTkLabel(
            self.root,
            text="",
            font=("Segoe UI", 26),
            wraplength=1000,
            text_color="gray"
        )

        self.next_label.pack(
            pady=(0, 40)
        )

        # =================================================
        # BUTTON FRAME
        # =================================================

        self.button_frame = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )

        self.button_frame.pack(
            pady=20
        )

        # =================================================
        # OPEN BUTTON
        # =================================================

        self.open_button = ctk.CTkButton(
            self.button_frame,
            text="Open MP3",
            command=self.open_song
        )

        self.open_button.pack(
            side="left",
            padx=10
        )

        # =================================================
        # PAUSE BUTTON
        # =================================================

        self.pause_button = ctk.CTkButton(
            self.button_frame,
            text="Pause",
            command=self.toggle_pause
        )

        self.pause_button.pack(
            side="left",
            padx=10
        )

        # =================================================
        # STOP BUTTON
        # =================================================

        self.stop_button = ctk.CTkButton(
            self.button_frame,
            text="Stop",
            command=self.stop_song
        )

        self.stop_button.pack(
            side="left",
            padx=10
        )

        # =================================================
        # VLC PLAYER
        # =================================================

        self.instance = vlc.Instance()

        self.player = self.instance.media_player_new()

        # =================================================
        # DATA
        # =================================================

        self.lyrics = []

        self.current_index = 0

        self.is_paused = False

        self.after_id = None
        self.root.protocol(
                            "WM_DELETE_WINDOW",
                             self.on_close
                            )
    #==============================================
    # OPEN SONG
    # =================================================

    def open_song(self):
       
        song_path = filedialog.askopenfilename(
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.flac")
            ]
        )

        if not song_path:
            return
        
        # -----------------------------------------
        # METADATA
        # -----------------------------------------

        meta = get_song_metadata(song_path)

        artist = meta["artist"]

        title = meta["title"]

        self.root.title(
            f"{artist} - {title}"
        )

        # -----------------------------------------
        # CANCEL OLD LOOP
        # -----------------------------------------

        if self.after_id:

            self.root.after_cancel(
                self.after_id
            )

        # -----------------------------------------
        # RESET UI
        # -----------------------------------------

        self.lyric_label.configure(
            text="Loading..."
        )

        self.next_label.configure(
            text=""
        )

        # -----------------------------------------
        # STOP PREVIOUS SONG
        # -----------------------------------------

        self.player.stop()

        # -----------------------------------------
        # LOAD MEDIA
        # -----------------------------------------

        media = self.instance.media_new(
            song_path
        )

        self.player.set_media(media)

        self.player.play()
        
        self.root.after(500, self.start_visualizer)

        # give VLC time to initialize
        self.root.after(
            300,
            self.update_lyrics
        )

        # -----------------------------------------
        # LOAD LYRICS
        # -----------------------------------------

        self.lyrics = load_lyrics(song_path)

        success = False

        # -----------------------------------------
        # DOWNLOAD IF MISSING
        # -----------------------------------------

        if not self.lyrics:

            try:

                from lyrics_downloader import (
                    download_lrc
                )

                self.lyric_label.configure(
                    text="Downloading lyrics..."
                )

                self.root.update()
                                
                import threading

                threading.Thread(
                    target=lambda: download_lrc(song_path),
                    daemon=True
                ).start()
                
            except Exception as e:

                print("Lyrics download failed:")
                print(e)

        # -----------------------------------------
        # RELOAD AFTER DOWNLOAD
        # -----------------------------------------

        if success:

            self.lyrics = load_lyrics(
                song_path
            )

        self.current_index = 0
                # -----------------------------------------
                # NO LYRICS
                # ----------------------------------------
        if not self.lyrics:

            self.lyric_label.configure(
            text="No lyrics found."
                    )

            return

    
    # =================================================
    # PAUSE / RESUME
    # =================================================

    def toggle_pause(self):

        self.player.pause()

        self.is_paused = not self.is_paused

        if self.is_paused:

            self.pause_button.configure(
                text="Resume"
            )

        else:

            self.pause_button.configure(
                text="Pause"
            )

    # =================================================
    # STOP SONG
    # =================================================

    def stop_song(self):

        self.visualizer.stop()
        self.player.stop()

        if self.after_id:
            self.root.after_cancel(self.after_id)

        self.lyric_label.configure(text="Stopped")
        self.next_label.configure(text="")
        self.current_index = 0

    # =================================================
    # UPDATE LYRICS
    # =================================================

    def update_lyrics(self):

        # -----------------------------------------
        # NO LYRICS
        # -----------------------------------------

        if not self.lyrics:
            return

        # -----------------------------------------
        # PLAYER STATE
        # -----------------------------------------

        state = self.player.get_state()

        if state in (
            vlc.State.Ended,
            vlc.State.Stopped,
            vlc.State.Error
        ):
            return

        # -----------------------------------------
        # CURRENT TIME
        # -----------------------------------------

        current_ms = self.player.get_time()

        # VLC not ready yet
        if current_ms < 0:

            self.after_id = self.root.after(
                    100,
                    self.update_lyrics
                )

            return

        current_time = current_ms / 1000

        # -----------------------------------------
        # ADVANCE LYRIC
        # -----------------------------------------

        while self.current_index < len(self.lyrics) - 1:

            next_time = self.lyrics[
                self.current_index + 1
            ][0]

            if current_time >= next_time:

                self.current_index += 1

            else:
                break

        # -----------------------------------------
        # CURRENT LINE
        # -----------------------------------------

        current_line = self.lyrics[
            self.current_index
        ][1]

        self.lyric_label.configure(
            text=current_line,
            text_color="#FFD700"
        )

        # -----------------------------------------
        # NEXT LINE
        # -----------------------------------------

        if self.current_index < len(self.lyrics) - 1:

            next_line = self.lyrics[
                self.current_index + 1
            ][1]

            self.next_label.configure(
                text=next_line
            )

        else:

            self.next_label.configure(
                text=""
            )

        # -----------------------------------------
        # LOOP
        # -----------------------------------------

        self.after_id = self.root.after(
            50,
            self.update_lyrics
        )
    
    # =================================================
    # RUN
    # =================================================

    def run(self):

        self.root.mainloop()
    def on_close(self):

        try:
            if self.after_id:
                self.root.after_cancel(self.after_id)

            self.visualizer.stop()

            self.player.stop()
            self.player.release()

        except Exception as e:
            print(e)

        self.root.destroy()   
    def start_visualizer(self):

        try:
            # always recreate clean instance
            self.visualizer = AudioVisualizer()

            self.visualizer.start()

        except Exception as e:
            print("Visualizer start failed:", e)
# =====================================================
# START
# =====================================================

if __name__ == "__main__":

    ctk.set_appearance_mode("dark")

    ctk.set_default_color_theme("blue")

    app = KaraokeApp()

    app.run()
    
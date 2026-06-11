import customtkinter as ctk
import io
import tkinter as tk
from tkinter import ttk
from PIL import Image
from views.eq_panel import EQPanel

from CTkMenuBar import CTkMenuBar
from CTkMenuBar.dropdown_menu import CustomDropdownMenu
from tkinterdnd2 import TkinterDnD

# =========================================================
# THEME
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainView:

    PAD_X = 15
    PAD_Y = 15

    def __init__(self):

        self.root = TkinterDnD.Tk()

        self.root.geometry("1100x650")
        self.root.title("LibreKanta Free Player/Basic Karaoke")

        # self.root.iconbitmap("asset\\mp3.ico")

        # =====================================================
        # MENU
        # =====================================================

        self.create_menu()

        # =====================================================
        # MAIN CONTAINER
        # =====================================================

        self.create_main_container()

        # =====================================================
        # UI SECTIONS
        # =====================================================

        self.create_left_panel()
        self.create_right_panel()
        self.create_bottom_panel()

    # =========================================================
    # MAIN CONTAINER
    # =========================================================

    def create_main_container(self):

        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=2)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)

    # =========================================================
    # MENU BAR
    # =========================================================

    def create_menu(self):

        self.menu = CTkMenuBar(master=self.root)

        # FILE MENU
        self.file_button = self.menu.add_cascade("File")

        self.file_dropdown = CustomDropdownMenu(
            widget=self.file_button
        )

        self.open_mp3_option = self.file_dropdown.add_option(
            option="Open MP3",
            command=self.close_menu_focus_bug
        )

        self.save_playlist_option = self.file_dropdown.add_option(
            option="Save Playlist",
            command=self.close_menu_focus_bug
        )

        self.load_playlist_option = self.file_dropdown.add_option(
            option="Load Playlist",
            command=self.close_menu_focus_bug
        )

        self.file_dropdown.add_separator()

        self.exit_option = self.file_dropdown.add_option(
            option="Exit",
            command=self.close_menu_focus_bug
        )
        # TOOLS MENU
        self.tools_button = self.menu.add_cascade("Tools")

        self.tools_dropdown = CustomDropdownMenu(
            widget=self.tools_button
        )

        self.open_lyrics_option = self.tools_dropdown.add_option(
            option="Open Lyrics",
            command=self.close_menu_focus_bug
        )
        
        self.edit_metadata_option = self.tools_dropdown.add_option(
        option="Edit Metadata",
        command=self.close_menu_focus_bug
    )

        self.generate_lyrics_option = self.tools_dropdown.add_option(
            option="Generate Lyrics",
            command=self.close_menu_focus_bug
        )

        self.karaoke_option = self.tools_dropdown.add_option(
            option="Karaoke Mode",
            command=self.close_menu_focus_bug
        )
        self.launch_visual_option = self.tools_dropdown.add_option(
            option="Launch Radio",
            command=self.close_menu_focus_bug
        )
        
    # =========================================================
    # LEFT PANEL
    # =========================================================

    def create_left_panel(self):

        self.left_panel = ctk.CTkFrame(
            self.main_frame,
            corner_radius=20
        )

        self.left_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=self.PAD_X,
            pady=self.PAD_Y
        )
          # NOW PLAYING
        self.song_title_label = ctk.CTkLabel(
        self.left_panel,
        text="No Song",
        font=("Segoe UI", 20, "bold"),
        width=260,
        wraplength=260
        )
        self.song_title_label.pack(
                                    pady=(10, 0)
                                    )

        self.artist_label = ctk.CTkLabel(
            self.left_panel,
            text="Unknown Artist",
            font=("Segoe UI", 13)
        )
        self.artist_label.pack(
                                    pady=(0, 10)
                                    )
        
        
        # =====================================================
        # ALBUM ART
        # =====================================================

        self.album_art = ctk.CTkLabel(
            self.left_panel,
            text="No Album Art",
            width=340,
            height=340,
            corner_radius=20
        )

        self.album_art.pack(
            pady=30
        )
        self.album_art.pack_propagate(False)
        
      
    # =========================================================
    # RIGHT PANEL
    # =========================================================

    def create_right_panel(self):

        self.right_panel = ctk.CTkFrame(
            self.main_frame,
            corner_radius=20
        )

        self.right_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=self.PAD_X,
            pady=self.PAD_Y
        )
            # CONFIGURE RIGHT PANEL GRID
        self.right_panel.grid_rowconfigure(2, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

    # =====================================================
    # PLAYLIST TITLE
    # =====================================================

        self.playlist_title = ctk.CTkLabel(
            self.right_panel,
            text="Playlist (0 songs)",
            font=("Segoe UI", 28, "bold")
        )

        self.playlist_title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(15, 10)
        )

        # =====================================================
        # SEARCH FRAME
        # =====================================================

        search_frame = ctk.CTkFrame(
            self.right_panel,
            fg_color="transparent"
        )

        search_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=(5, 0)
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search songs...",
            height=40,
            corner_radius=12
        )

        self.search_entry.pack(
            fill="x",
            side="left",
            expand=True,
            padx=(0, 5)
        )

        self.search_button = ctk.CTkButton(
            search_frame,
            text="🔍",
            width=42,
            height=40,
            corner_radius=12
        )

        self.search_button.pack(
            side="right"
        )
        ToolTip(self.search_button, "Search songs")
        # =====================================================
        # PLAYLIST CONTAINER
        # =====================================================

        playlist_container = ctk.CTkFrame(
            self.right_panel
        )

        playlist_container.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        # =====================================================
        # SCROLLBAR
        # =====================================================

        scrollbar = ttk.Scrollbar(
            playlist_container,
            orient="vertical"
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # =====================================================
        # TREEVIEW
        # =====================================================

        style = ttk.Style()

        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#252525",
            foreground="#f0f0f0",
            fieldbackground="#252525",
            rowheight=36,
            borderwidth=0,
            font=("Segoe UI", 11)
        )

        style.configure(
            "Treeview.Heading",
            background="#2f2f2f",
            foreground="#ffffff",
            font=("Segoe UI", 11, "bold")

        )

        style.map(
            "Treeview",
            background=[
                ("selected", "#2563EB")
            ],
            foreground=[
                ("selected", "#FFFFFF")
            ]
        )

        style.map(
            "Treeview.Heading",
            background=[("active", "#3a3a3a")],
            foreground=[("active", "#ffffff")]
        )
        self.playlist_box = ttk.Treeview(
            playlist_container,
            columns=(
                "Title",
                "Artist",
                "Duration"
            ),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        

        self.playlist_box.pack(
            side="left",
            fill="both",
            expand=True
        )
        scrollbar.config(
                            command=self.playlist_box.yview
                        )
        self.playlist_box.heading("Title", text="Title")
        self.playlist_box.heading("Artist", text="Artist")
        self.playlist_box.heading("Duration", text="Duration")

        self.playlist_box.column("Title", width=450)
        self.playlist_box.column("Artist", width=220)
        self.playlist_box.column("Duration", width=100, anchor="center")



        # =====================================================
        # ACTION BUTTONS
        # =====================================================

        actions_frame = ctk.CTkFrame(
            self.right_panel
        )

        actions_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0, 10)
        )

        self.remove_song_button = ctk.CTkButton(
            actions_frame,
            text="🗑 Remove",
            width=100
        )

        self.remove_song_button.pack(
            side="left",
            padx=5
        )
        
        ToolTip(self.remove_song_button, "Remove selected song")

        self.clear_playlist_button = ctk.CTkButton(
            actions_frame,
            text="🧹 Clear",
            width=100
        )

        self.clear_playlist_button.pack(
            side="left",
            padx=5
        )
        ToolTip(self.clear_playlist_button, "Clear playlist")

        self.shuffle_button = ctk.CTkButton(
            actions_frame,
            text="🔀",
            width=60
        )

        self.shuffle_button.pack(
            side="left",
            padx=5
        )
        ToolTip(self.shuffle_button, "Shuffle playlist")

        self.repeat_button = ctk.CTkButton(
            actions_frame,
            text="🔁",
            width=60
        )

        self.repeat_button.pack(
            side="left",
            padx=5
        )
        ToolTip(self.repeat_button, "Repeat playlist")
    # =========================================================
    # BOTTOM PANEL
    # =========================================================

    def create_bottom_panel(self):

        self.bottom_panel = ctk.CTkFrame(
            self.main_frame,
            corner_radius=20
        )

        self.bottom_panel.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=self.PAD_X,
            pady=self.PAD_Y
        )

        # =====================================================
        # LEFT — visualizer placeholder
        # =====================================================

        self.viz_placeholder = ctk.CTkFrame(
            self.bottom_panel,
            fg_color="#0a0a0a",
            width=200,
            height=200,
            corner_radius=12
        )
        self.viz_placeholder.pack(side="left", padx=15, pady=10)
        self.viz_placeholder.pack_propagate(False)

        # =====================================================
        # RIGHT — all controls
        # =====================================================
  
        right_controls = ctk.CTkFrame(
            self.bottom_panel,
            fg_color="transparent"
        )
        right_controls.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=10)
       
        # PROGRESS
        progress_frame = ctk.CTkFrame(right_controls, fg_color="transparent")
        progress_frame.pack(padx=15, pady=(10, 5))

        self.progress_slider = ctk.CTkSlider(progress_frame, from_=0, to=100,width=400)
        self.progress_slider.pack( padx=10)
        self.progress_slider.set(0)

        self.time_label = ctk.CTkLabel(progress_frame, text="00:00 / 00:00")
        self.time_label.pack(pady=5)

        # STATUS
        self.status_label = ctk.CTkLabel(right_controls, text="Ready", font=("Segoe UI", 11))
        self.status_label.pack(pady=(0, 5))

        # CONTROLS
        controls_frame = ctk.CTkFrame(right_controls, fg_color="transparent")
        controls_frame.pack(pady=10)

        self.prev_button = ctk.CTkButton(controls_frame, text="⏮", width=60)
        self.prev_button.pack(side="left", padx=5)
        ToolTip(self.prev_button, "Previous track")

        self.play_button = ctk.CTkButton(controls_frame, text="▶", width=80, height=50, corner_radius=12)
        self.play_button.pack(side="left", padx=5)
        ToolTip(self.play_button, "Play selected song")

        self.pause_button = ctk.CTkButton(controls_frame, text="⏸", width=60)
        self.pause_button.pack(side="left", padx=5)
        ToolTip(self.pause_button, "Pause")

        self.stop_button = ctk.CTkButton(controls_frame, text="⏹", width=60)
        self.stop_button.pack(side="left", padx=5)
        ToolTip(self.stop_button, "Stop")

        self.next_button = ctk.CTkButton(controls_frame, text="⏭", width=60)
        self.next_button.pack(side="left", padx=5)
        ToolTip(self.next_button, "Next track")

        self.mic_button = ctk.CTkButton(controls_frame, text="🎤 Mic", width=90)
        self.mic_button.pack(side="left", padx=5)
        ToolTip(self.mic_button, "Enable microphone")

        # AUDIO INFO
        self.audio_info_label = ctk.CTkLabel(right_controls, text="MP3 • 320kbps • 44.1kHz", font=("Segoe UI", 11))
        self.audio_info_label.pack(pady=(0, 5))

        # VOLUME
        volume_frame = ctk.CTkFrame(right_controls, fg_color="transparent")
        volume_frame.pack(pady=(0, 10))

        volume_label = ctk.CTkLabel(volume_frame, text="🔊 Volume")
        volume_label.pack(side="left", padx=10)

        self.volume_slider = ctk.CTkSlider(volume_frame, from_=0, to=100, width=200)
        self.volume_slider.set(50)
        self.volume_slider.pack(side="left")
        bottom_left = ctk.CTkFrame(
            self.bottom_panel,
            fg_color="transparent"
        )
        bottom_left.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=10)
        
        self.eq_panel = EQPanel(bottom_left)
        self.eq_panel.pack(side="right",pady=(0, 10))
    
    
    def add_song_to_playlist(
                                self,
                                title,
                                artist,
                                duration
                            ):

        self.playlist_box.insert(
            "",
            "end",
            values=(
                title,
                artist,
                duration
            )
        )
        self.update_song_count()
    def close_menu_focus_bug(self):

        self.root.focus_force()

        self.root.after(
            10,
            lambda: self.root.focus_set()
        )
    def get_selected_index(self):

        selected = self.playlist_box.selection()

        if not selected:
            return None

        item = selected[0]

        return self.playlist_box.index(item)
    


    def run(self):

        self.root.mainloop()

    def set_close_callback(self, callback):

        self.root.protocol(
            "WM_DELETE_WINDOW",
            callback
        )
    def update_album_art(self, image_data):

        if image_data:

            image = Image.open(
                io.BytesIO(image_data)
            )

            image.thumbnail((340, 340))

            cover = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(340, 340)
            )

            self.album_art.configure(
                image=cover,
                text=""
            )

            self.album_art.image = cover

        else:

            self.album_art.configure(
                image=None,
                text="🎵\nNo Album Art",
                font=("Segoe UI", 18)
            )
            
    def get_song_count(self):
        return len(self.playlist_box.get_children())
    
    def update_song_count(self):
        count = self.get_song_count()
        self.playlist_title.configure(
            text=f"Playlist ({count} songs)"
        )
    def update_audio_info(self, text):

        self.audio_info_label.configure(
            text=text
    )
    def after(self, delay, callback):

        return self.root.after(
            delay,
            callback
        )

    def set_song_count(self, count=None):
        self.update_song_count()
    def after_cancel(self, after_id):
        self.root.after_cancel(
            after_id
        )
    def clear_playlist_view(self):
        self.playlist_box.delete(*self.playlist_box.get_children())
        self.set_song_count()

    def remove_item(self, path):
        if self.playlist_box.exists(path):
            self.playlist_box.delete(path)
    def render_playlist(self, songs):

        self.playlist_box.delete(*self.playlist_box.get_children())

        for song in songs:
            self.playlist_box.insert(
                "",
                "end",
                values=(song.title, song.artist, song.duration)
            )

        self.update_song_count()
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None

        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tooltip:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tooltip,
            text=self.text,
            bg="#2B2B2B",
            fg="white",
            relief="solid",
            borderwidth=1,
            padx=8,
            pady=4
        )
        label.pack()

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

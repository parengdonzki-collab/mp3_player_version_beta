import customtkinter as ctk
import io
import tkinter as tk
from tkinter import ttk
from PIL import Image

from CTkMenuBar import CTkMenuBar
from CTkMenuBar.dropdown_menu import CustomDropdownMenu


# =========================================================
# THEME
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainView:

    PAD_X = 10
    PAD_Y = 10

    def __init__(self):

        self.root = ctk.CTk()

        self.root.geometry("1100x650")
        self.root.title("MP3 Player")

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
            command=lambda: None
        )

        self.save_playlist_option = self.file_dropdown.add_option(
            option="Save Playlist",
            command=lambda: None
        )

        self.load_playlist_option = self.file_dropdown.add_option(
            option="Load Playlist",
            command=lambda: None
        )

        self.file_dropdown.add_separator()

        self.exit_option = self.file_dropdown.add_option(
            option="Exit",
            command=lambda: None
        )

    # =========================================================
    # LEFT PANEL
    # =========================================================

    def create_left_panel(self):

        self.left_panel = ctk.CTkFrame(
            self.main_frame,
            corner_radius=10
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
        font=("Segoe UI", 14, "bold"),
        width=260,
        wraplength=260
        )
        self.song_title_label.pack(
                                    pady=(10, 0)
                                    )

        self.artist_label = ctk.CTkLabel(
            self.left_panel,
            text="Unknown Artist",
            font=("Segoe UI", 14)
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
            width=280,
            height=280,
            corner_radius=15
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
            corner_radius=10
        )

        self.right_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=self.PAD_X,
            pady=self.PAD_Y
        )

        # PLAYLIST TITLE
        self.playlist_title = ctk.CTkLabel(
            self.right_panel,
            text="Playlist",
            font=("Segoe UI", 22, "bold")
        )

        self.playlist_title.pack(
            pady=(10, 5)
        )

        
       

        # =====================================================
        # PLAYLIST CONTAINER
        # =====================================================

        playlist_container = ctk.CTkFrame(
            self.right_panel
        )

        playlist_container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =====================================================
        # TREEVIEW STYLE
        # =====================================================

        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#1e1e1e",
            foreground="white",
            fieldbackground="#1e1e1e",
            rowheight=28,
            borderwidth=0,
            font=("Segoe UI", 11)
        )

        style.configure(
            "Treeview.Heading",
            background="#2b2b2b",
            foreground="white",
            font=("Segoe UI", 11, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#3a7ebf")]
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

        # =====================================================
        # HEADINGS
        # =====================================================

        self.playlist_box.heading(
            "Title",
            text="Title"
        )

        self.playlist_box.heading(
            "Artist",
            text="Artist"
        )

        self.playlist_box.heading(
            "Duration",
            text="Time"
        )

        # =====================================================
        # COLUMNS
        # =====================================================

        self.playlist_box.column(
            "Title",
            width=350
        )

        self.playlist_box.column(
            "Artist",
            width=180
        )

        self.playlist_box.column(
            "Duration",
            width=80,
            anchor="center"
        )
        # ACTION BUTTONS
        actions_frame = ctk.CTkFrame(
            self.right_panel
        )

        actions_frame.pack(
            pady=10
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

        self.clear_playlist_button = ctk.CTkButton(
            actions_frame,
            text="🧹 Clear",
            width=100
        )

        self.clear_playlist_button.pack(
            side="left",
            padx=5
        )
        
        self.shuffle_button = ctk.CTkButton(
            actions_frame,
            text="🔀",
            width=60
        )

        self.shuffle_button.pack(
            side="left",
            padx=5
        )

        self.repeat_button = ctk.CTkButton(
            actions_frame,
            text="🔁",
            width=60
        )

        self.repeat_button.pack(
            side="left",
            padx=5
        )

    # =========================================================
    # BOTTOM PANEL
    # =========================================================

    def create_bottom_panel(self):

        self.bottom_panel = ctk.CTkFrame(
            self.main_frame,
            corner_radius=10
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
        # PROGRESS SECTION
        # =====================================================

        progress_frame = ctk.CTkFrame(
            self.bottom_panel,
            fg_color="transparent"
        )

        progress_frame.pack(
            fill="x",
            padx=15,
            pady=(10, 5)
        )

        self.progress_slider = ctk.CTkSlider(
            progress_frame,
            from_=0,
            to=100
        )

        self.progress_slider.pack(
            fill="x",
            padx=10
        )

        self.progress_slider.set(0)

        self.time_label = ctk.CTkLabel(
            progress_frame,
            text="00:00 / 00:00"
        )

        self.time_label.pack(
            pady=5
        )

        # =====================================================
        # PLAYER CONTROLS
        # =====================================================

        controls_frame = ctk.CTkFrame(
            self.bottom_panel,
            fg_color="transparent"
        )

        controls_frame.pack(
            pady=10
        )

        self.prev_button = ctk.CTkButton(
            controls_frame,
            text="⏮",
            width=60
        )

        self.prev_button.pack(
            side="left",
            padx=5
        )

        self.play_button = ctk.CTkButton(
            controls_frame,
            text="▶",
            width=60
        )

        self.play_button.pack(
            side="left",
            padx=5
        )

        self.pause_button = ctk.CTkButton(
            controls_frame,
            text="⏸",
            width=60
        )

        self.pause_button.pack(
            side="left",
            padx=5
        )

        self.stop_button = ctk.CTkButton(
            controls_frame,
            text="⏹",
            width=60
        )

        self.stop_button.pack(
            side="left",
            padx=5
        )

        self.next_button = ctk.CTkButton(
            controls_frame,
            text="⏭",
            width=60
        )

        self.next_button.pack(
            side="left",
            padx=5
        )


        # =====================================================
        # VOLUME
        # =====================================================

        volume_frame = ctk.CTkFrame(
            self.bottom_panel,
            fg_color="transparent"
        )

        volume_frame.pack(
            pady=(0, 10)
        )

        volume_label = ctk.CTkLabel(
            volume_frame,
            text="🔊 Volume"
        )

        volume_label.pack(
            side="left",
            padx=10
        )

        self.volume_slider = ctk.CTkSlider(
            volume_frame,
            from_=0,
            to=100,
            width=200
        )

        self.volume_slider.set(50)

        self.volume_slider.pack(
            side="left"
        )

    # =========================================================
    # HELPER METHODS
    # =========================================================

    def clear_playlist(self):

        for item in self.playlist_box.get_children():

            self.playlist_box.delete(item)
        
    def add_song_to_playlist(
        self,
        title,
        artist,
        duration
        ):

        minutes = duration // 60
        seconds = duration % 60

        duration_text = f"{minutes}:{seconds:02}"

        self.playlist_box.insert(
            "",
            "end",
            values=(
                title,
                artist,
                duration_text
            )
        )
    def get_selected_index(self):

        selected = self.playlist_box.selection()

        if not selected:
            return None

        item = selected[0]

        return self.playlist_box.index(item)
    
    def set_status(self, text):

        self.status_label.configure(
            text=text
        )

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

            image.thumbnail((280, 280))

            cover = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(280, 280)
            )

            self.album_art.configure(
                image=cover,
                text=""
            )

            self.album_art.image = cover

        else:

            self.album_art.configure(
                image=None,
                text="No Album Art"
            )

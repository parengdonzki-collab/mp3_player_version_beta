import customtkinter as ctk
from tkinter import ttk

class RadioView:
    def __init__(self, parent):
        self.root = ctk.CTkToplevel(parent)
        self.root.title("Internet Radio")
        self.root.geometry("700x500")

        # SEARCH BAR
        search_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=10)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search stations...",
            height=40
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.search_button = ctk.CTkButton(
            search_frame, text="🔍 Search", width=100, height=40
        )
        self.search_button.pack(side="left")

        # STATION LIST
        style = ttk.Style()
        style.configure("Radio.Treeview",
            background="#252525", foreground="#f0f0f0",
            fieldbackground="#252525", rowheight=32,
            font=("Segoe UI", 11)
        )

        self.station_list = ttk.Treeview(
            self.root,
            columns=("Name", "Country"),
            show="headings",
            style="Radio.Treeview"
        )
        self.station_list.heading("Name", text="Station")
        self.station_list.heading("Country", text="Country")
        self.station_list.column("Name", width=450)
        self.station_list.column("Country", width=150)
        self.station_list.pack(fill="both", expand=True, padx=15, pady=5)

        # CONTROLS
        controls = ctk.CTkFrame(self.root, fg_color="transparent")
        controls.pack(fill="x", padx=15, pady=10)

        self.play_button = ctk.CTkButton(controls, text="▶ Play", width=80)
        self.play_button.pack(side="left", padx=5)

        self.stop_button = ctk.CTkButton(controls, text="⏹ Stop", width=80)
        self.stop_button.pack(side="left", padx=5)

        self.status_label = ctk.CTkLabel(controls, text="Ready")
        self.status_label.pack(side="left", padx=15)

        # store url per row
        self._urls = {}

    def add_station(self, name, country, url):
        iid = self.station_list.insert("", "end", values=(name, country))
        self._urls[iid] = url

    def clear_stations(self):
        self.station_list.delete(*self.station_list.get_children())
        self._urls.clear()

    def get_selected_url_and_name(self):
        selected = self.station_list.selection()
        if not selected:
            return None, None
        iid = selected[0]
        name = self.station_list.item(iid, "values")[0]
        return self._urls.get(iid), name

    def set_status(self, text):
        self.status_label.configure(text=text)
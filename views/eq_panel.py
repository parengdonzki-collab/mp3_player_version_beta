import customtkinter as ctk


class EQPanel:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, corner_radius=12)

        ctk.CTkLabel(
            self.frame,
            text="EQ",
            font=("Segoe UI", 13, "bold"),
        ).pack(pady=(10, 6))

        # ── Bands container (horizontal row of vertical sliders) ──
        bands_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        bands_frame.pack(padx=14, pady=(0, 6))

        self._band_vars = {}
        self._value_labels = {}

        for band in ("Bass", "Mid", "Treble"):
            self._build_band(bands_frame, band)

        # ── Reset ──────────────────────────────────────────────
        self.reset_button = ctk.CTkButton(
            self.frame,
            text="Reset",
            width=80,
            height=28,
            command=self._reset,
        )
        self.reset_button.pack(pady=(4, 10))

    # ── Private helpers ────────────────────────────────────────

    def _build_band(self, parent, name: str) -> None:
        """Create a vertical column: top dB label, slider, band name."""
        col = ctk.CTkFrame(parent, fg_color="transparent")
        col.pack(side="left", padx=10)

        # Live dB readout at the top
        lbl = ctk.CTkLabel(col, text=" 0.0 dB", font=("Segoe UI", 10),
                           width=58, anchor="center")
        lbl.pack()
        self._value_labels[name] = lbl

        # Vertical slider — orientation="vertical", slider moves up/down
        var = ctk.DoubleVar(value=0.0)
        self._band_vars[name] = var

        slider = ctk.CTkSlider(
            col,
            from_=12,          # top = +12 dB (CTk vertical: from_ is top)
            to=-12,            # bottom = -12 dB
            number_of_steps=24,
            variable=var,
            height=160,        # tall axis
            orientation="vertical",
            command=lambda v, n=name: self._on_change(n, v),
        )
        slider.pack(pady=(4, 4))
        setattr(self, f"{name.lower()}_slider", slider)
        # Band name at the bottom
        ctk.CTkLabel(col, text=name, font=("Segoe UI", 11),
                     anchor="center").pack()

    def _on_change(self, band: str, value: float) -> None:
        sign = "+" if value >= 0 else ""
        self._value_labels[band].configure(text=f"{sign}{value:.1f} dB")

    def _reset(self) -> None:
        for band, var in self._band_vars.items():
            var.set(0.0)
            self._value_labels[band].configure(text=" 0.0 dB")

    # ── Public API ─────────────────────────────────────────────

    def get_values(self) -> dict[str, float]:
        return {band: var.get() for band, var in self._band_vars.items()}

    def pack(self, **kwargs) -> None:
        self.frame.pack(**kwargs)

    def grid(self, **kwargs) -> None:
        self.frame.grid(**kwargs)

    def place(self, **kwargs) -> None:
        self.frame.place(**kwargs)
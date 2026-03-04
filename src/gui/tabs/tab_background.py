import customtkinter as ctk

from src.core.schema import BackgroundEntry, ProfileConfig


class _BackgroundRow(ctk.CTkFrame):
    def __init__(self, parent, entry: BackgroundEntry, on_remove):
        super().__init__(parent, fg_color=("#2b2b2b", "#2b2b2b"), corner_radius=8)
        self.pack(fill="x", pady=4, padx=2)
        self._on_remove = on_remove
        self._build(entry)

    def _build(self, entry: BackgroundEntry):
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=10)
        row.columnconfigure(5, weight=1)

        ctk.CTkLabel(row, text="Icon", width=35, anchor="w").grid(row=0, column=0, sticky="w")
        self._icon = ctk.CTkEntry(row, width=44, placeholder_text="🎓")
        self._icon.grid(row=0, column=1, padx=(4, 10))

        ctk.CTkLabel(row, text="Label", width=40, anchor="w").grid(row=0, column=2, sticky="w")
        self._label_e = ctk.CTkEntry(row, width=130, placeholder_text="Education")
        self._label_e.grid(row=0, column=3, padx=(4, 10))

        ctk.CTkLabel(row, text="Value", width=40, anchor="w").grid(row=0, column=4, sticky="w")
        self._value = ctk.CTkEntry(row, placeholder_text="Details…")
        self._value.grid(row=0, column=5, sticky="ew", padx=(4, 10))

        ctk.CTkButton(
            row, text="✕", width=30,
            fg_color="#6b2424", hover_color="#8b2424",
            command=lambda: self._on_remove(self),
        ).grid(row=0, column=6)

        self._set_entry(self._icon, entry.icon)
        self._set_entry(self._label_e, entry.label)
        self._set_entry(self._value, entry.value)

    @staticmethod
    def _set_entry(entry: ctk.CTkEntry, value: str) -> None:
        entry.delete(0, "end")
        if value:
            entry.insert(0, value)

    def to_entry(self) -> BackgroundEntry:
        return BackgroundEntry(
            icon=self._icon.get().strip() or "🔹",
            label=self._label_e.get().strip(),
            value=self._value.get().strip(),
        )


class BackgroundTab(ctk.CTkFrame):
    def __init__(self, parent, config: ProfileConfig):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self._rows: list[_BackgroundRow] = []
        self._build(config)

    def _build(self, config: ProfileConfig):
        ctk.CTkLabel(
            self,
            text="Add education, work experience, languages, certifications, etc.",
            text_color="gray",
        ).pack(anchor="w", pady=(0, 4))
        ctk.CTkButton(self, text="+ Add Entry", command=self._add_row).pack(
            anchor="w", pady=(0, 8)
        )
        self._scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._scroll.pack(fill="both", expand=True)
        for entry in config.background:
            self._add_row(entry)

    def _add_row(self, entry: BackgroundEntry = None):
        row = _BackgroundRow(
            self._scroll, entry or BackgroundEntry(), on_remove=self._remove_row
        )
        self._rows.append(row)

    def _remove_row(self, row: _BackgroundRow):
        row.destroy()
        self._rows.remove(row)

    def load_from(self, config: ProfileConfig) -> None:
        for row in self._rows[:]:
            row.destroy()
        self._rows.clear()
        for entry in config.background:
            self._add_row(entry)

    def apply_to(self, config: ProfileConfig) -> None:
        config.background = [row.to_entry() for row in self._rows]

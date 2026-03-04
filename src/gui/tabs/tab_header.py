import customtkinter as ctk

from src.core.schema import ProfileConfig


class HeaderTab(ctk.CTkFrame):
    def __init__(self, parent, config: ProfileConfig):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self._build(config)

    # ── helpers ───────────────────────────────────────────────────────────────

    def _labeled_entry(
        self, parent, label: str, row: int, placeholder: str = ""
    ) -> ctk.CTkEntry:
        ctk.CTkLabel(parent, text=label, anchor="w").grid(
            row=row, column=0, sticky="w", padx=(0, 12), pady=4
        )
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=420)
        entry.grid(row=row, column=1, sticky="ew", pady=4)
        return entry

    @staticmethod
    def _set_entry(entry: ctk.CTkEntry, value: str) -> None:
        entry.delete(0, "end")
        if value:
            entry.insert(0, value)

    @staticmethod
    def _set_textbox(tb: ctk.CTkTextbox, value: str) -> None:
        tb.delete("1.0", "end")
        if value:
            tb.insert("1.0", value)

    # ── build ─────────────────────────────────────────────────────────────────

    def _build(self, config: ProfileConfig):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        scroll.columnconfigure(1, weight=1)

        self._name = self._labeled_entry(scroll, "Display Name", 0, "e.g. Jane Dev")
        self._username = self._labeled_entry(scroll, "GitHub Username", 1, "e.g. janedev")
        self._github = self._labeled_entry(scroll, "GitHub Profile URL", 2, "https://github.com/...")
        self._linkedin = self._labeled_entry(scroll, "LinkedIn URL", 3, "https://linkedin.com/in/...")
        self._email = self._labeled_entry(scroll, "Email", 4, "user@example.com")
        self._twitter = self._labeled_entry(scroll, "Twitter URL (optional)", 5, "https://twitter.com/...")

        ctk.CTkLabel(scroll, text="Taglines (one per line)", anchor="w").grid(
            row=6, column=0, sticky="nw", padx=(0, 12), pady=4
        )
        self._taglines = ctk.CTkTextbox(scroll, height=80)
        self._taglines.grid(row=6, column=1, sticky="ew", pady=4)

        ctk.CTkLabel(scroll, text="About Me", anchor="w").grid(
            row=7, column=0, sticky="nw", padx=(0, 12), pady=4
        )
        self._about = ctk.CTkTextbox(scroll, height=140)
        self._about.grid(row=7, column=1, sticky="ew", pady=4)

        self._footer = self._labeled_entry(
            scroll, "Footer Text", 8, "Built with curiosity. Updated with intent."
        )

        self.load_from(config)

    # ── public interface ───────────────────────────────────────────────────────

    def load_from(self, config: ProfileConfig) -> None:
        self._set_entry(self._name, config.name)
        self._set_entry(self._username, config.github_username)
        self._set_entry(self._github, config.socials.github)
        self._set_entry(self._linkedin, config.socials.linkedin)
        self._set_entry(self._email, config.socials.email)
        self._set_entry(self._twitter, config.socials.twitter)
        self._set_textbox(self._taglines, "\n".join(config.taglines))
        self._set_textbox(self._about, config.about)
        self._set_entry(self._footer, config.footer_text)

    def apply_to(self, config: ProfileConfig) -> None:
        config.name = self._name.get().strip()
        config.github_username = self._username.get().strip()
        config.socials.github = self._github.get().strip()
        config.socials.linkedin = self._linkedin.get().strip()
        config.socials.email = self._email.get().strip()
        config.socials.twitter = self._twitter.get().strip()
        config.taglines = [
            ln.strip()
            for ln in self._taglines.get("1.0", "end").strip().splitlines()
            if ln.strip()
        ]
        config.about = self._about.get("1.0", "end").strip()
        config.footer_text = (
            self._footer.get().strip() or "Built with curiosity. Updated with intent."
        )

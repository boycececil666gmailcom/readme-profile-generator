from tkinter import filedialog, messagebox

import customtkinter as ctk

import os

from src.core.config_io import get_available_themes, get_base_dir, get_default_config_path, load_config, save_config
from src.core.renderer import preview_in_browser, render_readme
from src.core.schema import ProfileConfig
from src.gui.tabs.tab_background import BackgroundTab
from src.gui.tabs.tab_header import HeaderTab
from src.gui.tabs.tab_projects import ProjectsTab
from src.gui.tabs.tab_skills import SkillsTab


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("ProfileForge")
        self.geometry("960x720")
        self.minsize(700, 520)

        icon_path = os.path.join(get_base_dir(), "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self._config = ProfileConfig()
        self._build_ui()
        self._load_default_config()

    # ── UI construction ────────────────────────────────────────────────────────

    def _build_ui(self):
        self.tabview = ctk.CTkTabview(self, anchor="nw")
        self.tabview.pack(fill="both", expand=True, padx=16, pady=(16, 8))

        for label in ("Header", "Skills", "Projects", "Background"):
            self.tabview.add(label)

        self._tab_header = HeaderTab(self.tabview.tab("Header"), self._config)
        self._tab_skills = SkillsTab(self.tabview.tab("Skills"), self._config)
        self._tab_projects = ProjectsTab(self.tabview.tab("Projects"), self._config)
        self._tab_background = BackgroundTab(self.tabview.tab("Background"), self._config)

        # ── bottom action bar ──────────────────────────────────────────────────
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=16, pady=(0, 16))

        ctk.CTkLabel(bar, text="Theme:").pack(side="left", padx=(0, 4))
        self._theme_var = ctk.StringVar(value="developer")
        ctk.CTkOptionMenu(
            bar,
            values=get_available_themes(),
            variable=self._theme_var,
            width=140,
        ).pack(side="left", padx=(0, 20))

        ctk.CTkButton(bar, text="Load Config", width=120, command=self._load_config).pack(
            side="left", padx=4
        )
        ctk.CTkButton(bar, text="Save Config", width=120, command=self._save_config).pack(
            side="left", padx=4
        )
        ctk.CTkButton(
            bar, text="Preview in Browser", width=160, command=self._preview
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            bar,
            text="Export README.md",
            width=160,
            fg_color="#2ea44f",
            hover_color="#22863a",
            command=self._export,
        ).pack(side="right", padx=4)

        tip = ctk.CTkFrame(self, fg_color="transparent")
        tip.pack(fill="x", padx=16, pady=(0, 8))
        ctk.CTkLabel(
            tip,
            text="💡 Tip: Share the config JSON with an AI along with your own data to auto-generate a personalised config for you.",
            text_color="gray",
            font=ctk.CTkFont(size=11, slant="italic"),
            anchor="w",
            justify="left",
        ).pack(side="left")

    # ── actions ────────────────────────────────────────────────────────────────

    def _load_default_config(self):
        path = get_default_config_path()
        if not __import__('os').path.exists(path):
            return
        try:
            self._config = load_config(path)
            self._theme_var.set(self._config.theme)
            self._tab_header.load_from(self._config)
            self._tab_skills.load_from(self._config)
            self._tab_projects.load_from(self._config)
            self._tab_background.load_from(self._config)
        except Exception:
            pass

    def _collect(self) -> ProfileConfig:
        self._tab_header.apply_to(self._config)
        self._tab_skills.apply_to(self._config)
        self._tab_projects.apply_to(self._config)
        self._tab_background.apply_to(self._config)
        self._config.theme = self._theme_var.get()
        return self._config

    def _preview(self):
        preview_in_browser(render_readme(self._collect()))

    def _export(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown", "*.md"), ("All files", "*.*")],
            initialfile="README.md",
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(render_readme(self._collect()))
            messagebox.showinfo("Exported", f"README.md saved to:\n{path}")

    def _save_config(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON config", "*.json"), ("All files", "*.*")],
            initialfile="profile.config.json",
        )
        if path:
            save_config(self._collect(), path)
            messagebox.showinfo("Saved", f"Config saved to:\n{path}")

    def _load_config(self):
        path = filedialog.askopenfilename(
            filetypes=[("JSON config", "*.json"), ("All files", "*.*")]
        )
        if not path:
            return
        self._config = load_config(path)
        self._theme_var.set(self._config.theme)
        self._tab_header.load_from(self._config)
        self._tab_skills.load_from(self._config)
        self._tab_projects.load_from(self._config)
        self._tab_background.load_from(self._config)

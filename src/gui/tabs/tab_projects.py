import customtkinter as ctk

from src.core.schema import ProfileConfig, Project


class _ProjectRow(ctk.CTkFrame):
    def __init__(self, parent, project: Project, on_remove):
        super().__init__(parent, fg_color=("#2b2b2b", "#2b2b2b"), corner_radius=8)
        self.pack(fill="x", pady=4, padx=2)
        self._on_remove = on_remove
        self._build(project)

    def _build(self, project: Project):
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(10, 4))
        top.columnconfigure(1, weight=1)
        top.columnconfigure(3, weight=1)

        ctk.CTkLabel(top, text="Repo Name", width=90, anchor="w").grid(row=0, column=0, sticky="w")
        self._name = ctk.CTkEntry(top, placeholder_text="my-project")
        self._name.grid(row=0, column=1, sticky="ew", padx=(4, 12))

        ctk.CTkLabel(top, text="Demo URL", width=70, anchor="w").grid(row=0, column=2, sticky="w")
        self._demo = ctk.CTkEntry(top, placeholder_text="https://... (optional)")
        self._demo.grid(row=0, column=3, sticky="ew", padx=4)

        ctk.CTkButton(
            top, text="✕", width=30,
            fg_color="#6b2424", hover_color="#8b2424",
            command=lambda: self._on_remove(self),
        ).grid(row=0, column=4, padx=(8, 0))

        bot = ctk.CTkFrame(self, fg_color="transparent")
        bot.pack(fill="x", padx=10, pady=(0, 10))
        bot.columnconfigure(1, weight=1)
        bot.columnconfigure(3, weight=1)

        ctk.CTkLabel(bot, text="Description", width=90, anchor="w").grid(row=0, column=0, sticky="w")
        self._desc = ctk.CTkEntry(bot, placeholder_text="What this project does")
        self._desc.grid(row=0, column=1, sticky="ew", padx=(4, 12))

        ctk.CTkLabel(bot, text="Tech (comma)", width=70, anchor="w").grid(row=0, column=2, sticky="w")
        self._tech = ctk.CTkEntry(bot, placeholder_text="Python, Unity, C#")
        self._tech.grid(row=0, column=3, sticky="ew", padx=4)

        self._load(project)

    @staticmethod
    def _set_entry(entry: ctk.CTkEntry, value: str) -> None:
        entry.delete(0, "end")
        if value:
            entry.insert(0, value)

    def _load(self, project: Project):
        self._set_entry(self._name, project.name)
        self._set_entry(self._desc, project.description)
        self._set_entry(self._demo, project.demo_url)
        self._set_entry(self._tech, ", ".join(project.tech))

    def to_project(self) -> Project:
        return Project(
            name=self._name.get().strip(),
            description=self._desc.get().strip(),
            demo_url=self._demo.get().strip(),
            tech=[t.strip() for t in self._tech.get().split(",") if t.strip()],
        )


class ProjectsTab(ctk.CTkFrame):
    def __init__(self, parent, config: ProfileConfig):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self._rows: list[_ProjectRow] = []
        self._build(config)

    def _build(self, config: ProfileConfig):
        ctk.CTkButton(self, text="+ Add Project", command=self._add_row).pack(
            anchor="w", pady=(0, 8)
        )
        self._scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._scroll.pack(fill="both", expand=True)
        for project in config.projects:
            self._add_row(project)

    def _add_row(self, project: Project = None):
        row = _ProjectRow(self._scroll, project or Project(), on_remove=self._remove_row)
        self._rows.append(row)

    def _remove_row(self, row: _ProjectRow):
        row.destroy()
        self._rows.remove(row)

    def load_from(self, config: ProfileConfig) -> None:
        for row in self._rows[:]:
            row.destroy()
        self._rows.clear()
        for project in config.projects:
            self._add_row(project)

    def apply_to(self, config: ProfileConfig) -> None:
        config.projects = [row.to_project() for row in self._rows]

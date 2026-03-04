# SuperAmazingReadmeForge

> **🆓 Freeware — free to use, forever.**
> This tool was built as a genuine contribution to the developer community. A polished GitHub profile
> helps everyone stand out — and yes, building something useful for others is also the best kind of self-promotion.
> Use it, share it, and make your profile shine.

A desktop app (Python + CustomTkinter) to visually build and export a GitHub profile `README.md`.
Fill in your details, preview in your browser, then export — no Markdown knowledge required.

![SuperAmazingReadmeForge icon](assets/icon.ico)

## Features

- **4-tab form** — Header, Skills, Projects, Background
- **Live browser preview** — renders with GitHub-style CSS; dynamic badges load from CDN
- **Theme selector** — `developer` (dark blue), `minimal`, `vibrant`, or add your own
- **Load / Save config** — save your profile as a `.json` file and reload it anytime
- **Export** — outputs a ready-to-paste `README.md`
- **Packagable to `.exe`** via PyInstaller

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## Build .exe

```bash
pip install pyinstaller
pyinstaller build.spec
# output: dist/SuperAmazingReadmeForge.exe
```

> The `build.spec` bundles the `templates/` folder automatically.
> On non-Windows platforms, drop the `icon` line or provide a `.icns` / `.png`.

## Project Structure

```
SuperAmazingReadmeForge/
├── main.py                     # Entry point
├── requirements.txt
├── build.spec                  # PyInstaller config
├── src/
│   ├── core/
│   │   ├── schema.py           # Pydantic config models
│   │   ├── renderer.py         # Jinja2 renderer + browser preview
│   │   ├── badge_map.py        # Skill → shields.io badge URL dictionary
│   │   └── config_io.py        # Load / save JSON config & themes
│   └── gui/
│       ├── app.py              # Main CustomTkinter window
│       └── tabs/
│           ├── tab_header.py
│           ├── tab_skills.py
│           ├── tab_projects.py
│           └── tab_background.py
└── templates/
    ├── sections/               # Jinja2 templates (.md.j2) per README section
    └── themes/                 # JSON theme files (accent colors, badge styles)
```

## Adding a Custom Theme

Create `templates/themes/mytheme.json`:
```json
{
  "name": "mytheme",
  "accent_color": "FF6B6B",
  "badge_style": "flat-square",
  "badge_style_social": "for-the-badge",
  "background_color": "1a1a2e"
}
```
It will appear in the Theme dropdown automatically.

## Adding Skills / Badges

Edit `src/core/badge_map.py` and add an entry:
```python
"My Tool": "https://img.shields.io/badge/MyTool-COLOR?style=flat-square&logo=...",
```

## Showcase

Here's a real GitHub profile README generated with this tool:

👉 **[github.com/boycececil666gmailcom](https://github.com/boycececil666gmailcom)**

## License

MIT

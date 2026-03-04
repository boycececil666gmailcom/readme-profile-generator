import os
import sys
import tempfile
import webbrowser
from urllib.parse import quote_plus

import markdown as md_lib
from jinja2 import Environment, FileSystemLoader

from src.core.badge_map import BADGE_MAP
from src.core.config_io import _get_base_dir, load_theme
from src.core.schema import ProfileConfig


def _get_sections_dir() -> str:
    return os.path.join(_get_base_dir(), "templates", "sections")


# Each entry: (config field name, display label, badge URL template, link URL template).
# {s} is replaced by the theme's badge style; {v} is replaced by the field value.
_SOCIAL_DEFS = [
    ("github",   "GitHub",   "https://img.shields.io/badge/GitHub-181717?style={s}&logo=github&logoColor=white",   "https://github.com/{v}"),
    ("linkedin", "LinkedIn", "https://img.shields.io/badge/LinkedIn-0A66C2?style={s}&logo=linkedin&logoColor=white", "{v}"),
    ("email",    "Email",    "https://img.shields.io/badge/Email-D14836?style={s}&logo=gmail&logoColor=white",      "mailto:{v}"),
    ("twitter",  "Twitter",  "https://img.shields.io/badge/Twitter-1DA1F2?style={s}&logo=twitter&logoColor=white",  "{v}"),
]


def render_readme(config: ProfileConfig) -> str:
    theme = load_theme(config.theme)
    env = Environment(
        loader=FileSystemLoader(_get_sections_dir()),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    style_social = theme.get("badge_style_social", "for-the-badge")

    # Build social badge list from any populated fields.
    socials = [
        {
            "label": label,
            "badge_url": badge_tmpl.format(s=style_social, v=value),
            "url": url_tmpl.format(v=value),
        }
        for field, label, badge_tmpl, url_tmpl in _SOCIAL_DEFS
        if (value := getattr(config.socials, field, ""))
    ]

    taglines_encoded = ";".join(quote_plus(t) for t in config.taglines)

    # Shorthand keys let templates stay concise (e.g. `tier1` instead of `config.skills.tier1`).
    ctx = {
        "config": config,
        "theme": theme,
        "github_username": config.github_username,
        "taglines_encoded": taglines_encoded,
        "socials": socials,
        "about_text": config.about,
        "tier1": config.skills.tier1,
        "tier2": config.skills.tier2,
        "tier3": config.skills.tier3,
        "projects": config.projects,
        "background": config.background,
        "footer_text": config.footer_text,
        "badge_map": BADGE_MAP,
    }

    parts = []
    for section in config.sections:
        try:
            parts.append(env.get_template(f"{section}.md.j2").render(**ctx))
        except Exception:
            # Skip sections whose template cannot be found or rendered.
            pass

    return "\n".join(parts)


def preview_in_browser(markdown_content: str) -> None:
    html_body = md_lib.markdown(
        markdown_content,
        extensions=["tables", "fenced_code", "nl2br"],
    )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>README Preview</title>
  <link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown-dark.min.css">
  <style>
    body {{
      box-sizing: border-box;
      min-width: 200px;
      max-width: 980px;
      margin: 0 auto;
      padding: 45px;
    }}
    @media (max-width: 767px) {{ body {{ padding: 15px; }} }}
  </style>
</head>
<body class="markdown-body">
{html_body}
</body>
</html>"""

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False, encoding="utf-8"
    ) as f:
        f.write(html)
        tmp_path = f.name

    webbrowser.open(f"file:///{tmp_path.replace(os.sep, '/')}")

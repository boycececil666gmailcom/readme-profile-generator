import json
import os
import sys
from typing import Any

from src.core.schema import ProfileConfig


def _get_base_dir() -> str:
    if getattr(sys, "frozen", False):
        return sys._MEIPASS  # type: ignore[attr-defined]
    # This file lives at src/core/config_io.py — three levels up is the project root.
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_base_dir() -> str:
    """Public alias for _get_base_dir — use this outside core."""
    return _get_base_dir()


def load_theme(theme_name: str) -> dict[str, Any]:
    themes_dir = os.path.join(_get_base_dir(), "templates", "themes")
    path = os.path.join(themes_dir, f"{theme_name}.json")
    if not os.path.exists(path):
        path = os.path.join(themes_dir, "developer.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_available_themes() -> list[str]:
    themes_dir = os.path.join(_get_base_dir(), "templates", "themes")
    return [
        os.path.splitext(f)[0]
        for f in os.listdir(themes_dir)
        if f.endswith(".json")
    ]


def get_default_config_path() -> str:
    return os.path.join(_get_base_dir(), "default.config.json")


def save_config(config: ProfileConfig, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(config.model_dump_json(indent=2))


def load_config(path: str) -> ProfileConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return ProfileConfig.model_validate(data)

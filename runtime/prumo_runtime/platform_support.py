from __future__ import annotations

import os
import platform
import sys
from pathlib import Path


def platform_system() -> str:
    return platform.system() or "Unknown"


def platform_family() -> str:
    system = platform_system()
    if system == "Darwin":
        return "macos"
    if system == "Windows":
        return "windows"
    if system == "Linux":
        return "linux"
    return system.lower()


def platform_label() -> str:
    family = platform_family()
    if family == "macos":
        return "macOS"
    if family == "windows":
        return "Windows"
    if family == "linux":
        return "Linux"
    return platform_system()


def is_macos() -> bool:
    return platform_family() == "macos"


def is_windows() -> bool:
    return platform_family() == "windows"


def is_linux() -> bool:
    return platform_family() == "linux"


def python_version() -> str:
    return platform.python_version()


def runtime_app_dir() -> Path:
    if is_macos():
        return Path.home() / "Library" / "Application Support" / "Prumo"
    if is_windows():
        base = os.environ.get("APPDATA") or os.environ.get("LOCALAPPDATA")
        if base:
            return Path(base) / "Prumo"
        return Path.home() / "AppData" / "Roaming" / "Prumo"
    xdg_state = os.environ.get("XDG_STATE_HOME")
    if xdg_state:
        return Path(xdg_state) / "prumo"
    return Path.home() / ".local" / "state" / "prumo"


def runtime_platform_summary() -> dict[str, str]:
    return {
        "system": platform_system(),
        "family": platform_family(),
        "label": platform_label(),
        "release": platform.release(),
        "python_version": python_version(),
        "runtime_app_dir": str(runtime_app_dir()),
    }

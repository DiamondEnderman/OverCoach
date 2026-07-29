from libraries.controllers.setting_manager import CONFIG
import os
import webbrowser

def _open_protocol(url: str) -> None:
    if hasattr(os, "startfile"):
        os.startfile(url)
    else:
        webbrowser.open(url)

def launch_overwatch() -> None:
    launcher = CONFIG.get("launcher")
    match launcher:
        case "steam":
            try:
                _open_protocol("steam://rungameid/2357570")
            except OSError:
                print("Steam protocol failed to open, Steam might not be installed")
        case _:
            print("Unsupported Launcher")
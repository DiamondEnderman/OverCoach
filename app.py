import flet
import sys
import os

from libraries.consts import AppConfig as AppConfig

import libraries.controllers.file_controller as filecontroller
from libraries.controllers.github_manager import GitChallenges
import libraries.debug.crash_logs as crashlogs

from libraries.controllers.setting_manager import CONFIG
from libraries.controllers.profile_manager import Profile

from libraries.ui.dashboard.main import run as run_dashboard
import libraries.ui.dashboard.profile_card as profile_card

from libraries.controllers.asset_handler import get_hero_icon

from libraries.controllers.rollover_manager import rollover

def app(page: flet.Page) -> None:
    page.window.width = AppConfig.WINDOW_WIDTH
    page.window.height = AppConfig.WINDOW_HEIGHT
    page.window.resizable = False

    page.title = f"OverCoach Version {AppConfig.VERSION_NUMBER}"
    page.theme_mode = flet.ThemeMode.DARK

    active_profile = CONFIG.get("active_profile")
    if active_profile:
        profile = Profile(active_profile)
        profile.load_from_file()
        page.active_profile = profile
        print(f"Auto-loaded profile: {active_profile}")

        rollover(profile)

        if profile.current_hero:
            profile_card.profile_avatar.src = get_hero_icon(profile.current_hero)

        profile_card.refresh_card_data(page, active_profile)

    run_dashboard(page)

if __name__ == "__main__":

    crashlogs.initialize_crash_logger()

    filecontroller.initialize_system_folders()
    print("Application folders successfully initialized.")

    if getattr(sys, "frozen", False):
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        assets_path = os.path.join(base_dir, "assets")
    else:
        assets_path = "assets"

    GitChallenges.sync()

    flet.run(main=app, assets_dir=assets_path)
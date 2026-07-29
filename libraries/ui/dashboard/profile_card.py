import flet
from libraries.consts import Colors
from libraries.consts import Text
from libraries.consts import UI

from libraries.controllers.profile_manager import Profile
from libraries.controllers.profile_manager import get_all_profiles

from libraries.controllers.overfast_api import CareerStats
from libraries.controllers.setting_manager import CONFIG

from libraries.controllers.asset_handler import get_hero_icon

from libraries.ui.templates import TextTemplate

from libraries.ui.dashboard import challenge_card

import requests

bg_color = Colors.BLUE_GREY

profile_avatar = flet.Image(
    src = get_hero_icon(None),
    width = 130,
    height = 130,
    fit = flet.BoxFit.CONTAIN,
)

hero_icon = flet.Container(
    content = profile_avatar,
    width = 135,
    height = 135,
    alignment = flet.Alignment.CENTER,
    border = flet.Border.all(2, Colors.WHITE)
)

class TextReg:
    battletag = TextTemplate.create("No Profile Loaded", "h3")
    main_hero = TextTemplate.create("Main Hero: None", "h3")
    global_winrate = TextTemplate.create("Global Winrate: -", "h3")
    winrate = TextTemplate.create("Character Winrate: -", "h3")

    averages = TextTemplate.create("10 Minute Averages for Current Hero:", "h2")
    damage = TextTemplate.create("Damage: -", "pg")
    healing = TextTemplate.create("Healing: -", "pg")
    deaths = TextTemplate.create("Deaths: -", "pg")
    elims = TextTemplate.create("Eliminations: -", "pg")
    solos = TextTemplate.create("Solo Kills: -", "pg")

def refresh_card_data(page:flet.Page, profile_name = None) -> None:
    if profile_name is None:
        TextReg.battletag.value = "No Profile Loaded"
        TextReg.main_hero.value = "Main Hero: None"
        TextReg.global_winrate.value = "Global Winrate: -"
        TextReg.winrate.value = "Character Winrate: -"

        TextReg.damage.value = "Damage: -"
        TextReg.healing.value = "Healing: -"
        TextReg.deaths.value = "Deaths: -"
        TextReg.elims.value = "Eliminations: -"
        TextReg.solos.value = "Solo Kills: -"

        profile_avatar.src = get_hero_icon(None)
        return

    profile = Profile(profile_name)
    profile.load_from_file()
    profile.fetch_data()


    profile_avatar.src = get_hero_icon(profile.current_hero)

    print(f"Loaded profile: {[profile.profile]} | Battletag: {profile.battletag}")

    CONFIG.set("active_profile", profile_name)
    page.active_profile = profile

    challenge_card.refresh_challenges_ui(page)

    hero_stats = CareerStats(profile.battletag, profile.current_hero)

    TextReg.battletag.value = f"BattleTag: {profile.battletag}"
    TextReg.main_hero.value = f"Main Hero: {profile.main_hero.replace("-", " ").title()}"
    TextReg.global_winrate.value = f"Global Winrate: {hero_stats.get_winrate("all")}%"
    TextReg.winrate.value = f"Character Winrate: {hero_stats.get_winrate(profile.current_hero)}%"

    TextReg.damage.value = f"Damage: {hero_stats.damage_per_ten}"
    TextReg.healing.value = f"Healing: {hero_stats.healing_per_ten}"
    TextReg.deaths.value = f"Deaths: {hero_stats.deaths_per_ten}"
    TextReg.elims.value = f"Eliminations: {hero_stats.elims_per_ten}"
    TextReg.solos.value = f"Solo Kills: {hero_stats.solos_per_ten}"

def _on_profile_change(e) -> None:
    selected_name = e.control.value
    if not selected_name:
        return

    refresh_card_data(e.page, selected_name)

    e.page.update()

profile_dropdown = flet.Dropdown(
    width = 200,
    height = 45,
    on_select = _on_profile_change,
    value = CONFIG.get("active_profile"),
    options = [
        flet.dropdown.Option(profile) for profile in get_all_profiles()
    ]
)

class NewProfileSetup:
    NAME_INPUT = flet.TextField(
        hint_text = "ex: Main Profile",
        max_length = 50,
    )
    BATTLETAG_INPUT = flet.TextField(
        hint_text = "ex: PLAYER#12345",
        max_length = 50
    )
    PLATFORM_DROPDOWN = flet.Dropdown(
        value = "PC",
        options = [
            flet.dropdown.Option("PC"),
            flet.dropdown.Option("XBOX"),
            flet.dropdown.Option("PSN")
        ]
    )

    @staticmethod
    def open_dialog(e) -> None:
        if not NewProfileSetup.ALERT_DIALOG in e.page.overlay:
            e.page.overlay.append(NewProfileSetup.ALERT_DIALOG)
        NewProfileSetup.ALERT_DIALOG.open = True
        e.page.update()

    @staticmethod
    def close_dialog(e) -> None:
         NewProfileSetup.ALERT_DIALOG.open = False
         e.page.update()

    def _show_error(page, msg: str) -> None:
        def close_error():
            error_dialog.open = False
        error_dialog = flet.AlertDialog(
            title = TextTemplate.create("Error", "error"),
            content = flet.Text(value = msg),
            actions = [
                flet.TextButton(
                    content = "OK",
                    on_click = close_error,
                    style = UI.DEFAULT_BUTTON_STYLE
                )
            ]
        )
        page.overlay.append(error_dialog)
        error_dialog.open = True
        page.update()

    @staticmethod
    def confirm_creation(e) -> None:
        profile_name = NewProfileSetup.NAME_INPUT.value
        if profile_name in get_all_profiles():
            error_msg = f"Profile already existing with the same name."
            NewProfileSetup._show_error(e.page, error_msg)
            return

        profile = Profile(profile_name)
        profile.battletag = NewProfileSetup.BATTLETAG_INPUT.value
        profile.platform = NewProfileSetup.PLATFORM_DROPDOWN.value.lower()

        try:
            profile.fetch_data()
            profile.create()
            profile.save_to_file()

            NewProfileSetup.close_dialog(e)
            profile_dropdown.options.append(flet.dropdown.Option(profile.profile))
            profile_dropdown.value = profile.profile
            e.page.active_profile = profile
            print(f"New Profile Added: {profile.profile}")

            refresh_card_data(e.page, profile.profile)
            e.page.update()
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                error_msg = (
                    f"Could not find or load player '{profile.battletag}' on {profile.platform.upper()}.\n\n"
                    "Please double check that: \n"
                    "1. Your BattleTag is spelled correctly (including the # and following numbers).\n"
                    "2. Your in-game Career Profile is set to 'Public' under Social Settings"
                )
                NewProfileSetup._show_error(e.page, error_msg)
            else:
                NewProfileSetup._show_error(e.page, f"Network Connection Failed: {err}")
        except Exception as err:
            NewProfileSetup._show_error(e.page, f"An unexpected error occured: {err}")

    ALERT_DIALOG = flet.AlertDialog(
        title = flet.Text(value = "Create a New Profile"),
        content = flet.Column(
            controls = [
                TextTemplate.create("Profile Name:","big_pg"),
                NAME_INPUT,
                TextTemplate.create("BattleTag:","big_pg"),
                BATTLETAG_INPUT,
                TextTemplate.create("Platform:","big_pg"),
                PLATFORM_DROPDOWN,
            ]
        ),
        actions = [
            flet.Button(
                content = TextTemplate.create("Confirm", "h2"),
                bgcolor = Colors.ORANGE,
                width = 200,
                height = 45,
                on_click = confirm_creation,
                style = UI.DEFAULT_BUTTON_STYLE
            ),
            flet.TextButton(
                content = "cancel",
                on_click = close_dialog,
                style = UI.DEFAULT_BUTTON_STYLE
            )
        ]
    )

new_profile_button = flet.Button(
    width = 130,
    height = 50,
    bgcolor = Colors.ORANGE,
    style = UI.DEFAULT_BUTTON_STYLE,
    content = TextTemplate.create("Create", "h2"),
    on_click = NewProfileSetup.open_dialog
)

def delete_profile(e) -> None:
    profile = Profile(CONFIG.get("active_profile"))
    profile.delete()
    CONFIG.set("active_profile", None)
    e.page.active_profile = None
    profile_dropdown.value = None
    profile_dropdown.options = [flet.dropdown.Option(profile) for profile in get_all_profiles()]
    refresh_card_data(e.page)
    e.page.update()

delete_profile_text_button = flet.TextButton(
    content = TextTemplate.create("Delete Profile", "error"),
    on_click = delete_profile,
    style = UI.DEFAULT_BUTTON_STYLE
)

profile_card = flet.Container(
    bgcolor = bg_color,
    width = 500,
    height = 500,
    border_radius = UI.EDGE_ROUNDING,
    padding = 20,
    content = flet.Column(
        controls = [
            flet.Row(
                controls = [
                    flet.Text(
                        value = "Profile:",
                        size = 20,
                        weight = Text.BOLD,
                        color = Colors.WHITE
                    ),
                    profile_dropdown,
                    new_profile_button
                ],
                alignment=flet.MainAxisAlignment.CENTER,
            ),
            flet.Row(
                controls = [
                    hero_icon,
                    flet.Column(
                        controls = [
                            TextReg.battletag,
                            TextReg.main_hero,
                            TextReg.global_winrate,
                            TextReg.winrate
                        ]
                    )
                ],
                alignment = flet.MainAxisAlignment.START
            ),
            flet.Row(
                controls = [
                    flet.Column(
                        controls = [
                            TextReg.averages,
                            TextReg.damage,
                            TextReg.healing,
                            TextReg.deaths,
                            TextReg.elims,
                            TextReg.solos
                        ],
                    )
                ],
                alignment = flet.MainAxisAlignment.START
            ),
            flet.Row(
                controls = [
                    delete_profile_text_button
                ],
                alignment = flet.MainAxisAlignment.END
            )
        ],
        scroll = flet.ScrollMode.AUTO
    )
)
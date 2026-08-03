import flet
from libraries.consts import Colors as Colors
from libraries.consts import UI as UI
from libraries.consts import Text as Text
from libraries.controllers.setting_manager import CONFIG

import libraries.controllers.launcher as launcher

from libraries.ui.dashboard.challenge_card import challenge_card
from libraries.ui.dashboard.profile_card import profile_card

from libraries.ui.dashboard.settings_menu import SettingMenu
from libraries.ui.learn.main import LearnMenu

IS_TEST = False

def _build_header() -> flet.Row:
    bg_color = Colors.BRIGHT_RED if IS_TEST else None
    header_container = flet.Container(
        alignment = flet.Alignment.CENTER,
        bgcolor=bg_color,
        width = 600,
        height = 70,
        content = flet.Text(
            spans = [
                flet.TextSpan(
                    text = "Over",
                    style = flet.TextStyle(
                        color=Colors.WHITE,
                        weight=Text.BOLD
                    )
                ),
                flet.TextSpan(
                    text = "Coach",
                    style = flet.TextStyle(
                        color = Colors.BRIGHT_ORANGE,
                        weight = Text.BOLD
                    )
                )
            ],
            size = 50
        )
    )

    return flet.Row(
        controls = [header_container], 
        alignment = flet.MainAxisAlignment.CENTER
    )

def _build_body() -> flet.Row:
    return flet.Row(
        controls = [challenge_card, profile_card],
        alignment = flet.MainAxisAlignment.CENTER,
        spacing = 20
    )

def _build_footer(page: flet.Page) -> flet.Row:
    button_height = 60
    font_size = 24
    
    settings_btn = flet.Button(
        width = 275,
        height = button_height,
        style = UI.DEFAULT_BUTTON_STYLE,
        content = flet.Text(
            value = "Settings",
            size = font_size,
            weight = Text.BOLD,
            color = Colors.WHITE,
        ),
        on_click = lambda: SettingMenu.open(page)
    )

    launch_btn = flet.Button(
        width = 350,
        height = button_height,
        bgcolor = Colors.ORANGE,
        style = UI.DEFAULT_BUTTON_STYLE,
        content = flet.Text(
            spans = [
                flet.TextSpan(
                    text = "Launch Overwatch\n",
                    style = flet.TextStyle(
                        size = font_size,
                        weight = Text.BOLD,
                        color = Colors.WHITE
                    )
                ),
                flet.TextSpan(
                    text = f"({CONFIG.get("launcher")})",
                    style = flet.TextStyle(
                        size = 10,
                        color = Colors.WHITE
                    )
                )
            ],
            text_align = flet.TextAlign.CENTER,
            
        ),
        on_click = lambda: launcher.launch_overwatch(page)
    )

    learn_btn = flet.Button(
        width = 275,
        height = button_height,
        style = UI.DEFAULT_BUTTON_STYLE,
        content = flet.Text(
            value = "Learn",
            size = font_size,
            weight = Text.BOLD,
            color = Colors.WHITE,
        ),
        on_click = lambda: LearnMenu.open(page)
    )

    return flet.Row(
        controls=[settings_btn, launch_btn, learn_btn],
        alignment = flet.MainAxisAlignment.CENTER,
        spacing= 10
    )

def run(page: flet.Page):
    layout = flet.Column(
        controls = [_build_header(), _build_body(), _build_footer(page)],
        alignment = flet.MainAxisAlignment.CENTER,
        spacing = 20
    )
    page.add(layout)
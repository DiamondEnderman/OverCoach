import flet

from libraries.controllers.setting_manager import CONFIG

from libraries.ui.templates import TextTemplate

from libraries.consts import UI

class Launcher:
    SUPPORTED_LAUNCHERS = [
        "steam"
    ]

    options = [
        flet.dropdown.Option(
            text = launcher.capitalize(),
            key = launcher
        ) for launcher in SUPPORTED_LAUNCHERS
    ]

    dropdown = flet.Dropdown(options = options, value = CONFIG.get("launcher"))

    row = flet.Row(
        controls = [
            TextTemplate.create("Launcher:", "h3"),
            dropdown
        ]
    )

SETTING_COLUMN = flet.Column(
    controls = [
        Launcher.row
    ],
    scroll = flet.ScrollMode.AUTO
)

class SettingMenu:
    def open(page: flet.Page) -> None:
        if not SettingMenu.DIALOG in page.overlay:
            page.overlay.append(SettingMenu.DIALOG)
        SettingMenu.DIALOG.open = True
        page.update()

    @staticmethod
    def close(e) -> None:
        SettingMenu.DIALOG.open = False
        e.page.update()

    @staticmethod
    def _save(e) -> None:
        CONFIG.set("launcher", Launcher.dropdown.value)
        SettingMenu.close(e)

    DIALOG = flet.AlertDialog(
        title = TextTemplate.create("Settings", "h2"),
        content = SETTING_COLUMN,
        open = False,
        actions = [
            flet.TextButton(
                content = "Save",
                on_click = lambda e: SettingMenu._save(e),
                style = UI.DEFAULT_BUTTON_STYLE
            ),
            flet.TextButton(
                content = "Cancel",
                on_click = lambda e: SettingMenu.close(e),
                style = UI.DEFAULT_BUTTON_STYLE
            )
        ]
    )
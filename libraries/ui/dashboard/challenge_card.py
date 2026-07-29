import flet
from libraries.consts import Colors
from libraries.consts import Text
from libraries.consts import UI

from libraries.controllers.setting_manager import CONFIG
from libraries.controllers.profile_manager import Profile

from libraries.ui.templates import TextTemplate

bg_color = Colors.BLUE_GREY

challenge_column = flet.Column(spacing=15, scroll = flet.ScrollMode.AUTO)

def refresh_challenges_ui(page: flet.Page) -> None:
    challenge_column.controls.clear()
    active_profile = getattr(page, "active_profile", None)
    if not active_profile or not active_profile.active_challenges:
        challenge_column.controls.append(
            TextTemplate.create("Select a profile to load daily challenges", "pg")
        )
        page.update()
        return

    for category, challenge_list in active_profile.active_challenges.items():
        challenge_column.controls.append(
            TextTemplate.create(f"{category}:".capitalize(), "h3")
        )

        for challenge in challenge_list:
            challenge_column.controls.append(
                flet.Checkbox(
                    label = TextTemplate.create(challenge.get("title", "Untitled, Challenge"), "pg"),
                    value = False,
                    tooltip = challenge.get("description", ""),
                    mouse_cursor = flet.MouseCursor.CLICK,
                )
            )
    page.update()

challenge_card = flet.Container(
    bgcolor = bg_color,
    width = 390,
    height = 500,
    border_radius = UI.EDGE_ROUNDING,
    padding = 20,
    content = flet.Column(
        controls = [
            flet.Row(
                controls = [TextTemplate.create("Daily Challenges:", "h3")],
                alignment = flet.MainAxisAlignment.CENTER,
            ),
            challenge_column
        ],
        scroll = flet.ScrollMode.AUTO
    )
)
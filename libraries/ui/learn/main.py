import flet

from libraries.ui.templates import TextTemplate
from libraries.consts import Text
from libraries.consts import Colors
from libraries.consts import UI

class _Consts:
    CARD_HEIGHT = 100
    CARD_WIDTH = 180

def _create_concept_card(title: str, tooltip_text: str = "") -> flet.Container:
    return flet.Container(
        width = _Consts.CARD_WIDTH,
        height = _Consts.CARD_HEIGHT,
        bgcolor = Colors.ORANGE,
        border_radius = UI.EDGE_ROUNDING,
        
        shadow=flet.BoxShadow(
            spread_radius = 1,
            blur_radius = 10,
            color = flet.Colors.BLACK_38,
            offset = flet.Offset(0, 4)
        ),
        
        alignment = flet.Alignment.CENTER,
        padding = 10,
        tooltip = tooltip_text,
        content = TextTemplate.create(title, "h3"),
    )

def _build_category_rail(title: str, concepts: dict) -> flet.Container:
    cards = [
        _create_concept_card(concept.get("title", "Concept"), concept.get("tooltip", ""))
        for concept in concepts
    ]

    inner_row_container = flet.Container(
        bgcolor = Colors.BLUE_GREY,
        border_radius = UI.EDGE_ROUNDING,
        padding = 15,
        content = flet.Row(
            controls = cards,
            scroll = flet.ScrollMode.AUTO,
            spacing = 15
        )
    )

    return flet.Container(
        padding = 10,
        content = flet.Column(
            controls = [
                TextTemplate.create(title, "h2"),
                inner_row_container
            ]
        )
    )

class LearnMenu:
    @staticmethod
    def close(e) -> None:
        LearnMenu.LEARN_DIALOG.open = False
        e.page.update()

    @staticmethod
    def open(page = flet.Page) -> None:
        if LearnMenu.LEARN_DIALOG not in page.overlay:
            page.overlay.append(LearnMenu.LEARN_DIALOG)
        LearnMenu.LEARN_DIALOG.open = True
        page.update()

    _dummy_beginner_concepts = [
        {"title": "Use Cover", "tooltip": "Learn how to die less"},
        {"title": "High Ground", "tooltip": "Gain sightline advantage"},
        {"title": "Turn Off Comms", "tooltip": "Protect your mental game"},
        {"title": "Side Angle", "tooltip": "Avoid standing in main"},
        {"title": "Relax", "tooltip": "Keep wrist tension low"},
    ]

    _dummy_intermediate_concepts = [
        {"title": "Peeker's Advantage", "tooltip": "Take tight angles"},
        {"title": "Isolate 1v1s", "tooltip": "Section off enemies using walls"},
        {"title": "Engagement Timing", "tooltip": "Strike when enemies are distracted"},
    ]

    LEARN_DIALOG = flet.AlertDialog(
        title=flet.Row(
            controls=[
                flet.Container(width = 48),
                flet.Text(
                    value = "Learn",
                    size = 36,
                    weight = Text.BOLD,
                    color = Colors.BLUE,
                    expand = True,
                    text_align = flet.TextAlign.CENTER
                ),
                flet.IconButton(
                    icon=flet.Icons.CLOSE,
                    icon_color=Colors.WHITE,
                    on_click=close,
                    width = 48
                ),
            ],
            alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
        ),
        content=flet.Container(
            width=850,
            height=550,
            content=flet.Column(
                controls=[
                    _build_category_rail("Beginner", _dummy_beginner_concepts),
                    _build_category_rail(
                        "Intermediate", _dummy_intermediate_concepts
                    ),
                ],
                scroll=flet.ScrollMode.AUTO,
                spacing=20,
            ),
        ),
        actions=[],
    )
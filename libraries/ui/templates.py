import flet

from libraries.consts import Text
from libraries.consts import Colors

class TextTemplate:
    templates = {
        "pg": {
            "fontsize": 16,
            "weight": Text.NORMAL,
            "color": Colors.WHITE
        },
        "big_pg": {
            "fontsize": 20,
            "weight": Text.NORMAL,
            "color": Colors.WHITE
        },
        "h1": {
            "fontsize": 24,
            "weight": Text.BOLD,
            "color": Colors.WHITE
        },
        "h2": {
            "fontsize": 20,
            "weight": Text.BOLD,
            "color": Colors.WHITE
        },
        "h3": {
            "fontsize": 18,
            "weight": Text.BOLD,
            "color": Colors.WHITE
        },
        "error": {
            "fontsize": 12,
            "weight": Text.NORMAL,
            "color": Colors.BRIGHT_RED
        } 
    }

    @classmethod
    def create(cls, text, template):
        """
        "pg": 
            Fontsize: 16
            Weight: Normal
            Color: White
        "big_pg":
            Fontsize: 20,
            Weight: Normal,
            Color: White
        "h1":
            Fontsize: 24
            Weight: Bold
            Color: White
        "h2":
            Fontsize: 20
            Weight: Bold
            Color: White
        "h3":
            Fontsize: 18
            Weight: Bold
            Color: White
        "error":
            Fontsize: 12
            Weight: Normal
            Color: Red
        """
        t = cls.templates[template]
        return flet.Text(
            value = text,
            size = t["fontsize"],
            weight = t["weight"],
            color = t["color"]
        )
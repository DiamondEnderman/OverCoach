from enum import StrEnum
import flet
import os

class AppConfig():
    VERSION_NUMBER = "0.1.0"

    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 750

    PROFILE_DATA_NAME = "data.json"
    CONFIG_FILE_NAME = "config.json"

class Roles(StrEnum):
    def __eq__(self, other):
        if isinstance(other, str):
            return self.lower() == other.lower()
        return NotImplemented
    
    def __hash__(self):
        return hash(self.lower())

    TANK = "tank"
    DAMAGE = "damage"
    SUPPORT = "support"
    OPEN = "open"

    @classmethod
    def all(cls):
        return [cls.TANK, cls.DAMAGE, cls.SUPPORT, cls.OPEN]

class Platforms(StrEnum):
    PC = "pc"
    XBOX = "xbox"
    PLAYSTATION = "psn"

class Colors(StrEnum):
    def __eq__(self, other):
        if isinstance(other, str):
            return self.lower() == other.lower()
        return NotImplemented
    
    def __hash__(self):
        return hash(self.lower())
    
    BRIGHT_RED = flet.Colors.RED_700.value
    BRIGHT_ORANGE = flet.Colors.ORANGE_500.value
    ORANGE = flet.Colors.ORANGE_700.value
    BLUE = flet.Colors.BLUE_400.value
    DARK_BLUE = flet.Colors.BLUE_900.value
    BLUE_GREY = flet.Colors.BLUE_GREY_900.value
    WHITE = flet.Colors.WHITE.value
    BLACK = flet.Colors.BLACK.value

class UI:
    EDGE_ROUNDING = flet.BorderRadius.all(5)
    DEFAULT_BUTTON_STYLE = flet.ButtonStyle(
        shape = flet.RoundedRectangleBorder(radius = 10),
        mouse_cursor = flet.MouseCursor.CLICK
    )

class Text:
    BOLD = flet.FontWeight.BOLD
    NORMAL = flet.FontWeight.NORMAL

def _hero_icon_helper(hero):
    return f"/hero_icons/{hero}.png"

"""
This class was written primarily with AI, I do not have the patience
to write every single hero in manually,

I will add new heroes manually however (all heroes released after mauga were not in
the ai's database)
"""
class HeroIcons(StrEnum):
    def __eq__(self, other):
        if isinstance(other, str):
            return self.lower() == other.lower()
        return NotImplemented

    def __hash__(self):
        return hash(self.lower())

    # Standard Fallback / Placeholder Icon
    NA = _hero_icon_helper("unimplemented")

    # --- TANKS ---
    DVA = _hero_icon_helper("dva")
    DOMINA = _hero_icon_helper("domina")
    DOOMFIST = _hero_icon_helper("doomfist")
    HAZARD = _hero_icon_helper("hazard")
    JUNKER_QUEEN = _hero_icon_helper("junker-queen")
    MAUGA = _hero_icon_helper("mauga")
    ORISA = _hero_icon_helper("orisa")
    RAMATTRA = _hero_icon_helper("ramattra")
    REINHARDT = _hero_icon_helper("reinhardt")
    ROADHOG = _hero_icon_helper("roadhog")
    SIGMA = _hero_icon_helper("sigma")
    WINSTON = _hero_icon_helper("winston")
    WRECKING_BALL = _hero_icon_helper("wrecking-ball")
    ZARYA = _hero_icon_helper("zarya")

    # --- DAMAGE ---
    ANRAN = _hero_icon_helper("anran")
    ASHE = _hero_icon_helper("ashe")
    BASTION = _hero_icon_helper("bastion")
    CASSIDY = _hero_icon_helper("cassidy")
    ECHO = _hero_icon_helper("echo")
    EMRE = _hero_icon_helper("emre")
    FREJA = _hero_icon_helper("freja")
    GENJI = _hero_icon_helper("genji")
    HANZO = _hero_icon_helper("hanzo")
    JUNKRAT = _hero_icon_helper("junkrat")
    MEI = _hero_icon_helper("mei")
    PHARAH = _hero_icon_helper("pharah")
    REAPER = _hero_icon_helper("reaper")
    SHION = _hero_icon_helper("shion")
    SIERRA = _hero_icon_helper("sierra")
    SOJOURN = _hero_icon_helper("sojourn")
    SOLDIER_76 = _hero_icon_helper("soldier-76")
    SOMBRA = _hero_icon_helper("sombra")
    SYMMETRA = _hero_icon_helper("symmetra")
    TORBJORN = _hero_icon_helper("torbjorn")
    TRACER = _hero_icon_helper("tracer")
    VENDETTA = _hero_icon_helper("vendetta")
    VENTURE = _hero_icon_helper("venture")
    WIDOWMAKER = _hero_icon_helper("widowmaker")

    # --- SUPPORT ---
    ANA = _hero_icon_helper("ana")
    BAPTISTE = _hero_icon_helper("baptiste")
    BRIGITTE = _hero_icon_helper("brigitte")
    ILLARI = _hero_icon_helper("illari")
    JETPACK_CAT = _hero_icon_helper("jetpack-cat")
    JUNO = _hero_icon_helper("juno")
    KIRIKO = _hero_icon_helper("kiriko")
    LIFEWEAVER = _hero_icon_helper("lifeweaver")
    LUCIO = _hero_icon_helper("lucio")
    MERCY = _hero_icon_helper("mercy")
    MIZUKI = _hero_icon_helper("mizuki")
    MOIRA = _hero_icon_helper("moira")
    WUYANG = _hero_icon_helper("wuyang")
    ZENYATTA = _hero_icon_helper("zenyatta")
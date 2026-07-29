from libraries.consts import HeroIcons

def get_hero_icon(hero):
    """
    if None or "na" are given as arguments
    will return the default hero icon
    """
    if hero is None:
        return HeroIcons.NA
    
    formatted_string = hero.upper().replace("-", "_")

    return getattr(HeroIcons, formatted_string)
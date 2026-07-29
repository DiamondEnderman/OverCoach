import requests
from libraries.consts import Roles as Roles

import sys

def _format_battletag(battletag: str) -> str:
    return battletag.replace("#", "-")

class Ranks:
    def __init__(self, battletag: str, platform: str):
        self.battletag = battletag
        self.platform = platform

        self.comp_data = None

        self.tank = None
        self.damage = None
        self.support = None
        self.open = None

        self._load()

    def _fetch_player_summary(self) -> dict:
        id = _format_battletag(self.battletag)
        url = f"https://overfast-api.tekrop.fr/players/{id}/summary"

        response = requests.get(url, timeout=10)

        if sys.stdout and hasattr(sys.stdout, "encoding") and sys.stdout.encoding:
            terminal_encoding = sys.stdout.encoding
        else:
            terminal_encoding = "utf-8"

        safe_tag = self.battletag.encode(terminal_encoding, errors = "replace").decode(terminal_encoding)

        if sys.stdout:
            print(f"Pinging Overfast Api for {safe_tag} player summary")

        response.raise_for_status()
        return response.json()
    
    def get_ranks(self) -> dict:
        """
        Returns a dictionary of all ranks
        """
        platform_data = self.comp_data.get(self.platform, {})

        roles = Roles.all()
        ranks = {}

        for role in roles:
            role_data = platform_data.get(role)
            if role_data:
                division = role_data.get("division", "unranked").capitalize()
                tier = role_data.get("tier", "")
                ranks[role] = f"{division} {tier}".strip()
            else:
                ranks[role] = "Unranked"
        
        return ranks
    
    def _load(self) -> None:
        self.comp_data = self._fetch_player_summary().get("competitive", {})

        ranks = self.get_ranks()

        self.tank = ranks[Roles.TANK]
        self.damage = ranks[Roles.DAMAGE]
        self.support = ranks[Roles.SUPPORT]
        self.open = ranks[Roles.OPEN]

class CareerStats:
    def __init__(self, battletag: str, current_hero: str = None):
        self.ALL = "all-heroes"
        self.battletag = battletag
        self.career_stats = None

        self.main_hero = None
        self.current_hero = current_hero

        self.damage_per_ten = None
        self.healing_per_ten = None
        self.deaths_per_ten = None
        self.elims_per_ten = None
        self.solos_per_ten = None

        self._load()

    def _fetch_career_stats(self) -> dict:
        id = _format_battletag(self.battletag)
        url = f"https://overfast-api.tekrop.fr/players/{id}/stats/career?gamemode=competitive"

        response = requests.get(url, timeout=10)

        if sys.stdout:
            print(f"Pinging Overfast Api for {self.battletag} career stats")

        response.raise_for_status()

        return response.json()

    def get_hero_stats(self, hero:str = "current") -> dict:
        """
        Returns entire dictionary for hero statistics

        "all" returns global statistics
        "main" returns stats from main hero
        "current" returns stats from current hero

        if no hero argument is given, returns from current hero
        """
        match hero:
            case "all":
                return self.career_stats.get(self.ALL, {})
            case "main":
                return self.career_stats.get(self.main_hero, {})
            case "current":
                return self.career_stats.get(self.current_hero, {})
            case _:
                return self.career_stats.get(hero)
    
    def _get_main_hero(self) -> str:
        main = None
        time_spent = 0

        for hero in self.career_stats:
            if hero == self.ALL:
                continue
            hero_time_spent = self.career_stats[hero]["game"]["time_played"]
            if hero_time_spent > time_spent:
                main = hero
                time_spent = hero_time_spent

        return main
    
    def _load_hero_averages(self, hero) -> None:
        """
        Loads the averages from given hero into memory
        """
        averages = self.get_hero_stats(hero).get("average", None)
        if averages is None:
            self.damage_per_ten = None
            self.healing_per_ten = None
            self.deaths_per_ten = None
            self.elims_per_ten = None
            self.solos_per_ten = None
            return
        self.damage_per_ten = averages["hero_damage_done_avg_per_10_min"]
        self.healing_per_ten = averages["healing_done_avg_per_10_min"]
        self.deaths_per_ten = averages["deaths_avg_per_10_min"]
        self.elims_per_ten = averages["eliminations_avg_per_10_min"]
        self.solos_per_ten = averages["solo_kills_avg_per_10_min"]

    def get_average(self, avg_type, hero="all") -> float:
        """
        Loads averages into memory and returns the average
        average types are:
        "damage", "healing", "elims", "deaths", "solos" <- (solo kills)

        if "main" is given as a hero arguement, it will load from main hero

        if "current" is given, it will load from the current hero selection

        if no hero arg is given it will load global averages
        """
        match hero:
            case "main":
                self._load_hero_averages(self.main_hero)
            case "all":
                self._load_hero_averages(self.ALL)
            case "current":
                self._load_hero_averages(self.current_hero)
            case _:
                self._load_hero_averages(hero)

        match avg_type:
            case "damage":
                return self.damage_per_ten
            case "healing":
                return self.healing_per_ten
            case "elims":
                return self.elims_per_ten
            case "deaths":
                return self.deaths_per_ten
            case "solos":
                return self.solos_per_ten
    
    def get_winrate(self, hero = "current") -> int:
        """
        Returns winrate for a given hero
        if no argument is given, or "current" is given, returns from current hero
        "all" returns global winrate
        "main" returns winrate from main character
        """
        game_stats = self.get_hero_stats(hero).get("game", None)

        if game_stats is None:
            return None
        
        if hero == "all":
            games_played = game_stats.get("games_played", 0)

            if games_played == 0:
                return None
            
            winrate = (game_stats.get("games_won", 0)/games_played) * 100
            return round(winrate)
        
        return game_stats.get("win_percentage", None)

    def select_hero(self, hero) -> None:
        """
        Sets current hero to whatever is given in the hero argument,
        Loads the hero data into memory
        """
        self.current_hero = hero
        self._load_hero_averages(hero)
    
    def _load(self) -> None:
        self.career_stats = self._fetch_career_stats()
        self.main_hero = self._get_main_hero()
        if self.current_hero is None:
            self.current_hero = self.main_hero
        self._load_hero_averages(self.current_hero)

#Test Block
if __name__ == "__main__":
    test_tag = "TeKrop#2217"

    ranks = Ranks(test_tag, "pc")

    career_stats = CareerStats(test_tag)

    print(career_stats.career_stats)
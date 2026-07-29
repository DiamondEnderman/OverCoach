import libraries.controllers.file_controller as fc
import libraries.controllers.overfast_api as of

from libraries.consts import AppConfig as AppConfig

PROFILES_FOLDER_PATH = fc.SYSTEM_PATHS["profiles"]

class Profile:
    def __init__(self, profile: str):
        self.profile = profile
        self.profile_path = fc.get_folder_path("profiles", profile)

        self.data_path = f"{self.profile_path}/{AppConfig.PROFILE_DATA_NAME}"

        self.battletag = None
        self.platform = None
        self.layer = 1 #Default Layer is 1
        self.ranks = None
        self.main_hero = None

        self.current_hero = None

        self.last_challenge_roll_date = None
        self.active_challenges = None

    def create(self) -> None:
        self.profile_path = fc.create_folder("profiles", self.profile)
        self.save_to_file()
    
    def fetch_data(self):
        """
        Fetches data from OverFast API and pushes it to the profile instance
        specifically grabs ranks and main hero
        """
        ranks = of.Ranks(self.battletag, self.platform)
        self.ranks = ranks.get_ranks()

        career_stats = of.CareerStats(self.battletag)
        self.main_hero = career_stats.main_hero

    def load_from_file(self) -> None:
        if not fc.os.path.exists(self.profile_path):
            self.create()
        data = fc.pull_data(self.data_path)
        self.battletag = data["battletag"]
        self.platform = data["platform"]
        self.layer = data["layer"]
        self.ranks = data["ranks"]
        self.main_hero = data["main_hero"]

        if data["current_hero"] is None:
            self.current_hero = data["main_hero"]
        else:
            self.current_hero = data["current_hero"]

        self.last_challenge_roll_date = data["last_challenge_roll_date"]
        self.active_challenges = data["active_challenges"]

    def save_to_file(self) -> None:
        data = {
            "battletag": self.battletag,
            "platform": self.platform,
            "layer": self.layer,
            "ranks": self.ranks,
            "main_hero": self.main_hero,
            "last_challenge_roll_date": self.last_challenge_roll_date,
            "active_challenges": self.active_challenges,
            "current_hero": self.current_hero,
        }
        fc.push_data(self.data_path, data)

    def delete(self) -> None:
        fc.remove_folder("profiles", self.profile)

def get_all_profiles():
    if not fc.os.path.exists(PROFILES_FOLDER_PATH):
        return []
    return fc.os.listdir(PROFILES_FOLDER_PATH)

if __name__ == "__main__":
    test_profile = Profile("test")
    test_profile.battletag = "Archaeus#11103"
    test_profile.fetch_data()
    test_profile.platform = "pc"
    test_profile.create()
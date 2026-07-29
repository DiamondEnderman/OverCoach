from datetime import datetime

from libraries.controllers.challenge_manager import Challenges

def _get_current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def _is_current_date(date_str) -> bool:
    if _get_current_date() == date_str:
        return True
    return False

def _roll_next_day(profile_instance) -> None:
    challenges = Challenges(profile_instance.layer)
    profile_instance.last_challenge_roll_date = _get_current_date()
    profile_instance.active_challenges = challenges.get_statics(1)
    profile_instance.save_to_file()

def rollover(profile_instance) -> None:
    last_date = profile_instance.last_challenge_roll_date
    if not _is_current_date(last_date):
        _roll_next_day(profile_instance)
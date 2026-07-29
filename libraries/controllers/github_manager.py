import requests
import os
import libraries.controllers.file_controller as file_controller

class GitChallenges:
    challenge_folder_path = file_controller.SYSTEM_PATHS["challenges"]

    files_to_sync = [
        "version.json",
        "layer1.json",
        "layer2.json",
        "layer3.json",
        "layer4.json"
    ]

    base_url = "https://raw.githubusercontent.com/DiamondEnderman/OverCoach-Challenges/refs/heads/main/challenges/"
    challenges_version_url = f"{base_url}version.json"
    
    @classmethod
    def get_local_version(cls):
        json_path = os.path.join(cls.challenge_folder_path, "version.json")
        if not os.path.exists(json_path):
            return "0.0.0"
        return file_controller.pull_data(json_path).get("version_number", "0.0.0")

    @classmethod
    def get_latest_version(cls):
        print("Attempting to pull latest version number of challenges from github...")
        response = requests.get(cls.challenges_version_url, timeout = 10)
        response.raise_for_status()
        return response.json().get("version_number", None)

    @classmethod
    def sync(cls):
        try:
            if cls.get_local_version() != cls.get_latest_version():
                print("Update Found! Downloading newest version.")

                for file in cls.files_to_sync:
                    url = f"{cls.base_url}{file}"
                    response = requests.get(url, timeout = 10)
                    response.raise_for_status()
                    file_path = os.path.join(cls.challenge_folder_path, file)
                    file_controller.push_data(file_path, response.json())

                print("Update Complete!")
            else:
                print("Challenges are up-to-date!")

        except requests.exceptions.RequestException as err:
            print(f"Offline or couldnt reach GitHub repo ({err}). \n Loading local data.")

        except Exception as err:
            print(f"An unexpected error occured: {err}")
